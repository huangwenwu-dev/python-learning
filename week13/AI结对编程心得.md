## 第 13 周

### 一、这周 AI 帮我最多的地方
没让它写过初稿。这周卡的主要是语法零件和环境问题（循环嵌套、f-string 花括号位置、相对路径、import 搜索起点、缩进归属），Chroma、记忆、摘要压缩这些本周正题反而没怎么卡。

### 二、⚠️ 版本坑
这周遇到两次"照着写却跑不通"，都出在版本上：

1. **`SummarizationMiddleware` 参数名新旧两套。** 网上和记忆里的写法与我装的这版对不上。处理方式：`pip show langchain` 拿到版本号，翻自己那版官方文档；更直接的是 `inspect.signature` 把参数清单直接打出来——这是硬证据，比翻网页快。
2. **`create_agent(response_format=ToolStrategy(...))` 配 `deepseek-v4-pro` 报 400**：`Thinking mode does not support this tool_choice`。原因是 ToolStrategy 把 schema 伪装成工具、用 `tool_choice` 强制调用，思考模式不支持。换 `deepseek-chat` 后跑通。这不是 LangChain 的锅，是模型侧能力差异——**同一段代码换个模型串就崩**。

**教训：AI 给的代码在版本敏感处可信度很低。** 凡是涉及具体参数名、具体模型串、具体 API 形状的地方，一律以"自己机器上跑出来的 `pip show` / `inspect.signature` / 官方文档"为准。第 12 周 DeepSeek 老模型名下线那次已经踩过一遍，这周是第二次确认。
