import click
import requests
import os
import configparser

CONFIG_PATH = os.path.join(os.path.expanduser("~"), ".cronhub")
BASE_URL = "http://cronhub.local"

@click.group()
@click.version_option()
def cli():
    """
    A CLI interface that works with Cronhub.
    """

@cli.command("config")
@click.option("--api-key", required=True, help="Your Cronhub API Key")
def config(api_key):
    """Save your Cronhub API key in $HOME/.cronhub."""
    config = configparser.ConfigParser()
    config['crhb'] = {'api_key': api_key}
    with open(CONFIG_PATH, 'w') as f:
        config.write(f)
    click.echo("We have successfully stored your key in $HOME/.cronhub file")


@cli.command("monitors")
@click.option("--api-key", help="Your Cronhub API key")
def monitors(api_key):
    """List all your existing monitors."""
    if not api_key:
        api_key = get_key()
    headers = {"X-Api-Key": api_key}
    r = requests.get("%s/api/v1/monitors" % BASE_URL, headers=headers)
    click.echo(r.json())

@cli.command("monitor")
@click.argument("uuid", type=click.UUID)
@click.option("--api-key", help="Your Cronhub API key")
def monitor(uuid, api_key):
    """Get the monitor by its UUID."""
    if not api_key:
        api_key = get_key()
    headers = {"X-Api-Key": api_key}
    r = requests.get("%s/api/v1/monitors/%s" % (BASE_URL, uuid), headers=headers)
    click.echo(r.json())

@cli.command("ping")
@click.argument("uuid", type=click.UUID)
@click.option("-s", "--start", is_flag=True, help="Make a /start ping")
@click.option("-f", "--finish", is_flag=True, help="Make a /finish ping")
def ping(uuid, start, finish):
    """Ping the monitor using its UUID."""
    if start:
        url = "%s/start/%s" % (BASE_URL, uuid)
    elif finish:
        url = "%s/finish/%s" % (BASE_URL, uuid)
    else:
        url = "%s/ping/%s" % (BASE_URL, uuid)

    r = requests.get(url)
    click.echo(r.json())

def get_key():
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)
    if not config.has_option('crhb', 'api_key'):
        return None
    return config.get('crhb', 'api_key')

if __name__ == '__main__':
    cli()
