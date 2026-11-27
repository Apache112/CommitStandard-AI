# Guía de operación

## Alcance

La versión actual es una herramienta local. No hay servicio remoto, despliegue
de backend, almacenamiento de métricas ni conexión automática a un proveedor de
IA. La persona revisa el resultado antes de copiarlo a otra herramienta.

## Preparación

1. Instalar Python 3.10 o superior y Git.
2. Crear y activar un entorno virtual:

   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   python -m pip install pytest ruff
   ```

3. Ejecutar las verificaciones:

   ```powershell
   python -m pytest -q
   ruff check sanitizer.py test_sanitizer.py tests FUNCIONANDO
   ```

## Uso de la CLI

Desde la raíz de un repositorio Git:

```powershell
git add <archivos-a-revisar>
python FUNCIONANDO\main.py
```

Si no hay cambios staged, la CLI termina sin procesar un diff y solicita usar
`git add`. Ese mensaje es el comportamiento esperado. La salida limpia es una
reducción heurística, no una garantía de que se eliminaron todos los secretos;
debe revisarse manualmente y no enviarse automáticamente a un servicio externo.

## Integración continua

El workflow [tests.yml](../.github/workflows/tests.yml) corre pytest y Ruff en
Python 3.10 y 3.14 al publicar cambios o abrir un pull request. Consulta la
[página de ejecuciones](https://github.com/Apache112/CommitStandard-AI/actions)
y confirma que la ejecución más reciente corresponde al commit entregado y
terminó exitosamente.

## Incidentes y recuperación

- Ante un fallo de pruebas o lint, no considerar válida la publicación; revisar
  el log del job y corregir el cambio.
- Si una versión nueva causa regresiones, volver a una versión conocida del
  código mediante un commit de reversión revisado por el mantenedor.
- Si se sospecha que un secreto real fue compartido, revocarlo en el proveedor
  correspondiente. La redacción por patrones no sustituye la revocación.

No existe procedimiento de despliegue productivo porque no hay servicio
productivo implementado.
