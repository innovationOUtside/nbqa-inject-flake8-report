import click
from .flake8_report_injecter import flake8_report_insertion

@click.group()
def cli():
	pass


@cli.command()
@click.argument('path', default='.', type=click.Path(exists=True))
def flake_8(path):
	"""Link reports for OU-XML files in specified directory."""
	click.echo('Using file/directory: {}'.format(path))
	flake8_report_insertion(path)

