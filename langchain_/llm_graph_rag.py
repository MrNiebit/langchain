# --coding: utf-8--
from langchain_community.graphs.nebula_graph import NebulaGraph
from langchain_community.chains.graph_qa.nebulagraph import NebulaGraphQAChain
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

# 按优先级依次加载配置文件
load_dotenv('../.env', override=True)            # 最低优先级
load_dotenv('../.env.local', override=True)      # 最高优先级

API_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = os.getenv("OPENAI_BASE_URL")
CHAT_MODEL = os.getenv("CHAT_MODEL_NAME")

llm = ChatOpenAI(
    model=CHAT_MODEL,
    api_key=API_KEY,
    base_url=BASE_URL
)
graph_db = NebulaGraph(
    space="nezha2",
    username="root",
    password="nebula",
    address="10.118.21.49",
    port=9669,
)
graph_db.refresh_schema()
print(graph_db.get_schema)

qa_chain = NebulaGraphQAChain.from_llm(
    llm=llm,
    graph=graph_db,
    verbose=True,  # 开启详细输出，便于调试
    allow_dangerous_requests=True  # 明确确认风险
)
question = "查询下所有人物"
result = qa_chain.invoke({"query": question})
for k,v in result.items():
    print(k, ": ", v)
