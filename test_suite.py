# -*- coding: utf-8 -*-
import io
import time
import pandas as pd
from datetime import datetime
import warnings

# 忽略 pandas 的一些警告输出，保持测试报告干净
warnings.filterwarnings("ignore")

from modules.daily_report import generate_report
from modules.excel_analyzer import generate_data_summary, analyze_excel_data
from modules.excel_processor import clean_excel_data, format_excel_style
from modules.meeting_notes import extract_meeting_notes

def write_log(f, text):
    print(text)
    f.write(text + "\n")

def run_tests():
    report_filename = "test_report.txt"
    with open(report_filename, "w", encoding="utf-8") as f:
        write_log(f, "==================================================")
        write_log(f, "       AI智能办公助手 —— 自动化系统测试报告       ")
        write_log(f, f"       测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}       ")
        write_log(f, "==================================================\n")

        # ---------------------------------------------------------
        # 测试模块1：智能日报生成器
        # ---------------------------------------------------------
        write_log(f, "▶ 测试模块1：智能日报生成器 (Daily Report)")
        try:
            start_time = time.time()
            test_items = "今天修复了2个登录页面的UI Bug。"
            write_log(f, f"  [输入] 极简输入: '{test_items}'")
            write_log(f, f"  [风格] 详细说明")
            
            report_result = generate_report(test_items, "日报", "详细说明")
            cost_time = time.time() - start_time
            
            # 校验项
            has_summary = "**今日工作总结**" in report_result
            no_ai_trace = "好的" not in report_result and "为您生成" not in report_result
            
            write_log(f, f"  [结果] 耗时: {cost_time:.2f}秒")
            write_log(f, f"  [校验] 是否包含'**今日工作总结**'等强制排版? {'✅ 通过' if has_summary else '❌ 失败'}")
            write_log(f, f"  [校验] 是否消除AI痕迹(无'好的'等废话)? {'✅ 通过' if no_ai_trace else '❌ 失败'}")
            write_log(f, f"  [输出截取] \n{report_result[:150]}...\n")
        except Exception as e:
            write_log(f, f"  ❌ 模块1测试异常: {str(e)}\n")

        # ---------------------------------------------------------
        # 测试模块2：Excel智能分析
        # ---------------------------------------------------------
        write_log(f, "▶ 测试模块2：Excel智能分析 (Excel Analyzer)")
        try:
            # 构造测试数据
            df_mock = pd.DataFrame({
                '销售额': [100.5, 200.0, 300.5],
                '产品': ['A', 'B', 'A'],
                '日期': pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03'])
            })
            
            # 测试特征提取
            summary = generate_data_summary(df_mock)
            has_numeric = "数值型" in summary
            has_text = "分类/文本型" in summary
            has_date = "日期型" in summary
            write_log(f, f"  [校验] 数据特征自动提取 (数值/文本/日期识别)? {'✅ 通过' if (has_numeric and has_text and has_date) else '❌ 失败'}")
            
            # 测试大模型分析
            start_time = time.time()
            analysis_result = analyze_excel_data(df_mock, "请分析这三天的销售情况")
            cost_time = time.time() - start_time
            
            no_ai_trace = "好的" not in analysis_result and "以下是" not in analysis_result
            
            write_log(f, f"  [结果] 分析耗时: {cost_time:.2f}秒")
            write_log(f, f"  [校验] 是否消除AI痕迹并直接输出业务结论? {'✅ 通过' if no_ai_trace else '❌ 失败'}")
            write_log(f, f"  [输出截取] \n{analysis_result[:150]}...\n")
        except Exception as e:
            write_log(f, f"  ❌ 模块2测试异常: {str(e)}\n")

        # ---------------------------------------------------------
        # 测试模块3：批量Excel处理
        # ---------------------------------------------------------
        write_log(f, "▶ 测试模块3：批量Excel处理 (Batch Excel Processor)")
        try:
            # 构造包含空行和重复行的脏数据
            df_dirty = pd.DataFrame({
                '列1': [1, 2, 2, None],
                '列2': ['x', 'y', 'y', None]
            })
            
            # 写入内存文件对象
            dirty_io = io.BytesIO()
            df_dirty.to_excel(dirty_io, index=False)
            dirty_io.seek(0)
            
            # 测试数据清洗
            cleaned_io, orig_rows, clean_rows = clean_excel_data(dirty_io, "test.xlsx")
            write_log(f, f"  [校验] 数据清洗 (原行数:{orig_rows} -> 期望处理后:2, 实际:{clean_rows})? {'✅ 通过' if clean_rows == 2 else '❌ 失败'}")
            
            # 测试格式统一
            formatted_io = format_excel_style(cleaned_io)
            write_log(f, f"  [校验] 内存格式统一处理 (未抛出异常即为通过)? ✅ 通过")
            write_log(f, f"  [结果] 内存文件流大小: {len(formatted_io.getvalue())} bytes (准备提供给用户下载)\n")
        except Exception as e:
            write_log(f, f"  ❌ 模块3测试异常: {str(e)}\n")

        # ---------------------------------------------------------
        # 测试模块4：会议纪要整理
        # ---------------------------------------------------------
        write_log(f, "▶ 测试模块4：会议纪要整理 (Meeting Notes)")
        try:
            start_time = time.time()
            meeting_text = "今天开会大家同意了新版UI设计。另外李四要去推进一下服务器采购，时间没定。王五下周五前出个测试报告。"
            write_log(f, f"  [输入] 包含缺失要素的会议记录")
            
            notes_result = extract_meeting_notes(meeting_text)
            cost_time = time.time() - start_time
            
            # 校验项
            has_todo = "**待办事项**" in notes_result
            has_pending = "待定" in notes_result # 李四的时间没定，应该输出待定
            
            write_log(f, f"  [结果] 耗时: {cost_time:.2f}秒")
            write_log(f, f"  [校验] 是否包含'**待办事项**'结构? {'✅ 通过' if has_todo else '❌ 失败'}")
            write_log(f, f"  [校验] 缺失要素是否按要求处理为'待定'? {'✅ 通过' if has_pending else '❌ 失败'}")
            write_log(f, f"  [输出截取] \n{notes_result[:150]}...\n")
        except Exception as e:
            write_log(f, f"  ❌ 模块4测试异常: {str(e)}\n")

        write_log(f, "==================================================")
        write_log(f, "              测试执行完毕，结果已保存              ")
        write_log(f, "==================================================")

if __name__ == "__main__":
    run_tests()
