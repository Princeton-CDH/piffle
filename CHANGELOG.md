# Change & Version Information

## 0.9.0

- Revise git-flow configuration so releases and hotfixes merge to main instead of squash merge
- Update software release GitHub issue template

## 0.8.0

- Restored `piffle.presentation` unit tests from v0.6.1; separated tests for `piffle.iiif_dataclasses` presentation implementation
- Drop Python 3.8, 3.9 support and add Python 3.14 support
- Adopted uv support and package src layout
- Adopt git-flow-next for git-flow branching conventions
- Add custom hooks for git-flow workflow in `gitflow-hooks`
- Add custom script for configuring git-flow `setup_gitflow.sh`
- Add additional pre-commit hooks and adopted Ruff-based formatting
- Adopt Dependabot version updates for GitHub Actions and pre-commit
- Add CodeQL GitHub Action
- Add GitHub Action for Ruff lint and format checks
- Add GitHub Action to check for changelog updates
- Add GitHub Action to check that pull requests align with git-flow workflow
- Add custom GitHub issue template for software releases
- Add custom config for codecov to create separate checks for the core package, tests, and experimental code

## 0.7.0

*experimental* new dataclass interfaces in `piffle.iiif_dataclasses` thanks to @rwood-97

- Add dataclasses for parsing IIIF Presentation and Image APIs.
  - New `collect_annotations` method to collect annotations on a presentation
- Now supports IIIF Presentation API and Image API version 3.
- Adds `load_iiif_image` and `load_iiif_presentation` functions for loading IIIF into dataclasses.

**NOTE**: new dataclasses do not yet replace the existing default API;
interface and package structure may change in future releases.

## 0.6.1

- Add explicit support for and testing against python 3.13 (thanks to @rettinghaus)

## 0.6.0

- HTTP request method `get_iiif_url` is now a class method on
  `piffle.presentation.IIIFPresentation`, which can be extended when request
  customization is needed
- Manifests now supports attr-dict style access to `@id` in `seeAlso` list entries

## 0.5.1

- Add explicit support and testing for python 3.12

## 0.5.0

- Now supports python 3.8-3.11; dropped support for Python versions 3.6, 3.7
- Converted setup.py to pyproject.toml
- The alias for accessing `piffle.image` via `piffle.iiif` has been removed
- Setup pre-commit hooks and adopted Ruff+Black style formatting

## 0.4.0

- Dropped support for Python versions 2.7, 3.4, 3.5
- Now tested against python 3.7 and 3.8
- Moved continues integration from Travis-CI to GitHub Actions
- Renamed `piffle.iiif` to `piffle.image`, but for backwards compatibility `piffle.iiif` will still work
- Now includes `piffle.presentation` for simple read access to IIIF Presentation content

## 0.3.2

- Dropped support for Python 3.3

## 0.3.1

- Added long description content type for PyPi

## 0.3.0

- Now Python 3 compatible
- URI canonicalization for size, region, rotation, and URL as a whole

## 0.2.1

- Bug fix: chaining multiple different options combines all of them properly and does not modify
  the original image object.

## 0.2.0

- New methods to parse urls and provide image option information. Contributed by [Graham Hukill (@ghukill)](https://github.com/ghukill) [PR #1](https://github.com/emory-lits-labs/piffle/pull/1)
- New method to parse a IIIF Image url and initialize IIIFImageClient via url
- New methods to make IIIF Image options available as dictionary
- Options are now stored internally in logical, dictionary form rather than as IIIF option strings

## 0.1.0

Initial alpha release, extracting basic IIIF Image API client from [readux codebase](https://github.com/emory-libraries/readux)

- Image client can handle custom id and generates urls for json info, and custom sizes and formats.
