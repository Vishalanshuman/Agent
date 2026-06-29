import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from langchain.agents import create_agent
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

from functions import (
    create_file,
    delete_file,
    get_current_directory_files,
    get_file_content,
    override_file,
)
from calculator import calculate
from prompts import prompts

load_dotenv()

app = FastAPI(title="Agent API")
agent = None


class AskRequest(BaseModel):
    message: str


def get_agent():
    global agent

    if agent is not None:
        return agent

    huggingface_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
    if not huggingface_token:
        raise RuntimeError("HUGGINGFACEHUB_API_TOKEN is not set.")

    print(f"Hugging Face API Token: {huggingface_token[:4]}...{huggingface_token[-4:]}")

    tools = [
        get_current_directory_files,
        get_file_content,
        create_file,
        override_file,
        calculate,
        delete_file,
    ]

    model_repo = "Qwen/Qwen2.5-7B-Instruct"
    llm_endpoint = HuggingFaceEndpoint(
        repo_id=model_repo,
        task="text-generation",
        max_new_tokens=2048,
        do_sample=False,
    )

    llm = ChatHuggingFace(llm=llm_endpoint)
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=prompts["ai_agent"],
    )
    return agent


@app.get("/")
def health_check():
    return {"status": "ok"}


@app.post("/ask")
def ask(request: AskRequest):
    current_agent = get_agent()
    state = {"messages": [{"role": "user", "content": request.message}]}
    response = current_agent.invoke(state)
    answer = response["messages"][-1].content
    return {"answer": answer}


