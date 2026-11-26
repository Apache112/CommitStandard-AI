"""
CommitStandard-AI — Módulo principal
Sanitiza el git diff, elimina secretos/credenciales y valida tamaño
antes de enviarlo a un LLM para generar mensajes de commit convencionales.
"""

import re
import shutil
import subprocess
from typing import List


# ─── Patrones de secretos a eliminar del diff ───────────────────────────────
SENSITIVE_PATTERNS: List[re.Pattern] = [
    # api_key, secret_key, password, token = "valor"
    re.compile(
        r"(?i)(api[_-]?key|secret[_-]?key|password|db_password|token)"
        r"\s*[:=]\s*['\"]?([a-zA-Z0-9_\-\.]{8,})['\"]?"
    ),
    re.compile(r"ghp_[a-zA-Z0-9]{36}"),   # GitHub Personal Access Token
    re.compile(r"sk-[a-zA-Z0-9]{48}"),    # OpenAI API Key
    re.compile(r"(?i)-----BEGIN (RSA |EC )?PRIVATE KEY-----"),  # Claves privadas
]

# Archivos que nunca deben incluirse en el diff enviado al LLM
FORBIDDEN_FILES = [".env", ".env.local", ".env.production", "secrets.yml", "*.pem"]

MAX_BYTES_DEFAULT = 51_200  # 50 KB


def _contiene_secreto(linea: str) -> bool:
    """Retorna True si la línea contiene algún patrón sensible."""
    for pattern in SENSITIVE_PATTERNS:
        if pattern.search(linea):
            return True
    return False


def _es_archivo_prohibido(linea: str) -> bool:
    """Retorna True si la línea de diff hace referencia a un archivo prohibido."""
    for nombre in FORBIDDEN_FILES:
        nombre_limpio = nombre.replace("*", "")
        if nombre_limpio in linea:
            return True
    return False


def _redactar_secreto(linea: str) -> str:
    """Reemplaza el valor del secreto con [REDACTED_SECRET] en la línea."""
    resultado = linea
    for pattern in SENSITIVE_PATTERNS:
        resultado = pattern.sub(
            lambda m: m.group(0).split(m.group(0)[len(m.group(1)):], 1)[0]
            if hasattr(m, "group") and m.lastindex and m.lastindex >= 1
            else "[REDACTED_SECRET]",
            resultado,
        )
    # Sustitución directa más simple y confiable
    resultado = re.sub(
        r"(?i)(api[_-]?key|secret[_-]?key|password|db_password|token)"
        r"(\s*[:=]\s*)['\"]?([a-zA-Z0-9_\-\.]{8,})['\"]?",
        r"\1\2[REDACTED_SECRET]",
        linea,
    )
    for pattern in [
        re.compile(r"ghp_[a-zA-Z0-9]{36}"),
        re.compile(r"sk-[a-zA-Z0-9]{48}"),
        re.compile(r"(?i)-----BEGIN (RSA |EC )?PRIVATE KEY-----"),
    ]:
        resultado = pattern.sub("[REDACTED_SECRET]", resultado)
    return resultado


def preparar_diff_para_llm(diff_text: str, max_bytes: int = MAX_BYTES_DEFAULT) -> dict:
    """
    Recibe el diff bruto de Git, lo sanitiza eliminando líneas con secretos/claves,
    ignora archivos prohibidos (.env) y valida que cumpla con los límites de tamaño.

    Args:
        diff_text (str): El volcado crudo del comando git diff.
        max_bytes (int): Límite máximo del payload en bytes (por defecto 50 KB).

    Returns:
        dict: Diccionario con 'status', 'clean_diff' y 'message'.
              status = 'success' | 'error'
    """
    # Validación de tipos
    if not isinstance(diff_text, str):
        return {
            "status": "error",
            "clean_diff": "",
            "message": "El diff_text debe ser una cadena de texto (str).",
        }

    # Diff vacío
    if not diff_text.strip():
        return {
            "status": "error",
            "clean_diff": "",
            "message": "El diff está vacío. No hay cambios en staging para procesar.",
        }

    # Verificar tamaño antes de procesar
    if len(diff_text.encode("utf-8")) > max_bytes:
        return {
            "status": "error",
            "clean_diff": "",
            "message": "Payload demasiado grande. El diff supera el límite permitido.",
        }

    # Procesar línea a línea
    lineas_limpias = []
    ignorar_bloque = False

    for linea in diff_text.splitlines():
        # Detectar inicio de bloque de archivo prohibido
        if linea.startswith("diff --git") and _es_archivo_prohibido(linea):
            ignorar_bloque = True

        # Fin de bloque prohibido al encontrar nuevo archivo
        if linea.startswith("diff --git") and not _es_archivo_prohibido(linea):
            ignorar_bloque = False

        if ignorar_bloque:
            continue

        # Redactar secretos en líneas añadidas (+)
        if linea.startswith("+") and _contiene_secreto(linea):
            linea = _redactar_secreto(linea)

        lineas_limpias.append(linea)

    clean_diff = "\n".join(lineas_limpias)

    if len(clean_diff.encode("utf-8")) > max_bytes:
        return {
            "status": "error",
            "clean_diff": "",
            "message": "Payload demasiado grande. El diff supera el límite permitido.",
        }

    # Verificar tamaño del diff limpio
    if not clean_diff.strip():
        return {
            "status": "error",
            "clean_diff": "",
            "message": "Tras la sanitización el diff quedó vacío.",
        }

    return {
        "status": "success",
        "clean_diff": clean_diff,
        "message": "Diff preparado con éxito.",
    }


def obtener_diff_staging() -> str:
    """
    Ejecuta 'git diff --cached' y retorna el diff de los archivos en staging.

    Returns:
        str: Texto del diff, o cadena vacía si no hay cambios staged.

    Raises:
        RuntimeError: Si Git no está disponible o hay un error al ejecutarlo.
    """
    git_executable = shutil.which("git")
    if git_executable is None:
        raise RuntimeError("Git no está instalado o no está en el PATH del sistema.")

    try:
        resultado = subprocess.run(  # noqa: S603
            [git_executable, "diff", "--cached"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=10,
        )
        if resultado.returncode != 0:
            raise RuntimeError(f"Git error: {resultado.stderr.strip()}")
        return resultado.stdout
    except FileNotFoundError as err:
        raise RuntimeError(
            "Git no está instalado o no está en el PATH del sistema."
        ) from err
    except subprocess.TimeoutExpired as err:
        raise RuntimeError("Tiempo de espera agotado al ejecutar git diff.") from err
