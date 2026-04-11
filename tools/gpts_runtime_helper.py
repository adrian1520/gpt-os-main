import base64
import hashlib
import json
import time
from datetime import datetime, timezone

import requests
from jsonschema import validate


class GPTExecutionHelper:
    """
    Runtime helper for GPT workflows (no backend).
    - Delegates persistence to GitHub adapter
    - Enforces schema validation and write ordering
    - Supports idempotency + retry on SHA conflicts
    """

    def __init__(self, case_id, github_adapter, schemas):
        self.case_id = case_id
        self.github = github_adapter
        self.schemas = schemas

    def process_document(self, document):
        graph, sha = self._load_graph()

        idempotency_key = self._hash(document.get("content", ""))
        if self.github.event_exists_by_idempotency(self.case_id, idempotency_key):
            return {"status": "SKIPPED_DUPLICATE"}

        txn_id = self._generate_txn_id()

        event = self._create_event(document, txn_id, idempotency_key, graph.get("last_event"))
        self._validate(event, "event")

        updated_graph = self._apply_event(graph, event, txn_id)
        self._validate(updated_graph, "graph")

        self._commit_with_retry(updated_graph, event, document, sha)

        return {
            "status": "OK",
            "transaction_id": txn_id,
            "event_id": event["event_id"],
        }

    def run_snapshot_pipeline(self):
        graph, _ = self._load_graph()
        self.github.create_snapshot(self.case_id, graph)
        return {"status": "SNAPSHOT_CREATED"}

    def get_case(self):
        graph, _ = self._load_graph()
        return graph

    def get_dashboard(self, timeline_limit=5):
        graph, _ = self._load_graph()
        self._validate(graph, "graph")

        nodes = graph.get("nodes", [])
        if not nodes:
            raise ValueError("EMPTY_GRAPH")

        core_state = {
            "case_id": graph.get("case_id"),
            "version": graph.get("version"),
            "last_event": graph.get("last_event"),
            "status": graph.get("meta", {}).get("status"),
            "updated_at": graph.get("meta", {}).get("updated_at"),
            "meta.status": graph.get("meta", {}).get("status"),
            "meta.updated_at": graph.get("meta", {}).get("updated_at"),
        }

        metrics = self._compute_metrics(graph)
        timeline = self._build_timeline_from_graph(graph)[:timeline_limit]

        dashboard = {
            "core_state": core_state,
            "metrics": metrics,
            "timeline": timeline,
        }
        return {"status": "OK", "ui": self._render_dashboard_ui(dashboard)}

    def _load_graph(self):
        path = f"cases/{self.case_id}/graph.json"
        data = self.github.get_file(path)
        if not data.get("content"):
            raise ValueError(f"Missing graph content at {path}")
        return json.loads(data["content"]), data.get("sha")

    def _create_event(self, document, txn_id, idempotency_key, prev_event):
        event = {
            "event_id": self._generate_id("EVT"),
            "type": "DOCUMENT_ADDED",
            "timestamp": self._now(),
            "actor": "SYSTEM",
            "actor_details": {
                "id": "system",
                "type": "SYSTEM",
                "role": "SYSTEM",
            },
            "payload": {
                "doc_id": document.get("doc_id"),
                "type": document.get("type"),
                "source": document.get("source", "SYSTEM"),
            },
            "prev_event": prev_event,
            "idempotency_key": idempotency_key,
            "transaction_id": txn_id,
        }
        event["hash"] = self._hash(event)
        return event

    def _apply_event(self, graph, event, txn_id):
        graph = json.loads(json.dumps(graph))
        graph["version"] = int(graph.get("version", 0)) + 1
        graph["last_event"] = event["event_id"]
        graph["transaction_id"] = txn_id
        graph.setdefault("meta", {})["updated_at"] = self._now()
        graph["hash"] = self._hash(graph)
        return graph

    def _commit_with_retry(self, graph, event, document, sha, retries=3):
        base = f"cases/{self.case_id}"

        for attempt in range(retries):
            try:
                self.github.put_file(
                    f"{base}/graph.json",
                    graph,
                    message=f"case {self.case_id}: update graph {event['event_id']}",
                    sha=sha,
                )
                self.github.put_file(
                    f"{base}/events/{event['event_id']}.json",
                    event,
                    message=f"case {self.case_id}: add event {event['event_id']}",
                )
                self.github.put_file(
                    f"{base}/documents/{document['doc_id']}.json",
                    document,
                    message=f"case {self.case_id}: add document {document['doc_id']}",
                )

                self.github.update_index(self.case_id)
                return
            except Exception as exc:
                if "SHA mismatch" in str(exc) and attempt < retries - 1:
                    latest_graph, latest_sha = self._load_graph()
                    graph = self._apply_event(latest_graph, event, event["transaction_id"])
                    sha = latest_sha
                    continue
                raise

    def _validate(self, data, schema_type):
        validate(instance=data, schema=self.schemas[schema_type])

    def _compute_metrics(self, graph):
        nodes = graph.get("nodes", [])
        edges = graph.get("edges", [])
        documents_count = len([n for n in nodes if n.get("type") == "DOCUMENT"])
        events_count = len([n for n in nodes if n.get("type") == "EVENT"])
        return {
            "documents_count": documents_count,
            "events_count": events_count,
            "nodes_count": len(nodes),
            "edges_count": len(edges),
        }

    def _build_timeline_from_graph(self, graph):
        items = []
        for node in graph.get("nodes", []):
            if node.get("type") not in ("EVENT", "DOCUMENT"):
                continue
            data = node.get("data", {})
            ts = data.get("timestamp") or data.get("created_at") or graph.get("meta", {}).get("updated_at")
            items.append(
                {
                    "id": node.get("id"),
                    "type": node.get("type"),
                    "timestamp": ts,
                    "label": data.get("title") or data.get("type") or node.get("type"),
                }
            )
        items.sort(key=lambda x: x.get("timestamp") or "", reverse=True)
        return items

    def _render_dashboard_ui(self, dashboard):
        core = dashboard.get("core_state", {})
        metrics = dashboard.get("metrics", {})
        timeline = dashboard.get("timeline", [])
        alerts = dashboard.get("alerts", [])

        def safe(val, default="-"):
            return val if val not in [None, ""] else default

        def shorten(text, max_len=60):
            text = str(text)
            return text if len(text) <= max_len else text[: max_len - 3] + "..."

        def status_icon(status):
            return {
                "ACTIVE": "🟢",
                "CLOSED": "🔴",
                "SUSPENDED": "🟡",
            }.get(status, "⚪")

        def event_icon(event_type):
            return {
                "DOCUMENT_ADDED": "🟢",
                "CASE_CREATED": "🔵",
                "NODE_ADDED": "🟡",
                "EDGE_ADDED": "🟣",
                "STATUS_CHANGED": "⚪",
            }.get(event_type, "⚪")

        case_block = [
            f"📁 {safe(core.get('case_id'))}",
            f"{status_icon(core.get('meta.status'))} {safe(core.get('meta.status'))} | v{safe(core.get('version'))}",
            f"🕒 {shorten(safe(core.get('meta.updated_at')))}",
        ]

        alerts_block = []
        if alerts:
            alerts_block.append("⚠️ ALERTS")
            for alert in alerts[:2]:
                alerts_block.append("• " + shorten(alert, 55))

        metrics_block = (
            f"📊 📄{metrics.get('documents_count', 0)} "
            f"⚡{metrics.get('events_count', 0)} "
            f"🧩{metrics.get('nodes_count', 0)} "
            f"🔗{metrics.get('edges_count', 0)}"
        )
        actions_block = "⚙️ ➕ dokument | 🔄 odśwież | 🧠 strategia | 🚨 ryzyko"

        timeline_block = ["🕒 TIMELINE"]
        if not timeline:
            timeline_block.append("• brak zdarzeń w sprawie")
        else:
            for item in timeline[:5]:
                item_type = safe(item.get("type"))
                ts = safe(item.get("timestamp", ""))[:10]
                line = f"{event_icon(item_type)} {ts} {item_type}"
                timeline_block.append(shorten(line, 60))

        text_lines = []
        text_lines.extend(case_block)
        if alerts_block:
            text_lines.append("")
            text_lines.extend(alerts_block)
        text_lines.append("")
        text_lines.append(metrics_block)
        text_lines.append(actions_block)
        text_lines.append("")
        text_lines.extend(timeline_block)

        return {
            "case": dashboard["core_state"],
            "metrics": dashboard["metrics"],
            "timeline": dashboard["timeline"],
            "cards": [
                {"title": "Status", "value": dashboard["core_state"].get("status")},
                {"title": "Version", "value": dashboard["core_state"].get("version")},
                {"title": "Documents", "value": dashboard["metrics"].get("documents_count", 0)},
                {"title": "Events", "value": dashboard["metrics"].get("events_count", 0)},
            ],
            "text": "\n".join(text_lines),
        }

    def _generate_id(self, prefix):
        return f"{prefix}_{int(time.time() * 1000)}"

    def _generate_txn_id(self):
        return f"TXN_{int(time.time() * 1000)}"

    def _now(self):
        return datetime.now(timezone.utc).isoformat()

    def _hash(self, data):
        if isinstance(data, str):
            payload = data
        else:
            payload = json.dumps(
                data,
                sort_keys=True,
                ensure_ascii=False,
                separators=(",", ":"),
            )
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()


