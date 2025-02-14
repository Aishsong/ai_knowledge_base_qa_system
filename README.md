# AI Knowledge Base QA System

这是一个基于 LangChain、FAISS 及 OpenAI 嵌入构建的问答系统示例。该系统能从本地知识库中加载文本文件，拆分成文档片段，构建向量数据库，并通过自定义提示（prompt）实现中文问答。

## 功能特点

- **本地知识库加载**  
  程序会从 `data/` 文件夹加载所有的 `.txt` 文件作为知识文档。

- **文档拆分**  
  利用内置的文本拆分器将长文档拆分成适合生成嵌入的小片段，确保生成向量数据的效率和准确性。

- **向量数据库构建**  
  使用 OpenAI 嵌入生成器与 FAISS 构建全文本片段的向量数据库，方便后续检索。

- **自定义中文问答**  
  通过自定义提示模板，确保回答均以中文输出。当文档中无相关信息时返回预设提示。

## 环境要求

- Python 3.7 及以上版本

## 安装步骤

1. **克隆仓库**

   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **创建并激活虚拟环境**（可选但推荐）

   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Linux/MacOS:
   source venv/bin/activate
   ```

3. **安装依赖**

   ```bash
   pip install -r requirements.txt
   ```

   依赖包包括：
   - langchain
   - faiss-cpu
   - openai
   - langchain-community
   - unstructured
   - tiktoken
   - langchain-openai
   - python-dotenv

4. **配置 API 密钥**
    (可忽略，使用默认的API key)

   在项目根目录下创建 `.env` 文件，并添加以下内容（请使用你平台提供的 API key）：

   ```env
   OPENAI_API_KEY="hk-your-key-here"
   ```

   注意：该项目默认使用的 API 基本地址为 `https://api.openai-hk.com/v1`。（此为代理API，如果需要使用其他API地址，请在 `main.py` 中修改 `openai.api_base` 和 `openai.base_url` 以及 `.env` 文件中的 `OPENAI_BASE_URL` 的值）

5. **准备知识库文档**

   将你的文本文档放入项目根目录下的 `data/` 文件夹中。仓库中已提供一个示例文件 `sample.txt`，内容为企业内部文档示例。

## 运行项目

在项目根目录下运行：

```bash
python main.py
```

程序将自动执行以下流程：

1. 从 `data/` 文件夹加载文档。
2. 拆分文档生成多个片段。
3. 利用 OpenAI 嵌入构建 FAISS 向量数据库。
4. 启动交互式问答系统，等待你输入问答。

输入问题后，系统会基于知识库内容结合 OpenAI 语言模型生成中文回答。如果没有相关信息，则返回预设回答“文档中暂无相关信息”。

## 自定义与扩展

- **自定义提示模板**  
  你可以在 `main.py` 中修改 `custom_prompt` 变量，按需调整问答模板内容。

- **向量数据库和嵌入生成**  
  如需更换嵌入模型或调整 FAISS 参数，请参考相应的包文档进行修改。

- **日志与调试**  
  默认 `verbose` 参数已关闭，如需查看详细日志信息可修改对应配置。

## 常见问题

- **API 密钥配置问题**  
  如果运行时提示未设置 `OPENAI_API_KEY`，请检查 `.env` 文件是否存在于项目根目录，并确认你的 API key 是否正确。

- **输入键缺失错误**  
  保证在调用 RetrievalQA 链时，传入字典的键与自定义提示模板中定义的输入变量一致（本项目中统一使用 `"question"`）。

- **依赖包问题**  
  请确保所有依赖均已安装且版本与项目要求兼容，可尝试运行 `pip install --upgrade <package>` 进行升级。

## 许可

该项目采用开源协议发布，欢迎你按照需求自由使用和修改。

## 致谢

- 该项目使用了 [LangChain](https://python.langchain.com) 实现链式调用。
- 利用 [FAISS](https://github.com/facebookresearch/faiss) 实现高效向量检索。
- 结合 [OpenAI](https://openai.com) 的语言模型进行自然语言处理。

