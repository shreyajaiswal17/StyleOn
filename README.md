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

## Deploy on Vercel and Render

Deploy the React frontend to Vercel and the Flask API to Render. The repository includes `render.yaml` for the backend.

### Backend on Render

Create a new Render Blueprint from this repository. Render will use `render.yaml`:

- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn app:app`

Copy the deployed Render URL, for example `https://styleon-api.onrender.com`.

### Frontend on Vercel

Import this repository into Vercel. Use the default Create React App settings, or configure:

- Build command: `npm run build`
- Output directory: `build`

Add this Vercel environment variable before deploying:

```text
REACT_APP_API_URL=https://styleon-api.onrender.com
```

After Vercel provides the frontend URL, set this Render environment variable to that exact URL:

```text
FRONTEND_URL=https://your-project.vercel.app
```