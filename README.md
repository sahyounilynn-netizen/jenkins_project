# jenkins_project — EECE 435L Lab 10

A small Python application built, checked, tested and deployed by a Jenkins
CI/CD pipeline.

**Author:** Lynn Sahyouni

## Contents

| File | Purpose |
| --- | --- |
| `app.py` | `greet(name)` returns `Hello, <name> from Lynn Sahyouni!`; running the script prints the greeting for `World`. |
| `tests/test_app.py` | unittest-style tests, run with pytest. |
| `requirements.txt` | Tools used by the pipeline: flake8, pytest, coverage, bandit. |
| `Jenkinsfile_Lynn_Sahyouni` | Declarative Jenkins pipeline (Windows agent, `bat` steps). |

## Run locally (Windows)

```bat
py -3.13 -m venv venv
venv\Scripts\python.exe -m pip install -r requirements.txt
venv\Scripts\python.exe -m flake8 app.py tests
venv\Scripts\python.exe -m pytest -v
venv\Scripts\python.exe app.py
```

Expected output of the last command:

```
Hello, World from Lynn Sahyouni!
```

## Jenkins

Pipeline job `Python-CI-CD`, *Pipeline script from SCM* (Git, branch `main`),
Script Path `Jenkinsfile_Lynn_Sahyouni`.
