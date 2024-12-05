import os
from typing import Optional

import click

from ..api_client import download_image, remove_background


@click.command()
@click.argument(
    "file_path",
    type=click.Path(
        exists=True, dir_okay=False, file_okay=True, readable=True, resolve_path=True
    ),
)
@click.option(
    "--response-format",
    type=click.Choice(["url", "base64"]),
    help="Format of the response (default: url)",
)
@click.option("--timeout", default=60, help="Timeout for the API request in seconds")
@click.option("--no-download", is_flag=True, help="Skip automatic image download")
@click.option(
    "--output-dir",
    type=click.Path(file_okay=False, dir_okay=True, writable=True, resolve_path=True),
    default=None,
    help="Directory to save downloaded image",
)
def remove_bg(
    file_path: str,
    response_format: Optional[str],
    timeout: int,
    no_download: bool,
    output_dir: Optional[str],
):
    """Remove background from an image."""
    click.echo(click.style("\n🖼️  Background Removal 🖼️", fg="bright_cyan", bold=True))

    # If no response format provided, default to URL
    if response_format is None:
        response_format = "url"

    try:
        result = remove_background(
            file_path, response_format=response_format, timeout=timeout
        )

        if result:
            # If result is a URL and download is not skipped, download the image
            if response_format == "url":
                success_msg = click.style(
                    f"\n✅ Background removed successfully: {result}", fg="bright_green"
                )
                click.echo(success_msg)

                if not no_download:
                    # Generate custom filename with "-removed-bg" suffix
                    original_filename = os.path.basename(file_path)
                    filename_base, ext = os.path.splitext(original_filename)
                    custom_filename = f"{filename_base}-removed-bg{ext}"

                    # Download with custom filename
                    download_image(result, output_dir, custom_filename)
            else:
                # If base64, just show the result
                click.echo(
                    click.style(
                        "\n✅ Background removed successfully!", fg="bright_green"
                    )
                )
                click.echo(click.style(f"Result: {result}", fg="bright_blue"))
    except Exception as e:
        click.echo(click.style(f"\n❌ Background removal failed: {e}", fg="bright_red"))
