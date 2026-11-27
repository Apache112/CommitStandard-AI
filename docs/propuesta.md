# Propuesta del proyecto

## Problema y usuario

El proyecto aborda la dificultad de mantener mensajes de commit consistentes y
útiles en equipos de desarrollo. Su usuario previsto es la persona que prepara
cambios en un repositorio Git y necesita describirlos con Conventional Commits.
También se busca reducir el riesgo de compartir accidentalmente credenciales
incluidas en un diff.

## Solución prevista

La propuesta del módulo 2 describe un asistente para inspeccionar cambios staged,
preparar un diff y solicitar una sugerencia de mensaje convencional a un modelo
de lenguaje. El criterio de éxito propuesto fue que al menos 18 de 20 mensajes
de una muestra de prueba fueran aceptados sin edición (90%).

## Estado real en el repositorio

La versión publicada prepara y muestra un diff con filtros y redacción
heurística. No implementa una llamada a un LLM, no mide la tasa de aceptación de
20 mensajes y no está integrada como plugin de IDE. Por tanto, el criterio del
90% es una meta propuesta, no un resultado medido.

## Uso de IA registrado

El documento original del módulo 2 declara que Gemini ayudó a refinar la
redacción de la propuesta. También contiene un banco de diez prompts de práctica
con ChatGPT, GitHub Copilot, Claude y otras herramientas; varios ejercicios
(facturación, correo, biblioteca, pagos y APIs) no pertenecen al alcance de
CommitStandard-AI y no se usan aquí como evidencia de funcionalidades.

Este resumen se preparó a partir del documento compartido para la entrega final.
El documento original contiene datos identificativos y no se copia al
repositorio público.
