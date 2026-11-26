# Informe final del proyecto integrador

**Proyecto:** CommitStandard-AI — asistente para commits convencionales

**Estudiante:** Jorge Alberto Apache Cardozo

**Repositorio:** https://github.com/Apache112/CommitStandard-AI

**Fecha:** 2026-11-26

> **Alcance de esta versión del informe.** Se contrastaron las afirmaciones con los archivos del repositorio y se ejecutaron las pruebas localmente. La copia disponible no contiene evidencia primaria de todos los módulos 1–6 ni una ejecución de GitHub Actions. Esas limitaciones se declaran en vez de atribuir resultados no comprobados. El prototipo ubicado en `FUNCIONANDO/` es una copia local separada y no se considera parte comprobada del código publicado.

## 1. Resumen

CommitStandard-AI explora cómo ayudar a quienes preparan mensajes de commit y reducir la exposición accidental de secretos. En la copia verificable del repositorio, `sanitizer.py` normaliza texto, enmascara algunos patrones de credenciales y valida mensajes; el README también describe un flujo futuro para sanitizar diffs antes de usar un LLM. La bitácora disponible documenta el uso de IA para diseñar pruebas, no el proceso completo de los seis módulos. Verifiqué el código con 43 pruebas automatizadas: las 43 pasaron en Python 3.14. Añadí un workflow local de GitHub Actions para repetir pruebas y análisis estático al publicar los cambios; todavía no hay ejecución remota porque el workflow aún no está en GitHub. Por ello, el estado es un prototipo probado, no una integración completa con un LLM.

## 2. Problema y usuario

**Usuario objetivo:** desarrolladores que crean commits convencionales y quieren evitar incluir accidentalmente credenciales u otros valores sensibles en el texto que revisan o comparten.

**Necesidad:** contar con una revisión local previa a la generación de un mensaje de commit. La propuesta documentada en el [README](README.md) plantea tomar el diff de staging, retirar secretos y archivos prohibidos, y validar el tamaño antes de entregar el texto a un LLM. La motivación es reducir errores humanos y limitar la divulgación de código.

**Límite de la evidencia:** no se encontró en esta copia una propuesta del módulo 1, registro de entrevista o validación de usuario del módulo 2. Por tanto, la descripción del usuario y su necesidad se presenta como el planteamiento del proyecto, no como hallazgo confirmado mediante entrevista.

## 3. La IA en el ciclo de vida

| Módulo y fase | Uso de IA que puede sustentarse | Herramienta registrada | Evidencia disponible | Verificación |
|---|---|---|---|---|
| 1. Fundamentos | La bitácora disponible no registra esta fase. | No consta | No se encontró propuesta del módulo 1 | No verificable con los archivos recibidos |
| 2. Requisitos | El README contiene HU-01 y un contrato propuesto para preparar el diff. No se encontró el historial de prompts ni la entrevista. | No consta en la bitácora disponible | [README](README.md) | Comparé el contrato con el código versionado; la función descrita no está en la raíz publicada |
| 3. Diseño | Se documentó la firma, entradas y salidas esperadas del preparador de diff. | No consta en la bitácora disponible | [README](README.md) | Inspección del árbol del repositorio; el contrato está documentado, pero no se verificó como código publicado |
| 4. Código | `Sanitizer` implementa normalización, enmascaramiento por patrones y validación de mensajes. La bitácora no conserva prompts de generación de este código. | No consta | [sanitizer.py](sanitizer.py) | Revisión del código y ejecución de la suite |
| 5. Pruebas | La IA ayudó a proponer particiones de equivalencia, valores límite y tabla de decisión; también se registraron correcciones y descartes. | Antigravity (Gemini), según la [bitácora](bitacora_ia.md) | [bitacora_ia.md](bitacora_ia.md), [registro_pruebas.md](registro_pruebas.md), [tests/test_reglas.py](tests/test_reglas.py) | `pytest`: 43 passed; revisión manual de entradas y salidas |
| 6. Operación | Se documentó una revisión de seguridad. Se añadió un workflow para ejecutar controles en push y pull request. | La herramienta de revisión no está corroborada en la bitácora disponible | [revision_seguridad.md](revision_seguridad.md), [workflow](.github/workflows/tests.yml) | `ruff` y `pytest` localmente; ejecución remota pendiente de publicar el workflow |

