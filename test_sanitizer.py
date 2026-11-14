"""
Pruebas unitarias para el módulo Sanitizer.
"""

import pytest
from sanitizer import Sanitizer


def test_sanitize_text_valid():
    """Verifica la limpieza correcta de espacios y saltos de línea."""
    raw_text = "  Hola   Mundo \n con saltos  "
    assert Sanitizer.sanitize_text(raw_text) == "Hola Mundo con saltos"


def test_sanitize_text_invalid_type():
    """Verifica que se lance TypeError al pasar tipos no válidos."""
    with pytest.raises(TypeError):
        Sanitizer.sanitize_text(12345)  # type: ignore


def test_mask_sensitive_data():
    """Verifica el enmascaramiento correcto de claves API y tokens."""
    text_with_secret = "Mi clave de API es api_key = 'sk-1234567890abcdef1234567890abcdef12345678nad'"
    result = Sanitizer.mask_sensitive_data(text_with_secret)
    assert "[REDACTED]" in result
    assert "sk-12345678" not in result


def test_validate_commit_message_success():
    """Verifica un mensaje de commit válido."""
    assert Sanitizer.validate_commit_message("feat: añadir módulo de sanitización") is True


def test_validate_commit_message_too_short():
    """Verifica que rechace mensajes demasiado cortos."""
    assert Sanitizer.validate_commit_message("fix") is False


def test_validate_commit_message_with_secret():
    """Verifica que rechace un commit que contenga secretos."""
    malicious_commit = "fix: actualizar token password=secret_super_secure"
    assert Sanitizer.validate_commit_message(malicious_commit) is False