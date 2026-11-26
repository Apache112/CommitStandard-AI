from FUNCIONANDO.commit_guard import preparar_diff_para_llm


def _diff(archivo: str, linea: str) -> str:
    return (
        f"diff --git a/{archivo} b/{archivo}\n"
        f"--- a/{archivo}\n"
        f"+++ b/{archivo}\n"
        f"{linea}"
    )


def test_preparar_diff_conserva_cambios_sin_secretos():
    diff = _diff("README.md", "+documentación")

    resultado = preparar_diff_para_llm(diff)

    assert resultado["status"] == "success"
    assert resultado["clean_diff"] == diff


def test_preparar_diff_rechaza_diff_vacio_y_tipo_invalido():
    assert preparar_diff_para_llm("")["status"] == "error"
    assert preparar_diff_para_llm(None)["status"] == "error"


def test_preparar_diff_redacta_credencial():
    secreto = "api_key=abcdefgh"
    resultado = preparar_diff_para_llm(_diff("config.py", "+" + secreto))

    assert resultado["status"] == "success"
    assert secreto not in resultado["clean_diff"]
    assert "[REDACTED_SECRET]" in resultado["clean_diff"]


def test_preparar_diff_redacta_token_github():
    token = "ghp_" + "A" * 36
    resultado = preparar_diff_para_llm(_diff("config.py", "+" + token))

    assert resultado["status"] == "success"
    assert token not in resultado["clean_diff"]
    assert "[REDACTED_SECRET]" in resultado["clean_diff"]


def test_preparar_diff_excluye_env_y_conserva_archivo_permitido():
    diff = _diff(".env", "+password=abcdefgh") + "\n" + _diff(
        "README.md", "+contenido público"
    )

    resultado = preparar_diff_para_llm(diff)

    assert resultado["status"] == "success"
    assert ".env" not in resultado["clean_diff"]
    assert "contenido público" in resultado["clean_diff"]
    assert "abcdefgh" not in resultado["clean_diff"]


def test_preparar_diff_rechaza_payload_original_demasiado_grande():
    diff = _diff("large.txt", "+" + "x" * 100)

    resultado = preparar_diff_para_llm(diff, max_bytes=20)

    assert resultado["status"] == "error"
    assert resultado["clean_diff"] == ""


def test_preparar_diff_rechaza_payload_que_crece_al_redactar():
    diff = _diff("config.py", "+token=12345678")

    resultado = preparar_diff_para_llm(diff, max_bytes=len(diff.encode("utf-8")))

    assert resultado["status"] == "error"
    assert resultado["clean_diff"] == ""
