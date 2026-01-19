# webui.py
# 最终版：兼容 本地 / Docker / Streamlit Cloud

import os
import streamlit as st

# ===============================
# 环境判断
# ===============================
# Streamlit Cloud 一定会注入该环境变量
IS_STREAMLIT_CLOUD = os.getenv("STREAMLIT_SERVER_PORT") is not None

# ===============================
# 你原来依赖的 import（保持不动）
# ===============================
from http.server import ThreadingHTTPServer
# 其他你原有的 import 请继续保留


# ===============================
# 原 HTTP Server 启动逻辑（仅本地/Docker用）
# ===============================

def _start_http_server(host, port, handler):
    """仅在非 Streamlit Cloud 环境启动 HTTP Server"""
    server = ThreadingHTTPServer((host, port), handler)
    server.serve_forever()


# ===============================
# UI 渲染逻辑（把你原来 main 里画 UI 的代码放这里）
# ===============================

def render_ui():
    """Streamlit UI 渲染函数（不监听端口）"""
    # ===== 下面这一段示意，请替换为你原来的 UI 代码 =====
    st.title("每日股票分析系统")
    st.caption("Streamlit Cloud / 本地 / Docker 统一 UI 层")

    # 这里继续放你原来的 st.xxx 逻辑
    # 例如：
    # st.sidebar.selectbox(...)
    # st.dataframe(...)
    # ================================================


# ===============================
# 原 main 函数（已改造）
# ===============================

def main():
    # ① 先渲染 Streamlit UI（Cloud / 本地都允许）
    render_ui()

    # ② Streamlit Cloud：禁止启动 HTTP Server
    if IS_STREAMLIT_CLOUD:
        return

    # ③ 本地 / Docker：允许启动你原来的 HTTP Server
    # ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
    # 如果你原来有 host / port / handler，请替换下面示例
    # host = "0.0.0.0"
    # port = 8000
    # handler = _Handler
    # _start_http_server(host, port, handler)
    # ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑


# ===============================
# Streamlit Cloud / 统一入口
# ===============================

def render_webui():
    """供 streamlit_app.py 调用的标准入口"""
    return main()


# ===============================
# 本地 / Docker 直接运行支持
# ===============================

if __name__ == "__main__":
    main()
