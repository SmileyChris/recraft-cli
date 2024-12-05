from typing import Any, Dict, Literal, Optional, Union

from .base import process_image


def upscale_image(
    file_path: str,
    mode: Literal["clarity", "generative"] = "clarity",
    response_format: Optional[str] = None,
    timeout: int = 30,
) -> Optional[Union[str, Dict[str, Any]]]:
    """
    Enhances a given raster image using upscaling techniques.

    Args:
        file_path (str): Path to the PNG image to upscale
        mode (str, optional): Upscaling mode. Defaults to 'clarity'.
            - 'clarity': Enhances resolution with clarity
            - 'generative': Enhances resolution with generative details, focusing on small details and faces
        response_format (str, optional): Format of the response. Defaults to None (url).
        timeout (int, optional): Timeout for the API request. Defaults to 30 seconds.

    Returns:
        Optional[Union[str, Dict[str, Any]]]: Upscaled image URL or base64 JSON, or None if upscaling fails

    Raises:
        ValueError: If an invalid mode is provided
    """
    # Validate mode
    if mode not in ["clarity", "generative"]:
        raise ValueError("Mode must be either 'clarity' or 'generative'")

    # Select appropriate endpoint based on mode
    endpoints = {
        "clarity": "https://external.api.recraft.ai/v1/images/clarityUpscale",
        "generative": "https://external.api.recraft.ai/v1/images/generativeUpscale",
    }

    # Select operation name based on mode
    operation_names = {
        "clarity": "Clarity Upscaling",
        "generative": "Generative Upscaling",
    }

    return process_image(
        file_path=file_path,
        endpoint=endpoints[mode],
        operation_name=operation_names[mode],
        response_format=response_format,
        timeout=timeout,
    )


def clarity_upscale(
    file_path: str, response_format: Optional[str] = None, timeout: int = 30
) -> Optional[Union[str, Dict[str, Any]]]:
    """
    Shorthand for upscale_image with clarity mode.

    Args:
        file_path (str): Path to the PNG image to upscale
        response_format (str, optional): Format of the response. Defaults to None (url).
        timeout (int, optional): Timeout for the API request. Defaults to 30 seconds.

    Returns:
        Optional[Union[str, Dict[str, Any]]]: Upscaled image URL or base64 JSON, or None if upscaling fails
    """
    return upscale_image(
        file_path=file_path,
        mode="clarity",
        response_format=response_format,
        timeout=timeout,
    )


def generative_upscale(
    file_path: str, response_format: Optional[str] = None, timeout: int = 30
) -> Optional[Union[str, Dict[str, Any]]]:
    """
    Shorthand for upscale_image with generative mode.

    Args:
        file_path (str): Path to the PNG image to upscale
        response_format (str, optional): Format of the response. Defaults to None (url).
        timeout (int, optional): Timeout for the API request. Defaults to 30 seconds.

    Returns:
        Optional[Union[str, Dict[str, Any]]]: Upscaled image URL or base64 JSON, or None if upscaling fails
    """
    return upscale_image(
        file_path=file_path,
        mode="generative",
        response_format=response_format,
        timeout=timeout,
    )
