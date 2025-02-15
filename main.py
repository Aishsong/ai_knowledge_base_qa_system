import os
import openai
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate

load_dotenv()

# 设置自定义的 API 基本地址
openai.api_base = "https://api.openai.com/v1"
openai.base_url = "https://api.openai.com/v1"
openai.api_key = os.environ["OPENAI_API_KEY"]

# 检查是否设置了 OPENAI_API_KEY 环境变量
if "OPENAI_API_KEY" not in os.environ:
    print("请先设置 OPENAI_API_KEY 环境变量，例如：set OPENAI_API_KEY=你的openai_api_key")
    exit(1)

from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

def main():
    # 检查 data 文件夹是否存在
    data_dir = "data"
    if not os.path.exists(data_dir):
        print(f"未找到数据文件夹 '{data_dir}'，请在项目根目录下创建该文件夹，并放入文本文件。")
        return

    print("正在从 data/ 目录加载文档……")
    # 加载所有 txt 文件（根据需要修改 glob 参数适用于其他文件类型）
    loader = DirectoryLoader(data_dir, glob="**/*.txt")
    docs = loader.load()
    print(f"共加载到 {len(docs)} 个文档。")

    # 对加载的文档进行拆分，防止文本太长
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.split_documents(docs)
    print(f"文档拆分后生成 {len(docs)} 个文档片段。")

    # 使用 OpenAI 嵌入构建 FAISS 向量数据库
    print("正在构建向量数据库……")
    embeddings = OpenAIEmbeddings()
    vector_db = FAISS.from_documents(docs, embeddings)
    print("向量数据库构建完成。")

    # 自定义提示模板，使用变量 "question"
    custom_prompt = PromptTemplate(
        input_variables=["context", "question"],
        template='请用中文回答下面的问题。如果文档中没有相关信息，请回答“文档中暂无相关信息”。\n\n文档片段：\n{context}\n\n问题：{question}\n答案：'
    )

    # 创建 RetrievalQA 链，显式设置输入键为 "question"
    qa = RetrievalQA.from_chain_type(
        llm=OpenAI(temperature=0, verbose=False),
        chain_type="stuff",
        retriever=vector_db.as_retriever(),
        chain_type_kwargs={"prompt": custom_prompt, "verbose": False},
        input_key="question"
    )

    print("问答系统已就绪，输入问题后回车即可（输入 q 或 Q 退出）：")
    while True:
        query = input("请输入您的问题 (q 退出): ")
        if query.strip().lower() == "q":
            print("退出问答系统！")
            break
        # 调用链时传入字典，键为 "question"
        answer = qa({"question": query})
        # 仅输出返回结果中的 'result' 内容
        print("回答：", answer.get("result", answer))
        print("-" * 50)

if __name__ == "__main__":
    main()