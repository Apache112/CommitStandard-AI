# Diseño y ADR

## Diseño objetivo descrito en el módulo 4

El documento de diseño eligió la alternativa B: extensión de IDE más un Gateway
backend que sanitizaría el diff, aplicaría políticas y consultaría un LLM. El
ADR-001 favorece el control de privacidad y costos centralizado frente a una
llamada directa desde el IDE. Se identificaron como consecuencias el costo de
operar el backend y el riesgo de un punto único de falla.

El diseño también propone diagramas C4, un modelo de datos para feedback y
métricas, y endpoints REST. Son diseños académicos; no describen servicios que
existan en esta versión del repositorio.

## Verificaciones y correcciones registradas

1. **Ubicación de la base de datos:** el borrador de IA la ubicaba en el equipo
   del desarrollador. Se movió al límite del backend en el diagrama de
   contenedores, coherente con la alternativa seleccionada.
2. **Rutas REST:** el borrador usó verbos en algunas rutas. Se corrigieron a
   rutas orientadas a recursos y se añadieron códigos de error.
3. **Retención de código:** el modelo inicial incluía guardar el diff fuente
   completo. Se eliminó esa persistencia del diseño por privacidad.
4. **Fine-tuning:** se descartó una propuesta de reentrenamiento continuo por
   sobreingeniería y costo; se prefirió probar primero un prompt especializado.

El documento compartido del módulo 4 contiene estos detalles. No hay commits
históricos del repositorio que tracen cada corrección individual; este resumen
no inventa esos enlaces.

## Diferencia con la implementación

El código real es una CLI local en Python que prepara y muestra texto. No existe
la extensión de VS Code, el Gateway Node.js, la base de datos, la API REST, el
enrutamiento a un modelo local/cloud ni la medición del 90%. El diseño objetivo
no debe presentarse como arquitectura implementada.

## Referencias

- [Implementación de la CLI](../FUNCIONANDO/main.py)
- [Preparación del diff](../FUNCIONANDO/commit_guard.py)
- [Propuesta](propuesta.md)
- [Requisitos](requisitos.md)
