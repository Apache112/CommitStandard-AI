# Sustentación — CommitStandard-AI

## Diapositiva 1 — Problema y usuario (1 min)

- Usuario previsto: desarrolladores que preparan cambios en Git.
- Problema: mensajes de commit inconsistentes y riesgo de compartir secretos.
- Meta propuesta: 18 de 20 mensajes aceptados sin edición; no medida aún.
- Evidencia: [propuesta](docs/propuesta.md).

## Diapositiva 2 — Solución implementada (1 min)

- Python local: valida mensajes y prepara `git diff --cached`.
- Excluye algunos archivos y redacta patrones conocidos.
- No tiene plugin, backend ni llamada automática a un LLM.
- Evidencia: [README](README.md), [CLI](FUNCIONANDO/main.py).

## Diapositiva 3 — IA en el ciclo de vida (2 min)

- Fundamentos: comparación DeepSeek/Gemini, código ejecutado.
- Propuesta: Gemini ayudó a refinar la idea; meta 18/20.
- Diseño: Gemini sugirió alternativas, C4, modelo y API; correcciones humanas.
- Pruebas: IA ayudó con PE, valores límite y tablas de decisión.
- Vacíos: requisitos recibidos son de otro proyecto; falta evidencia de IA en
  las seis fases.
- Evidencia: [mapa de módulos](docs/evidencia_modulos.md), [bitácora](bitacora_ia.md).

## Diapositiva 4 — Error de diseño verificado (1.5 min)

- IA situó la base de métricas en el equipo del desarrollador.
- Lo detecté comparando el C4 con el ADR de Gateway.
- Moví la base de datos al backend en el diseño.
- El Gateway es objetivo académico; no está implementado.
- Evidencia: [diseño y ADR](docs/diseno-adr.md).

## Diapositiva 5 — Verificación en código (1.5 min)

- Hallazgo: secretos en contexto/eliminaciones y bloques PEM podían sobrevivir.
- Añadí fixtures sintéticos y comprobé el fallo antes de corregir.
- La primera fixture `.pem` no probaba redacción: el archivo era excluido.
- Corregí el caso y redacción; muestra en vivo `pytest tests/test_commit_guard.py`.
- Evidencia: [pruebas](tests/test_commit_guard.py), [bitácora](bitacora_ia.md).

## Diapositiva 6 — Privacidad, ética y ley (1 min)

- Un diff puede contener datos personales o credenciales.
- No se envía a un proveedor externo en la versión publicada.
- Regex no garantiza detección completa; revisión humana obligatoria.
- Antes de integrar un LLM: informar, pedir consentimiento y definir retención.
- Evidencia: [revisión de seguridad](revision_seguridad.md), [operación](docs/operacion.md).

## Diapositiva 7 — Estado y pipeline (1 min)

- Demo local: `git add` de un archivo sintético y ejecutar la CLI.
- CI: pytest + Ruff, Python 3.10 y 3.14.
- Mostrar el último run verde después de publicar la corrección; run previo:
  [GitHub Actions](https://github.com/Apache112/CommitStandard-AI/actions).
- No hay despliegue productivo ni backend.

## Diapositiva 8 — Aprendizajes y preguntas (1 min)

- Un test verde no basta: comprobar que el input sí coincide con la regla.
- No mezclar documentos de proyectos distintos ni convertir metas en resultados.
- Pendientes: requisitos válidos, bitácora completa y tres casos de fases
  distintas con commits históricos.
- Preguntas: 4 minutos.
