# 第四周笔记：Pydantic + asyncio

## 一、Pydantic 用法速查（我要吃透的）
- 定义模型：继承 `BaseModel`，字段用**冒号**声明类型 `name: str`
- 必填 vs 可选：v2 里 `Optional[int]` **仍是必填**！要 `= None` 才真可选（**v2 大坑**）
- `Field()` 约束：`ge` / `le`（范围）、`min_length` / `max_length`（长度）
- 校验报错：抛 `ValidationError`，用 `try/except` 接；`e.errors()` 看结构化错误
- `model_validate`（进：字典/JSON → 对象）/ `model_dump`（出：对象 → 字典/JSON）
- 自定义校验器：`@field_validator` + `@classmethod`，**函数必须 `return` 值**（否则字段变 None）

## 二、异步的直觉理解（及格即可）
- 一句话：异步就是"烧水时去切菜，而不是盯着水壶干等"（我先填的比喻，可换成你自己的）
- 对 **I/O 等待**（网络请求、读文件）有用；对**纯计算**（CPU 算数）没用
- 三件套模板：`async def` 定义 → `await` 等待 → `asyncio.run()` 启动
- `gather`：`asyncio.gather()` 把多个任务**一起发出去并发等**，总耗时≈最慢那个，而不是相加
- ⚠️ 我目前不懂的地方：事件循环到底怎么调度的（先记住模板会用即可）

## 三、本周踩坑记录
- `Optional[int]` 以为可选，其实必填 → 要 `= None`
- `field_validator` 忘 `return` → 字段被悄悄改成 `None`
- `async` 函数不能直接调，要 `asyncio.run()` 或 `await`
- 跟着网上 v1 老教程写，语法对不上（认准 v2）

## 四、回头补的盲区
- 事件循环原理 → 【第 19 周回头补】