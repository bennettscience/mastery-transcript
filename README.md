## Mastery Transcript

This is an experiment in a system that would allow users to pull data from an LMS and pair it with narrative for highlighting skills and learning. This is based on a model shared by the Mastery Learning Consortium.

This project uses [Flask-RESTX](https://github.com/python-restx/flask-restx) to handle endpoint routing and [Marshmallow](https://github.com/marshmallow-code/marshmallow) for serialization. 

### Install

Packages are managed using [Poetry](https://python-poetry.org). You can install using poetry or pip:

1. Using poetry, clone this repo and initialize a virtualenv. Run `poetry install --no-dev` to install packages.

```bash
git clone https://github.com/bennettscience/mastery-transcript.git your-dir && cd your-dir
virtualenv venv
poetry install --no-dev
# include dev dependencies
# poetry install 
```
2. Using `pip`, you can install either from `requirements.txt` or from `requirements-dev.txt` to include the tooling.

```bash
git clone https://github.com/bennettscience/mastery-transcript.git your-dir && cd your-dir
virtualenv venv
pip install -r requirements.txt
# include dev dependencies
# pip install -r requirements-dev.txt
```

## Contributing

Feel free to open issues or pull requests if you'd like to contribute ideas, but reports, or code.