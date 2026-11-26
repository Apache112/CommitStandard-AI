# CommitStandard-AI

Prototipo en Python para ayudar a preparar mensajes de commit convencionales y reducir la exposición accidental de algunos patrones de credenciales.

**Estudiante:** Jorge Alberto Apache Cardozo  
**Institución:** Fundación Escuela Tecnológica Jesús Oviedo Pérez (FET)  
**Docente:** Jorge Luis Trujillo Artunduaga

## Estado actual

La raíz publicada contiene `sanitizer.py`, que proporciona:

- `Sanitizer.sanitize_text`: normaliza espacios, saltos de línea y tabulaciones.
- `Sanitizer.mask_sensitive_data`: oculta algunos formatos conocidos, como asignaciones a `api_key`, `secret_key`, `password` o `token`, tokens `ghp_` y cadenas con prefijo `sk-`.
- `Sanitizer.validate_commit_message`: valida tipo y longitud (de 5 a 100 caracteres) y rechaza mensajes que coinciden con los patrones definidos.

La historia HU-01 y el contrato de `preparar_diff_para_llm` describen el objetivo de una siguiente fase: obtener el diff de staging, excluir archivos prohibidos, sanitizarlo y validar tamaño. **Ese flujo no está integrado en la raíz publicada.** Tampoco hay generación automática con un servicio LLM.

Los patrones son heurísticos; no detectan todos los secretos y pueden producir falsos positivos. No envíes diffs a un servicio externo basándote únicamente en este prototipo.

## Requisitos e instalación

- Python 3.10 o superior.
- `pytest` y `ruff` para las verificaciones de desarrollo.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install pytest ruff
```

## Pruebas y análisis estático

Desde la raíz del repositorio:

```powershell
python -m pytest -q
ruff check sanitizer.py test_sanitizer.py tests
```

La suite usa particiones de equivalencia, valores límite y tablas de decisión en `tests/test_reglas.py`, además de los casos básicos en `test_sanitizer.py`. La ejecución local registrada para la entrega final obtuvo **43 pruebas aprobadas** en Python 3.14.

El workflow [`.github/workflows/tests.yml`](.github/workflows/tests.yml) repite las pruebas y el lint en Python 3.10 y 3.14 para cada push y pull request. La primera ejecución remota aparecerá después de publicar el workflow en GitHub: https://github.com/Apache112/CommitStandard-AI/actions

## Evidencias del seminario

- [Bitácora de IA](bitacora_ia.md)
- [Registro de pruebas](registro_pruebas.md)
- [Revisión de seguridad](revision_seguridad.md)
- [Informe final](informe_final.md)
- [Diapositivas de sustentación](diapositivas_sustentacion.md)

La bitácora disponible documenta el trabajo de pruebas de la semana 7; no incluye evidencias primarias de todos los módulos 1–6. El informe final distingue explícitamente las evidencias disponibles de las que faltan.
