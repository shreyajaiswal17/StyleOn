# StyleOn

StyleOn is a React and Flask fashion recommendation app. Select an occasion, gender, season, color, and clothing category to receive matching items from the catalog.

## Run locally

Install frontend dependencies and start React:

```bash
npm install
npm run dev
```

In a second terminal, install the backend dependencies and start Flask:

```bash
python -m pip install -r requirements.txt
python app.py
```

The frontend runs at `http://localhost:3000` and the API runs at `http://localhost:5000`. For a deployed API, set `REACT_APP_API_URL` before building the frontend.

## Deploy on Render

This repository includes `render.yaml` for a Flask API and React static site. In Render, create a new Blueprint and select this repository. Render will create both services.

The frontend uses `REACT_APP_API_URL` to call the API. For a manual setup, set it to the deployed API URL before the frontend build, for example `https://styleon-api.onrender.com`.