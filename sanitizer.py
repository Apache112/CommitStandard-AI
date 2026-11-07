import re

def preparar_diff_para_llm(diff_text: str, max_bytes: int = 51200) -> dict:
    """
    Sanitiza y prepara el git diff para ser enviado de forma segura al LLM.
    """
    if not diff_text or not diff_text.strip():
        return {
            "status": "error",
            "clean_diff": "",
            "message": "El diff de entrada está vacío."
        }
        
    if len(diff_text.encode('utf-8')) > max_bytes:
        return {
            "status": "error",
            "clean_diff": "",
            "message": "Payload demasiado grande. El diff supera el límite permitido."
        }

    # Regla: Si el diff pertenece a un archivo .env, se elimina por completo
    if "diff --git a/.env" in diff_text:
        return {
            "status": "success",
            "clean_diff": "",
            "message": "Diff preparado con éxito."
        }

    # Sanitización de secretos/claves en las líneas del código
    lineas = diff_text.split('\n')
    lineas_limpias = []
    
    patron_secreto = re.compile(r'(KEY|SECRET|PASSWORD|PASS|TOKEN|KEY)\s*=\s*["\'][^"\']+["\']', re.IGNORECASE)

    for linea in lineas:
        if patron_secreto.search(linea):
            # Reemplazar el secreto con la etiqueta de ofuscación
            linea_modificada = re.sub(r'=(.*)', '= "[REDACTED_SECRET]"', linea)
            lineas_limpias.append(linea_modificada)
        else:
            lineas_limpias.append(linea)

    return {
        "status": "success",
        "clean_diff": '\n'.join(lineas_limpias),
        "message": "Diff preparado con éxito."
    }
