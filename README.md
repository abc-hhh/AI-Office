# LocalAI-Office-Hub (企业级私有化 AI 办公自动化平台)

基于 Ollama (Qwen2.5) 与 Streamlit 构建的纯本地、零外发智能办公中台。致力于解决企业场景下大模型使用的数据隐私合规痛点，并提供自动化的 ETL 与文本结构化解析能力。

## 项目亮点

- 纯本地零风险推理：基于 Ollama 部署本地大模型引擎，实现敏感业务数据（如财务报表、内部会议记录）完全断网运行，从根本上杜绝数据外泄。
- 消除“AI痕迹”的 Prompt 工程：引入多层级 Prompt 强约束设计（Few-Shot + 角色约束），彻底解决大模型常见的过渡性废话，使生成的汇报文书可直接用于职场。
- 内存态 ETL 流水线：封装基于 Pandas 的自动化数据扫描与清洗脚本。所有 Excel 处理均在内存态（BytesIO）完成，绝对隔离并保护原始业务数据的不可篡改性。
- 企业级前端中台：利用 Streamlit 构建现代化 Web UI，实现“前端交互防呆确认 -> 后端算法调度 -> 处理结果无损导出”的完整工作流闭环。

## 核心功能模块

1. 智能工作汇报 (Smart Reporting)
   将碎片化的日常工作日志，一键转换为标准格式的日报/周报。支持动态语气调节：标准商务汇报、极简执行摘要、技术细节说明。

2. 数据智能分析 (Data Insights)
   自动扫描解析 Excel/CSV 文件，提取多维数据特征（数值极值、高频词汇）。结合大模型输出深度业务洞察，支持针对特定数据的定向提问。

3. 自动化数据清洗 (Automated ETL)
   内存级批量处理，支持脏数据清洗（空行、重复项、N/A 填充）。自动化格式规范（企业级标准字体、居中、边框、列宽自适应），生成独立防呆副本。

4. 智能会议纪要 (Meeting Summarization)
   自动解析非结构化会议文本，精准提取“会议主旨”、“核心决策”与“责任人待办任务”。具备缺失要素智能识别能力，避免 AI 幻觉与胡编乱造。

## 技术栈架构

- 前端交互: Streamlit, Custom CSS
- 核心算法: Python, Pandas, Openpyxl
- 大模型底座: LangChain, Ollama (模型: Qwen2.5-7B)

## 快速启动

1. 环境准备
确保本地已安装 Python 3.9+，并提前安装并启动 Ollama。
在终端拉取 Qwen2.5 模型：
```bash
ollama run qwen2.5:7b
```

2. 安装依赖
```bash
git clone https://github.com/你的用户名/LocalAI-Office-Hub.git
cd LocalAI-Office-Hub
pip install -r requirements.txt
```

3. 运行平台
```bash
streamlit run app.py
```
启动后，浏览器将自动打开 http://localhost:8501 进入企业级中台界面。

## 自动化系统测试

本项目内置了工程级自动化测试脚本，用于校验大模型结构化输出的稳定性以及 Pandas 数据清洗的有效性。
```bash
python test_suite.py
```
测试结果将自动生成并输出至根目录的 test_report.txt 中。
