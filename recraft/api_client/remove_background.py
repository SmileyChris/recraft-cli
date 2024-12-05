from typing import Any, Dict, Optional, Union

from .base import process_image


def remove_background(
    file_path: str, response_format: Optional[str] = None, timeout: int = 30
) -> Optional[Union[str, Dict[str, Any]]]:
    """
    Removes background of a given raster image.

    Args:
        file_path (str): Path to the PNG image to remove background from
        response_format (str, optional): Format of the response. Defaults to None (url).
        timeout (int, optional): Timeout for the API request. Defaults to 30 seconds.

    Returns:
        Optional[Union[str, Dict[str, Any]]]: Background-removed image URL or base64 JSON, or None if removal fails
    """
    return process_image(
        file_path=file_path,
        endpoint="https://external.api.recraft.ai/v1/images/removeBackground",
        operation_name="Removing Background",
        response_format=response_format,
        timeout=timeout,
    )
