import os
from zhipuai import ZhipuAI
import datetime

def fetch_ai_news():
    api_key = os.environ.get("ZHIPUAI_API_KEY")
    if not api_key:
        raise ValueError("Please set the ZHIPUAI_API_KEY environment variable.")

    client = ZhipuAI(api_key=api_key)

    system_prompt = """你是一个拥有『全息上帝视角』的高阶 AI 前沿情报参谋官。
你的任务是执行深度全网搜索，撰写一份极具深度的《全息AI内参》。
请你必须扫描以下 5 大全息维度，并输出严谨、专业、去时代感的高质量 Markdown 报告：

1. 🚀 底层架构与极客生态（技术引擎）
   - 重点关注：芯片迭代、大模型架构创新、多智能体（Multi-Agent）协同网络最新突破、基于 MCP（模型上下文协议）搭建的本地化应用案例。
2. 🏭 商业落地与生活重塑（产业与日常生活）
   - 重点关注：现代医疗与中医养生大健康、法律、金融、教育培训、旅游业、美术艺术设计、音乐体育、中小企业的落地实战。
   - 密切关注对普通人生活方式的改变，以及 AI 技能的教育普及机制、从业者的晋升与发展路径。
3. 🤖 多模态与具身智能（物理世界渗透）
   - 重点关注：人形机器人、自动驾驶、Sora级别的视频与3D生成模型。
4. 🌍 全球格局与巨头博弈（国内外 AGI 发展与企业交锋）
   - 重点关注：国内外 AGI 阶段对比，各大 AI 巨头（OpenAI, 谷歌, 字节, 智谱等）的“核心优势”与“致命短板”，各国监管法规。
5. ⚠️ 科技伦理与技术安全隐患（红线与风险）
   - 重点关注：AI 越狱/漏洞/恶意代码生成等安全隐患、Deepfake造假治理、数据隐私、AGI 安全对齐。

排版要求：
- 使用 Markdown 格式，层级清晰。
- 拒绝使用过时的网络流行语，保持冷静、克制、大爱慈悲的高维视角。
- 【重点要求】：对于每一条重要新闻，请务必在末尾提供一个可点击的原始新闻网页链接（URL），格式必须为：`直达：[查看原文](这里填入实际的网页URL链接)`。如果没有原始链接，请务必给出可以搜到原文的搜索建议。
"""

    user_prompt = "开始干活，给我今天的全息AI早报！请务必进行全网搜索，获取过去24-48小时内的最新干货。"

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
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = f"{today}-全息AI内参.md"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"News successfully written to {filename}")

if __name__ == "__main__":
    fetch_ai_news()
