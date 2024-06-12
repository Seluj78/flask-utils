[![Documentation Status](https://readthedocs.org/projects/flask-utils/badge/?version=latest)](https://flask-utils.readthedocs.io/en/latest/?badge=latest)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/Seluj78/flask-utils)
![GitHub commits since latest release](https://img.shields.io/github/commits-since/seluj78/flask-utils/latest)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/seluj78/flask-utils/tests.yml?label=tests)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/seluj78/flask-utils/linting.yml?label=linting)
![GitHub License](https://img.shields.io/github/license/seluj78/flask-utils)
[![All Contributors](https://img.shields.io/github/all-contributors/seluj78/flask-utils?color=ee8449&style=flat-square)](#contributors)
[![codecov](https://codecov.io/gh/Seluj78/flask-utils/graph/badge.svg?token=ChUOweAp4b)](https://codecov.io/gh/Seluj78/flask-utils)

[//]: # (TODO: Uncomment when flask-utils had been freed from pypi)
[//]: # (![PyPI - Downloads]&#40;https://img.shields.io/pypi/dm/flask-utils&#41;)
[//]: # (![PyPI - Implementation]&#40;https://img.shields.io/pypi/implementation/flask-utils&#41;)
[//]: # (![PyPI - Python Version]&#40;https://img.shields.io/pypi/pyversions/flask-utils&#41;)
[//]: # (![PyPI - Versions from Framework Classifiers]&#40;https://img.shields.io/pypi/frameworkversions/:frameworkName/flask-utils&#41;)
[//]: # (![PyPI - Wheel]&#40;https://img.shields.io/pypi/wheel/flask-utils&#41;)
[//]: # (![PyPI - Version]&#40;https://img.shields.io/pypi/v/flask-utils&#41;)

# Flask-Utils

A collection of useful Flask utilities I use every day in my Flask projects.

## Installation

```bash
pip install flask-utils
```

## Usage

```python
from flask import Flask
from flask_utils import FlaskUtils
from flask_utils import BadRequestError

app = Flask(__name__)
utils = FlaskUtils(app, register_error_handlers=True)

@app.route('/')
def index():
    raise BadRequestError
```

```python
from typing import List, Optional
from flask import Flask
from flask_utils import validate_params

app = Flask(__name__)

@app.post('/create-user')
@validate_params({"first_name": str, "last_name": str, "age": Optional[int], "hobbies": List[str]})
def create_user():
    # ...
    # This will enforce the following rules:
    # - first_name and last_name must be strings and are required
    # - age is optional and must be an integer
    # - hobbies is a list of strings
    # This is just an example, you can use any type of validation you want
    return "User created"
```

## Documentation

You can find the full documentation at [Read the Docs](https://flask-utils.readthedocs.io/en/latest/)

## Testing

Install the requirements
```bash
pip install -r requirements-dev.txt
```

Make sure tox is at the latest version
```bash
pip install --upgrade tox
```

Run the tests
```bash
tox
```

OR

Run the tests multi-threaded
```bash
tox -p
```


## Contributors

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://juleslasne.com"><img src="https://avatars.githubusercontent.com/u/4641317?v=4?s=100" width="100px;" alt="Jules Lasne"/><br /><sub><b>Jules Lasne</b></sub></a><br /><a href="#code-Seluj78" title="Code">💻</a> <a href="#doc-Seluj78" title="Documentation">📖</a> <a href="#infra-Seluj78" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a> <a href="#example-Seluj78" title="Examples">💡</a> <a href="#mentoring-Seluj78" title="Mentoring">🧑‍🏫</a> <a href="#platform-Seluj78" title="Packaging/porting to new platform">📦</a> <a href="#projectManagement-Seluj78" title="Project Management">📆</a> <a href="#review-Seluj78" title="Reviewed Pull Requests">👀</a> <a href="#tutorial-Seluj78" title="Tutorials">✅</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Mews"><img src="https://avatars.githubusercontent.com/u/60406199?v=4?s=100" width="100px;" alt="Mews"/><br /><sub><b>Mews</b></sub></a><br /><a href="#doc-Mews" title="Documentation">📖</a> <a href="#tutorial-Mews" title="Tutorials">✅</a></td>
    </tr>
  </tbody>
  <tfoot>
    <tr>
      <td align="center" size="13px" colspan="7">
        <img src="https://raw.githubusercontent.com/all-contributors/all-contributors-cli/1b8533af435da9854653492b1327a23a4dbd0a10/assets/logo-small.svg">
          <a href="https://all-contributors.js.org/docs/en/bot/usage">Add your contributions</a>
        </img>
      </td>
    </tr>
  </tfoot>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->
