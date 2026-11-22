# Registro de Pruebas — CommitStandard-AI
**Semana 7 | Pruebas Unitarias con Técnicas Formales apoyadas en IA**

---

## 1. Módulo bajo prueba

**Archivo:** `sanitizer.py`  
**Clase:** `Sanitizer`  
**Funciones probadas:**
- `sanitize_text(text)`
- `mask_sensitive_data(text)`
- `validate_commit_message(message)`

---

## 2. Particiones de Equivalencia

### 2.1 `sanitize_text(text)`

| ID | Clase de Equivalencia | Entrada representativa | Salida esperada | Válida |
|----|-----------------------|------------------------|-----------------|--------|
| PE-1 | Texto con espacios múltiples | `"  Hola   Mundo  "` | `"Hola Mundo"` | ✅ |
| PE-2 | Texto con saltos de línea `\n` | `"error\nen prod"` | `"error en prod"` | ✅ |
| PE-3 | Texto con tabulaciones `\t` | `"feat:\tadd"` | `"feat: add"` | ✅ |
| PE-4 | Texto ya limpio | `"fix: corregir bug"` | sin cambios | ✅ |
| PE-5 | Tipo entero | `12345` | `TypeError` | ❌ |
| PE-6 | `None` | `None` | `TypeError` | ❌ |
| PE-7 | Lista | `["fix: algo"]` | `TypeError` | ❌ |

### 2.2 `validate_commit_message(message)`

| ID | Clase de Equivalencia | Entrada representativa | Salida esperada | Válida |
|----|-----------------------|------------------------|-----------------|--------|
| PE-1 | Mensaje convencional bien formado | `"feat: añadir OAuth2"` | `True` | ✅ |
| PE-2 | Cadena vacía | `""` | `False` | ❌ |
| PE-3 | `None` | `None` | `False` | ❌ |
| PE-4 | Entero | `42` | `False` | ❌ |
| PE-5 | Mensaje muy corto (< 5 chars) | `"x"` | `False` | ❌ |
| PE-6 | Mensaje con credencial expuesta | `"fix: api_key=abc..."` | `False` | ❌ |

### 2.3 `mask_sensitive_data(text)`

| ID | Clase de Equivalencia | Entrada representativa | Salida esperada | Válida |
|----|-----------------------|------------------------|-----------------|--------|
| PE-1 | Sin datos sensibles | `"feat: agregar reportes"` | texto sin cambios | ✅ |
| PE-2 | Con `api_key=` | `"api_key=AbCdEfGh..."` | contiene `[REDACTED]` | ✅ |
| PE-3 | Con `password=` | `"password=Pass123..."` | contiene `[REDACTED]` | ✅ |
| PE-4 | Con token GitHub `ghp_` | `"ghp_BBBBB..."` | contiene `[REDACTED]` | ✅ |
| PE-5 | Tipo `None` | `None` | `TypeError` | ❌ |
| PE-6 | Tipo entero | `999` | `TypeError` | ❌ |

---

## 3. Valores Límite

### 3.1 `sanitize_text(text)` — longitud de entrada

| ID | Valor Límite | Entrada | Salida esperada |
|----|-------------|---------|-----------------|
| VL-1 | Cadena vacía (límite inferior) | `""` | `""` |
| VL-2 | Un solo carácter | `"x"` | `"x"` |
| VL-3 | Solo espacios | `"     "` | `""` |
| VL-4 | Cadena de 1000 chars | `"a" * 1000` | misma cadena |

### 3.2 `validate_commit_message(message)` — longitud (rango 5–100)

| ID | Valor Límite | Longitud | Resultado |
|----|-------------|----------|-----------|
| VL-1 | Mínimo válido | 5 chars | `True` |
| VL-2 | Justo bajo el mínimo | 4 chars | `False` |
| VL-3 | Máximo válido | 100 chars | `True` |
| VL-4 | Justo sobre el máximo | 101 chars | `False` |

### 3.3 `mask_sensitive_data(text)` — casos límite

| ID | Valor Límite | Entrada | Resultado |
|----|-------------|---------|-----------|
| VL-1 | Cadena vacía | `""` | `""` |
| VL-2 | Múltiples secretos | texto con 2+ patrones | 2+ `[REDACTED]` |
| VL-3 | Secreto de 8 chars (mínimo patrón) | `"token=12345678"` | `[REDACTED]` |

---

## 4. Tabla de Decisión — `validate_commit_message`

**Condiciones:**
- C1: Longitud entre 5 y 100 caracteres
- C2: Contiene patrón de credencial/secreto

**Acciones:**
- A1: Retorna `True`
- A2: Retorna `False`

| Regla | C1 (longitud OK) | C2 (tiene secreto) | A1 (True) | A2 (False) |
|-------|-----------------|-------------------|-----------|-----------|
| R1 | ✅ | ❌ | ✅ | |
| R2 | ✅ | ✅ | | ✅ |
| R3 | ❌ | ❌ | | ✅ |
| R4 | ❌ | ✅ | | ✅ |

---

## 5. Revisión de pruebas generadas por IA

