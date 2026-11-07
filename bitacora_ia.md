# Bitácora de uso de IA

Proyecto: CommitStandard AI
Estudiante: Jorge Alberto Apache Cardozo
Funcionalidad: HU-01 Generación de propuesta de commit basada en cambios staged.
Asistente usado: Gemini (Modo Chat)

## Entradas

### Entrada 1
- **Fecha:** 2026-11-07
- **Prompt o sugerencia:** Solicité la estructura inicial del contrato de la función para el archivo README.md.
- **Decisión:** Aceptada
- **Por qué:** Definió con precisión los tipos de entrada (`str` e `int`) y una salida estructurada en formato JSON/Dict ideal para una API REST.
- **Verificación:** Se documentó en el README.md del repositorio y sirvió como guía de desarrollo.
- **Commit relacionado:** `docs: agregar contrato de la funcion en README`

### Entrada 2
- **Fecha:** 2026-11-07
- **Prompt o sugerencia:** El asistente sugirió usar una biblioteca de terceros pesada para buscar secretos en el diff de git.
- **Decisión:** Rechazada
- **Por qué:** El ADR-001 de mi proyecto exige bajo consumo de recursos y baja latencia. Añadir dependencias externas retrasaría el backend proxy.
- **Verificación:** Decidí usar expresiones regulares (`re`) nativas de Python, logrando que las pruebas pasaran en menos de 0.01 segundos.
- **Commit relacionado:** `feat: implementar logica de sanitizacion de diffs`

### Entrada 3
- **Fecha:** 2026-11-07
- **Prompt o sugerencia:** Proponer casos de prueba límite para evaluar el comportamiento del sanitizador de código.
- **Decisión:** Aceptada con cambios
- **Por qué:** Sugirió probar archivos extremadamente grandes, pero olvidó el caso crítico del archivo `.env` completo que restringe el ADR corporativo.
- **Verificación:** Tomé su sugerencia e incluí manualmente el caso de prueba `test_preparar_diff_ignora_archivos_env_completos`.
- **Commit relacionado:** `test: escribir pruebas unitarias para el sanitizador`

### Entrada 4
- **Fecha:** 2026-11-07
- **Prompt o sugerencia:** Implementar la lógica de filtrado de líneas usando bucles condicionales.
- **Decisión:** Aceptada
- **Por qué:** Permite analizar línea por línea el git diff e interceptar únicamente las inserciones que comprometan la seguridad de la empresa.
- **Verificación:** Se ejecutó `pytest` y se validó que las líneas de código normales no se vieran afectadas.
- **Commit relacionado:** `feat: implementar logica de sanitizacion de diffs`

### Entrada 5
- **Fecha:** 2026-11-07
- **Prompt o sugerencia:** Refactorizar la función utilizando una función anidada interna para compilar la expresión regular.
- **Decisión:** Rechazada
- **Por qué:** Compilar la expresión regular dentro de la función en cada ejecución degrada la latencia (RNF-02). Es mejor compilarla globalmente.
- **Verificación:** Moví la compilación de la expresión regular fuera del bucle logrando mayor legibilidad y rendimiento de CPU.
- **Commit relacionado:** `refactor: optimizar busqueda de expresiones regulares`

## Resumen

| Decisión | Cantidad |
|---|---|
| Aceptadas | 2 |
| Aceptadas con cambios | 1 |
| Rechazadas | 2 |

## Errores que atraparon las pruebas
La prueba de caso límite `test_preparar_diff_censura_secretos_limite` falló inicialmente porque el código generado por la IA reemplazaba toda la línea del diff borrando código válido adyacente al secreto. Lo corregí modificando la expresión regular con grupos de captura (`re.sub`) para alterar únicamente el valor de la asignación tras el símbolo `=` y mantener las variables estructurales intactas.

## Reflexión final (5 a 8 líneas)
El asistente de IA fue un excelente aliado para estructurar rápidamente las pruebas unitarias y mapear escenarios que no había considerado inicialmente. Sin embargo, su desconocimiento de las restricciones de rendimiento locales de mi proyecto causó que sugiriera componentes innecesarios que debieron ser rechazados. Las pruebas escritas bajo el enfoque TDD fueron fundamentales, ya que detectaron de forma inmediata un fallo crítico de lógica en el reemplazo de strings que habría corrompido los diffs de código legítimos. En la próxima funcionalidad, priorizaré refinar mejor el contexto inicial sobre restricciones antes de pedir código.
