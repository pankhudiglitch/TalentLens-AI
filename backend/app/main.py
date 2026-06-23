from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.services.job_engine import shortlist_candidates

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():

    return {
        "status": "running"
    }


@app.get("/shortlist")
def shortlist():

    return shortlist_candidates()

from fastapi.responses import HTMLResponse

@app.get("/demo", response_class=HTMLResponse)
def demo_page():
    data = shortlist_candidates()
    candidates = data.get("top_candidates", [])

    html = """
    <html>
    <head>
        <title>TalentLens AI Demo</title>
        <style>
            body {
                font-family: Arial;
                background: #f5f6fa;
                padding: 20px;
            }
            h1 {
                text-align: center;
                color: #2c3e50;
            }
            .card {
                background: white;
                padding: 15px;
                margin: 10px auto;
                width: 60%;
                border-radius: 10px;
                box-shadow: 0px 2px 8px rgba(0,0,0,0.1);
            }
            .name {
                font-size: 20px;
                font-weight: bold;
            }
            .score {
                color: green;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <h1>TalentLens AI - Shortlisted Candidates</h1>
    """

    for i, c in enumerate(candidates):
        html += f"""
        <div class="card">
            <div class="name">#{i+1} {c.get('name')}</div>
            <div>{c.get('headline')}</div>
            <div class="score">⭐ Score: {c.get('score')}</div>
            <div>⏳ Experience: {c.get('experience')} years</div>
        </div>
        """

    html += """
    </body>
    </html>
    """

    return html