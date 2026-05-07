# piffle

Python library for generating and parsing [IIIF Image API](http://iiif.io/api/image/2.1/) URLs in an
object-oriented, pythonic fashion.

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.13308491.svg)](https://doi.org/10.5281/zenodo.13308491)
[![unit tests](https://github.com/Princeton-CDH/piffle/actions/workflows/unit_tests.yml/badge.svg)](https://github.com/Princeton-CDH/piffle/actions/workflows/unit_tests.yml)
[![codecov](https://codecov.io/gh/Princeton-CDH/piffle/branch/main/graph/badge.svg)](https://codecov.io/gh/Princeton-CDH/piffle)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/piffle)

Piffle was originally developed by Rebecca Sutton Koeser at Emory University as a part of [Readux](https://github.com/ecds/readux) and forked as a separate project under [emory-lits-labs](https://github.com/emory-lits-labs/). It was later transferred to Rebecca Sutton Koeser at the Center for Digital Humanities at Princeton.

## Installation and example use:

```sh
pip install piffle
```

Example use for generating an IIIF image url:

```sh
>>> from piffle.image import IIIFImageClient
>>> myimg = IIIFImageClient('http://image.server/path/', 'myimgid')
>>> print myimg
http://image.server/path/myimgid/full/full/0/default.jpg
>>> print myimg.info()
http://image.server/path/myimgid/info.json"
>>> print myimg.size(width=120).format('png')
http://image.server/path/myimgid/full/120,/0/default.png
```

Example use for parsing an IIIF image url:

```sh
>>> from piffle.image import IIIFImageClient
>>> myimg = IIIFImageClient.init_from_url('http://www.example.org/image-service/abcd1234/full/full/0/default.jpg')
>>> print myimg
http://www.example.org/image-service/abcd1234/full/full/0/default.jpg
>>> print myimg.info()
http://www.example.org/image-service/abcd1234/info.json
>>> myimg.as_dict()['size']['full']
True
>>> myimg.as_dict()['size']['exact']
False
>>> myimg.as_dict()['rotation']['degrees']
0.0
```

Example use for reading a IIIF manifest:

```sh
>>> from piffle.image import IIIFImageClient
>>> from piffle.presentation import IIIFPresentation
>>>  manifest = IIIFPresentation.from_url('https://iiif.bodleian.ox.ac.uk/iiif/manifest/60834383-7146-41ab-bfe1-48ee97bc04be.json')
>>> manifest.label
'Bodleian Library MS. Bodl. 264'
>>> manifest.id
'https://iiif.bodleian.ox.ac.uk/iiif/manifest/60834383-7146-41ab-bfe1-48ee97bc04be.json'
>>> manifest.type
'sc:Manifest'
>>> for canvas in manifest.sequences[0].canvases[:5]:
...     image_id = canvas.images[0].resource.id
...     iiif_img = IIIFImageClient(*image_id.rsplit('/', 1))
...     print(str(iiif_img.size(height=250)))
...
https://iiif.bodleian.ox.ac.uk/iiif/image/90701d49-5e0c-4fb5-9c7d-45af96565468/full/,250/0/default.jpg
https://iiif.bodleian.ox.ac.uk/iiif/image/e878cc78-acd3-43ca-ba6e-90a392f15891/full/,250/0/default.jpg
https://iiif.bodleian.ox.ac.uk/iiif/image/0f1ed064-a972-4215-b884-d8d658acefc5/full/,250/0/default.jpg
https://iiif.bodleian.ox.ac.uk/iiif/image/6fe52b9a-5bb7-4b5b-bbcd-ad0489fcad2a/full/,250/0/default.jpg
https://iiif.bodleian.ox.ac.uk/iiif/image/483ff8ec-347d-4070-8442-dbc15bc7b4de/full/,250/0/default.jpg
```

## Development and Testing

This project uses git flow branching conventions via [git-flow-next](https://github.com/gittower/git-flow-next).

> [!NOTE]
> Make sure you are using the correct version of git flow.
> The original [git-flow](https://github.com/nvie/gitflow) and its successor [git-flow-avh](https://github.com/petervanderdoes/gitflow-avh) are no longer maintained.
> While `git-flow-next` is backwards compatible, this project assumes the workflow and features of `git-flow-next`.

For development, we assume the usage of [uv](https://docs/astral.sh/uv/).
`uv` is compatible with the use of `pip` for python package management and a tool
of your choice for creating python virtual environments (e.g., `mamba`, `venv`).

### Initial setup and installation

- Install `uv` if it's not installed.
  It can be installed via PyPi, Homebrew, or a standalon installer.
  See `uv`'s [installation documentation](https://docs.astral.sh/uv/getting-started/installation)
  for more details.

- To explicitly sync the project's dependencies, including optional dependencies for
  development and testing, to your local environment run:

  ```sh
  uv sync
  ```

- Note that `uv` performs syncing and locking automatically (e.g., any time
  `uv run` is invoked). By default, syncing will remove any packages not
  specifically specified in the `pyproject.toml`.

### Setup git hooks

This project uses custom git hooks which are defined in `.githooks`.
To ensure these githooks are run, git needs to be reconfigured to use this directory:

```sh
git config core.hooksPath .githooks
```

If you have any pre-existing git hooks, make sure to copy them over to `.githooks`:

```sh
cp .git/hooks/* .githooks
```

### Install pre-commit hooks

Anyone who wants to contribute to this codebase should install the configured pre-commit hooks:

```sh
uv tool install pre-commit --with pre-commit-uv
```

This will configure a pre-commit hooks to automatically lint and format python code with [ruff](https://github.com/astral-sh/ruff) and [black](https://github.com/psf/black).

To run pre-commit explicitly run:

```sh
uv tool run pre-commit
```

Pre-commit hooks and formatting conventions were added at version 0.5, so `git blame` may not reflect the true author of a given change. To make `git blame` more accurate, ignore formatting revisions:

```sh
git blame <FILE> --ignore-revs-file .git-blame-ignore-revs
```

Or configure your git to always ignore styling revision commits:

```sh
git config blame.ignoreRevsFile .git-blame-ignore-revs
```

### Unit testing

Unit tests are set up to be used with [pytest](https://docs.pytest.org/).

To run the tests, run:

```sh
uv run pytest
```

### Pull requests

To propose code changes, create a pull request against the **develop** branch
(per our git flow workflow). Pull requests should include an update to `CHANGELOG.md`
documenting the changes to the project.

Several GitHub Actions are run for pull requests: unit testing, code coverage,
ruff checks, and a changelog check. By default, the changelog check will fail if
the PR does not update `CHANGELOG.md`. For pull requests that do not modify code,
the "no changelog" label can be added to skip this check.

### Publishing python packages

A new python package is automatically built and published to [PyPI](https://pypi.python.org/pypi) using a GitHub Actions workflow when a new release is created on GitHub.

## License

**piffle** is distributed under the Apache 2.0 License.

## Contributors

- Rebecca Sutton Koeser
- Graham Hukill
- Rosie Wood
- Klaus Rettinghaus
- Laure Thompson