| Test ID | Función | Técnica | Decisión | Justificación |
|---------|---------|---------|----------|---------------|
| `test_pe1_espacios_multiples` | `sanitize_text` | PE | ✅ Conservada | Verifica el caso central de normalización de espacios |
| `test_pe2_saltos_de_linea` | `sanitize_text` | PE | ✅ Conservada | Comportamiento clave del módulo (commits multilínea) |
| `test_pe3_tabulaciones` | `sanitize_text` | PE | ✅ Conservada | Patrón `\t` incluido en el regex del código |
| `test_pe4_texto_ya_limpio` | `sanitize_text` | PE | ✅ Conservada | Idempotencia: texto limpio no debe degradarse |
| `test_pe5_tipo_entero_lanza_type_error` | `sanitize_text` | PE | ✅ Conservada | Verifica el guard de tipo explícito del código |
| `test_pe6_tipo_none_lanza_type_error` | `sanitize_text` | PE | ✅ Conservada | None es el caso inválido más común en Python |
| `test_pe7_tipo_lista_lanza_type_error` | `sanitize_text` | PE | ✅ Conservada | Clase de equivalencia separada (tipo iterable) |
| `test_vl1_cadena_vacia` | `sanitize_text` | VL | ✅ Conservada | Límite inferior del dominio, resultado determinista |
| `test_vl2_un_solo_caracter` | `sanitize_text` | VL | ✅ Conservada | Mínimo no-vacío |
| `test_vl3_solo_espacios` | `sanitize_text` | VL | ✅ Conservada | El strip() debe devolver "" — fácil de olvidar |
| `test_vl4_cadena_muy_larga` | `sanitize_text` | VL | ✅ Conservada | Verifica que no hay límite de tamaño artificial |
| `test_vl_longitud_minima_valida` | `validate_commit_message` | VL | ✅ Conservada | Frontera exacta del rango permitido |
| `test_vl_longitud_bajo_minimo` | `validate_commit_message` | VL | ✅ Conservada | 4 chars = justo fuera del límite inferior |
| `test_vl_longitud_maxima_valida` | `validate_commit_message` | VL | ✅ Conservada | Frontera exacta del límite superior |
| `test_vl_longitud_sobre_maximo` | `validate_commit_message` | VL | ✅ Conservada | 101 chars = justo fuera del límite superior |
| `test_pe_mensaje_valido_convencional` | `validate_commit_message` | PE | ✅ Conservada | Caso base del flujo normal |
| `test_pe_mensaje_valido_fix` | `validate_commit_message` | PE | ✅ Conservada | Segundo tipo de commit más común |
| `test_pe_cadena_vacia` | `validate_commit_message` | PE | ✅ Conservada | Guard al inicio de la función |
| `test_pe_none` | `validate_commit_message` | PE | ✅ Conservada | Guard al inicio, retorna False (no excepción) |
| `test_pe_entero` | `validate_commit_message` | PE | ✅ Conservada | Guard al inicio con isinstance |
| `test_pe_un_caracter` | `validate_commit_message` | PE | ✅ Conservada | Longitud 1 < 5 → False |
| `test_td_r1_valido_sin_secreto` | `validate_commit_message` | TD | ✅ Conservada | Regla 1: camino feliz completo |
| `test_td_r2_valido_con_api_key` | `validate_commit_message` | TD | ✅ Conservada | Regla 2: dato sensible bloquea mensaje válido |
| `test_td_r2b_valido_con_password` | `validate_commit_message` | TD | ✅ Conservada | Regla 2 con segundo patrón (password) |
| `test_td_r2c_valido_con_github_token` | `validate_commit_message` | TD | ✅ Conservada | Regla 2 con tercer patrón (ghp_) |
| `test_td_r3_corto_sin_secreto` | `validate_commit_message` | TD | ✅ Conservada | Regla 3: longitud inválida sola |
| `test_td_r4_corto_con_secreto` | `validate_commit_message` | TD | ✅ Conservada | Regla 4: ambas condiciones negativas |
| `test_pe_sin_datos_sensibles` | `mask_sensitive_data` | PE | ✅ Conservada | El texto limpio no debe modificarse |
| `test_pe_con_api_key` | `mask_sensitive_data` | PE | ✅ Conservada | Patrón 1 de los 3 patterns del módulo |
| `test_pe_con_secret_key` | `mask_sensitive_data` | PE | ✅ Conservada | Mismo regex, clave `secret_key` |
| `test_pe_con_password` | `mask_sensitive_data` | PE | ✅ Conservada | Clave `password` en el mismo patrón |
| `test_pe_con_github_pat` | `mask_sensitive_data` | PE | ✅ Conservada | Patrón 2: `ghp_` + 36 chars |
| `test_pe_none_lanza_type_error` | `mask_sensitive_data` | PE | ✅ Conservada | Guard de tipo presente en el código |
| `test_pe_entero_lanza_type_error` | `mask_sensitive_data` | PE | ✅ Conservada | Clase de equivalencia de tipo inválido |
| `test_vl_cadena_vacia` | `mask_sensitive_data` | VL | ✅ Conservada | Límite inferior del dominio |
| `test_vl_multiples_secretos` | `mask_sensitive_data` | VL | ✅ Conservada | Verifica el loop sobre todos los patrones |
| `test_vl_secreto_longitud_minima` | `mask_sensitive_data` | VL | ✅ Conservada | Límite inferior del patrón regex ({8,}) |

---

## 6. Verificación: las pruebas fallan ante código defectuoso

Se introdujo un error intencional en `sanitizer.py` comentando el `strip()` para verificar que las pruebas detectan la regresión.

**Resultado:** Las pruebas `test_vl3_solo_espacios` y `test_pe4_texto_ya_limpio` **fallaron** correctamente, confirmando que las pruebas detectan cambios en el comportamiento esperado.

---

## 7. Resumen de cobertura

| Función | Tests PE | Tests VL | Tests TD | Total |
|---------|---------|---------|---------|-------|
| `sanitize_text` | 7 | 4 | — | 11 |
| `validate_commit_message` | 7 | 4 | 7 | 18 |
| `mask_sensitive_data` | 7 | 3 | — | 10 |
| **Total** | **21** | **11** | **7** | **39** |
