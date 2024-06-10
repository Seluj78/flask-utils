[![Documentation Status](https://readthedocs.org/projects/flask-utils/badge/?version=latest)](https://flask-utils.readthedocs.io/en/latest/?badge=latest)

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

# TODO

- [ ] Documentation
- [ ] Licence
- [ ] Badges
- [ ] Automatic build/deployment (https://github.com/pypa/cibuildwheel)
- [ ] https://github.com/PyCQA/flake8-bugbear
- [ ] Versioning of docs in Read the Docs
