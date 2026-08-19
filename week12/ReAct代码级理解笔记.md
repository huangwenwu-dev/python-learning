# ReAct 代码级理解笔记

## 测试问题
"北京现在几点了,天气怎么样?"

## 完整消息链
```
[0] HumanMessage                                   —— 用户提问
[1] AIMessage(tool_calls=[get_time, get_weather])  —— 模型决定调两个工具
[2] ToolMessage                                    —— get_time 的返回
[3] ToolMessage                                    —— get_weather 的返回
[4] AIMessage(tool_calls=[])                       —— 最终回答,循环结束
```

⚠️ 实际只有 5 条、2 轮,不是预想的 6 条 3 轮。
原因:模型在 [1] 里**一次性**提出了两个工具调用,没有分两轮查。
→ 一条 AIMessage 可以携带多个 tool_calls,消息条数和轮数不是固定比例。

## 逐轮拆解

### 第 1 轮
- **Thought**: 模型判断这个问题需要时间和天气两份数据
  - 日志证据:`[1]` 是 AIMessage,`finish_reason='tool_calls'`
  - 账单证据:`prompt_tokens: 517`(这是第一次真实调用模型)
- **Action**: 模型输出的**工具调用指令**,不是"工具跑起来"这个动作
  - 日志证据:`{'name': 'get_time', 'args': {'city': '北京'}}`
  - 日志证据:`{'name': 'get_weather', 'args': {'city': '北京'}}`
  - `'北京'` 是模型自己从问题里提取的参数
  - ⚠️ Thought 和 Action **在同一条消息里**,Action 没有独立消息,
    它就是 AIMessage 内部的 `tool_calls` 字段
  - ⚠️ 谁在执行:**模型只发指令,真正跑函数的是框架(LangGraph)**,
    跑的是我第三天自己写的 get_time / get_weather
- **Observation**: 两条 ToolMessage,是这一次决策的两份回执
  - 日志证据:`[2] content='2026-08-17 11:33:25' name='get_time'`
  - 日志证据:`[3] content='北京当前天气:晴,温度 28℃' name='get_weather'`
  - ⚠️ 谁在执行:**我的 Python 函数**。这两条没有 token_usage,
    一分钱没花,模型全程没参与
  - 这是真实数据,模型下一轮改不掉它

### 第 2 轮
- **Thought**: 两份数据都齐了,可以直接作答,不需要再调工具
  - 日志证据:`[4]` 的 `tool_calls=[]`,**空列表**
    (不是"没有这个字段",是字段在、里面一个都没有)
  - 账单证据:`prompt_tokens: 634`(第二次真实调用模型)
- **Final Answer**: 模型把时间和天气汇总成自然语言回答
  - 日志证据:`finish_reason='stop'`(第 1 轮是 `'tool_calls'`)
  - 循环为什么结束:框架每轮检查 AIMessage 里有没有 `tool_calls`,
    有就继续转,`[]` 就判定为最终回答,终止

## 我的观察

### 循环一共转了 2 轮
判断依据不是数消息条数,是数 **AIMessage 条数**。
一轮 = 模型被叫醒一次 = 一条 AIMessage = 一张 token 账单。
`[1]` `[4]` 各有一份 `token_usage` → 两次真实 API 请求 → 2 轮。
`[2]` `[3]` 是我的函数跑出来的,没有账单,不算轮。

> 类比:快递员把包裹放到门口是快递员的动作,
> 要等我开门那一下,才算我的一轮。

### prompt_tokens 从 517 涨到 634,多出的 117 是什么
**多出的 117 tokens = `[2]` 和 `[3]` 两条 ToolMessage。**
第二次调用模型时,框架把 `[0][1][2][3]` 全文重新发了一遍。
→ 这是"模型没有记忆"的代码级证据:
模型不是"记得"上一轮查到 28℃,是**又读了一遍**,117 就是重读的账单。

### 模型是怎么知道该调哪个工具的
靠第三天写的 **docstring**。框架把函数名 + docstring + 参数类型注解
打包成工具描述,随 system_prompt 发给模型。docstring 含糊,模型就选错。

---

## 异常场景:工具报错时的纠错能力

### 测试问题
"火星现在几点了,天气怎么样?"

### 消息链
```
[0] HumanMessage
[1] AIMessage(tool_calls=[get_time(火星), get_weather(火星)])  prompt_tokens: 517
[2] ToolMessage  content='2026-08-17 17:32:19'                 ← get_time 成功
[3] ToolMessage  content="错误:暂不支持查询城市'火星'的天气,
                          当前仅支持:['北京','上海','广州']"     ← get_weather 失败
[4] AIMessage(tool_calls=[])                                   prompt_tokens: 661
```

### 三个关键观察

**① 报错没有让程序崩溃**
`[3]` 的 content 是第三天在 `get_weather` 里写的那句 return,
它作为一条**正常的 ToolMessage** 流回了模型。
→ 周三"报错要 return 字符串、不要 raise"的设计今天见到回报了。
如果当初 raise,循环会直接断掉,模型连补救的机会都没有。

**② 模型读到了错误,并基于它调整了下一轮**
`[4]` 里模型说"我的天气查询工具目前只能支持北京、上海、广州这三个城市"。
⚠️ 这句话**不在我的 system_prompt 里**,是模型从 `[3]` 的错误文本里现学的。
→ 这就是 ReAct 的纠错能力,周二手动模拟过的场景,这是真实版。

**③ 部分成功也能收尾**
get_time 成了、get_weather 败了,模型没卡死,
而是"给出能给的 + 说清楚给不了的",并主动建议改查支持的城市。

### ⚠️ 但这一轮里有幻觉
`[4]` 里模型还说了火星平均气温零下 60℃、红色岩石、大气稀薄。
**日志里没有任何一条 ToolMessage 提供过这些数据**,是模型自己生成的。
→ 这条回答一半有工具证据(时间),一半没有(火星气候)。
工具能拴住的部分被拴住了,拴不住的部分照样自由发挥。

生产环境三个处理方向(第 14 周可观测性正面处理):
1. system_prompt 明确要求"工具查不到的信息不要自行补充"
2. 让工具报错信息更明确地封死追问方向
3. 对无工具证据的内容做标记 / 溯源

---

## 四个角色分工总表

| 角色 | 负责什么 | 日志里的痕迹 |
|---|---|---|
| 模型 | 决定调不调工具、调哪个、传什么参数;最后汇总答案 | AIMessage(有 token_usage) |
| 框架(LangGraph) | 执行函数、包成 ToolMessage、拼装历史、判断是否再转一轮 | 无独立消息,但决定消息顺序 |
| 我的代码 | 工具函数本体 + docstring(决定模型怎么选) | ToolMessage 的 content |
| 工具返回值 | 给模型的真实数据(模型改不掉) | ToolMessage(无 token_usage) |

## 一句话总结
**ReAct 循环的开关,就是 AIMessage 里有没有 `tool_calls`。**
有 → 执行工具 → 包成 ToolMessage → 连同全部历史重发给模型 → 下一轮
`[]` → 判定为 Final Answer → 循环结束

概念级理解让我会用,代码级理解让我会修。