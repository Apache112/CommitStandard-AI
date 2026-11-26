# Informe final del proyecto integrador

**Proyecto:** CommitStandard-AI — asistente para commits convencionales

**Estudiante:** Jorge Alberto Apache Cardozo

**Repositorio:** https://github.com/Apache112/CommitStandard-AI

**Fecha:** 2026-11-26

> **Alcance de esta versión del informe.** Se contrastaron las afirmaciones con los archivos del repositorio y se ejecutaron las pruebas localmente. La copia disponible no contiene evidencia primaria de todos los módulos 1–6 ni una ejecución remota de GitHub Actions. La carpeta `FUNCIONANDO/` contiene un prototipo versionado por separado del sanitizador principal; sus límites de verificación se declaran en vez de atribuir resultados no comprobados.

## 1. Resumen

CommitStandard-AI explora cómo ayudar a quienes preparan mensajes de commit y reducir la exposición accidental de secretos. `sanitizer.py` normaliza texto, enmascara patrones conocidos y valida mensajes; `FUNCIONANDO/` contiene un prototipo de preparación de diffs staged. La bitácora disponible documenta el uso de IA para diseñar pruebas, no el proceso completo de los seis módulos. Verifiqué el código con 50 pruebas automatizadas: las 50 pasaron en Python 3.14. El primer workflow remoto completó con éxito pruebas y Ruff en Python 3.10 y 3.14. El prototipo aún no se conecta a un LLM.

## 2. Problema y usuario

**Usuario objetivo:** desarrolladores que crean commits convencionales y quieren evitar incluir accidentalmente credenciales u otros valores sensibles en el texto que revisan o comparten.

**Necesidad:** contar con una revisión local previa a la generación de un mensaje de commit. La propuesta documentada en el [README](README.md) plantea tomar el diff de staging, retirar secretos y archivos prohibidos, y validar el tamaño antes de entregar el texto a un LLM. La motivación es reducir errores humanos y limitar la divulgación de código.

**Límite de la evidencia:** no se encontró en esta copia una propuesta del módulo 1, registro de entrevista o validación de usuario del módulo 2. Por tanto, la descripción del usuario y su necesidad se presenta como el planteamiento del proyecto, no como hallazgo confirmado mediante entrevista.

## 3. La IA en el ciclo de vida

| Módulo y fase | Uso de IA que puede sustentarse | Herramienta registrada | Evidencia disponible | Verificación |
|---|---|---|---|---|
| 1. Fundamentos | La bitácora disponible no registra esta fase. | No consta | No se encontró propuesta del módulo 1 | No verificable con los archivos recibidos |
| 2. Requisitos | El README contiene HU-01 y un contrato propuesto para preparar el diff. No se encontró el historial de prompts ni la entrevista. | No consta en la bitácora disponible | [README](README.md) | Contrasté el contrato con el prototipo separado en `FUNCIONANDO/`; no se comprobó la validación con usuarios |
| 3. Diseño | Se documentó la firma, entradas y salidas esperadas del preparador de diff. | No consta en la bitácora disponible | [README](README.md), [FUNCIONANDO/commit_guard.py](FUNCIONANDO/commit_guard.py) | Contrasté contrato, código y pruebas; no se verificó la integración con una API de LLM |
| 4. Código | `Sanitizer` y el prototipo `commit_guard` implementan normalización, redacción y preparación de diffs. La bitácora no conserva prompts de generación de este código. | No consta | [sanitizer.py](sanitizer.py), [FUNCIONANDO/commit_guard.py](FUNCIONANDO/commit_guard.py), [FUNCIONANDO/main.py](FUNCIONANDO/main.py) | Revisión del código, lint y ejecución de la suite |
| 5. Pruebas | La IA ayudó a proponer particiones de equivalencia, valores límite y tabla de decisión; también se registraron correcciones y descartes. | Antigravity (Gemini), según la [bitácora](bitacora_ia.md) | [bitacora_ia.md](bitacora_ia.md), [registro_pruebas.md](registro_pruebas.md), [tests](tests) | `pytest`: 50 passed; revisión manual de entradas y salidas |
| 6. Operación | Se documentó una revisión de seguridad. El workflow ejecuta pruebas y lint en push y pull request. | La herramienta de revisión no está corroborada en la bitácora disponible | [revision_seguridad.md](revision_seguridad.md), [workflow](.github/workflows/tests.yml) | `ruff` y `pytest` localmente; el primer run remoto en ambas versiones de Python terminó correctamente |

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
- [FUNCIONANDO/commit_guard.py](FUNCIONANDO/commit_guard.py) y [FUNCIONANDO/main.py](FUNCIONANDO/main.py): prototipo separado para leer el diff staged, filtrar algunos archivos y secretos, y mostrar el diff limpio.
- [tests/test_commit_guard.py](tests/test_commit_guard.py): casos automatizados para el comportamiento principal del prototipo.

