# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import SystemMessage, HumanMessage

# 加载环境变量
load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME", "qwen2.5:7b")
BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
DEFAULT_TEMPERATURE = float(os.getenv("TEMPERATURE", "0.3"))

def get_llm(temperature=None):
    """获取模型实例（统一配置）"""
    return ChatOllama(
        model=MODEL_NAME, 
        base_url=BASE_URL,
        temperature=temperature if temperature is not None else DEFAULT_TEMPERATURE
    )

def chat(prompt_text: str, system_prompt: str = None, temperature: float = None) -> str:
    """通用对话函数"""
    llm = get_llm(temperature=temperature)
    if system_prompt:
        messages = [
            SystemMessage(content=system_prompt), 
            HumanMessage(content=prompt_text)
        ]
        result = llm.invoke(messages)
    else:
        result = llm.invoke(prompt_text)
    return result.content

def build_chain(template: str):
    """构建Prompt调用链"""
    llm = get_llm()
    prompt = PromptTemplate.from_template(template)
    return prompt | llm | StrOutputParser()
