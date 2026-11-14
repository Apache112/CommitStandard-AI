# CommitStandard AI 🤖

**Asistente de Commits Convencionales para IDE**

**Estudiante:** Jorge Alberto Apache Cardozo  

**Institución:** Fundación Escuela Tecnológica Jesús Oviedo Pérez (FET)  

**Docente:** Jorge Luis Trujillo Artunduaga  



---



## Funcionalidad de la semana 5: Sanitizador y Preparador de Diff para IA



### Historia de Usuario

**ID:** HU-01
**Título:** Generación de propuesta de commit basada en cambios staged.
**Criterio de Aceptación:** El sistema debe tomar el git diff de los archivos en staging, eliminar cualquier información sensible (como variables de entorno o credenciales) y validar que el contenido no exceda el límite máximo permitido para optimizar el contexto enviado al LLM. Si el diff está vacío o supera los límites críticos tras la limpieza, debe arrojar un error controlado.


### Contrato de la Función



La función principal encargada de esta lógica en el backend proxy (`CommitGuard API Service`) es `preparar_diff_para_llm`.



#### Firma de la función:

```python

def preparar_diff_para_llm(diff_text: str, max_bytes: int = 51200) -> dict:

    """

    Recibe el diff bruto de Git, lo sanitiza eliminando líneas con secretos/claves,

    ignora archivos prohibidos (.env) y valida que cumpla con los límites de tamaño.

    """

```









**Entradas:**
  - `diff_text` (`str`): El volcado crudo del comando de git diff.

  - `max_bytes` (`int`): Límite de tamaño máximo del payload (por defecto 50 KB / 51,200 bytes).

**Salidas:** Un diccionario (`dict`) con la estructura:
  - `{ "status": "success", "clean_diff": "...", "message": "Diff preparado con éxito." }`

  - `{ "status": "error", "clean_diff": "", "message": "Motivo del fallo" }`



### Ejemplos de Entrada y Salida



#### Ejemplo 1: Caso Normal

**Entrada (`diff_text`):**
  ```diff

  diff --git a/src/auth.js b/src/auth.js

  +function login(user, provider) {

  ```

**Salida:**
  ```json

  {

    "status": "success",

    "clean_diff": "diff --git a/src/auth.js b/src/auth.js\n+function login(user, provider) {",

    "message": "Diff preparado con éxito."

  }

  ```



#### Ejemplo 2: Caso Límite (Censura de Secretos)

**Entrada (`diff_text`):**
  ```diff

  +db_password = "super_secret_password_123"

  ```

**Salida:**
  ```json

  {

    "status": "success",

    "clean_diff": "+db_password = \"[REDACTED_SECRET]\"",

    "message": "Diff preparado con éxito."

  }

  ```



#### Ejemplo 3: Caso de Error (Payload Excedido)

**Entrada:** Un `diff_text` que supera los `51,200` bytes.
**Salida:**
  ```json

  {

    "status": "error",

    "clean_diff": "",

    "message": "Payload demasiado grande. El diff supera el límite permitido."

  }

  ```



### Cómo ejecutar las pruebas

Para ejecutar la suite de pruebas automatizadas del proyecto, asegúrate de tener instalado `pytest` y ejecuta:

```bash

pytest

```
---
## 1. Qué es el proyecto
CommitStandard AI es una herramienta diseñada para asistir a los desarrolladores en la generación automatizada de mensajes de commits bajo el estandar convencional, sanitizando de forma segura los cambios en staging (`git diff`) antes de enviarlos a modelos de lenguaje (LLM), evitando filtraciones de secretos o credenciales.

## 2. Requisitos
- Python 3.10 o superior.
- Git instalado en el sistema operativo.
- Gestor de paquetes `pip`.

## 3. Instalación
Clona el repositorio y configura un entorno limpio ejecutando:
```bash
git clone <url-del-repositorio>
cd CommitStandard-AI
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate
pip install -r requirements.txt
pip install ruff pytest