La tabla distingue entre lo que muestran los artefactos y lo que no se puede confirmar. La bitácora existente se limita a la semana 7, por lo que no permite reconstruir de manera completa el uso de IA de los módulos 1–6.

## 4. Verificación: propuestas de IA revisadas

Los tres ejemplos verificables corresponden a la fase de pruebas; no se atribuyen errores a otras fases porque la bitácora disponible no los documenta.

### Caso 1: cobertura insuficiente de la regla con secretos

- **Fase:** Pruebas.
- **Qué propuso la IA:** usar un solo caso con `api_key` para la regla de mensaje válido con secreto.
- **Qué faltaba:** el código contempla patrones distintos, entre ellos credenciales tipo `password` y tokens `ghp_`; probar un solo patrón no ejercitaba esas variantes.
- **Cómo lo detecté:** comparé la propuesta registrada con los patrones y los casos de prueba.
- **Qué hice:** documenté casos separados para `api_key`, `password` y `ghp_` en [tests/test_reglas.py](tests/test_reglas.py). La bitácora describe la decisión en [bitacora_ia.md](bitacora_ia.md).

### Caso 2: límite inferior de longitud omitido

- **Fase:** Pruebas.
- **Qué propuso la IA:** probar una cadena vacía y múltiples secretos, pero no el mínimo de ocho caracteres del patrón de asignación.
- **Qué faltaba:** el cuantificador `{8,}` representa una frontera del comportamiento que debía verificarse expresamente.
- **Cómo lo detecté:** inspeccioné el patrón en [sanitizer.py](sanitizer.py) y contrasté el límite con los casos existentes.
- **Qué hice:** añadí el caso `token=12345678` en [tests/test_reglas.py](tests/test_reglas.py). La prueba confirma el mínimo del patrón de asignación, no todos los formatos posibles de secretos.

### Caso 3: prueba que pasaba por una entrada que no coincidía

- **Fase:** Pruebas.
- **Qué propuso la IA:** una entrada para el patrón `sk-` que incluía caracteres que no pertenecen a la clase alfanumérica del regex.
- **Qué estaba mal:** un test puede pasar sin demostrar que el patrón objetivo detectó el texto.
- **Cómo lo detecté:** ejecuté la prueba de forma aislada y comprobé el resultado, no solo el código de salida de pytest.
- **Qué hice:** descarté esa prueba según la [bitácora](bitacora_ia.md). La prueba de enmascaramiento para OpenAI no queda demostrada por la suite actual y sigue siendo una brecha.

## 5. Estado final del sistema

### Arquitectura verificada

- [sanitizer.py](sanitizer.py): clase `Sanitizer` con normalización, patrones de enmascaramiento y validación de mensajes.
- [test_sanitizer.py](test_sanitizer.py) y [tests/test_reglas.py](tests/test_reglas.py): pruebas unitarias del sanitizador.
- [README.md](README.md): describe además una HU-01 para sanitizar diffs de staging. Esa función no está en la raíz de la versión publicada.

Existe un prototipo separado en `FUNCIONANDO/`, pero no se verificó como código versionado utilizable por un clon limpio del repositorio. La raíz tampoco integra una llamada a una API de LLM.

### Funcionalidades y verificación

| Funcionalidad | Estado comprobado |
|---|---|
| Normalizar espacios, saltos de línea y tabulaciones | Implementada y probada |
| Enmascarar patrones comunes de credenciales | Implementada con cobertura parcial |
| Validar tipo y longitud del mensaje de commit | Implementada y probada |
| Leer y sanitizar `git diff --cached` antes de usar un LLM | Documentada como requisito; no comprobada en la raíz publicada |
| Generar automáticamente un mensaje mediante API de LLM | No implementada |

