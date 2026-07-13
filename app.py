# -*- coding: utf-8 -*-
import streamlit as st
import time
from modules.daily_report import generate_report

# 页面配置 (更具企业感)
st.set_page_config(
    page_title="AI 办公自动化平台",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 注入自定义 CSS 以提升企业级质感，并隐藏 Streamlit 的默认元素
st.markdown("""
<style>
    /* 隐藏 Streamlit 默认的右上角菜单和底部 Watermark */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* 调整主页面 padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 3rem;
        padding-right: 3rem;
    }
    
    /* 自定义按钮样式 */
    .stButton>button {
        border-radius: 6px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    /* 侧边栏标题样式 */
    .sidebar-title {
        font-size: 1.5rem;
        font-weight: bold;
        color: #1E3A8A;
        margin-bottom: 1rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# 侧边栏导航 (专业化命名)
st.sidebar.markdown('<div class="sidebar-title">🏢 AI Office Hub<br><span style="font-size: 0.9rem; color: #64748B;">企业级办公自动化平台</span></div>', unsafe_allow_html=True)
st.sidebar.markdown("---")

app_mode = st.sidebar.radio(
    "系统导航菜单",
    [
        "📝 智能工作汇报 (Smart Reporting)", 
        "📊 数据智能分析 (Data Insights)", 
        "🔄 自动化数据清洗 (Automated ETL)", 
        "📅 智能会议纪要 (Meeting Summarization)"
    ]
)

st.sidebar.markdown("---")
st.sidebar.caption("🔒 核心推理完全基于本地私有化部署，严格保障业务数据零泄露。")

# 主页面内容分发
if app_mode == "📝 智能工作汇报 (Smart Reporting)":
    st.header("📝 智能工作汇报系统")
    st.caption("基于本地私有化大模型，自动将碎片化工作日志转化为标准职场汇报格式。")
    st.divider()
    
    with st.form("report_form"):
        st.subheader("工作日志输入")
        items = st.text_area(
            "请输入今日/本周完成的核心工作（支持简写分点列出）：", 
            height=150, 
            placeholder="示例：\n1. 修复了系统登录页面的高频 UI 异常。\n2. 参与 Q3 产品需求评审会议。\n3. 优化数据库查询性能，降低慢查询延迟。"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            report_type = st.selectbox("报告级别", ["日报", "周报"])
        with col2:
            # 保持后端对应的 tone 字符串，但前端展示专业
            tone_mapping = {
                "标准商务汇报": "正式汇报",
                "执行摘要 (极简)": "简洁凝练",
                "技术细节说明": "详细说明"
            }
            tone_label = st.selectbox("汇报风格", list(tone_mapping.keys()))
            tone = tone_mapping[tone_label]
            
        submitted = st.form_submit_button("⚡ 执行生成任务", use_container_width=True)

    # 处理表单提交
    if submitted:
        if not items.strip():
            st.warning("⚠️ 任务中止：请输入工作日志内容后再执行。")
        else:
            with st.spinner(f"正在调用私有大模型引擎处理 {report_type}，请稍候..."):
                try:
                    start_time = time.time()
                    result = generate_report(items, report_type, tone)
                    end_time = time.time()
                    
                    st.success(f"✅ 任务完成 (计算耗时: {end_time - start_time:.2f} 秒)")
                    st.subheader("输出结果看板")
                    st.text_area("生成文本 (支持全选复制)：", result, height=350)
                    
                except Exception as e:
                    st.error(f"❌ 服务调用异常：{str(e)}")
                    st.info("💡 系统提示：请确保本地 Ollama 引擎处于运行状态。")

elif app_mode == "📊 数据智能分析 (Data Insights)":
    st.header("📊 数据智能分析引擎")
    st.caption("自动化提取多维数据特征，结合私有大模型输出深度业务洞察。")
    st.divider()
    
    uploaded_file = st.file_uploader("请上传数据集文件 (.xlsx, .xls, .csv)", type=["xlsx", "xls", "csv"])
    
    if uploaded_file is not None:
        try:
            from modules.excel_analyzer import load_data, generate_data_summary, analyze_excel_data
            
            with st.spinner("系统正在解析底层数据架构..."):
                df = load_data(uploaded_file, uploaded_file.name)
            
            st.success(f"✅ 数据集加载成功！规模: **{len(df)}** 行 × **{len(df.columns)}** 列。")
            
            with st.expander("👁️ 原始数据透视 (Top 10)", expanded=False):
                st.dataframe(df.head(10), use_container_width=True)
                
            with st.expander("📈 系统特征提取矩阵", expanded=False):
                summary_text = generate_data_summary(df)
                st.text(summary_text)
                
            st.subheader("🧠 业务洞察推演")
            user_question = st.text_input("定向分析需求（选填）", placeholder="例如：请基于上述特征，分析销售额的异常分布规律...")
            
            if st.button("⚡ 启动智能分析", use_container_width=True):
                with st.spinner("私有模型正在进行深度演算，请稍候..."):
                    start_time = time.time()
                    analysis_result = analyze_excel_data(df, user_question)
                    end_time = time.time()
                    
                    st.markdown("### 📊 分析报告")
                    st.info(analysis_result)
                    st.caption(f"⏱️ 推理耗时: {end_time - start_time:.2f} 秒")
                    
        except Exception as e:
            st.error(f"❌ 数据解析阻断：{str(e)}")

elif app_mode == "🔄 自动化数据清洗 (Automated ETL)":
    st.header("🔄 自动化数据清洗流水线")
    st.caption("在内存中执行批量表格格式化与脏数据清洗，严格保障原数据安全与不可篡改性。")
    st.divider()
    
    uploaded_files = st.file_uploader("请挂载需要处理的 Excel 文件源 (支持多选，限 .xlsx)", type=["xlsx"], accept_multiple_files=True)
    
    process_options = st.multiselect(
        "配置清洗流水线节点（可多选）",
        ["🧹 脏数据清洗 (剔除重复项、清理空行、N/A 填充)", "🎨 样式规范化 (企业级标准字体、居中、边框、列宽自适应)"],
        default=["🧹 脏数据清洗 (剔除重复项、清理空行、N/A 填充)"]
    )
    
    if uploaded_files and process_options:
        if st.button("⚡ 执行流水线处理", use_container_width=True):
            from modules.excel_processor import clean_excel_data, format_excel_style
            import io
            
            st.markdown("### 流水线执行日志")
            
            for file in uploaded_files:
                st.write(f"📄 **正在挂载处理**: `{file.name}`")
                try:
                    current_file_obj = file
                    original_rows = 0
                    cleaned_rows = 0
                    
                    if "🧹 脏数据清洗 (剔除重复项、清理空行、N/A 填充)" in process_options:
                        processed_io, original_rows, cleaned_rows = clean_excel_data(current_file_obj, file.name)
                        current_file_obj = processed_io
                        st.info(f"&nbsp;&nbsp;&nbsp;↳ [节点 1] 清洗完毕：原记录 **{original_rows}** 行 ➡️ 处理后 **{cleaned_rows}** 行 (已剔除 {original_rows - cleaned_rows} 行无效数据)")
                        
                    if "🎨 样式规范化 (企业级标准字体、居中、边框、列宽自适应)" in process_options:
                        processed_io = format_excel_style(current_file_obj)
                        current_file_obj = processed_io
                        st.info("&nbsp;&nbsp;&nbsp;↳ [节点 2] 规范化完毕：已应用企业级展示标准。")
                        
                    new_filename = file.name.replace(".xlsx", "_processed.xlsx")
                    st.download_button(
                        label=f"⬇️ 导出安全文件 ({new_filename})",
                        data=current_file_obj,
                        file_name=new_filename,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key=file.name
                    )
                except Exception as e:
                    st.error(f"❌ 文件挂载失败 {file.name}: {str(e)}")

elif app_mode == "📅 智能会议纪要 (Meeting Summarization)":
    st.header("📅 智能会议纪要提取")
    st.caption("自然语言处理引擎自动解析非结构化会议文本，精准提取核心决策与待办任务。")
    st.divider()
    
    with st.form("meeting_form"):
        meeting_text = st.text_area(
            "输入非结构化会议文本记录：", 
            height=200, 
            placeholder="示例：今天我们开会讨论了Q3的销售计划。张三提到线上渠道的预算要增加20%，大家一致同意。另外李四要在下周三前输出一份具体的预算分配表。关于线下渠道要不要收缩，大家还没定论，等下次会再定。"
        )
        
        submitted = st.form_submit_button("⚡ 启动自然语言解析", use_container_width=True)
        
    if submitted:
        if not meeting_text.strip():
            st.warning("⚠️ 任务中止：请输入文本源数据。")
        else:
            from modules.meeting_notes import extract_meeting_notes
            with st.spinner("私有 NLP 引擎正在提取关键实体，请稍候..."):
                start_time = time.time()
                try:
                    result = extract_meeting_notes(meeting_text)
                    end_time = time.time()
                    
                    st.success(f"✅ 解析完成 (计算耗时: {end_time - start_time:.2f} 秒)")
                    st.markdown("### 📝 结构化纪要看板")
                    st.info(result)
                    
                    with st.expander("纯文本代码块（供跨系统复制）"):
                        st.text_area("", result, height=250, label_visibility="collapsed")
                        
                except Exception as e:
                    st.error(f"❌ 引擎解析异常：{str(e)}")
