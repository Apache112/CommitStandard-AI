# Requisitos y trazabilidad

> **Naturaleza de este archivo:** reconstrucción retrospectiva para hacer
> explícito el alcance que sí se puede inferir de la propuesta del módulo 2,
> el diseño del módulo 4 y el código publicado. No sustituye una entrevista ni
> el documento original de requisitos del módulo 3.

## Requisitos funcionales observables

| ID | Requisito | Estado en el repositorio | Evidencia |
|---|---|---|---|
| RF-01 | Obtener el diff staged mediante `git diff --cached`. | Implementado en el prototipo; la CLI real no tiene prueba de integración. | [commit_guard.py](../FUNCIONANDO/commit_guard.py), [README](../README.md) |
| RF-02 | Excluir del diff algunos archivos sensibles configurados. | Implementado con una lista limitada de nombres/patrones. | [commit_guard.py](../FUNCIONANDO/commit_guard.py), [pruebas](../tests/test_commit_guard.py) |
| RF-03 | Redactar patrones conocidos de credenciales en líneas de contenido. | Implementado para patrones enumerados; no es detección exhaustiva. | [commit_guard.py](../FUNCIONANDO/commit_guard.py), [pruebas](../tests/test_commit_guard.py) |
| RF-04 | Rechazar diff vacío o que exceda el máximo configurado. | Implementado y probado para los casos disponibles. | [commit_guard.py](../FUNCIONANDO/commit_guard.py), [pruebas](../tests/test_commit_guard.py) |
| RF-05 | Mostrar el diff preparado y permitir que la persona solicite una sugerencia por separado. | Implementado en la CLI. | [main.py](../FUNCIONANDO/main.py) |
| RF-06 | Validar longitud y patrones de mensajes de commit. | Implementado como utilidad independiente. | [sanitizer.py](../sanitizer.py), [pruebas](../tests/test_reglas.py) |

## Metas de diseño que no están implementadas

- Obtener 90% de aceptación sin edición en una muestra de 20 sugerencias.
- Responder en menos de 3 segundos.
- Integrar un plugin de IDE, backend Gateway, almacenamiento de métricas o API.
- Consultar automáticamente un proveedor LLM.

Estas metas aparecen en la propuesta/diseño, pero el código actual no permite
medirlas ni afirmar que estén satisfechas.

## Discrepancia del módulo 3

El documento recibido como requisitos del módulo 3 describe un sistema de ventas
para un minimercado: inventario, deudas/fiados y cierre de caja. Ese alcance no
coincide con la propuesta CommitStandard-AI del módulo 2, el diseño del módulo 4
ni el repositorio. Sus historias y la entrevista simulada no se incorporan a
este proyecto ni se presentan como evidencia válida de sus requisitos.

La reconstrucción de RF-01 a RF-06 debe ser revisada por el estudiante y el
docente. Para cerrar la trazabilidad académica hace falta el artefacto original
de requisitos de CommitStandard-AI o una validación explícita de esta
reconstrucción.
