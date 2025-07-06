# Webhook Repo Complete Solution

## Project Contents

- **app.py** — Flask server for GitHub webhook receiver and MongoDB integration
- **templates/index.html** — Basic frontend that polls the server
- **requirements.txt** — Python dependencies
- **README.md** — How to run instructions

## How to Run

1. Install dependencies: `pip install -r requirements.txt`
2. Make sure MongoDB is running.
3. Run: `python app.py`
4. Expose using ngrok: `ngrok http 5000`
5. Add your ngrok URL as a webhook in GitHub repo.
6. Push, create PR, merge → see updates on `http://localhost:5000`