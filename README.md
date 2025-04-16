# monte-carlo-parley

a monte carlo simulation for poker hands written in RUST

# installation

```bash
pip install -r requirements.txt
```

# run app

```bash

# development
python run_app.py

# production
gunicorn -c gunicorn_config.py wsgi:app
```
