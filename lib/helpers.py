import datetime
import os
import re
import shutil

def strftime(format: str = '%Y-%m-%d %H:%M:%S') -> str:
    """
    Returns the current date and time as a formatted string.

    Args:
        format (str): The format in which to return the date and time.
                      Default is '%Y-%m-%d %H:%M:%S'.

    Returns:
        str: The current date and time formatted as specified.
    """
    # Get the current date and time
    current_datetime = datetime.datetime.now()

    # Format the current date and time based on the specified format
    return current_datetime.strftime(format)

def sanitize_folder_name(name):

    """
    Sanear un string para que sea un nombre válido para un folder en Windows.
    """
    # Remover caracteres no permitidos
    sanitized_name = re.sub(r'[\\/:*?"<>|]', '', name)

    # Eliminar espacios o puntos al final
    sanitized_name = sanitized_name.rstrip(' .')

    # Manejar palabras reservadas (opcional)
    reserved_names = {"CON", "PRN", "AUX", "NUL", "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9", "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"}
    if sanitized_name.upper() in reserved_names:
        sanitized_name = f"{sanitized_name}_sanitized"

    # Si el nombre queda vacío, usar un nombre por defecto
    return sanitized_name or "default_folder"

def clear_folder(folder_path: str):
    """
    Elimina todo el contenido de una carpeta de manera recursiva,
    pero mantiene la carpeta principal intacta.
    """
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isdir(item_path):
            shutil.rmtree(item_path)
        else:
            os.remove(item_path)