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

La carpeta `FUNCIONANDO/` incluye un prototipo independiente con `commit_guard.py` y `main.py` para preparar el diff de staging. No está integrado con `Sanitizer`, y todavía no genera mensajes mediante un servicio LLM. Sus pruebas cubren la sanitización y los límites principales, pero no una ejecución de Git real desde la CLI.

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
ruff check sanitizer.py test_sanitizer.py tests FUNCIONANDO
```

La suite usa particiones de equivalencia, valores límite y tablas de decisión en `tests/test_reglas.py`, casos básicos en `test_sanitizer.py` y siete pruebas para el prototipo en `tests/test_commit_guard.py`. La ejecución local obtuvo **50 pruebas aprobadas** en Python 3.14.

Para probar la CLI desde la raíz del proyecto:

```powershell
python FUNCIONANDO\main.py
```

El workflow [`.github/workflows/tests.yml`](.github/workflows/tests.yml) repite las pruebas y el lint en Python 3.10 y 3.14 para cada push y pull request. Consulta https://github.com/Apache112/CommitStandard-AI/actions para ver el resultado de cada ejecución.

## Evidencias del seminario

- [Bitácora de IA](bitacora_ia.md)
- [Registro de pruebas](registro_pruebas.md)
- [Revisión de seguridad](revision_seguridad.md)
- [Informe final](informe_final.md)
- [Diapositivas de sustentación](diapositivas_sustentacion.md)

La bitácora disponible documenta el trabajo de pruebas de la semana 7; no incluye evidencias primarias de todos los módulos 1–6. El informe final distingue explícitamente las evidencias disponibles de las que faltan.
