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

The FastAPI application is run locally with

```bash
python src/llm_api/main.py
```

This runs the application via the [Uvicorn](https://www.uvicorn.org/) ASGI server on `http://localhost:8000`. Any changes to the code are immediately reflected in the running application. This setup is designed for local testing, and does not target production releases.

This default behaviour may be changed by running the uvicorn server directly via

```bash
uvicorn llm_api.main:app --host {your host here} --port {your port here}
```

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

## Contributing

To contribute to the project as a developer, use the following as a guide. These are based on ARC Collaborations [group practices](https://github.com/UCL-ARC/research-software-documentation/blob/main/processes/programming_projects/group_practices.md) and [code review documentation](https://github.com/UCL-ARC/research-software-documentation/blob/main/processes/programming_projects/review.md).

### Developer install

Install the project and development dependencies via `pip` with

```bash
pip install -e ".[dev,tests]"
```

Install pre-commit hooks with

```bash
pre-commit install
```

Future `git commit` operations will now run pre-commit hooks to ensure code style and typing conventions are followed. _Please remember to do this!_

### Python standards we follow

To make explicit some of the potentially implicit:

- We will target Python versions `>= 3.11`
- We will use [ruff](https://beta.ruff.rs/docs/) for linting and [black](https://github.com/psf/black) for code formatting to standardise code, improve legibility and speed up code reviews
- Function arguments and return types will be annotated, with type checking via [mypy](https://mypy.readthedocs.io/en/stable/)
- We will use [docstrings](https://peps.python.org/pep-0257/) to annotate classes, class methods and functions
  - If you use Visual Studio Code, [autoDocstring](https://marketplace.visualstudio.com/items?itemName=njpwerner.autodocstring) is recommended to speed this along.

### General GitHub workflow

- Create a branch for each new piece of work with a suitable descriptive name, such as `feature-newgui` or `adding-scaffold`
- Do all work on this branch
- Open a new PR for that branch to contain discussion about your changes
  - Do this **early** and set as a 'Draft PR' (on GitHub) until you are ready to merge to make your work visible to other developers
- Make sure the repository has CI configured so tests (ideally both of the branch, and of the PR when merged) are run on every push.
- If you need advice, mention @reviewer and ask questions in a PR comment.
- When ready for merge, request a review from the "Reviewer" menu on the PR.
- All work must go through a pull-request review before reaching `main`
  - **Never** commit or push directly to `main`

The `main` branch is for ready-to-deploy release quality code

- Any team member can review (but not the PR author)
  - try to cycle this around so that everyone becomes familiar with the code
- Try to cycle reviewers around the project's team: so that all members get familiar with all work.
- Once a reviewer approves your PR, **you** can hit the merge button
- Default to a 'Squash Merge', adding your changes to the main branch as a single commit that can be easily rolled back if need be

### Reviewing code

[The Turing Way](https://the-turing-way.netlify.app/index.html) provides an overview of best practices - it comes as recommended reading and includes some [possible workflows for code review](https://the-turing-way.netlify.app/reproducible-research/reviewing/reviewing-checklist.html?highlight=code%20review) - great if you're unsure what you're typically looking for during a code review.

## Roadmap

- [x] Initial Research
- [ ] Minimum viable product <-- You are Here
- [ ] Alpha Release
- [ ] Feature-Complete Release

## Acknowledgements

This work was funded through the UCL CDI.
