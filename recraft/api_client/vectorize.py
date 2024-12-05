from typing import Any, Dict, Optional, Union

from .base import process_image


def vectorize_image(
    file_path: str, response_format: Optional[str] = None, timeout: int = 30
) -> Optional[Union[str, Dict[str, Any]]]:
    """
    Converts a given raster image to SVG format.

    Args:
        file_path (str): Path to the PNG image to vectorize
        response_format (str, optional): Format of the response. Defaults to None (url).
        timeout (int, optional): Timeout for the API request. Defaults to 30 seconds.

    Returns:
        Optional[Union[str, Dict[str, Any]]]: Vectorized image URL or base64 JSON, or None if vectorization fails
    """
    return process_image(
        file_path=file_path,
        endpoint="https://external.api.recraft.ai/v1/images/vectorize",
        operation_name="Vectorizing Image",
        response_format=response_format,
        timeout=timeout,
    )
