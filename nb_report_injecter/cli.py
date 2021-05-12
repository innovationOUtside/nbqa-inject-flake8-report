import click
from .flake8_report_injecter import flake8_report_insertion

@click.group()
def cli():
	pass


@cli.command()
@click.argument('path', default='.', type=click.Path(exists=True))
@click.option('--overwrite/--no-overwrite', default=False, help="Overwrite original notebook cell outputs.")
@click.option('--tags/--no-tags', default=False, help="Add flake8 error code(s) to cell tags.")
def flake8(path, overwrite=False, tags=True):
	"""Link reports for OU-XML files in specified directory."""
	click.echo('Using file/directory: {}'.format(path))
	flake8_report_insertion(path, overwrite, tags )

