# -*- coding: utf-8 -*-
from utils.llm_client import build_chain

def generate_report(items: str, report_type: str = "日报", tone: str = "正式汇报") -> str:
    """
    调用本地大模型生成智能日报/周报
    """
    # 定义不同风格的强约束指令，让大模型产生明显的差异化输出
    tone_instructions = {
        "正式汇报": "语言严谨专业，使用标准的职场书面语，适当包装业务价值与项目意义，条理清晰，适合向上级正式汇报。",
        "简洁凝练": "语言极其精简，能用词语绝不用长句。每个工作项只保留【核心动作+最终结果】，去掉所有修饰词，干脆利落。",
        "详细说明": "内容详实丰满。针对提供的每一项工作，请主动扩写其技术细节、业务背景或实现过程，字数和篇幅要明显多于另外两种风格，体现出深入的思考和充实的工作量。"
    }
    
    specific_instruction = tone_instructions.get(tone, "")

    template = """
你是一个高级职场效率专家，擅长将碎片化的工作记录转化为专业、结构化的工作汇报。
请根据以下提供的工作事项，生成一份{report_type}。

【工作事项】
{items}

【风格强约束：{tone}】
你必须严格按照以下风格指令生成内容，确保与其它风格有巨大的差异：
>>> {specific_instruction} <<<

【强制排版与基础约束】
1. 必须包含以下三个标准板块，并且使用加粗短句前缀：
   - **今日工作总结**：（或者“本周工作总结”，视报告类型而定）
   - **明日计划**：（或者“下周计划”）
   - **遇到的困难与解决方案**：（如果没有则直接写“无”）
2. 绝对禁止输出任何过渡语、寒暄语或解释性文字（例如严禁出现“好的”、“为您生成”、“以下是您的日报”、“综上所述”等），必须直接输出正文内容。
"""
    chain = build_chain(template)
    
    # 构造并调用大模型
    return chain.invoke({
        "report_type": report_type,
        "tone": tone,
        "specific_instruction": specific_instruction,
        "items": items
    })
