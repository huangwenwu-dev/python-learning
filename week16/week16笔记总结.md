# 第16周笔记总结：MCP + A2A

> 2026-10-27 ~ 2026-11-14 ｜ 第16周D7整理
> 说明：标【Claude补】的内容是 Claude 按学习记录补的，不是我当场答出来的。

**本周一句话**：让大模型通过 MCP 协议，安全地用上我自己写的工具；再了解 Agent 和 Agent 之间怎么对话（A2A）。

---

## 1. 这周做了什么

| 天 | 我的一句话 | 补充细节【Claude补】 | 主要文件 |
|---|---|---|---|
| D1 | 写了一个服务器和一个客户端，让客户端调用加法工具算出了 5 | 走 stdio：客户端亲手拉起服务器；握手（`initialize`）→ 问清单（`list_tools`）→ 下单（`call_tool`） | `server.py`、`client.py` |
| D2 | 写了一个服务器，里面有三个工具，每个都贴好了工具说明和参数说明 | 三个工具：`file_size`、`list_files`、`count_lines`；`count_lines` 的需求是我自己写的第一份需求（改了三版改对）；只准操作 `sandbox/` | `tools_server.py`、`tools_client.py`、`sandbox/` |
| D3 | 分清 MCP 资源和工具的区别 | 资源读 `../` 直接报 `Unknown resource`；同样的路径用工具版却读到了 `tools_server.py`：工具更危险，要自己把门 | `resource_server.py`、`resource_client.py` |
| D4 | 加了 `write_file` 工具；攻击脚本传 `../`，修复前成功读到了围墙外的文件，修复后被拒绝 | 修复办法：把路径检查拆成 `safe_path()`，读、写两个工具共用 | `resource_server.py`、`attack_client.py`、`攻击记录_修复前/后.txt` |
| D5 | 接入大模型（DeepSeek）来调用我写的工具 | 路线A：读到 a.txt，攻击被拒；路线B：用适配器把 MCP 工具接进 LangChain Agent，因为版本冲突另建了 `venv_b` | `agent.py`、`venv_b/` |
| D6 | 都是概念，主要分清 MCP 和 A2A 协议 | 按 A2A v1.0 写了 Agent 名片 `agent-card.json`（告诉别的 Agent "我是谁、会干什么"） | `A2A概念笔记.md`、`agent-card.json` |

---

## 2. 大白话三句

**MCP 三个角色**
- **Host（宿主）**：网店老板，带着大模型，决定要做什么
- **Client（客户端）**：老板助理，负责传话。一个助理只对接一个仓库，连三个服务器就有三个助理
- **Server（服务器）**：仓库管理员，管着工具，Client 要什么就给什么

**工具 vs 资源**
- 工具是用来干活的，资源是用来看的

**MCP vs A2A**
- MCP：Agent 连自家的数据和工具（老板 ↔ 仓库）
- A2A：Agent 和 Agent 之间，包括和外部公司的 Agent 对话（老板 ↔ 别家老板）

**路径安全**
- 防的是：有人传进来一个带 `../` 的路径，让仓库管理员跑到仓库外面去拿东西
- 怎么防：先用 `resolve()` 把路径算成真实位置，再看它在不在 sandbox 的安全范围内

```python
def safe_path(path: str) -> Path | None:
    sandbox_root = SANDBOX_DIR.resolve()           # 围墙也先算成真实位置
    target = (SANDBOX_DIR / path).resolve()        # 拼路径 + 算掉 ../
    if not target.is_relative_to(sandbox_root):    # 在不在围墙里？← ../ 在这里被拦
        return None
    return target
```

两道预测（今天答对的）：

| 传进来的 path | resolve 后 | 结果 |
|---|---|---|
| `../tools_server.py` | `...\week16\tools_server.py` | 不在围墙里 → 拒绝 |
| `sub/../a.txt` | `...\week16\sandbox\a.txt` | 在围墙里 → 放行（`sub` 不存在也不影响） |

---

## 3. 新词对照表【Claude补】

| 英文 | 中文意思 | 网店比方 |
|---|---|---|
| MCP | 模型上下文协议，大模型连工具的统一插头 | 老板和仓库之间的统一订货单 |
| stdio | 标准输入输出，用进口/出口说话 | 自己招来、坐在身边的客服 |
| HTTP | 按网址找对方 | 外包客服公司，按电话号码打过去 |
| schema | 参数格式说明书 | 下单页上要填的栏目 |
| `resolve()` | 把路径算成真实的完整路径 | 把"隔壁再往前一家"换成真实门牌号 |
| `is_relative_to()` | 是不是在某个文件夹里面 | 这个门牌在不在我们小区 |
| ToolMessage | 工具结果消息，带调用编号 | 仓库回的出库单，上面写着对应哪张订单 |
| A2A | Agent 对 Agent 的协议 | 老板和别家老板谈生意 |
| Agent Card | Agent 名片 | 店铺名片：我是谁、能干什么、怎么联系 |

