# Sustentación — CommitStandard-AI

## 1. Problema y propósito

- Los mensajes de commit pueden exponer por accidente credenciales copiadas desde cambios de código.
- Propósito: apoyar mensajes convencionales y reducir la exposición de patrones conocidos.
- No se conecta a un LLM remoto en la versión publicada.
- Pregunta guía: ¿qué hizo la IA y cómo comprobé sus propuestas?

## 2. Usuario y requisitos

- Usuario previsto: desarrolladores que preparan commits con Git.
- El README describe HU-01: revisar el diff de staging, sanitizar y controlar tamaño.
- `FUNCIONANDO/` incluye un prototipo aparte para sanitizar diffs staged; aún no está integrado con `Sanitizer`.
- Límite: no encontré la entrevista ni la propuesta original de módulos 1–2.

## 3. Ciclo de vida y uso de IA

- Evidencia completa disponible: bitácora de semana 7 sobre pruebas.
- IA registrada: Antigravity (Gemini), apoyo para PE, valores límite y tabla de decisión.
- Las evidencias de los módulos 1–6 no están completas en la copia recibida.
- Criterio: reportar solo lo corroborable, sin reconstruir prompts ni resultados de memoria.

## 4. Producto y arquitectura

- `sanitizer.py`: normaliza texto, oculta algunos patrones de secretos y valida mensajes.
- `tests/`: pruebas formales para ambos componentes; `README.md`: contrato y límites.
- Resultado local: 50 pruebas aprobadas en Python 3.14.
- No afirmar como implementado: integración del diff en la raíz ni generación por API de LLM.

## 5. Verificación crítica de IA

- R2: la propuesta cubría `api_key`, no las variantes `password` y `ghp_`; agregué casos.
- Regex `{8,}`: añadí un test justo en el mínimo de 8 caracteres.
- Patrón `sk-`: descarté una entrada con caracteres que no coincidían; un test verde no basta.
- Hallazgos y decisiones quedan en `bitacora_ia.md` y `tests/test_reglas.py`.

## 6. Ética, privacidad y seguridad

- El código local verificado no envía diffs a servicios externos.
- Los regex solo detectan patrones conocidos; pueden omitir secretos y tener falsos positivos.
- Un diff puede contener datos personales; no declarar que el sistema no los procesa.
- La decisión humana y el consentimiento siguen siendo necesarios antes de compartir código.

## 7. Estado de entrega y pendientes

- Workflow CI preparado para Python 3.10 y 3.14: pruebas + Ruff en ambos componentes.
- La ejecución remota se dispara al publicar; comprueba el resultado en GitHub Actions.
- Completar bitácora/evidencias de módulos 1–6 y pruebas de integración de la CLI.
- Adjunta el enlace del run correspondiente a esta publicación.

## 8. Cierre y preguntas

- Aprendizaje: verificar una prueba significa confirmar que detecta el comportamiento correcto.
- Próximo paso: integrar el flujo de diff, ampliar pruebas y ejecutar CI remoto antes de cerrar.
- Dilema central: automatización frente a privacidad del código.
- Preguntas.
