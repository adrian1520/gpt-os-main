import base64
import hashlib
import json
import time
from copy import deepcopy
from datetime import datetime, timezone


class ToolMappingRuntime:
    """Deterministic runtime that executes contract steps with tool_mapping."""

    def __init__(self, execution_tool, contracts, schemas):
        self.execution_tool = execution_tool
        self.contracts = contracts
        self.schemas = schemas

    def execute(self, input_data):
        contract = self._route(input_data)
        ctx = {"input": deepcopy(input_data)}
        ctx.update(contract.get("context", {}))

        for step in contract["steps"]:
            result = self._run_step(step, ctx, contract)
            if step.get("output"):
                ctx[step["output"]] = result
            if result == "SKIPPED_DUPLICATE":
                return {"status": "SKIPPED_DUPLICATE"}

        returns = contract.get("output", {}).get("returns", [])
        out = {"status": contract.get("output", {}).get("status", "OK")}
        for path in returns:
            key = path.split(".")[-1]
            out[key] = self._resolve(path, ctx)
        return out

    def _route(self, input_data):
        if input_data.get("doc_id") and input_data.get("content"):
            return self.contracts["AUTO_PIPELINE"]
        if input_data.get("case_id") and "content" not in input_data:
            return self.contracts["DASHBOARD"]
        raise ValueError("ROUTING_FAILED")

    def _run_step(self, step, ctx, contract):
        action = step["action"]
        if action in ("getFileOrDirectory", "createOrUpdateFile", "searchCode"):
            return self._call_external(action, step, ctx)
        if action == "decode_base64":
            raw = self._resolve(step["input"], ctx)
            return json.loads(base64.b64decode(raw).decode("utf-8"))
        if action == "encode_base64":
            data = self._resolve(step["input"], ctx)
            return base64.b64encode(json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")).decode("utf-8")
        if action == "extract_field":
            return self._resolve(step["input"], ctx)
        if action == "hash":
            data = self._resolve(step["input"], ctx)
            payload = data if isinstance(data, str) else json.dumps(data, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
            return hashlib.sha256(payload.encode("utf-8")).hexdigest()
        if action == "generate_txn_id":
            return f"TXN_{int(time.time() * 1000)}"
        if action == "conditional_abort":
            condition = step.get("condition", "")
            if "search_result.total_count > 0" in condition and self._resolve("search_result.total_count", ctx) > 0:
                return "SKIPPED_DUPLICATE"
            return None
        if action == "create_event_object":
            doc = ctx["input"]
            return {
                "event_id": f"EVT_{int(time.time() * 1000)}",
                "type": step["params"]["type"],
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "actor": "SYSTEM",
                "actor_details": {"id": "system", "type": "SYSTEM", "role": "SYSTEM"},
                "payload": {"doc_id": doc.get("doc_id"), "type": doc.get("type"), "source": doc.get("source", "SYSTEM")},
                "prev_event": self._resolve("graph.last_event", ctx),
                "idempotency_key": ctx["idempotency_key"],
                "transaction_id": ctx["transaction_id"],
            }
        if action == "merge_graph":
            graph = deepcopy(ctx["graph"])
            event = ctx["event"]
            graph["version"] = int(graph.get("version", 0)) + 1
            graph["last_event"] = event["event_id"]
            graph.setdefault("meta", {})["updated_at"] = datetime.now(timezone.utc).isoformat()
            graph["transaction_id"] = ctx["transaction_id"]
            return graph
        if action == "update_graph_meta":
            graph = deepcopy(self._resolve(step["input"], ctx))
            graph.setdefault("meta", {})["updated_at"] = datetime.now(timezone.utc).isoformat()
            return graph
        if action == "set_field":
            obj = deepcopy(self._resolve(step["input"], ctx))
            obj[step["params"]["field"]] = self._resolve(step["params"]["value"], ctx)
            return obj
        if action in ("assert_not_null", "assert_not_empty", "assert_equals"):
            return self._assertions(action, step, ctx)
        if action == "extract_fields":
            src = self._resolve(step["input"], ctx)
            return {f: self._resolve(f, {**ctx, "_": src}) if "." in f else src.get(f) for f in step["params"]["fields"]}
        if action == "compute_metrics":
            graph = self._resolve(step["input"], ctx)
            nodes = graph.get("nodes", [])
            edges = graph.get("edges", [])
            return {
                "documents_count": len([n for n in nodes if n.get("type") == "DOCUMENT"]),
                "events_count": len([n for n in nodes if n.get("type") == "EVENT"]),
                "nodes_count": len(nodes),
                "edges_count": len(edges),
            }
        if action == "build_timeline_from_graph":
            graph = self._resolve(step["input"], ctx)
            timeline = []
            for n in graph.get("nodes", []):
                if n.get("type") in ("EVENT", "DOCUMENT"):
                    data = n.get("data", {})
                    timeline.append({"id": n.get("id"), "type": n.get("type"), "timestamp": data.get("timestamp") or data.get("created_at")})
            return sorted(timeline, key=lambda x: x.get("timestamp") or "", reverse=True)
        if action == "slice":
            arr = self._resolve(step["input"], ctx) or []
            return arr[: step["params"]["limit"]]
        if action == "apply_fallback":
            return self._apply_fallback(step, ctx, contract)
        if action in ("dashboard_engine", "normalize_dashboard_shape", "render_dashboard_ui"):
            return self._render_actions(action, step, ctx)
        if action == "validate_schema":
            # Hook point: optionally connect jsonschema validator.
            return None
        raise ValueError(f"UNSUPPORTED_ACTION: {action}")

    def _call_external(self, action, step, ctx):
        params = deepcopy(step.get("params", {}))
        for k, v in list(params.items()):
            if isinstance(v, str):
                params[k] = self._interpolate(v, ctx)
        if action == "getFileOrDirectory":
            return self.execution_tool.getFileOrDirectory(params)
        if action == "createOrUpdateFile":
            return self.execution_tool.createOrUpdateFile(params)
        if action == "searchCode":
            return self.execution_tool.searchCode(params)
        raise ValueError(action)

    def _assertions(self, action, step, ctx):
        value = self._resolve(step.get("input", ""), ctx)
        if action == "assert_not_null" and value is None:
            raise ValueError(step.get("error", "ASSERT_NOT_NULL_FAILED"))
        if action == "assert_not_empty" and (value is None or len(value) == 0):
            raise ValueError(step.get("error", "ASSERT_NOT_EMPTY_FAILED"))
        if action == "assert_equals" and value != step["params"]["value"]:
            raise ValueError(step.get("error", "ASSERT_EQUALS_FAILED"))
        return None

    def _apply_fallback(self, step, ctx, contract):
        fallback = contract.get("fallbacks", {}).get(step.get("fallback"), {})
        if "metrics" in fallback:
            return fallback["metrics"]
        if "timeline" in fallback:
            return fallback["timeline"]
        return self._resolve(step.get("input", ""), ctx)

    def _render_actions(self, action, step, ctx):
        if action == "dashboard_engine":
            return {"core_state": ctx["core_state"], "metrics": ctx["metrics"], "timeline": ctx["timeline"]}
        if action == "normalize_dashboard_shape":
            dash = self._resolve(step["input"], ctx)
            dash.setdefault("metrics", {"documents_count": 0, "events_count": 0, "nodes_count": 0, "edges_count": 0})
            dash.setdefault("timeline", [])
            return dash
        if action == "render_dashboard_ui":
            dash = self._resolve(step["input"], ctx)
            return {"text": json.dumps(dash, ensure_ascii=False), **dash}

    def _interpolate(self, value, ctx):
        out = value
        for key in ["owner", "repo", "branch", "graph_path", "events_path", "documents_path", "idempotency_key"]:
            if "{" + key + "}" in out:
                out = out.replace("{" + key + "}", str(ctx.get(key, "")))
        if "{case_id}" in out:
            out = out.replace("{case_id}", str(ctx["input"].get("case_id", "")))
        if "{input.doc_id}" in out:
            out = out.replace("{input.doc_id}", str(ctx["input"].get("doc_id", "")))
        if "{event.event_id}" in out:
            out = out.replace("{event.event_id}", str(ctx.get("event", {}).get("event_id", "")))
        return out

    def _resolve(self, path, ctx):
        if not path:
            return None
        if path in ctx:
            return ctx[path]
        cur = ctx
        for part in path.split("."):
            if isinstance(cur, dict):
                cur = cur.get(part)
            else:
                return None
        return cur
