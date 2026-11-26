"""
CommitStandard-AI — Interfaz de línea de comandos (CLI)
Uso: python main.py

Obtiene el git diff de staging, lo sanitiza y muestra el diff limpio
listo para enviar a un LLM generador de commits convencionales.
"""

import sys
from commit_guard import obtener_diff_staging, preparar_diff_para_llm


BANNER = """
╔══════════════════════════════════════════════════╗
║        CommitStandard-AI  🤖  v1.0               ║
║   Asistente de Commits Convencionales para IDE   ║
╚══════════════════════════════════════════════════╝
"""


def main():
    print(BANNER)

    # 1. Obtener diff de staging
    print("📂 Obteniendo git diff --cached del repositorio actual...\n")
    try:
        diff_bruto = obtener_diff_staging()
    except RuntimeError as e:
        print(f"❌ Error al obtener el diff: {e}")
        sys.exit(1)

    if not diff_bruto.strip():
        print("⚠️  No hay archivos en staging.")
        print("    Usa 'git add <archivo>' antes de correr este comando.")
        sys.exit(0)

    print(f"📋 Diff obtenido ({len(diff_bruto.encode())} bytes). Sanitizando...\n")

    # 2. Sanitizar diff
    resultado = preparar_diff_para_llm(diff_bruto)

    if resultado["status"] == "error":
        print(f"❌ No se pudo preparar el diff:\n   {resultado['message']}")
        sys.exit(1)

    # 3. Mostrar resultado
    print("✅ Diff sanitizado exitosamente.\n")
    print("─" * 52)
    print("DIFF LIMPIO (listo para LLM):")
    print("─" * 52)
    print(resultado["clean_diff"])
    print("─" * 52)
    print("\n💡 Sugerencia de commit convencional:")
    print("   Envía este diff a tu LLM favorito con el prompt:")
    print('   "Genera un mensaje de commit convencional para este diff."')


if __name__ == "__main__":
    main()
