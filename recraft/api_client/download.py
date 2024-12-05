import mimetypes
import os
from typing import Optional
from urllib.parse import urlparse

import click
import httpx
from tqdm import tqdm


def download_image(
    image_url: str,
    output_dir: Optional[str] = None,
    custom_filename: Optional[str] = None,
) -> Optional[str]:
    """
    Download an image from a given URL with a progress bar.

    Args:
        image_url (str): URL of the image to download
        output_dir (str, optional): Directory to save the image. Defaults to current directory.
        custom_filename (str, optional): Custom filename for the downloaded image.

    Returns:
        Optional[str]: Path to the downloaded image file, or None if download fails
    """
    if not output_dir:
        output_dir = os.getcwd()

    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Determine filename
        if custom_filename:
            filename = custom_filename
        else:
            # Extract filename from URL or generate a unique name
            parsed_url = urlparse(image_url)
            filename = os.path.basename(parsed_url.path)

            # If no filename or no extension, use a default
            if not filename or not os.path.splitext(filename)[1]:
                # Try to guess mime type from URL
                mime_type, _ = mimetypes.guess_type(image_url)

                # Default to .png if no mime type or not an image
                if not mime_type or not mime_type.startswith("image/"):
                    filename = f"recraft_image_{hash(image_url)}.png"
                else:
                    # Use mime type extension if available
                    ext = mimetypes.guess_extension(mime_type) or ".png"
                    filename = f"recraft_image_{hash(image_url)}{ext}"

        output_path = os.path.join(output_dir, filename)

        # Notify about the image URL before downloading
        click.echo(
            click.style(f"📥 Downloading image from: {image_url}", fg="bright_blue")
        )

        # Download the image with progress bar
        with httpx.stream("GET", image_url) as response:
            total = int(response.headers.get("Content-Length", 0))

            with tqdm(
                total=total,
                unit_scale=True,
                unit_divisor=1024,
                unit="B",
                desc=click.style("Downloading", fg="bright_cyan"),
                bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]",
            ) as progress:
                with open(output_path, "wb") as download_file:
                    num_bytes_downloaded = 0
                    for chunk in response.iter_bytes():
                        download_file.write(chunk)
                        progress.update(len(chunk))
                        num_bytes_downloaded += len(chunk)

        click.echo(
            click.style(
                f"✅ Image downloaded successfully: {output_path}", fg="bright_green"
            )
        )
        return output_path

    except httpx.RequestError as exc:
        click.echo(click.style(f"\n❌ Error downloading image: {exc}", fg="bright_red"))
        return None
    except Exception as exc:
        click.echo(
            click.style(
                f"\n❌ Unexpected error downloading image: {exc}", fg="bright_red"
            )
        )
        return None
