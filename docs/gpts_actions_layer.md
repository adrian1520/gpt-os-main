# GPTs Actions layer (bez backendu) dla `adrian1520/cyfrowe_akta`

Ten projekt używa **GitHub REST API bez własnego backendu**. GPT wykonuje tylko akcje z OpenAPI i sam składa workflow.

## 1) Co dodać do GPT Actions

Wgraj plik OpenAPI:
- `schemas/github_gpts_actions_openapi.yaml`
- Helper runtime (Python, opcjonalny): `tools/gpts_runtime_helper.py`

Użyj PAT z zakresem:
- repo (private repo: pełny `repo`; public repo: `public_repo` może wystarczyć)

## 2) Kontrakt danych (walidacja payloadu)

Kontrakt JSON Schema:
- `schemas/legal_case_storage.schema.json`
- Kontrakt pipeline write: `schemas/auto_pipeline_document_write.contract.json`
- Kontrakt pipeline read/dashboard: `schemas/dashboard_read.contract.json`

W praktyce GPT powinien tworzyć **envelope** z jednym kluczem:
- `graph` **albo** `event` **albo** `document`

## 3) Konwencja ścieżek (storage layout)

- `cases/{case_id}/graph.json`
- `cases/{case_id}/events/{timestamp}_{event_id}.json`
- `cases/{case_id}/documents/{doc_id}.json`

## 4) Workflow akcji bez backendu

> Uwaga dot. mapowania akcji: w OpenAPI operationId to `getFileOrDirectory` (nie `getFile`).

### A. Odczyt grafu sprawy
1. `getFileOrDirectory` dla `cases/{case_id}/graph.json`
2. Zdekoduj base64 `content`.
3. Zwaliduj JSON względem kontraktu (`graph`).

### B. Zapis grafu (wersjonowany)
1. `getFileOrDirectory` -> pobierz aktualny `sha` pliku.
2. Zwiększ `version`, zaktualizuj `last_event`, `meta.updated_at`.
3. Zapisz przez `createOrUpdateFile` (PUT) z `sha` (optimistic lock).

### C. Append event
1. Utwórz payload `event` + `idempotency_key`.
2. Zapisz nowy plik `events/...json` przez `createOrUpdateFile` (bez `sha`, bo nowy plik).
3. Opcjonalnie zaktualizuj `graph.json` (last_event/version) przez PUT z `sha`.

### D. Lista drzew i folderów
- Płytko: `getFileOrDirectory` na folderze.
- Głęboko: `getTree` z `recursive=1`.

### E. Audyt i diff
- `listCommits` (dla `path=cases/{case_id}`)
- `compareRefs` (np. `main...feature-branch`)

### F. Wyszukiwanie
- `searchCode` np. `repo:adrian1520/cyfrowe_akta case_123 path:cases/ extension:json`

## 5) Contract pipeline v1.8 (document write)

Plik `schemas/auto_pipeline_document_write.contract.json` odwzorowuje pełny pipeline:
- load/decode graph, extract `sha`, idempotency check po `searchCode`,
- utworzenie i walidacja `event`,
- merge i walidacja `graph`,
- zapis w kolejności `graph -> event -> document`.

Najważniejsze korekty pod GPT Actions:
- `getFile` -> `getFileOrDirectory` (zgodnie z `operationId` w OpenAPI),
- query do `searchCode` zawiera `repo:{owner}/{repo}`.

## 6) Helper runtime (bez backendu)

`tools/gpts_runtime_helper.py` dostarcza:
- `GPTExecutionHelper.process_document(document)` z walidacją schema + retry 409,
- `GPTExecutionHelper.get_dashboard(timeline_limit=5)` dla pipeline `DASHBOARD` (READ),
- `GitHubAPIAdapter` (GET/PUT/search/index/snapshot) pod GitHub REST,
- idempotency (`event_exists_by_idempotency`) zawężone do `cases/{case_id}/events/`.
- UI engine zwraca zarówno strukturę (`case/metrics/timeline/cards`), jak i gotowy blok tekstowy (`ui.text`) pod Canvas/Interpreter.

## 7) Zasady bezpieczeństwa i spójności

- Każdy update istniejącego pliku rób z `sha`.
- Dla idempotencji eventów używaj `idempotency_key`.
- W razie konfliktu 409: ponowny GET -> merge -> PUT z nowym `sha`.
- Trzymaj `transaction_id` wspólne dla sekwencji zmian wykonanych w jednej operacji logicznej.
