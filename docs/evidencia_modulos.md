# Mapa de evidencias de los módulos

Este índice resume los documentos originales compartidos y los artefactos del
repositorio. Los originales con datos identificativos no se copian al
repositorio público; se conserva un resumen de evidencia y se señalan los
vacíos.

| Módulo/fase | Evidencia disponible | Uso de IA y verificación | Límite |
|---|---|---|---|
| 1. Fundamentos | Laboratorio comparativo de asistentes, resumido en el documento original del módulo. | Comparó salidas de DeepSeek y Gemini para validar correo; ejecutó las salidas y contrastó sus resultados. | Es un laboratorio académico general, no evidencia de implementación de CommitStandard-AI. |
| 2. Propuesta | [Propuesta](propuesta.md), resumen del banco de prompts y la propuesta del original. | Se declara que Gemini refinó la redacción; se propuso meta de 18/20 mensajes aceptados. | La meta no se midió; ejercicios del banco sobre otros dominios no se atribuyen al proyecto. |
| 3. Requisitos | [Nota de discrepancia y reconstrucción](requisitos.md). | El documento recibido describe un minimercado, así que se excluyó. La reconstrucción debe ser aprobada. | No hay un documento primario de requisitos de CommitStandard-AI entre los archivos recibidos. |
| 4. Diseño | [Diseño y ADR](diseno-adr.md). | Gemini apoyó alternativas, diagramas, modelo y API; el estudiante documenta revisiones y correcciones. | La arquitectura es propuesta; sus cambios no tienen commits individuales. |
| 5. Código y pruebas | [Código](../sanitizer.py), [prototipo](../FUNCIONANDO/commit_guard.py), [pruebas](../tests) y [bitácora](../bitacora_ia.md). | La bitácora registra asistencia de IA para PE, valores límite y tablas de decisión; la suite automatizada verifica los casos implementados. | No se conserva el historial de prompts de generación de la implementación principal. |
| 6. Operación | [Workflow](../.github/workflows/tests.yml), [página de ejecuciones](https://github.com/Apache112/CommitStandard-AI/actions) y [guía](operacion.md). | GitHub Actions ejecuta pytest y Ruff en Python 3.10 y 3.14. | No hay despliegue de servicio; el producto es una CLI local. Se debe confirmar que la ejecución más reciente de GitHub corresponde al commit final y terminó exitosamente. |

## Casos reales registrados

- **Diseño:** el borrador ubicó la base de datos en el IDE; se corrigió en el
  diagrama del backend.
- **Diseño:** se rechazó persistir el diff fuente completo y se revisaron las
  rutas con verbos.
- **Pruebas:** la propuesta de prueba para `sk-` usaba caracteres no admitidos
  por el patrón y se descartó; se detectó inspeccionando el regex y la entrada.
- **Verificación final de código:** una prueba sintética confirmó que el
  prototipo no limpiaba secretos en líneas de contexto/eliminadas ni bloques
  multilinea de claves privadas. Se corrigió y se añadieron regresiones en
  [test_commit_guard.py](../tests/test_commit_guard.py).

Los casos de diseño no tienen un commit histórico individual asociado y los
ejemplos de requisitos del minimercado pertenecen a otro proyecto. Por tanto,
la evidencia disponible no satisface íntegramente el criterio de tres errores
de IA en tres fases distintas con commits trazables. No se inventan casos ni
commits para cubrir ese vacío.
