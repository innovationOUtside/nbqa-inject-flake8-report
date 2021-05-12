# nbqa-inject-flake8-report
Inject nbqa flake8 report into notebooks


## Installation

```
pip install git+https://github.com/innovationOUtside/nbqa-inject-flake8-report.git
```

## Usage


For example, with `nbqa` installed, run:
```
nbqa flake8 notebooks/*.ipynb > flake8_reports.txt
```

And then to inject the flake8 reports into notebook code cell outputs:

```
nb_report_inject flake8 flake8_reports.txt

# Then to synch jupytext
jupytext --sync  notebooks/*.ipynb
# Jupytext doesn't map outputs but we need to keep timestamps in synch
```

By default, outputs are written to `notebooks/*_flake8.ipynb`We can clear and overwrite output cells in the reported on notebooks with the `--overwrite / --no-overwrite` flag:

```
nb_report_inject flake8 --overwrite flake8_reports.txt
```

By default, code cells with injected flake8 reports are annotated with a `flake8-error` tag and a `flake8-error-CODE` tag that identifies each distinct flake8 error codes reported for the cell (TO DO - also clear error code tags...); these can be explicilty enabled / disabled with the `--tags/--no-tags` flag:

```
nb_report_inject flake8 --no-tags flake8_reports.txt
```