**Pruebas:** `py -3.14 -m pytest -q` produjo **43 passed** el 26 de noviembre de 2026. La suite contiene 37 pruebas en `tests/test_reglas.py` y 6 en `test_sanitizer.py`. La ejecución local de `ruff check .` encontró cuatro observaciones en la copia separada bajo `FUNCIONANDO/`; por eso el workflow limita el análisis estático a los archivos fuente y pruebas de la raíz. El resultado local de CI no sustituye una ejecución de GitHub Actions.

### Condiciones para considerar completa la HU-01

La HU-01 del README se refiere al diff staged, no solo a validar un mensaje. Para evitar confundir el estado actual con el objetivo, estas son condiciones pendientes que deben probarse antes de presentarla como terminada:

1. **Origen y errores:** leer el diff de staging sin concatenar comandos de shell y distinguir claramente ausencia de cambios de errores de Git.
2. **Archivos excluidos:** demostrar con diffs de varios archivos que `.env` y los patrones de archivos prohibidos se excluyen sin descartar archivos permitidos.
3. **Redacción:** usar claves sintéticas válidas para cada patrón documentado y comprobar que el valor original no permanece en la salida; añadir casos que no deben coincidir para vigilar falsos positivos.
4. **Tamaño:** medir bytes UTF-8 del payload que realmente se prepara y probar el límite exacto, un byte por debajo y un byte por encima, incluso después de sanitizar.
5. **Vacíos y tipos:** probar diff vacío, entrada de tipo inválido y resultado vacío después de exclusiones, con errores observables y no salidas de éxito engañosas.
6. **Publicación al LLM:** no enviar el texto a un servicio externo por defecto; si se integra, documentar proveedor, consentimiento, tratamiento, retención y opciones para operar sin conexión.

Estas condiciones convierten la intención del requisito en evidencias repetibles. No son resultados atribuidos a la implementación actual; sirven como criterio para la siguiente iteración y para revisar si los cambios futuros satisfacen el objetivo de privacidad.

### Qué demuestra la suite y qué no demuestra

| Área | Evidencia observable | Alcance del resultado |
|---|---|---|
| Normalización de texto | 11 casos formales entre particiones y valores límite | Confirma espacios repetidos, saltos, tabulaciones y tipos inválidos en las entradas cubiertas |
| Validación de mensajes | 16 casos formales, incluidos límites de 5/4 y 100/101 caracteres y reglas de decisión | Confirma las reglas existentes de longitud y los patrones incluidos en los casos |
| Enmascaramiento | 10 casos formales con valores limpios, patrones comunes, entradas inválidas y secretos múltiples | No constituye una evaluación exhaustiva de formatos reales de credenciales |
| Suite previa | 6 pruebas adicionales en `test_sanitizer.py` | Repite algunos comportamientos con ejemplos básicos |

El número de pruebas aprobadas es una evidencia de que los casos ejecutados satisfacen sus aserciones; no es una medida de cobertura ni una prueba de seguridad. No se generó un informe de cobertura. En particular, no hay una prueba aislada que demuestre el patrón `sk-` con una clave alfanumérica válida, y el código no elimina ni rechaza todos los secretos posibles. Por esa razón, el resultado debe interpretarse como verificación funcional parcial del sanitizador.

### Riesgos operacionales que permanecen

| Riesgo | Evidencia en la versión publicada | Mitigación pendiente |
|---|---|---|
| Un secreto no coincide con los patrones conocidos | Detección basada en regex en [sanitizer.py](sanitizer.py) | Ampliar fixtures sintéticos y evaluar detectores especializados; mantener revisión humana |
| Se comparte un diff antes de una sanitización completa | La HU-01 describe esta necesidad, pero el flujo no está integrado en la raíz | No enviar diffs automáticamente; integrar primero filtros de archivos, secretos y tamaño con pruebas |
| El usuario asume que ya existe generación por IA | El README conserva un contrato de servicio propuesto | Mantener explícita la diferencia entre diseño documentado y funcionalidad implementada |

