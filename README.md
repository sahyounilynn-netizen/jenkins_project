# jenkins_project — EECE 435L Lab 10

A small Python application built, checked, tested and deployed by a Jenkins
CI/CD pipeline.

**Author:** Lynn Sahyouni

## Contents

| File | Purpose |
| --- | --- |
| `app.py` | `greet(name)` returns `Hello, <name> from Lynn Sahyouni!`; running the script prints the greeting for `World`. |
| `tests/` | unittest-style tests for the app and the deployment script, run with pytest. |
| `deploy.py` | Local deployment: copies the app to `%USERPROFILE%\Lab10_Deploy\Python-CI-CD`, runs the deployed copy and verifies the greeting. |
| `requirements.txt` | Tools used by the pipeline: flake8, pytest, coverage, bandit. |
| `Jenkinsfile_Lynn_Sahyouni` | Declarative Jenkins pipeline (Windows agent, `bat` steps). |

## Run locally (Windows)

```bat
py -3.13 -m venv venv
venv\Scripts\python.exe -m pip install -r requirements.txt
venv\Scripts\python.exe -m flake8 .
venv\Scripts\python.exe -m pytest -v
venv\Scripts\python.exe -m coverage run -m pytest -q
venv\Scripts\python.exe -m coverage report
venv\Scripts\python.exe -m bandit -r app.py deploy.py tests
venv\Scripts\python.exe app.py
```

Expected output of the last command:

```
Hello, World from Lynn Sahyouni!
```

## Jenkins

Pipeline job `Python-CI-CD`, *Pipeline script from SCM* (Git, branch `main`),
Script Path `Jenkinsfile_Lynn_Sahyouni`.

Stages: Setup → Lint → Test → Coverage → Security Scan → Deploy. Reports
(JUnit XML, coverage text/XML/HTML, Bandit text/JSON, deployment verification)
are archived as build artifacts before the workspace is cleaned.
