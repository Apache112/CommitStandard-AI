"""
Módulo Sanitizer - CommitStandard-AI
Proporciona utilidades para limpiar textos, validar mensajes de commit y 
enmascarar información sensible por razones de seguridad.
"""

import re
from typing import List


class Sanitizer:
    """Clase principal para la sanitización y validación de texto y commits."""

    # Patrones comunes para detección de secretos o datos sensibles
    SENSITIVE_PATTERNS: List[re.Pattern] = [
        re.compile(
            r"(?i)(api[_-]?key|secret[_-]?key|password|token)\s*[:=]\s*"
            r"['\"]?[a-zA-Z0-9_\-\.]{8,}['\"]?"
        ),
        re.compile(r"ghp_[a-zA-Z0-9]{36}"),  # GitHub Personal Access Token
        re.compile(r"sk-[a-zA-Z0-9]{48}"),  # OpenAI API Key format
    ]

    @staticmethod
    def sanitize_text(text: str) -> str:
        """
        Limpia espacios en blanco redundantes y caracteres de control.

        Args:
            text (str): Texto de entrada a sanitizar.

        Returns:
            str: Texto limpio y normalizado.
        
        Raises:
            TypeError: Si el input no es una cadena de texto.
        """
        if not isinstance(text, str):
            raise TypeError(
                "El argumento de entrada debe ser una cadena de texto (str)."
            )
        
        # Eliminar caracteres de control y normalizar espacios múltiples
        clean_text = re.sub(r'[\r\n\t]+', ' ', text)
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()
        return clean_text

    @classmethod
    def mask_sensitive_data(cls, text: str) -> str:
        """
        Detecta y enmascara posibles credenciales o claves API en el texto.

        Args:
            text (str): Texto a revisar.

        Returns:
            str: Texto con datos sensibles enmascarados con '[REDACTED]'.
        """
        if not isinstance(text, str):
            raise TypeError(
                "El argumento de entrada debe ser una cadena de texto (str)."
            )

        masked_text = text
        for pattern in cls.SENSITIVE_PATTERNS:
            masked_text = pattern.sub("[REDACTED]", masked_text)
            
        return masked_text

    @classmethod
    def validate_commit_message(cls, message: str) -> bool:
        """
        Valida que un mensaje de commit cumpla con estándares 
        de calidad y seguridad.

        Args:
            message (str): Mensaje de commit.

        Returns:
            bool: True si el mensaje es válido y seguro, False en caso contrario.
        """
        if not message or not isinstance(message, str):
            return False
        
        sanitized = cls.sanitize_text(message)
        
        # Validar longitud mínima y máxima razonable (ej. entre 5 y 100)
        if not (5 <= len(sanitized) <= 100):
            return False
            
        # Comprobar que no contenga credenciales expuestas
        for pattern in cls.SENSITIVE_PATTERNS:
            if pattern.search(message):
                return False
                
        return True