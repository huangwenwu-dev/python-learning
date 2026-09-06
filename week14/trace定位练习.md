## Bug 1: 摘要中间件在一次问答里压缩两次

**性质**：非人为制造，实际观测到
**现象**：一次问答 11.73 秒，其中两个 before_model 各 5.38 秒和 3.67 秒，合计占 77 %
**trace 定位过程**：
1. 看树的形状：一次问答里 before_model 出现了 2 次
2. 判断它不是空跑，因为 跑空的关卡不会调模型
3. ⭐ 点开 Input 栏确认：看到 Context Extraction Assistant / extract the highest quality/most relevant context from the
**诊断结论**：错在 SummarizationMiddleware 的 trigger 参数设置太低（2000 tokens），在带 RAG 的场景下每次调模型前都超标，
            ：证据是 before_model 出现 2 次，各挂 ChatDeepSeek（5.38s/3.67s），Input 栏为 Context Extraction Assistant 摘要提示词 → 
              两次均真实压缩，合计 9.05s 占 77%
**属于**：编排BUG，理由 因为我是从树看出来的，run 的数量不符合预期
**修复**：待定，理由 先量出带 RAG 场景下单次 messages 的典型 token 量，否则改成多少都是拍脑袋

## Bug 2: 把 Top-K 改成 1

**我改了什么**：search(query) → search(query, k=1)
**我的预测**：trace VectorStoreRetriever 的 Output 只有 1 个 Document / 回答 答一半，另一半瞎编
**测试问题**：我试用期3个月，转正后什么时候能开始休年假？
**最终表现**：回答正确
**trace 定位过程**：
1. 根节点：答案正确，但树上有 3 个 model、2 次 tools —— 一次问答不该跑三轮
2. 往下看第一次 tools：VectorStoreRetriever 的 Output 是「第一章 总则」，与「年假 转正 试用期」无关 → 模型拿到没用的资料，
   回到 Thought 换查询词重搜（ReAct 自纠）
3. ⭐ 病灶在 VectorStoreRetriever：Output 栏只有 1 个 Document（正常 3 个）→ 检索环节每次只给 1 块，是 k=1 造成的
**预测对账**：我预测 答一半+瞎编，实际 答对但多跑两轮，漏算了 ReAct 自纠
**属于**：①检索没召回（病灶在检索环节，k=1 导致单次召回不足），但被 ReAct 自纠掩盖，未表现出①的典型症状"回答说资料里没有"，
          而是转化成多轮重试——代价从"答错"变成"变慢"
**验证**：k=1 时 5.06 秒 / 3 轮模型；k=3 时 2.84 秒 / 2 轮模型；结论 修复有效（耗时降回基线水平、模型调用从 3 轮降到 2 轮、答案正确），
          但 k 不是病根
**额外发现**：万能块。查询词「年假 转正 试用期」捞回的是「第一章 总则」（内容为"本手册旨在为全体员工明确公司基本制度、岗位职责与行为规范"），
              与三个关键词均不沾边，但 k=1 和 k=3 下都排第一——第 11 周「万能块现象」的直接 trace 证据，第 14 周治分块的靶心。