import click

from .commands.generate import generate
from .commands.remove_bg import remove_bg
from .commands.token import token
from .commands.upscale import upscale


@click.group()
def main():
    """Recraft CLI for image generation and processing."""
    pass


main.add_command(token)
main.add_command(generate)
main.add_command(upscale)
main.add_command(remove_bg)

if __name__ == "__main__":
    main()
