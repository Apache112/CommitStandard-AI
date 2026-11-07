import pytest
from sanitizer import preparar_diff_para_llm

# --- CASOS NORMALES ---

def test_preparar_diff_caso_normal_exito():
    """Caso Normal 1: Verifica que un diff estándar y limpio se procese correctamente."""
    diff_valido = "diff --git a/src/main.py b/src/main.py\n+print('Hello World')\n"
    resultado = preparar_diff_para_llm(diff_valido)
    assert resultado["status"] == "success"
    assert "print('Hello World')" in resultado["clean_diff"]

def test_preparar_diff_con_comentarios_normales():
    """Caso Normal 2: Un diff con modificaciones ordinarias de comentarios no debe alterarse."""
    diff_comentarios = "diff --git a/app.py b/app.py\n+# Comentario ordinario de arquitectura"
    resultado = preparar_diff_para_llm(diff_comentarios)
    assert resultado["status"] == "success"
    assert "Comentario ordinario" in resultado["clean_diff"]

# --- CASOS LÍMITE ---

def test_preparar_diff_censura_secretos_limite():
    """Caso Límite 1: Detecta y censura contraseñas o tokens sensibles."""
    diff_con_secreto = "diff --git a/config.js\n+const API_KEY = 'secret123';\n+const PORT = 80;"
    resultado = preparar_diff_para_llm(diff_con_secreto)
    assert resultado["status"] == "success"
    assert "secret123" not in resultado["clean_diff"]
    assert "[REDACTED_SECRET]" in resultado["clean_diff"]

def test_preparar_diff_ignora_archivos_env_completos():
    """Caso Límite 2: El diff de un archivo .env debe ser purgado por completo."""
    diff_env = "diff --git a/.env b/.env\n+DB_PASS=1234\n+PORT=8080"
    resultado = preparar_diff_para_llm(diff_env)
    assert resultado["status"] == "success"
    assert "DB_PASS" not in resultado["clean_diff"]
    assert resultado["clean_diff"].strip() == ""

# --- CASOS DE ERROR ---

def test_preparar_diff_error_vacio():
    """Caso de Error 1: Si el diff está vacío, debe retornar un error controlado."""
    resultado = preparar_diff_para_llm("   ")
    assert resultado["status"] == "error"
    assert resultado["message"] == "El diff de entrada está vacío."
