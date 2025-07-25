from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama
from langchain_community.chat_models import ChatOpenAI, ChatAnthropic
import os
from dotenv import load_dotenv
import requests
from typing import Dict, Any

load_dotenv()

app = FastAPI()

class GitHubRequest(BaseModel):
    repo_url: str
    issue_number: int

response_schema = {
    "summary": "Concise problem summary",
    "type": "One of: bug, feature_request, documentation, question, other",
    "priority_score": "Integer from 1 (low) to 5 (critical)",
    "suggested_labels": "List of 2-3 relevant GitHub labels",
    "potential_impact": "Brief user impact description if bug"
}

def get_llm_chain():
    parser = JsonOutputParser()

    prompt = ChatPromptTemplate.from_template("""
    Analyze this GitHub issue and return JSON exactly matching this schema:
    {schema}

    Issue Title: {title}
    Issue Body: {body}

    Respond ONLY with valid JSON. No additional text.
    """)

    try:
        llm = Ollama(
            model="phi3:mini",
            temperature=0.3,
            system="You are a precise GitHub issue analyst."
        )
        return prompt | llm | parser
    except:
        pass

    try:
        if os.getenv("ANTHROPIC_API_KEY"):
            return prompt | ChatAnthropic(model="claude-3-haiku-20240307") | parser
    except:
        pass

    if os.getenv("OPENAI_API_KEY"):
        return prompt | ChatOpenAI(model="gpt-3.5-turbo-0125") | parser

    raise Exception("No working LLM provider found")

