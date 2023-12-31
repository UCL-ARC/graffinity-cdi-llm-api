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

[python-tooling](https://github.com/UCL-ARC/python-tooling)

[FastAPI](https://fastapi.tiangolo.com/)

[Pydantic](https://pydantic.dev/)

[LangChain](https://python.langchain.com/docs/get_started/introduction)

## Getting Started

### Prerequisites

<!-- Any tools or versions of languages needed to run code. For example specific Python or Node versions. Minimum hardware requirements also go here. -->

`llm-api` requires Python 3.11 or newer.

### Installation

<!-- How to build or install the application. -->

We recommend installing in a project specific virtual environment created using a environment management tool such as [Conda](https://conda.io/projects/conda/en/latest/). To install the latest development version of `llm-api` using `pip` in the currently active environment run

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

### Setting up environment variables

This is a crucial step in running the application and should not be skipped! We use [Pydantic settings management](https://docs.pydantic.dev/latest/concepts/pydantic_settings/#environment-variable-names) to configure and verify settings such as API keys, LLM model choice and, when running via Docker Compose, port choice. Pydantic will preferentially set the variables defined in [config.py](src/llm_api/config.py#L7) from existing environment variables, before reading from a `.env` file in the root directory of the repository. An example `.env.example` file is provided showing the correct naming scheme for all required settings variables, with a prefix defined in [config.py](src/llm_api/config.py#L13). Model names are defined as `StrEnums` to show developers the possible values each variable may take.

Before running the application (either locally or in a container), rename `.env.example` to `.env` and provide a value for each variable. Particular attention should be paid to API keys and model names.

A description of each variable is provided below:

- `LLM_API_OPENAI_API_KEY` is **your** OpenAI API key. You must have completed billing details and preloaded credit to your account before models are callable.
- `LLM_API_OPENAI_LLM_NAME` is set with a prefilled value in `.env.example` and is the recommended OpenAI model for use.
- `LLM_API_AWS_ACCESS_KEY_ID` is the Access Key ID from an AWS account with the Allow permission set on the `bedrock:InvokeModel` action on the resource `arn:aws:bedrock:*::foundation-model/*`.
- `LLM_API_AWS_SECRET_ACCESS_KEY` is the corresponding secret key to the above Access Key ID.
- `LLM_API_AWS_BEDROCK_MODEL_ID` is the bedrock model ID string. As a default, this is set to `anthropic.claude-v2`.
- `API_PORT` is set to 9000 as a default. Feel free to change this as required.

### Running Locally

The FastAPI application can be run locally with

```bash
python src/llm_api/main.py
```

This runs the application via the [Uvicorn](https://www.uvicorn.org/) ASGI server on [http://localhost:8000](http://localhost:8000), with automatically generated OpenAPI Swagger documentation available at [http://localhost:8000/docs](http://localhost:8000/docs). Any changes to the code are immediately reflected in the running application.

This default behaviour may be changed by running the uvicorn server directly via

```bash
uvicorn llm_api.main:app --host {your host here} --port {your port here}
```

Running the application with a Uvicorn server is intended only for local testing and is not recommended for use in production. For production deployment, please see [Docker deployment via Docker Compose](#docker-deployment-via-docker-compose).

### Docker deployment via Docker Compose

`Dockerfile` contains instructions for building a docker image that runs this application with a [Gunicorn](https://gunicorn.org/#docs) server. Gunicorn configuration can be found in `src/llm_api/gunicorn_conf.py`. Ensure the `API_PORT` variable is defined in the `.env` file.

Container orchestration is performed by [Docker Compose](https://docs.docker.com/compose/), allowing for multiple networked containers. You may prefer to use Kubernetes or similar, and this is just shown here as an example. The `compose.yml` file defines the service name, relevant env file to use, methods of determining container health, port mappings and internal network names. We currently deploy a single service, though this can be easily extended using Docker Compose.

Build and deploy the application on `http://localhost:{API_PORT}` with the following command

```bash
docker compose --project-name ${PROJECT_NAME} up --build
```

the application can be taken down via

```bash
docker compose  --project-name ${PROJECT_NAME} down
```

Any additional running containers associated with `${PROJECT_NAME}` but not defined in `compose.yml` (for whatever reason) can be stopped with

```bash
docker compose  --project-name llm_api down --remove-orphans
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
- We will use [ruff](https://beta.ruff.rs/docs/) for linting and code formatting to standardise code, improve legibility and speed up code reviews
- Function arguments and return types will be annotated, with type checking via [mypy](https://mypy.readthedocs.io/en/stable/)
- We will use [docstrings](https://peps.python.org/pep-0257/) to annotate classes, class methods and functions
  - If you use Visual Studio Code, [autoDocstring](https://marketplace.visualstudio.com/items?itemName=njpwerner.autodocstring) is recommended to speed this along.

### Secrets detection

We use a [secret detection pre-commit hook](https://github.com/Yelp/detect-secrets) to ensure that no passwords, API keys or similarly sensitive credentials are committed to the repository. If you add in some fake credentials (for testing purposes or similar), please update the `.secrets.baseline` file in order for CI checks on any resulting pull requests to pass. You can update this file by running

```bash
detect-secrets scan > .secrets.baseline
```

from the root directory of the repository. The `detect-secrets` dependency is installed via `pip` if you select the `dev` optional dependencies.

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
- [x] Minimum viable product <-- You are Here
- [ ] Alpha Release
- [ ] Feature-Complete Release

## Acknowledgements

This work was funded through the UCL CDI.