El prototipo está versionado en una carpeta independiente, no integrado con `Sanitizer`. Las pruebas ejercitan la preparación de texto, pero no ejecutan la CLI contra un repositorio Git de prueba. Ninguna versión integra una llamada a una API de LLM.

### Funcionalidades y verificación

| Funcionalidad | Estado comprobado |
|---|---|
| Normalizar espacios, saltos de línea y tabulaciones | Implementada y probada |
| Enmascarar patrones comunes de credenciales | Implementada con cobertura parcial |
| Validar tipo y longitud del mensaje de commit | Implementada y probada |
| Preparar y sanitizar texto de diff para `git diff --cached` | Prototipo en `FUNCIONANDO/`; sanitización probada, ejecución real de Git/CLI pendiente |
| Generar automáticamente un mensaje mediante API de LLM | No implementada |

**Pruebas:** `py -3.14 -m pytest -q` produjo **50 passed** el 26 de noviembre de 2026: 37 pruebas en `tests/test_reglas.py`, 6 en `test_sanitizer.py` y 7 en `tests/test_commit_guard.py`. `ruff check sanitizer.py test_sanitizer.py tests FUNCIONANDO` también pasó localmente. El resultado local de CI no sustituye una ejecución de GitHub Actions.

### Condiciones para considerar completa la HU-01

La HU-01 del README se refiere al diff staged, no solo a validar un mensaje. Para evitar confundir el estado actual con el objetivo, estas son condiciones pendientes que deben probarse antes de presentarla como terminada:

1. **Origen y errores:** probar la ejecución de Git desde un repositorio temporal y distinguir ausencia de cambios de errores del proceso.
2. **Archivos excluidos:** ampliar pruebas a todos los patrones de archivos prohibidos y confirmar que no se descarten archivos permitidos por coincidencias parciales.
3. **Redacción:** añadir fixtures sintéticos para todos los patrones (incluidos `sk-` y claves privadas) y entradas negativas para vigilar falsos positivos.
4. **Tamaño:** agregar pruebas de frontera exacta, un byte por debajo y un byte por encima del límite de bytes UTF-8.
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
| Preparación del diff | 7 casos en `tests/test_commit_guard.py` | Cubre secretos sintéticos, `.env`, entradas vacías y tamaño; no ejecuta Git real ni la CLI |

El número de pruebas aprobadas es una evidencia de que los casos ejecutados satisfacen sus aserciones; no es una medida de cobertura ni una prueba de seguridad. No se generó un informe de cobertura. En particular, no hay una prueba aislada que demuestre el patrón `sk-` con una clave alfanumérica válida, y el código no elimina ni rechaza todos los secretos posibles. Por esa razón, el resultado debe interpretarse como verificación funcional parcial del sanitizador.

### Riesgos operacionales que permanecen

| Riesgo | Evidencia en la versión publicada | Mitigación pendiente |
|---|---|---|
| Un secreto no coincide con los patrones conocidos | Detección basada en regex en [sanitizer.py](sanitizer.py) | Ampliar fixtures sintéticos y evaluar detectores especializados; mantener revisión humana |
| Se comparte un diff antes de una sanitización completa | Hay un prototipo separado, pero no una API LLM ni pruebas de ejecución real de Git | No enviar diffs automáticamente; completar pruebas de integración y revisión humana |
| El usuario asume que ya existe generación por IA | El README conserva un contrato de servicio propuesto | Mantener explícita la diferencia entre diseño documentado y funcionalidad implementada |

**Pipeline:** el primer run remoto, asociado al commit `38557ce`, terminó correctamente para Python 3.10 y 3.14. La [ejecución inicial](https://github.com/Apache112/CommitStandard-AI/actions/runs/45844098615) registra el resultado; la página de [GitHub Actions](https://github.com/Apache112/CommitStandard-AI/actions) muestra las ejecuciones posteriores y la más reciente.

### Pendientes

1. Añadir pruebas de integración de la CLI y de obtención de diffs staged en un repositorio temporal.
2. Completar la bitácora de IA de los módulos 1–6 y adjuntar la propuesta, entrevista, decisiones de diseño y evidencia de operación que no están en esta copia.
3. Añadir pruebas que demuestren detección de cada patrón sensible y evaluar falsos negativos; el enmascaramiento por regex no garantiza descubrir todo secreto.
4. Publicar el workflow y enlazar su primera ejecución exitosa.
5. Documentar los límites del prototipo separado y decidir si se integra con `Sanitizer` o permanece como herramienta experimental.

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
