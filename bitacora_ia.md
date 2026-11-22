# Bitácora de IA — CommitStandard-AI

---

## Semana 7 — 22 de noviembre de 2026

### Entrada 1 — Diseño de particiones de equivalencia

**Prompt enviado a la IA:**
> "Tengo la función `sanitize_text(text: str) -> str` que limpia espacios, saltos de línea y tabulaciones, y lanza TypeError si el input no es str. Ayúdame a identificar las particiones de equivalencia para diseñar casos de prueba."

**Respuesta de la IA (resumen):**
La IA identificó tres particiones válidas (texto con espacios múltiples, con `\n`, con `\t`) y tres inválidas (entero, None, lista). Sugirió además probar texto ya limpio como clase de equivalencia de identidad.

**Decisión:**
✅ Conservé todas las particiones — cubren tanto el comportamiento esperado (PE 1-4) como los guards de tipo (PE 5-7). Añadí PE-4 (texto ya limpio) por iniciativa propia, ya que la IA no la incluyó explícitamente.

---

### Entrada 2 — Generación de pruebas con valores límite para `validate_commit_message`

**Prompt enviado a la IA:**
> "La función `validate_commit_message` acepta mensajes entre 5 y 100 caracteres. Genera pruebas de valores límite para ese rango. Aquí está el código: [código del método]"

**Respuesta de la IA (resumen):**
Generó 4 pruebas: longitud 5 (True), longitud 4 (False), longitud 100 (True), longitud 101 (False). Los nombres de función eran descriptivos pero usaban inglés.

**Decisión:**
✅ Conservé las 4 pruebas. Adapté los nombres al estilo del proyecto en español (`test_vl_longitud_minima_valida`, etc.). Los valores de entrada (cadenas de `"a" * N`) son correctos y cubren exactamente las fronteras.

---

### Entrada 3 — Tabla de decisión para seguridad del commit

**Prompt enviado a la IA:**
> "Necesito una tabla de decisión para `validate_commit_message` que combine dos condiciones: (C1) longitud entre 5-100 y (C2) presencia de credenciales. Genera las 4 reglas y luego escribe los tests pytest."

**Respuesta de la IA (resumen):**
Generó correctamente las 4 reglas (R1: OK+limpio→True, R2: OK+secreto→False, R3: corto+limpio→False, R4: corto+secreto→False). Para R2 usó solo el patrón `api_key`; la IA no cubrió `password` ni `ghp_` por separado.

**Decisión:**
✅ Conservé R1, R3 y R4 sin cambios.  
⚠️ **Corregí R2**: la IA usó un solo caso para R2. Dividí en R2, R2b y R2c para cubrir los 3 patrones del módulo (`api_key`, `password`, `ghp_`). Esta decisión es mía — sin la corrección, dos de los tres patrones de detección quedarían sin prueba.

---

### Entrada 4 — Pruebas para `mask_sensitive_data`

**Prompt enviado a la IA:**
> "Escribe pruebas para `mask_sensitive_data`. La función tiene 3 patrones: (1) api_key/secret/password/token, (2) ghp_ + 36 chars, (3) sk- + 48 chars. Usa particiones de equivalencia y valores límite."

**Respuesta de la IA (resumen):**
Generó pruebas para los tres patrones principales. Para VL sugirió probar con cadena vacía y múltiples secretos. No incluyó el caso del límite inferior del regex (`{8,}`, exactamente 8 caracteres de valor).

**Decisión:**
✅ Conservé todo lo generado.  
➕ **Añadí** `test_vl_secreto_longitud_minima`: prueba con valor de exactamente 8 caracteres para verificar el límite inferior del patrón `{8,}`. La IA no lo propuso; lo identifiqué revisando el regex en el código fuente.  
🗑️ **Descarté** la prueba para `sk-` + 48 chars que generó la IA: el patrón existe en el código pero la prueba requería generar 48 chars alfanuméricos y la IA usó una cadena con caracteres especiales que no matchean el regex. Preferí no incluirla a incluir una prueba que falla por razones incorrectas.

---

### Entrada 5 — Verificación de fallo ante código defectuoso

**Prompt enviado a la IA:**
> "¿Cómo puedo introducir un error temporal en `sanitizer.py` para verificar que mis pruebas lo detectan?"

**Respuesta de la IA:**
Sugirió comentar el `.strip()` al final de `sanitize_text` y ejecutar pytest para ver cuáles pruebas fallan.

**Acción realizada:**
- Comenté `.strip()` en `sanitize_text`
- Ejecuté `pytest tests/test_reglas.py -v`
- **Fallaron:** `test_vl3_solo_espacios` (esperaba `""`, obtuvo `" "`) y `test_pe4_texto_ya_limpio` (esperaba sin espacios al inicio/fin)
- Restauré el código original

**Conclusión:** Las pruebas detectan correctamente la regresión. Las pruebas de valores límite (`test_vl3_solo_espacios`) fueron las más sensibles, como se esperaba.

---

## Reflexión general

La IA fue útil para generar el esqueleto de las pruebas rápidamente, pero requirió supervisión en:
1. **Cobertura de patrones múltiples** (R2 de la tabla de decisión — la IA usó solo 1 de 3 patrones)
2. **Límites de regex** (`{8,}` — la IA no analizó el regex en profundidad)
3. **Calidad de inputs** (el test de `sk-` generó chars inválidos para el regex)

El criterio propio fue esencial para identificar estas brechas y decidir qué conservar, corregir o descartar.
