"""Utility functions for roadmapper."""

import sys
from pathlib import Path
from typing import Optional


def ensure_utf8_console():
    """
    Ensure UTF-8 encoding for console output, especially on Windows.
    
    This prevents encoding errors when displaying emojis and special characters
    in Windows PowerShell/CMD terminals.
    """
    if sys.platform == "win32":
        try:
            # Python 3.7+
            sys.stdout.reconfigure(encoding='utf-8')
            sys.stderr.reconfigure(encoding='utf-8')
        except (AttributeError, ValueError):
            # Python < 3.7 or if already reconfigured
            # Try setting environment variable as fallback
            import os
            os.environ['PYTHONIOENCODING'] = 'utf-8'


def read_text_file(file_path: Path, encoding: str = 'utf-8') -> str:
    """
    Read a text file with explicit UTF-8 encoding.
    
    Args:
        file_path: Path to the file to read
        encoding: Encoding to use (default: 'utf-8')
    
    Returns:
        File contents as string
    
    Raises:
        FileNotFoundError: If file doesn't exist
        UnicodeDecodeError: If file can't be decoded with specified encoding
    """
    return file_path.read_text(encoding=encoding)


def write_text_file(file_path: Path, content: str, encoding: str = 'utf-8') -> None:
    """
    Write text to a file with explicit UTF-8 encoding.
    
    Args:
        file_path: Path to the file to write
        content: Content to write
        encoding: Encoding to use (default: 'utf-8')
    """
    file_path.write_text(content, encoding=encoding)

