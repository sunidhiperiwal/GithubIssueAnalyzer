from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from analyzer import get_llm_chain
from github_fetcher import fetch_github_issue
from models import IssueRequest

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze_issue(request: IssueRequest):
    try:
        result = fetch_github_issue(request.repo_url, request.issue_number)
        # analyze=get_llm_chain()
        return result
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
