"""
Pruebas unitarias para el módulo Sanitizer — CommitStandard-AI
Semana 7 — Técnicas: Particiones de Equivalencia, Valores Límite, Tablas de Decisión
"""

import pytest
from sanitizer import Sanitizer


# ─────────────────────────────────────────────────────────────────────────────
# sanitize_text — Particiones de Equivalencia
# ─────────────────────────────────────────────────────────────────────────────

class TestSanitizeTextParticionesEquivalencia:
    """PE-1 a PE-5: Particiones válidas e inválidas para sanitize_text."""

    # PE-1: texto normal con espacios múltiples → debe normalizarse
    def test_pe1_espacios_multiples(self):
        assert Sanitizer.sanitize_text("  Hola   Mundo  ") == "Hola Mundo"

    # PE-2: texto con saltos de línea → se reemplazan por espacio
    def test_pe2_saltos_de_linea(self):
        assert Sanitizer.sanitize_text("fix: error\nen producción") == "fix: error en producción"

    # PE-3: texto con tabulaciones → se reemplazan por espacio
    def test_pe3_tabulaciones(self):
        assert Sanitizer.sanitize_text("feat:\tadd\tlogin") == "feat: add login"

    # PE-4: texto ya limpio → no cambia
    def test_pe4_texto_ya_limpio(self):
        assert Sanitizer.sanitize_text("fix: corregir bug") == "fix: corregir bug"

    # PE-5 (inválida): entero como entrada → TypeError
    def test_pe5_tipo_entero_lanza_type_error(self):
        with pytest.raises(TypeError):
            Sanitizer.sanitize_text(12345)  # type: ignore

    # PE-6 (inválida): None como entrada → TypeError
    def test_pe6_tipo_none_lanza_type_error(self):
        with pytest.raises(TypeError):
            Sanitizer.sanitize_text(None)  # type: ignore

    # PE-7 (inválida): lista como entrada → TypeError
    def test_pe7_tipo_lista_lanza_type_error(self):
        with pytest.raises(TypeError):
            Sanitizer.sanitize_text(["fix: algo"])  # type: ignore


# ─────────────────────────────────────────────────────────────────────────────
# sanitize_text — Valores Límite
# ─────────────────────────────────────────────────────────────────────────────

class TestSanitizeTextValoresLimite:
    """VL-1 a VL-4: Cadenas vacías, 1 carácter, cadena muy larga."""

    # VL-1: cadena vacía → devuelve cadena vacía (límite inferior)
    def test_vl1_cadena_vacia(self):
        assert Sanitizer.sanitize_text("") == ""

    # VL-2: un solo carácter → lo devuelve tal cual
    def test_vl2_un_solo_caracter(self):
        assert Sanitizer.sanitize_text("x") == "x"

    # VL-3: solo espacios → devuelve cadena vacía tras strip
    def test_vl3_solo_espacios(self):
        assert Sanitizer.sanitize_text("     ") == ""

    # VL-4: cadena de 1000 caracteres → se procesa sin error
    def test_vl4_cadena_muy_larga(self):
        long_text = "a" * 1000
        result = Sanitizer.sanitize_text(long_text)
        assert result == long_text


# ─────────────────────────────────────────────────────────────────────────────
# validate_commit_message — Particiones de Equivalencia + Valores Límite
# ─────────────────────────────────────────────────────────────────────────────

class TestValidateCommitMessageParticiones:
    """PE/VL para validate_commit_message (longitud 5-100 caracteres)."""

    # VL longitud — exactamente 5 caracteres (límite inferior válido)
    def test_vl_longitud_minima_valida(self):
        assert Sanitizer.validate_commit_message("abcde") is True

    # VL longitud — exactamente 4 caracteres (justo debajo del límite)
    def test_vl_longitud_bajo_minimo(self):
        assert Sanitizer.validate_commit_message("abcd") is False

    # VL longitud — exactamente 100 caracteres (límite superior válido)
    def test_vl_longitud_maxima_valida(self):
        message = "a" * 100
        assert Sanitizer.validate_commit_message(message) is True

    # VL longitud — exactamente 101 caracteres (justo sobre el límite)
    def test_vl_longitud_sobre_maximo(self):
        message = "a" * 101
        assert Sanitizer.validate_commit_message(message) is False

    # PE válida — mensaje convencional bien formado
    def test_pe_mensaje_valido_convencional(self):
        assert Sanitizer.validate_commit_message("feat: añadir autenticación OAuth2") is True

    # PE válida — mensaje con tipo fix
    def test_pe_mensaje_valido_fix(self):
        assert Sanitizer.validate_commit_message("fix: corregir null pointer en login") is True

    # PE inválida — cadena vacía
    def test_pe_cadena_vacia(self):
        assert Sanitizer.validate_commit_message("") is False

    # PE inválida — None
    def test_pe_none(self):
        assert Sanitizer.validate_commit_message(None) is False  # type: ignore

    # PE inválida — entero
    def test_pe_entero(self):
        assert Sanitizer.validate_commit_message(42) is False  # type: ignore

    # PE inválida — mensaje muy corto (1 carácter)
    def test_pe_un_caracter(self):
        assert Sanitizer.validate_commit_message("x") is False


