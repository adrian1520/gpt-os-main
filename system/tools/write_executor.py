# tools/write_executor.py (v8 PURE TRANSFORM MODULE)

import base64


# --- VALIDATION ---

def validate_repo(owner: str, repo: str) -> None:
    """Sprawdza, czy nazwa właściciela i repozytorium są poprawne."""
    if not owner or not repo:
        raise ValueError("Invalid repository: owner and repo must be provided.")


def validate_path(path: str) -> None:
    """Sprawdza ścieżkę do pliku pod kątem bezpieczeństwa (np. path traversal)."""
    if not path or ".." in path:
        raise ValueError("Invalid path: path cannot be empty or contain '..'.")

    if path.startswith("/"):
        raise ValueError("Invalid path: absolute paths are not allowed.")


def validate_message(message: str) -> None:
    """Sprawdza poprawność wiadomości commitu."""
    if not message or len(message.strip()) < 3:
        raise ValueError("Invalid commit message: must be at least 3 characters long.")


def validate_content(content: str) -> None:
    """Sprawdza wielkość i zawartość pliku przed transformacją."""
    if not content or not content.strip():
        raise ValueError("Content is empty.")

    # Limit wielkości pliku (~1MB) chroniący limity akcji API
    if len(content.encode('utf-8')) > 1_000_000:
        raise ValueError("Content too large: exceeds 1MB limit.")


# --- NORMALIZATION ---

def normalize_content(content: str) -> str:
    """
    Normalizuje zawartość pliku tekstowego:
    - Zamienia Windowsowe CRLF (\r\n) na UNIXowe LF (\n)
    - Zamienia taby na spacje (dla spójności kodu)
    - Usuwa białe znaki na końcach linii
    - Zapewnia dokładnie jedną pustą linię na końcu pliku
    """
    if not isinstance(content, str):
        raise ValueError("Invalid content type: expected string.")

    content = content.replace("\r\n", "\n")
    content = content.replace("\t", "  ")
    
    content = "\n".join(line.rstrip() for line in content.splitlines())

    if not content.endswith("\n"):
        content += "\n"

    return content


# --- ENCODING ---

def encode_base64(content: str) -> str:
    """Koduje znormalizowaną zawartość do Base64 (wymóg API GitHuba)."""
    try:
        return base64.b64encode(content.encode("utf-8")).decode("utf-8")
    except Exception as e:
        raise ValueError(f"Encoding failed: {str(e)}")


# --- MAIN TRANSFORM FUNCTION ---

def prepare_content(raw_content: str) -> str:
    """
    Główna funkcja wywoływana przez Interpretera.
    Pobiera surowy tekst wygenerowany przez LLM, normalizuje go,
    waliduje ograniczenia wielkościowe i koduje do Base64.
    
    Zwraca: (str) zakodowany string Base64 gotowy do przekazania
    jako parametr 'content' do akcji API createOrUpdateFile.
    """
    # 1. Normalizacja (formatowanie tekstu pod repozytorium)
    normalized = normalize_content(raw_content)
    
    # 2. Walidacja (upewnienie się, że znormalizowany plik mieści się w limitach)
    validate_content(normalized)
    
    # 3. Transformacja do oczekiwanego formatu
    return encode_base64(normalized)

