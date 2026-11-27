# Informe final del proyecto integrador

**Proyecto:** CommitStandard-AI — prototipo de preparación de commits convencionales
**Repositorio:** https://github.com/Apache112/CommitStandard-AI
**Fecha:** 27 de noviembre de 2026

> La consigna prohíbe incluir datos personales reales en el informe y el
> repositorio. Por ello, este PDF no incluye nombres, correos ni identificadores
> personales.

## 1. Resumen

CommitStandard-AI es un prototipo local en Python que valida mensajes de commit
y prepara un `git diff --cached` con exclusión de algunos archivos y redacción
heurística de patrones conocidos. La propuesta académica prevé consultar un
modelo de lenguaje, pero el código publicado no hace llamadas a servicios LLM,
no genera mensajes automáticamente ni implementa el Gateway del diseño. La IA
se documentó en el laboratorio de fundamentos, en la propuesta, en el diseño y
en la preparación de pruebas; la bitácora histórica no cubre todas las fases.
La suite local se verificó con pytest y Ruff; se añadieron pruebas que
encontraron y comprobaron una omisión real en la sanitización de líneas de
contexto/eliminación y bloques de claves privadas. El material de requisitos
recibido corresponde a otro proyecto, por lo que la brecha se declara en vez de
presentarse como evidencia válida.

## 2. Problema y usuario

El usuario previsto es una persona desarrolladora que prepara cambios en Git y
quiere mensajes de commit consistentes, además de reducir el riesgo de
compartir accidentalmente credenciales incluidas en un diff. La propuesta del
módulo 2 fija como meta que 18 de 20 mensajes sugeridos sean aceptados sin
edición; esa meta no se ha medido porque el repositorio no integra un LLM.

La solución actualmente disponible valida mensajes localmente y ofrece una CLI
que obtiene cambios staged, filtra algunos archivos y patrones, y muestra el
texto preparado para que la persona lo revise. El flujo no envía datos a un
servicio externo. El [README](README.md), la [propuesta](docs/propuesta.md) y el
[código](FUNCIONANDO/main.py) distinguen el prototipo del producto objetivo.

**Límite de requisitos:** el documento recibido para el módulo 3 describe una
aplicación de minimercado con ventas, inventario y fiados, no CommitStandard-AI.
No se puede usar esa entrevista como evidencia del usuario de este proyecto.
Los requisitos resumidos en [docs/requisitos.md](docs/requisitos.md) son una
reconstrucción retrospectiva que debe validarse; no reemplaza el artefacto
primario faltante.

## 3. La IA en el ciclo de vida