**Pipeline:** la consulta a GitHub encontró cero workflows y cero ejecuciones antes de este cambio. El archivo [`.github/workflows/tests.yml`](.github/workflows/tests.yml) queda preparado localmente; su primera ejecución remota requiere publicar los cambios. La pestaña de [GitHub Actions](https://github.com/Apache112/CommitStandard-AI/actions) es el lugar para enlazar esa ejecución cuando exista.

### Pendientes

1. Integrar y probar el flujo de diff de staging en la raíz publicada, o retirar del README las capacidades aún no implementadas.
2. Completar la bitácora de IA de los módulos 1–6 y adjuntar la propuesta, entrevista, decisiones de diseño y evidencia de operación que no están en esta copia.
3. Añadir pruebas que demuestren detección de cada patrón sensible y evaluar falsos negativos; el enmascaramiento por regex no garantiza descubrir todo secreto.
4. Publicar el workflow y enlazar su primera ejecución exitosa.
5. Revisar la distribución de `FUNCIONANDO/` para que no dependa de un repositorio anidado local sin instrucciones reproducibles.

## 6. Reflexión ética y legal

| Principio | Decisión y análisis | Evidencia / límite |
|---|---|---|
| Datos personales — Ley 1581 de 2012 | No se envían diffs a un servicio externo desde la implementación verificada. Sin embargo, un diff puede contener datos personales; no es correcto afirmar que el proyecto nunca los procesa. | Código local en [sanitizer.py](sanitizer.py); no hay evaluación legal formal |
| Sesgo y falsos positivos | Los patrones explícitos evitan depender de un modelo para detectar estos formatos, pero pueden omitir secretos distintos y marcar texto legítimo. La cobertura de falsos positivos y negativos es incompleta. | Patrones en [sanitizer.py](sanitizer.py), casos en [tests/test_reglas.py](tests/test_reglas.py) |
| Transparencia | La bitácora registra decisiones de la semana 7 y reconoce propuestas descartadas; no contiene una bitácora completa de todos los módulos. | [bitacora_ia.md](bitacora_ia.md) |
| Responsabilidad | Revisé las pruebas propuestas y descarté una que podía pasar por la razón equivocada. La aprobación final del código y de su publicación sigue siendo responsabilidad humana. | [registro_pruebas.md](registro_pruebas.md) |
| Propiedad intelectual y política de uso | No se encontró un inventario de fuentes, licencias o política institucional de IA. No afirmo que todo el código sea original solo por no ver dependencias de ejecución externas. | `pyproject.toml` y bitácora disponibles; revisión de licencias pendiente |

El dilema principal es la tensión entre automatizar la generación de commits y proteger el código que se compartiría con un LLM externo. La decisión verificable fue no incorporar una llamada remota en la versión publicada. La sanitización por patrones es una defensa parcial, no una garantía: antes de enviar cambios a un proveedor se requiere revisión humana, consentimiento y cumplimiento de las políticas de la organización.

## 7. Aprendizajes

Aprendí a convertir requisitos de texto en particiones de equivalencia, valores límite y reglas de decisión, y a inspeccionar si una prueba realmente ejercita el comportamiento que dice cubrir. Confié demasiado en que un test que pasa demuestra su utilidad; el caso del patrón `sk-` mostró que hay que revisar el input y la salida observada. En un siguiente ciclo separaría las evidencias por módulo desde el inicio, mantendría una bitácora contemporánea y ejecutaría el pipeline remoto antes de declarar terminada una entrega.

## 8. Anexos

- [Bitácora de IA](bitacora_ia.md)
- [Registro de pruebas](registro_pruebas.md)
- [Revisión de seguridad](revision_seguridad.md)
- [Código del sanitizador](sanitizer.py)
- [Pruebas formales](tests/test_reglas.py)
- [Workflow de CI](.github/workflows/tests.yml)
- Repositorio: https://github.com/Apache112/CommitStandard-AI
