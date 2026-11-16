from dotenv import load_dotenv
from crewai import Agent, Crew, LLM, Task   # type: ignore

load_dotenv()

llm = LLM(model="deepseek/deepseek-v4-pro")

writer = Agent(
    role="电商文案",
    goal="写出让人想下单的商品文案",
    backstory="做过3年淘宝详情页文案，说话口语化，不堆形容词",
    llm=llm,
)

write_task = Task(
    description=(
        "给一款法兰绒毛毯写一段商品文案，有 70×100、100×150、130×150、150×200、180×200 "
        "五个尺寸，卖点是可以机洗、不掉毛"
    ),
    expected_output="一段80~120字的中文文案，不写任何促销活动、优惠、折扣信息",
    agent=writer,
)

editor = Agent(
    role="资深电商文案审核运营",
    goal="在保持原意核心卖点的前提下，把初稿打磨得更通顺、更具吸引力，并揪出所有不合规的地方",
    backstory=(
        "你是一个在电商行业摸爬滚打8年的挑剔运营，你极度注重转化和点击，"
        "眼里容不下任何语病和不痛不痒的废话"
    ),
    llm=llm,
)

edit_task = Task(
    description=(
        "拿到作者交来的毛毯文案初稿，直接修改打磨，输出终稿。"
        "要求：1）不许改变原文的核心卖点（尺寸、机洗、不掉毛这些信息必须保留）；"
        "2）不许编造任何虚假或夸大的促销信息（比如编造折扣、限时、销量数字等初稿里没有的内容）；"
        "3）终稿字数控制在80~120字；"
        "4）至少做2处实质性修改（替换说法、调整句式结构、补强卖点表达等），"
        "只把某个词换成同义词不算一处实质修改；"
        "5）真实商品信息：法兰绒毛毯，尺寸有 70×100、100×150、130×150、150×200、180×200 五种，"
        "卖点是可以机洗、不掉毛，本店目前没有任何促销活动。"
    ),
    expected_output=(
        "先给出修改后的终稿文案（80~120字）。\n"
        "然后另起一段，标题写「修改清单」，用编号列表列出每一处修改，"
        "每条格式为「序号. 原文：xxx → 改为：xxx（原因：xxx）」。"
    ),
    agent=editor,
    context=[write_task],
)

crew = Crew(agents=[writer, editor], tasks=[write_task, edit_task])

result = crew.kickoff()

print("===== 作者初稿 =====")
print(write_task.output.raw)

print("\n===== 运营终稿（含修改清单） =====")
print(edit_task.output.raw)
print(result.raw == edit_task.output.raw)
print(len(result.raw))
