import asyncio
import math
import time
from typing import Any, Dict, Optional, Union

import click
import httpx
from tqdm import tqdm


async def async_api_call(
    file_path: str,
    endpoint: str,
    api_token: str,
    response_format: Optional[str] = None,
    timeout: int = 30,
) -> Union[str, Dict[str, Any]]:
    """
    Async API call for image processing with progress tracking.

    Args:
        file_path (str): Path to the image file
        endpoint (str): API endpoint URL
        api_token (str): Authentication token
        response_format (str, optional): Format of the response. Defaults to None (url).
        timeout (int, optional): Timeout for the API request. Defaults to 30 seconds.

    Returns:
        Union[str, Dict[str, Any]]: Processed image URL or base64 JSON
    """
    async with httpx.AsyncClient() as client:
        # Prepare the request
        with open(file_path, "rb") as file:
            files = {"file": file}
            headers = {
                "Authorization": f"Bearer {api_token}",
            }
            params = {}
            if response_format:
                params["response_format"] = response_format

            # Create a progress bar for image processing with continuous updates
            with tqdm(
                total=100, desc="Processing Image", bar_format="{l_bar}{bar}"
            ) as pbar:
                start_time = time.time()

                # Simulate continuous progress while waiting for the API
                def update_progress():
                    elapsed = time.time() - start_time
                    # Asymptotic progress that approaches 90% but never quite reaches it
                    progress = min(90, 50 * (1 - math.exp(-0.2 * elapsed)))
                    pbar.n = progress
                    pbar.refresh()

                # Start a background task for progress updates
                async def progress_task():
                    while pbar.n < 90:
                        update_progress()
                        await asyncio.sleep(0.5)

                # Make the actual API request
                try:
                    # Start progress tracking
                    progress_coro = asyncio.create_task(progress_task())

                    # Send the request
                    response = await client.post(
                        endpoint,
                        headers=headers,
                        files=files,
                        params=params,
                        timeout=timeout,
                    )
                    response.raise_for_status()

                    # Cancel progress task
                    progress_coro.cancel()

                    # Ensure progress bar reaches 100%
                    pbar.n = 100
                    pbar.refresh()

                    # Return the image URL or base64 JSON based on response format
                    response_data = response.json()
                    return (
                        response_data["image"]["url"]
                        if "url" in response_data["image"]
                        else response_data
                    )

                except Exception:
                    # Cancel progress task in case of any exception
                    progress_coro.cancel()
                    raise


def process_image(
    file_path: str,
    endpoint: str,
    operation_name: str,
    response_format: Optional[str] = None,
    timeout: int = 30,
) -> Optional[Union[str, Dict[str, Any]]]:
    """
    Synchronous wrapper for async API call.

    Args:
        file_path (str): Path to the image file
        endpoint (str): API endpoint URL
        operation_name (str): Name of the operation for progress description
        response_format (str, optional): Format of the response. Defaults to None (url).
        timeout (int, optional): Timeout for the API request. Defaults to 30 seconds.

    Returns:
        Optional[Union[str, Dict[str, Any]]]: Processed image URL or base64 JSON, or None if processing fails
    """
    from ..commands.token import ensure_token

    try:
        api_token = ensure_token()
        return asyncio.run(
            async_api_call(file_path, endpoint, api_token, response_format, timeout)
        )
    except httpx.HTTPStatusError as exc:
        click.echo(
            f"\nHTTP error occurred: {exc.response.status_code} - {exc.response.text}"
        )
        return None
    except httpx.RequestError as exc:
        click.echo(f"\nRequest error occurred: {exc}")
        return None
    except Exception as exc:
        click.echo(f"\nUnexpected error occurred: {exc}")
        return None