class GitHubAPIAdapter:
    def __init__(self, owner, repo, token, branch="main"):
        self.owner = owner
        self.repo = repo
        self.branch = branch
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
        }

    def get_file(self, path):
        url = f"{self.base_url}/repos/{self.owner}/{self.repo}/contents/{path}"
        res = self._request("GET", url, params={"ref": self.branch})

        content = None
        if res.get("content"):
            content = base64.b64decode(res["content"].replace("\n", "")).decode("utf-8")

        return {"content": content, "sha": res.get("sha"), "encoding": res.get("encoding")}

    def put_file(self, path, data, message="update", sha=None):
        url = f"{self.base_url}/repos/{self.owner}/{self.repo}/contents/{path}"
        payload = {
            "message": message,
            "content": base64.b64encode(
                json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
            ).decode("utf-8"),
            "branch": self.branch,
        }
        if sha:
            payload["sha"] = sha
        return self._request("PUT", url, json_payload=payload)

    def event_exists_by_idempotency(self, case_id, key):
        query = f"repo:{self.owner}/{self.repo} {key} path:cases/{case_id}/events/"
        try:
            res = self._request("GET", f"{self.base_url}/search/code", params={"q": query})
            return res.get("total_count", 0) > 0
        except Exception:
            return False

    def update_index(self, case_id):
        path = "cases/index.json"
        try:
            file_data = self.get_file(path)
            data = json.loads(file_data["content"]) if file_data.get("content") else {"cases": {}}
            sha = file_data.get("sha")
        except Exception:
            data, sha = {"cases": {}}, None

        data.setdefault("cases", {})[case_id] = {"last_update": datetime.now(timezone.utc).isoformat()}
        self.put_file(path, data, message=f"index: update {case_id}", sha=sha)

    def create_snapshot(self, case_id, graph):
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ")
        path = f"cases/{case_id}/snapshots/{ts}.json"
        self.put_file(path, graph, message=f"snapshot: {case_id} {ts}")

    def _request(self, method, url, params=None, json_payload=None, retries=3):
        for attempt in range(retries):
            response = requests.request(
                method,
                url,
                headers=self.headers,
                params=params,
                json=json_payload,
                timeout=30,
            )

            if response.status_code in (200, 201):
                return response.json()

            if response.status_code in (403, 429):
                time.sleep(2**attempt)
                continue

            if response.status_code == 409:
                raise Exception("SHA mismatch")

            if response.status_code == 404:
                raise Exception(f"Not found: {url}")

            raise Exception(f"GitHub API error {response.status_code}: {response.text}")

        raise Exception("GitHub API failure after retries")
