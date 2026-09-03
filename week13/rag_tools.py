from langchain.tools import tool
from week13.retriever_test import search

@tool
def search_documents(query: str) -> str:
    """在本地知识库中检索与问题相关资料。
    当用户询问文档、手册、知识库中具体内容时使用此工具。
    知识库目前包含两份文档：
    - 电商公司员工手册：考勤与休假、薪酬与绩效、奖惩制度等公司制度。
    - ai agent未来发展趋势：涉及到AI的市场需求、从数字到物理等信息。
    输入应该是一个清晰的检索关键词或问题。
    闲聊、常识性问题不使用此工具。"""

    docs = search(query)
    if not docs:
        return "未找到相关资料"
    return "\n\n".join([
        f"来源: {d.metadata.get('source')}\n{d.page_content}" 
        for d in docs
    ])
if __name__ == "__main__":
    print(search_documents.invoke({"query": "年假有几天"}))