# -*- coding: utf-8 -*-
import pandas as pd
from utils.llm_client import chat

def load_data(file_obj, filename: str) -> pd.DataFrame:
    """
    根据文件后缀名加载数据，返回 Pandas DataFrame
    """
    if filename.lower().endswith('.csv'):
        return pd.read_csv(file_obj)
    else:
        return pd.read_excel(file_obj)

def generate_data_summary(df: pd.DataFrame) -> str:
    """
    自动检测 DataFrame 并生成结构化的数据统计摘要
    """
    summary = "【数据概览】\n"
    summary += f"- 总行数：{len(df)}\n- 总列数：{len(df.columns)}\n"
    summary += f"- 列名：{', '.join(df.columns.tolist())}\n\n"
    
    summary += "【字段统计详情】\n"
    for col in df.columns:
        # 判断是否为数值型
        if pd.api.types.is_numeric_dtype(df[col]):
            summary += f"- {col} (数值型): 均值={df[col].mean():.2f}, 最小值={df[col].min()}, 最大值={df[col].max()}, 中位数={df[col].median():.2f}\n"
        # 判断是否为日期型
        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            summary += f"- {col} (日期型): 起始时间={df[col].min()}, 结束时间={df[col].max()}\n"
        # 其他默认为分类/文本型
        else:
            unique_count = df[col].nunique()
            # 提取前3个最高频的值
            top_values = df[col].value_counts().head(3).to_dict()
            summary += f"- {col} (分类/文本型): 唯一值数量={unique_count}, 高频分布={top_values}\n"
            
    return summary

def analyze_excel_data(df: pd.DataFrame, user_question: str = "") -> str:
    """
    将统计摘要喂给大模型，生成数据分析结论
    """
    summary = generate_data_summary(df)
    
    system_prompt = """
你是一个资深业务数据分析师。请根据提供的数据摘要，给出专业、客观的业务分析结论。
【严格约束】
1. 语言必须高度精炼，禁止使用任何废话、过渡语或解释性的话术（严禁出现“好的”、“以下是您的分析”等）。
2. 直接输出分析结果。
3. 排版必须使用加粗短句前缀（如：**核心特征发现**：...）。
"""
    
    prompt_text = f"以下是某数据集的自动统计摘要：\n{summary}\n\n"
    
    if user_question.strip():
        prompt_text += f"【用户特别关注的问题】\n{user_question}\n\n请重点围绕上述问题进行深度分析，并给出可操作的建议。"
    else:
        prompt_text += "【分析要求】\n请提取数据中的核心特征、发现潜在规律或异常点，并给出2-3条具有商业或业务指导意义的建议。"
        
    return chat(prompt_text=prompt_text, system_prompt=system_prompt)
