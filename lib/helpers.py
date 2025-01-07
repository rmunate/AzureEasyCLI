import datetime
import re

def strftime(format: str = '%Y-%m-%d %H:%M:%S') -> str:
    """
    Returns the current date and time as a formatted string.

    Args:
        format (str): The format in which to return the date and time.
                      Default is '%Y-%m-%d %H:%M:%S'. The format follows
                      Python's datetime formatting conventions.

    Returns:
        str: The current date and time formatted as specified.

    Example:
        >>> strftime('%Y-%m-%d')
        '2025-01-07'
    """

    # Get the current date and time using the current system time
    current_datetime = datetime.datetime.now()

    # Format the current date and time according to the specified format string
    return current_datetime.strftime(format)

def sanitize_folder_name(name: str) -> str:
    """
    Sanitizes a string to ensure it is a valid folder name in Windows.

    Args:
        name (str): The name to sanitize, potentially containing invalid characters.

    Returns:
        str: A valid folder name. If the input name is empty or contains reserved
             Windows names, a default folder name is returned.

    Example:
        >>> sanitize_folder_name("My:Folder|Name?")
        'MyFolderName'
    """
    # Remove characters that are not allowed in Windows folder names
    sanitized_name = re.sub(r'[\\/:*?"<>|]', '', name)

    # Remove trailing spaces or periods
    sanitized_name = sanitized_name.rstrip(' .')

    # Define reserved names in Windows that cannot be used for folder names
    reserved_names = {"CON", "PRN", "AUX", "NUL", "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9", "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"}

    # Check if the sanitized name is one of the reserved names
    if sanitized_name.upper() in reserved_names:
        # Append '_sanitized' to make it unique
        sanitized_name = f"{sanitized_name}_sanitized"

    # If the sanitized name is empty, return a default folder name
    return sanitized_name or "default_folder"