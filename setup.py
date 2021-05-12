from setuptools import setup

setup(
    name="nb_report_injecter",
    packages=['nb_report_injecter'],
    version='0.0.1',
    author="Tony Hirst",
    author_email="tony.hirst@gmail.com",
    description="Simple report injecter into ipynb.",
    long_description='''
    Tools for injecting reports into ipynb Jupyter notebooks.
    ''',
    long_description_content_type="text/markdown",
    install_requires=[
        'click',
        'nbformat'
    ],
    entry_points='''
        [console_scripts]
        nb_report_inject=nb_report_injecter.cli:cli
    '''

)