---

## 4. 预测错得最记得住的三条【Claude补】

1. **D1 实验2**：我当时以为调用不存在的工具 `minus` 服务器会报错崩掉，实际服务器没崩，只在回包上贴了 `is_error=True`，真正摔倒的是 client.py 自己（对 None 取 `["result"]`）。
2. **D2 count_lines**：我当时以为 a.txt 有 4 行（VSCode 多显示了一个空的第4行），实际是 3 行：每行末尾各一个换行符，最后那个空行不算。
3. **D2 实验1**：我当时以为删掉 path 的类型注解，schema 里的 type 会消失，实际框架默认填成了 `'string'`。

共同点：都是"输出具体长什么样"没算准。

---

## 5. 环境坑：遇到什么 → 怎么解决【Claude补】

| 遇到什么 | 怎么解决 |
|---|---|
| mcp 2.3.0 把 `FastMCP` 改名成 `MCPServer`，旧导入路径 `mcp.server.fastmcp` 已删除 | 写代码前先查已装的版本（`pip show mcp`），让 Claude Code 先看源码再写 |
| D5 用的适配器只支持 mcp 1.x，和主环境的 2.3.0 冲突 | 单独建 `week16/venv_b` 装 mcp 1.30，主环境不动；`venv_b` 加进 `.gitignore` |
| stdio 服务器里 `print` 中文：Windows 走 GBK，客户端按 UTF-8 读 → UnicodeDecodeError | stdio 服务器里不要往 stdout 打印（那是通信管道）；要打印用 `print(..., file=sys.stderr)` |
| Claude Code 报 403 / Login expired；pip 装不上 | 命令行不读系统代理 → 先设 `HTTPS_PROXY` / `HTTP_PROXY`（端口 10808），再 `/login` |
| `.gitignore` 第8行 `*.txt` 把 `sandbox/a.txt` 也忽略了 | `git add -f sandbox/a.txt` 强制加入 |
| 闭卷时 VSCode 的 Quick Suggestions 显示"已在其他位置修改" | 只能去 `settings.json` 里改；改之前先截图记下原值，写完改回去 |

---

## 6. 本周闭卷 + 读码题

**阶段1 闭卷手写（读文件工具）**

| 项 | 结果 |
|---|---|
| 装饰器 `@mcp.tool()` | ✅ |
| 函数签名（`Annotated[str, Field(description=...)]` → `str`） | ✅ |
| docstring | ✅ |
| 路径检查 3 行 | ❌ 没写出来；但两道预测全对：**读得懂，写不出** |
| 返回 | ❌ 没写出来；也没想到"文件不存在"要先 `exists()` 检查、返回一句说明 |

对答案时看到 D4 写法的两处不同：
1. 路径检查单独拆成 `safe_path()`，`read_file` 和 `write_file` 共用，改一处两边都生效
2. 多一步 `if not target.exists()`：文件不存在就返回一句说明，不让程序直接报错（D2 实验3 的结论：返回说明，模型才知道原因和下一步）

**阶段2 读码题**

| 题 | 结果 |
|---|---|
| 1 客户端怎么知道有哪些工具 | 参数说明 ✅（`Field(description=...)`）/ 名称半对 / ★ `list_tools()` |
| 2 谁执行、谁打包 | ✅ |
| 3 stdio vs HTTP | 谁启动 ✅ / ★ 在哪 |
| 4 `../` 在哪被拦 | ✅ `if not target.is_relative_to(sandbox_root)` |
| 5 结果怎么回到 messages | ✅ |

★ 的正确答案：
- 第1题：客户端**主动调用 `list_tools()`** 去问服务器。工具名来自 `def` 的函数名，`@mcp.tool()` 只负责登记（挂上货架）
- 第3题：stdio 的服务器和客户端在**同一台电脑**上，是客户端拉起来的；HTTP 的服务器**在哪都行**，提前启动、一直开着，按网址找

**两道主语题（第15周D1起的老坑，这周一次答对）**
- 调用链：客户端发请求 → **框架**收下、先检查参数 → **框架**调用函数 → **函数**读文件、return → **框架**打包 → 客户端收到、喂给模型
- 工具结果回到 messages：**适配器**包成 ToolMessage（带 `tool_call_id`）→ **跑工具的节点**把它作为增量交出 → **LangGraph 框架**按 `add_messages` 合并进单子
