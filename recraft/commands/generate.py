from typing import Optional

import click

from ..api_client import download_image, generate_image
from ..api_client.generate import ALLOWED_STYLES

# Style categories and their corresponding styles
STYLE_CATEGORIES = {
    "1": {"name": "Any Style (Random)", "styles": ["any"]},
    "2": {
        "name": "Realistic Image",
        "styles": [
            style
            for style in ALLOWED_STYLES
            if style.startswith("realistic_image") and style != "any"
        ],
    },
    "3": {
        "name": "Digital Illustration",
        "styles": [
            style
            for style in ALLOWED_STYLES
            if style.startswith("digital_illustration")
        ],
    },
    "4": {
        "name": "Vector Illustration",
        "styles": [
            style for style in ALLOWED_STYLES if style.startswith("vector_illustration")
        ],
    },
}


@click.command()
@click.argument("prompt", required=False)
@click.option("--style", default=None, help="Style of the generated image")
@click.option("--timeout", default=60, help="Timeout for the API request in seconds")
@click.option("--no-download", is_flag=True, help="Skip automatic image download")
@click.option(
    "--output-dir",
    type=click.Path(file_okay=False, dir_okay=True, writable=True, resolve_path=True),
    default=None,
    help="Directory to save downloaded image",
)
def generate(
    prompt: Optional[str],
    style: Optional[str],
    timeout: int,
    no_download: bool,
    output_dir: Optional[str],
):
    """Generate an image using the Recraft API."""
    click.echo(click.style("\n🖌️  Image Generation 🖌️", fg="bright_cyan", bold=True))

    # If no prompt provided, ask the user
    if not prompt:
        prompt = click.prompt(
            click.style(
                "Enter a description for the image you want to generate",
                fg="bright_blue",
            ),
            type=str,
        )

    # If no style provided, guide user through selection
    if not style:
        click.echo("\nChoose a style category:")
        for key, category in STYLE_CATEGORIES.items():
            click.echo(f"{key}. {category['name']}")

        while True:
            category_choice = click.prompt(
                click.style("Enter the number of the style category", fg="bright_blue"),
                type=str,
            )

            if category_choice in STYLE_CATEGORIES:
                selected_category = STYLE_CATEGORIES[category_choice]

                # If "Any" style is selected, use it directly
                if selected_category["styles"] == ["any"]:
                    style = "any"
                    break

                click.echo(
                    click.style(
                        f"\nAvailable {selected_category['name']} Styles:", fg="green"
                    )
                )
                for i, sub_style in enumerate(selected_category["styles"], 1):
                    click.echo(f"{i}. {sub_style}")

                while True:
                    sub_style_choice = click.prompt(
                        click.style(
                            "Enter the number of the specific style", fg="bright_blue"
                        ),
                        type=str,
                    )

                    try:
                        sub_style_index = int(sub_style_choice) - 1
                        if 0 <= sub_style_index < len(selected_category["styles"]):
                            style = selected_category["styles"][sub_style_index]
                            break
                        else:
                            click.echo(
                                click.style(
                                    "Invalid style number. Please try again.", fg="red"
                                )
                            )
                    except ValueError:
                        click.echo(
                            click.style("Please enter a valid number.", fg="red")
                        )

                break
            else:
                click.echo(click.style("Invalid category. Please try again.", fg="red"))

    image_url = generate_image(prompt, style, timeout)
    if image_url:
        click.echo(
            click.style(f"Image generated successfully: {image_url}", fg="bright_green")
        )

        if not no_download:
            download_image(image_url, output_dir)