| Fase/módulo | Uso de IA que sí está documentado | Herramienta | Evidencia y verificación |
|---|---|---|---|
| 1. Fundamentos | Comparación de dos asistentes para generar una función de validación de correo; el informe académico registra pruebas ejecutadas y comparación de salidas. | DeepSeek y Gemini, según el original del módulo 1. | Resumen anonimizado en [evidencia_modulos.md](docs/evidencia_modulos.md). Es aprendizaje general, no una funcionalidad del producto. |
| 2. Propuesta | Se declara que Gemini ayudó a refinar la redacción y se propuso medir 18/20 sugerencias aceptadas. | Gemini. | [Propuesta](docs/propuesta.md). La meta no se ejecutó ni se midió. |
| 3. Requisitos | No hay un documento primario de requisitos de CommitStandard-AI entre los materiales recibidos. El archivo del módulo 3 es de otro proyecto y se excluye. | No verificable para este producto. | [Nota de discrepancia y reconstrucción](docs/requisitos.md). Requiere validación del estudiante/docente. |
| 4. Diseño | IA apoyó alternativas, diagramas, modelo de datos y rutas; el original registra correcciones humanas por privacidad y coherencia. | Gemini. | [Diseño y ADR](docs/diseno-adr.md). Se contrastaron los diagramas y rutas con la decisión de arquitectura; el backend descrito no está implementado. |
| 5. Código y pruebas | La bitácora registra asistencia para particiones, valores límite y tablas de decisión. La revisión final con IA ayudó a buscar huecos en la sanitización del diff. | Antigravity/Gemini en la bitácora existente; asistente de IA para la revisión final. | [Bitácora](bitacora_ia.md), [pruebas](tests) y [código](FUNCIONANDO/commit_guard.py). Los nuevos tests reproducen y luego cubren el defecto. |
| 6. Operación | No se encontró uso histórico de IA para despliegue u operación. Se configuró CI para verificar cambios. | GitHub Actions (automatización, no IA). | [Workflow](.github/workflows/tests.yml), [guía operativa](docs/operacion.md) y [ejecuciones](https://github.com/Apache112/CommitStandard-AI/actions). La página muestra el resultado vigente. |

La evidencia disponible permite explicar el uso de IA, pero **no demuestra uso
documentado y verificado de IA en las seis fases**. En particular, no se debe
presentar CI como IA ni atribuirle a la IA generación de código que la bitácora
no registra.

## 4. Verificación: propuestas incorrectas, incompletas o riesgosas

### Caso 1: ubicación de la base de datos en el diseño

- **Fase:** diseño.
- **Qué propuso la IA:** el borrador C4 situó la base de datos de métricas en el
  equipo del desarrollador.
- **Qué estaba mal:** contradice la alternativa Gateway seleccionada, que
  centraliza las métricas en el backend.
- **Cómo se detectó:** comparación de los contenedores C4 con el ADR y la
  matriz de alternativas.
- **Qué se hizo:** se movió la base de datos al límite del backend. El original
  del módulo 4 documenta la corrección; no hay un commit histórico individual
  asociado a ese cambio.
- **Evidencia:** [diseño y ADR](docs/diseno-adr.md).

### Caso 2: retención de diffs fuente en el modelo de datos

- **Fase:** diseño.
- **Qué propuso la IA:** el modelo inicial incluía guardar contenido del diff.
- **Riesgo:** conservar código fuente y datos que pueden ser sensibles no era
  necesario para calcular aceptación y aumentaba el riesgo de exposición.
- **Cómo se detectó:** revisión de los atributos frente al objetivo de medir
  feedback sin almacenar el diff original.
- **Qué se hizo:** se retiró la persistencia del código fuente del diseño. La
  decisión está descrita en el original del módulo 4, sin commit histórico
  individual.
- **Evidencia:** [diseño y ADR](docs/diseno-adr.md).

### Caso 3: una prueba generada para `sk-` no ejercitaba el patrón

- **Fase:** pruebas.
- **Qué propuso la IA:** una entrada con caracteres que no pertenecían a la
  clase alfanumérica del regex para `sk-`.
- **Qué estaba mal:** un test verde con una entrada que no coincide no demuestra
  que se detecte el patrón.
- **Cómo se detectó:** inspección del regex y de la entrada sugerida.
- **Qué se hizo:** se descartó esa prueba en vez de contabilizarla como
  cobertura; la brecha se mantuvo explícita en el informe.
- **Evidencia:** [bitácora](bitacora_ia.md) y [patrones](sanitizer.py).

### Verificación adicional de código en la preparación final

La revisión asistida por IA observó que el prototipo solo buscaba secretos en
líneas añadidas (`+`). Pruebas con valores sintéticos confirmaron que un patrón
en una línea de contexto o eliminada podía sobrevivir; otro caso confirmó que
solo se ocultaba el marcador de una clave privada multilínea, no su contenido.
Se amplió la redacción a líneas añadidas, eliminadas y de contexto, se añadió
estado para el bloque privado y se decidió fallar de forma explícita si el
bloque queda incompleto. La primera prueba sugerida usó un archivo `.pem`, que
el filtro de archivos ya excluye; pytest mostró que la prueba no estaba midiendo
la redacción. Se corrigió el fixture a un archivo sintético permitido y se
volvieron a ejecutar las pruebas.

**Conclusión frente a la rúbrica:** hay casos verificables de diseño y pruebas,
y una corrección de código actual. Sin embargo, no hay tres casos válidos de
errores de IA en tres fases distintas con commits históricos trazables. Los
ejemplos de requisitos del minimercado pertenecen a otro proyecto y no se usan
para completar artificialmente ese criterio.

## 5. Estado final del sistema

### Arquitectura y funcionalidades

- `sanitizer.py`: normalización, redacción de patrones conocidos y validación
  de mensajes de 5 a 100 caracteres.
- `FUNCIONANDO/commit_guard.py`: obtención del diff staged, exclusión de una
  lista limitada de archivos, redacción heurística, control de tamaño y manejo
  explícito de bloques de clave privada.
- `FUNCIONANDO/main.py`: CLI que imprime el diff preparado y un prompt manual.
- `tests/`: pruebas de reglas, sanitización y comportamiento del prototipo.

No existen plugin de IDE, backend Gateway, endpoints, base de datos, generación
automática de mensajes ni conexión a un proveedor LLM. El [diseño](docs/diseno-adr.md)
describe una arquitectura objetivo, no funcionalidades terminadas.

### Verificación

La suite comprende pruebas de particiones de equivalencia, valores límite,
tablas de decisión y casos de sanitización del diff. La ejecución local final
con `py -3.14 -m pytest -q` obtuvo **53 passed**; `ruff check sanitizer.py
test_sanitizer.py tests FUNCIONANDO` terminó con **All checks passed**. El
workflow corre pytest y Ruff en Python 3.10 y 3.14; consulta la página de
[GitHub Actions](https://github.com/Apache112/CommitStandard-AI/actions) para
verificar el resultado remoto posterior a la publicación de estos cambios.

### Pendientes

1. Validar y versionar los requisitos correctos de CommitStandard-AI; el
   documento recibido de módulo 3 es incompatible.
2. Completar la bitácora de IA de las seis fases con evidencia contemporánea,
   herramienta, propósito, verificación y commit.
3. Añadir integración de la CLI en un repositorio Git temporal y ampliar casos
   de archivos, falsos positivos y formatos de secretos.
4. Si se implementa el Gateway/LLM, definir consentimiento, retención, controles
   de privacidad, manejo de fallos y medición real de 18/20.
5. Obtener casos de error de IA de tres fases distintas y enlazar los commits
   originales; no se reconstruyen de memoria.
6. Completar el inventario de licencias y una política de uso/atribución de IA.

## 6. Reflexión ética y legal

| Principio | Decisión aplicada al proyecto | Evidencia y límite |
|---|---|---|
| Datos personales — Ley 1581 de 2012 | La herramienta local no envía diffs a un proveedor ni conserva una base de datos. Aun así, los diffs pueden contener datos personales, identificadores o secretos; el sistema los procesa localmente. | [CLI](FUNCIONANDO/main.py), [sanitizador](FUNCIONANDO/commit_guard.py). No hay evaluación legal formal. |
| Sesgo y errores de clasificación | Las expresiones regulares pueden omitir formatos no conocidos o marcar texto legítimo. No se afirma detección completa. | Patrones y [casos de prueba](tests/test_commit_guard.py). |
| Transparencia | Se declara que la IA no está integrada y que el Gateway es diseño futuro. Se excluyen del informe los datos identificativos de los documentos fuente. | [README](README.md), [evidencia por módulo](docs/evidencia_modulos.md). |
| Responsabilidad | La revisión final y aprobación de cualquier diff o commit son humanas. La salida limpia es heurística y exige inspección. | [Guía de operación](docs/operacion.md). |
| Propiedad intelectual | El repositorio no contiene inventario completo de licencias ni una política institucional de IA. Se deben verificar antes de una distribución externa. | Brecha documentada; no se declara originalidad total a partir de la ausencia de dependencias externas. |

El dilema principal es la utilidad de pedir a un LLM mensajes de commit frente
al riesgo de exponer código fuente y datos personales. La decisión actual fue
no implementar la llamada externa y no afirmar que los patrones garantizan
privacidad. Antes de integrar un proveedor se necesita informar al usuario,
obtener consentimiento, definir tratamiento/retención y completar pruebas
independientes.

## 7. Aprendizajes

Aprendí que una prueba aprobada solo aporta evidencia si la entrada realmente
ejercita la regla que pretende comprobar. También confirmé que la IA puede
acelerar propuestas de diseño y pruebas, pero requiere contraste con el código,
los criterios del usuario y los límites de privacidad. El error de alcance
entre el documento de requisitos y el proyecto demuestra la importancia de
verificar que cada artefacto pertenezca al mismo producto. En una siguiente
iteración mantendría prompts, salidas, revisiones y commits en una bitácora
desde cada módulo, y mediría el criterio 18/20 con una muestra reproducible.

## 8. Anexos y evidencias

- [Mapa de evidencias de los módulos 1–6](docs/evidencia_modulos.md)
- [Propuesta](docs/propuesta.md)
- [Requisitos y brecha del módulo 3](docs/requisitos.md)
- [Diseño y ADR](docs/diseno-adr.md)
- [Guía de operación](docs/operacion.md)
- [Bitácora de IA](bitacora_ia.md)
- [Registro de pruebas](registro_pruebas.md)
- [Revisión de seguridad](revision_seguridad.md)
- [Código y pruebas](tests)
- [Repositorio](https://github.com/Apache112/CommitStandard-AI)
- [Última ejecución de GitHub Actions](https://github.com/Apache112/CommitStandard-AI/actions)
