# CommitStandard-AI

Prototipo en Python para validar mensajes de commit y preparar un diff de Git con
redacción heurística de algunos patrones sensibles antes de compartirlo.

## Alcance implementado

- `sanitizer.py` normaliza texto, valida mensajes de 5 a 100 caracteres y oculta
  algunos patrones conocidos de credenciales.
- `FUNCIONANDO/commit_guard.py` lee diffs staged, excluye ciertos archivos,
  redacta patrones conocidos y aplica un límite de tamaño.
- `FUNCIONANDO/main.py` muestra el diff limpio y una instrucción para pedir una
  sugerencia a un asistente externo manualmente.

El proyecto **no** llama a una API de LLM, no genera commits automáticamente y
no integra la arquitectura Gateway descrita como diseño objetivo. La detección
por patrones no garantiza que todos los secretos o datos personales sean
identificados. No se debe compartir código usando solo este prototipo como
garantía de privacidad.

## Requisitos

- Python 3.10 o superior.
- `pytest` y `ruff` para desarrollo.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install pytest ruff
```

## Ejecutar y verificar

Desde la raíz del repositorio:

```powershell
python -m pytest -q
ruff check sanitizer.py test_sanitizer.py tests FUNCIONANDO
python FUNCIONANDO\main.py
```

La CLI solo procesa cambios preparados en staging (`git add`). Si no hay cambios
staged, informa que no hay diff que procesar; no es una falla de ejecución.
Consulta [la guía de operación](docs/operacion.md) antes de usarla.

## Evidencias del seminario

- [Propuesta del proyecto](docs/propuesta.md)
- [Requisitos y brechas](docs/requisitos.md)
- [Diseño y ADR](docs/diseno-adr.md)
- [Evidencias por módulo](docs/evidencia_modulos.md)
- [Bitácora de IA](bitacora_ia.md)
- [Registro de pruebas](registro_pruebas.md)
- [Revisión de seguridad (con nota de alcance)](revision_seguridad.md)
- [Informe final](informe_final.md) y [PDF](informe_final.pdf)
- [Diapositivas](diapositivas_sustentacion.md) y [PDF](diapositivas_sustentacion.pdf)

La documentación distingue los artefactos originales del trabajo retrospectivo
de preparación de esta entrega. El documento de requisitos recibido para el
módulo 3 corresponde a un minimercado, no a CommitStandard-AI, y por ello no se
presenta como evidencia válida de requisitos de este proyecto.
