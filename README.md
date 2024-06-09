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
- [ ] Automatic build/deployment