# ─────────────────────────────────────────────────────────────────────────────
# validate_commit_message — Tabla de Decisión (seguridad)
# TD combina: longitud OK | contiene secreto | resultado esperado
# ─────────────────────────────────────────────────────────────────────────────

class TestValidateCommitMessageTablaDecision:
    """
    Tabla de decisión (4 reglas):
    R1: longitud OK | sin secreto  → True
    R2: longitud OK | con secreto  → False
    R3: longitud MAL | sin secreto → False
    R4: longitud MAL | con secreto → False
    """

    # R1: longitud válida + sin secreto → True
    def test_td_r1_valido_sin_secreto(self):
        assert Sanitizer.validate_commit_message("docs: actualizar README del proyecto") is True

    # R2: longitud válida + API key expuesta → False
    def test_td_r2_valido_con_api_key(self):
        msg = "fix: agregar api_key=supersecreta123"
        assert Sanitizer.validate_commit_message(msg) is False

    # R2b: longitud válida + password expuesto → False
    def test_td_r2b_valido_con_password(self):
        msg = "refactor: cambiar password=MiClave123!"
        assert Sanitizer.validate_commit_message(msg) is False

    # R2c: longitud válida + token GitHub expuesto → False
    def test_td_r2c_valido_con_github_token(self):
        msg = "fix: ghp_" + "A" * 36
        assert Sanitizer.validate_commit_message(msg) is False

    # R3: longitud inválida (muy corta) + sin secreto → False
    def test_td_r3_corto_sin_secreto(self):
        assert Sanitizer.validate_commit_message("ok") is False

    # R4: longitud inválida + con secreto → False
    def test_td_r4_corto_con_secreto(self):
        assert Sanitizer.validate_commit_message("tok") is False


# ─────────────────────────────────────────────────────────────────────────────
# mask_sensitive_data — Particiones de Equivalencia
# ─────────────────────────────────────────────────────────────────────────────

class TestMaskSensitiveDataParticiones:
    """PE para mask_sensitive_data."""

    # PE válida: texto sin datos sensibles → no cambia
    def test_pe_sin_datos_sensibles(self):
        text = "feat: agregar módulo de reportes"
        assert Sanitizer.mask_sensitive_data(text) == text

    # PE válida: contiene api_key → enmascarado con [REDACTED]
    def test_pe_con_api_key(self):
        text = "config: api_key=AbCdEfGhIj1234567890"
        result = Sanitizer.mask_sensitive_data(text)
        assert "[REDACTED]" in result

    # PE válida: contiene secret_key → enmascarado
    def test_pe_con_secret_key(self):
        text = "config: secret_key=MiSecretoSuperLargo"
        result = Sanitizer.mask_sensitive_data(text)
        assert "[REDACTED]" in result

    # PE válida: contiene password → enmascarado
    def test_pe_con_password(self):
        text = "setup: password=Pass1234567890"
        result = Sanitizer.mask_sensitive_data(text)
        assert "[REDACTED]" in result

    # PE válida: contiene token GitHub (ghp_) → enmascarado
    def test_pe_con_github_pat(self):
        token = "ghp_" + "B" * 36
        result = Sanitizer.mask_sensitive_data(f"auth: usar {token}")
        assert "[REDACTED]" in result
        assert token not in result

    # PE inválida: None → TypeError
    def test_pe_none_lanza_type_error(self):
        with pytest.raises(TypeError):
            Sanitizer.mask_sensitive_data(None)  # type: ignore

    # PE inválida: entero → TypeError
    def test_pe_entero_lanza_type_error(self):
        with pytest.raises(TypeError):
            Sanitizer.mask_sensitive_data(999)  # type: ignore


# ─────────────────────────────────────────────────────────────────────────────
# mask_sensitive_data — Valores Límite
# ─────────────────────────────────────────────────────────────────────────────

class TestMaskSensitiveDataValoresLimite:
    """VL para mask_sensitive_data."""

    # VL-1: cadena vacía → devuelve cadena vacía
    def test_vl_cadena_vacia(self):
        assert Sanitizer.mask_sensitive_data("") == ""

    # VL-2: texto con múltiples secretos → todos enmascarados
    def test_vl_multiples_secretos(self):
        text = "api_key=secret123456789 y password=clave9876543"
        result = Sanitizer.mask_sensitive_data(text)
        assert result.count("[REDACTED]") >= 2

    # VL-3: secreto en límite de 8 caracteres (mínimo del patrón)
    def test_vl_secreto_longitud_minima(self):
        text = "token=12345678"  # exactamente 8 caracteres de valor
        result = Sanitizer.mask_sensitive_data(text)
        assert "[REDACTED]" in result
