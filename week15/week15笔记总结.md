# 第15周笔记：LangGraph 入门

> 本周主线：**节点交、框架写、下一个节点读。**
> 节点只交回自己要改的那几栏（增量），合并永远是框架做的。

---

## 一、五个零件

| 零件 | 一句话 | 比喻 |
|---|---|---|
| **StateGraph**（状态图） | 组织节点和执行流程；开工前要先交给它单子模板（State 类） | 流水线，把各个工位连起来 |
| **reducer**（合并器） | 决定节点交回的新数据怎么和旧值合并 | 账本：是盖掉旧记录，还是往后追加 |
| **条件边**（Conditional Edge） | 运行时由路由函数看 State 的值，决定下一站去哪个节点 | 交通岔路口，按条件选路 |
| **checkpointer**（存档器） | 每个节点跑完就存一张整张单子的快照，可以中断后恢复 | 档案袋：每个 thread_id 一个袋子，换了 id 就是新袋子，所以"失忆" |
| **interrupt**（中断） | 暂停工作流，把问题递给外面的人，等人工回复后再继续 | 审批窗口：递出去的是问题，递回来的答案落进等号左边的变量 |

---

## 二、预测错过的三条

1. **周三（D3）summary 打印的日志**
   我当时以为：打印出来的 logs 里会有"summary 来过"。
   实际是：没有。`print` 在 `return` 之前执行，"summary 来过"要等 return 交出后才由框架合并进 State。

2. **周二（D2）stream 拍到的是什么**
   我当时以为：每次打印的是整个工作流的完整状态。
   实际是：`stream_mode="updates"` 每次打印的是当前节点交回的那一小段增量，不是完整 State。

3. **周五（D5）中断恢复**
   我当时以为：恢复时会从中断的那一行直接继续往下执行。
   实际是：中断之前已跑完的节点不重跑；包含 `interrupt()` 的节点从头重跑一遍。因为快照只在节点**跑完**后才拍，这个节点没跑完、没有它的快照。
   → 推论："真正退钱/扣款"不能放在 interrupt 之前，也不能和 interrupt 放同一个节点，要放进只有批准路才走到的独立节点。

---

## 三、周日闭卷（退款 Agent）错项

条件说明：这次在 VSCode 里写的，不是纸上；中途请 Claude 直接给了改法。题 3（interrupt）跳过。

| 我当时写的是…… | 应该是…… |
|---|---|
| `classify_refund` 没有 return | 节点要交回字典，只装要改的栏 |
| 边界写成 `== 200` / `>= 200` | `> 200`，"不超过"包含 200 |
| 路由读 `amount`，大额去 `auto_refund` | 读 `refund_type`，大额去 `manager_review` |
| 路由标 `-> int` | `-> str`，返回的是工位名 |
| `"loge"` | `"logs"`，和栏名一字不差 |
| `StateGraph(TypedDict)` | `StateGraph(RefundState)`，要传自己的蓝图 |
| `add_edge("classify-refund", ...)` | `add_conditional_edges("classify_refund", ...)`，横杠改下划线 |
| `InMemorySaver` | `InMemorySaver()`，要造出实例 |

两个预测都对：
- `amount=200` → 小额 → `auto_refund`
- logs 写成 `state["logs"] + [...]` → 旧的会重复一次（交上去的已是"旧+新"，框架再按 add 接一次）

---

## 四、读码题复习里标 ★ 的题

**★ 第5题：interrupt 递出的值、Command(resume=...) 送回的值，各被谁接住？**
- `interrupt(问题)` 的"问题"递到图外面，出现在 invoke 返回结果的 `__interrupt__` 里。
- `Command(resume=批复)` 的"批复"成为节点里 `interrupt()` 的返回值，被等号左边的变量接住（如 `answer = interrupt(...)`）。

**★ 第6题：旅行 Agent 里第2个节点从哪拿到第1个节点的结果？**
- 答案是 `"weather"` 这一栏：`check_weather` 交进 `"weather"`，`make_itinerary` 用 `state["weather"]` 读。
- 三个像的名字别混：

| 名字 | 是什么 | 比喻 |
|---|---|---|
| `check_weather` | 节点名 | 工位 |
| `"weather"` | State 栏名 | 单子上的格子 |
| `weather`（无引号） | 函数里的局部变量 | 工人手里的草稿纸，不跟单子走 |

**半对 第8题：Traceback 看哪？**
最后一行看**错误类型和原因**；摔倒的**位置**往上找离最后一行最近、指向自己文件的 `File "...", line xx`。两处一起看。

**半对 第10题：logs 被写了6次**
- 写几次：实际跑到的节点里，有几个 return 带了 `"logs"`（含投单那一次）。
- 怎么写：由 reducer（`add`）决定，是追加还是覆盖。
- 写什么：由节点的 return 决定。
- 一句话：**几次看谁交，怎么写看 add，写什么看 return。**

**待验证 第9题：用不存在的 thread_id 去 resume，框架怎么处理？**
（周五实验：thread "9" 时从 START 全新开跑，节点读不到栏 → KeyError。是否随版本变化，待破坏实验确认。）
