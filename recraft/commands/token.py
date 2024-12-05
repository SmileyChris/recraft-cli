import click
import keyring


@click.command()
@click.argument("token", required=False)
def token(token):
    """Set the Recraft API token in the system keychain."""
    if not token:
        token = click.prompt("Enter your Recraft API token", hide_input=True)

    keyring.set_password("recraft-cli", "api_token", token)
    click.echo("API token has been securely stored in the system keychain.")


def ensure_token():
    """
    Check if token exists, and if not, prompt user to set it.

    Returns the API token.
    """
    token = keyring.get_password("recraft-cli", "api_token")
    if not token:
        click.echo("No API token found. Please set your Recraft API token.")
        token = click.prompt("Enter your Recraft API token", hide_input=True)
        keyring.set_password("recraft-cli", "api_token", token)
        click.echo("Token has been securely stored in the system keychain.")
    return token
