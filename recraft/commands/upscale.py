import os
from typing import Optional

import click

from ..api_client import download_image, upscale_image


@click.command()
@click.argument(
    "file_path",
    type=click.Path(
        exists=True, dir_okay=False, file_okay=True, readable=True, resolve_path=True
    ),
)
@click.option(
    "--mode", type=click.Choice(["clarity", "generative"]), help="Upscaling mode"
)
@click.option("--timeout", default=60, help="Timeout for the API request in seconds")
@click.option("--no-download", is_flag=True, help="Skip automatic image download")
@click.option(
    "--output-dir",
    type=click.Path(file_okay=False, dir_okay=True, writable=True, resolve_path=True),
    default=None,
    help="Directory to save downloaded image",
)
def upscale(
    file_path: str,
    mode: Optional[str],
    timeout: int,
    no_download: bool,
    output_dir: Optional[str],
):
    """Upscale an image with optional mode selection."""
    click.echo(click.style("\n🖼️  Image Upscaling 🖼️", fg="bright_cyan", bold=True))

    if mode is None:
        click.echo("\nChoose an upscaling method:")
        click.echo(
            click.style("1. Clarity Upscale ", fg="green") + "(Recommended, lower cost)"
        )
        click.echo(
            click.style("2. Generative Upscale ", fg="yellow")
            + "(Detailed, but ~20x more expensive)"
        )

        choice = click.prompt(
            click.style("Enter your choice", fg="bright_blue"),
            type=click.Choice(["1", "2"]),
        )

        if choice == "1":
            mode = "clarity"
        elif choice == "2":
            confirm_msg = click.style(
                "\n💸 Generative Upscale costs ~20x more. Are you sure you want to proceed?",
                fg="bright_red",
            )
            click.confirm(confirm_msg, abort=True)
            mode = "generative"

    try:
        result = upscale_image(file_path, mode=mode, timeout=timeout)
        if result:
            success_msg = click.style(
                f"\n✅ Image {mode} upscaled successfully: {result}", fg="bright_green"
            )
            click.echo(success_msg)

            if not no_download:
                # Generate custom filename with upscale mode suffix
                original_filename = os.path.basename(file_path)
                filename_base, ext = os.path.splitext(original_filename)

                if mode == "generative":
                    custom_filename = f"{filename_base}-upscaled-generative{ext}"
                else:
                    custom_filename = f"{filename_base}-upscaled{ext}"

                download_image(result, output_dir, custom_filename)

    except Exception as e:
        error_msg = click.style(f"\n❌ Upscaling failed: {e}", fg="bright_red")
        click.echo(error_msg)
