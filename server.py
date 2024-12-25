import os

from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import AzureChatOpenAI
from langserve import add_routes

load_dotenv(find_dotenv())

# プロンプトテンプレート、モデル、出力パーサーを定義します。
system_template = "Translate the following into {language}:"
prompt_template = ChatPromptTemplate.from_messages([("system", system_template), ("user", "{text}")])
model = AzureChatOpenAI(
    azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT"],
)
parser = StrOutputParser()

# チェーンを定義します。
chain = prompt_template | model | parser

# appの定義としてFastAPIアプリケーションのインスタンスを作成します。
app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="A simple API server using LangChain's Runnable interfaces",
)

# チェーンをエンドポイントに追加します。
add_routes(app, chain, path="/chain")

if __name__ == "__main__":
    import uvicorn

    # サーバーを起動します。
    uvicorn.run(app, host="localhost", port=8000)
