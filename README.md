# graffinity-cdi-llm-api

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Tests status][tests-badge]][tests-link]
[![Linting status][linting-badge]][linting-link]
[![License][license-badge]](./LICENSE.md)

<!--
[![PyPI version][pypi-version]][pypi-link]
[![Conda-Forge][conda-badge]][conda-link]
[![PyPI platforms][pypi-platforms]][pypi-link]
-->

<!-- prettier-ignore-start -->
[tests-badge]:              https://github.com/UCL-ARC/graffinity-cdi-llm-api/actions/workflows/tests.yml/badge.svg
[tests-link]:               https://github.com/UCL-ARC/graffinity-cdi-llm-api/actions/workflows/tests.yml
[linting-badge]:            https://github.com/UCL-ARC/graffinity-cdi-llm-api/actions/workflows/linting.yml/badge.svg
[linting-link]:             https://github.com/UCL-ARC/graffinity-cdi-llm-api/actions/workflows/linting.yml
[conda-badge]:              https://img.shields.io/conda/vn/conda-forge/llm-api
[conda-link]:               https://github.com/conda-forge/llm-api-feedstock
[pypi-link]:                https://pypi.org/project/llm-api/
[pypi-platforms]:           https://img.shields.io/pypi/pyversions/llm-api
[pypi-version]:             https://img.shields.io/pypi/v/llm-api
[license-badge]:            https://img.shields.io/badge/License-BSD_3--Clause-blue.svg
<!-- prettier-ignore-end -->

API for converting user searches to robust LLM prompts and returning a response.

This project is developed in collaboration with the [Centre for Advanced Research Computing](https://ucl.ac.uk/arc) (ARC), University College London and the [Centre for Digital Innovation](https://www.ucl.ac.uk/centre-digital-innovation) (CDI), University College London.

## About

### Project Team

Harry Moss ([h.moss@ucl.ac.uk](mailto:h.moss@ucl.ac.uk))
Sanaz Jabbari ([s.jabbari@ucl.ac.uk](mailto:s.jabbari@ucl.ac.uk))
Nik Khadijah Nik Aznan ([n.aznan@ucl.ac.uk](mailto:n.aznan@ucl.ac.uk))

### Research Software Engineering Contact

Centre for Advanced Research Computing, University College London
([arc.collaborations@ucl.ac.uk](mailto:arc.collaborations@ucl.ac.uk))

## Built With

[FastAPI](https://fastapi.tiangolo.com/)
[Pydantic](https://pydantic.dev/)

## Getting Started

### Prerequisites

<!-- Any tools or versions of languages needed to run code. For example specific Python or Node versions. Minimum hardware requirements also go here. -->

`llm-api` requires Python 3.11 or newer.

### Installation

<!-- How to build or install the application. -->

We recommend installing in a project specific virtual environment created using a environment management tool such as [Mamba](https://mamba.readthedocs.io/en/latest/user_guide/mamba.html) or [Conda](https://conda.io/projects/conda/en/latest/). To install the latest development version of `llm-api` using `pip` in the currently active environment run

```sh
pip install git+https://github.com/UCL-ARC/graffinity-cdi-llm-api.git
```

Alternatively create a local clone of the repository with

```sh
git clone https://github.com/UCL-ARC/graffinity-cdi-llm-api.git
```

and then install in editable mode by running

```sh
pip install -e .
```

### Running Locally

How to run the application on your local system.

### Running Tests

<!-- How to run tests on your local system. -->

Tests can be run across all compatible Python versions in isolated environments using
[`tox`](https://tox.wiki/en/latest/) by running

```sh
tox
```

To run tests manually in a Python environment with `pytest` installed run

```sh
pytest tests
```

again from the root of the repository.

## Roadmap

- [x] Initial Research
- [ ] Minimum viable product <-- You are Here
- [ ] Alpha Release
- [ ] Feature-Complete Release

## Acknowledgements

This work was funded through the UCL CDI.
