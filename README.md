# NutriLens

NutriLens is a food-based nutrition tracking application that uses advanced statistical probability modeling (Z-Scores via `scipy`) to visualize deficiency risks across multiple macro and micro nutrients.

## How to Run Locally

### 1. Extract the zip and install requirements
Open a terminal inside the downloaded directory and run:
```bash
pip install -r requirements.txt
```

### 2. Start the Local Server
Run the primary Flask application script via terminal:
```bash
python app.py
```

### 3. Explore The App!
Open your web browser and navigate to:
**http://127.0.0.1:5000**

## How to Deploy on Render

NutriLens is ready to be hosted natively on [Render](https://render.com) using its Python environment:

1. Push this repository to GitHub.
2. Create a new **Web Service** on Render and connect your GitHub repository.
3. Use the following configuration:
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: Free ($0/month)
4. Click Deploy!
