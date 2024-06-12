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
from flask_utils import register_error_handlers
from flask_utils import BadRequestError

app = Flask(__name__)

register_error_handlers(app)

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

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->
