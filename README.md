# First Time Setup

```
# Create a virtual environment
conda create --name gtd python=3.11

conda activate gtd

# Create requirements

For pip
pip freeze > requirements.txt

For conda
conda list --export > conda-requirements.txt


# Install dependencies

conda install conda-requirements.txt

pip install -r requirements.txt

```

# Running the app

### To run the Python server

```
flask run
```
