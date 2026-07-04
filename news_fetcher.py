import os
from zhipuai import ZhipuAI
import datetime

def fetch_ai_news():
    api_key = os.environ.get("ZHIPUAI_API_KEY")
    if not api_key:
        raise ValueError("Please set the ZHIPUAI_API_KEY environment variable.")

    client = ZhipuAI(api_key=api_key)

    system_prompt = """你是一个专门为顶级作家和前沿研究者提供写作素材的『AI 战略内参研究员』。
你的任务是执行深度全网搜索，撰写一份专供写书参考的高质量《专属AI内参》。
请你抛弃泛泛而谈的废话，只聚焦以下 4 个极具价值的核心领域，并给出深度洞察：

1. 💻 软件应用与商业前景 (Software & Prospects)
   - 发掘最新好用的 AI 应用软件，明确指出它们能解决什么具体问题。
   - 分析这些应用在未来各行各业（大健康、金融、教育等）的落地场景和发展前景。

2. ⚔️ 企业竞争与巨头动态 (Enterprise Dynamics)
   - 追踪国内外 AI 公司的竞争格局与商业交锋（如 Claude, OpenAI, 字节, 智谱等模型解禁、重磅更新）。
   - 评估公司动态对普通用户体验、付费模式或行业走向产生的实质性影响。

3. 🧬 科技突破与研发助力 (R&D & Life Sciences)
   - 关注 AI 在突破旧有科研瓶颈方面的最新进展（特别是生物科技、生命科学、医药研发领域）。
   - 追踪 AI 算力如何重塑经典文献研究和科学计算。

4. 🤖 智能体生态与多模态分级应用 (Multi-Agent Ecosystem)
   - 核心任务：深度追踪国内外（如 Coze, Dify, Claude Artifacts/Code, 字节等）在“多智能体（Multi-Agent）”和“工作流”平台上的最新应用案例。
   - 层级分析：当报道某个公司的 AI 应用时，必须明确指出它处于哪个层级（基础对话级、单点工具调用级、多智能体协同级、全自动决策级），并分析普通人或企业入局该应用的门槛和技术要求。

排版与输出要求：
- 使用 Markdown 格式，严格按照以上 4 个模块分类。
- 拒绝使用过时的网络流行语，必须保持专业、克制、深度剖析的文风。
- 【重点要求】：对于每一条重要新闻，务必在末尾提供一个可点击的原始新闻网页链接（URL），格式为：`直达：[查看原文](网页URL)`。
"""

    user_prompt = """开始干活！为了避免大模型通用搜索带来的信息遗漏，请你**必须使用 web_search 工具，分别针对以下 3 个核心关键词组进行深度搜索**，然后再汇总写报告：
1. "Claude Sonnet 模型解封 解绑 最新动态" 或者 "Anthropic 模型 限制 解除"
2. "多智能体 Multi-Agent Coze Dify 最新应用案例"
3. "AI 人工智能 生命科学 医药研发 突破 2026"

搜索完毕后，请综合所有信息，严格按照上述 4 个模块撰写今天的全息AI早报。千万不要遗漏 Claude 相关的重磅动态！"""

    print("Starting intelligence gathering with GLM-4...")
    response = client.chat.completions.create(
        model="glm-4-plus",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        tools=[{"type": "web_search", "web_search": {"enable": True, "search_result": True}}]
    )

    content = response.choices[0].message.content
    
    # Save to file
    # 强制使用北京时间 (UTC+8)，防止云端服务器 (UTC时间) 导致日期差一天
    tz_utc_8 = datetime.timezone(datetime.timedelta(hours=8))
    today = datetime.datetime.now(tz_utc_8).strftime("%Y-%m-%d")
    filename = f"{today}-全息AI内参.md"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"News successfully written to {filename}")

if __name__ == "__main__":
    fetch_ai_news()
