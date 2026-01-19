# webui.py
# === Streamlit Cloud 终极稳定版（强制阻断 HTTP Server 监听端口）===

import os
import streamlit as st

# ==================================================
# 环境判断：Streamlit Cloud 一定存在该环境变量
# ==================================================
IS_STREAMLIT_CLOUD = os.getenv("STREAMLIT_SERVER_PORT") is not None

# ==================================================
# 【硬闸门】Cloud 环境下彻底禁用 ThreadingHTTPServer
# 任何地方、任何路径只要尝试监听端口，直接报可读错误
# ==================================================
if IS_STREAMLIT_CLOUD:
    from http.server import ThreadingHTTPServer as _THTTP

    _orig_init = _THTTP.__init__

    def _blocked_init(self, *args, **kwargs):
        raise RuntimeError(
            "HTTP Server is disabled in Streamlit Cloud environment"
        )

    _THTTP.__init__ = _blocked_init

# ==================================================
# 其余原有 import（保持）
# ==================================================
from http.server import ThreadingHTTPServer
# ⚠️ 你原来 webui.py 里的其它 import 全部照旧放在这里


# ==================================================
# UI 渲染逻辑（只允许 st.xxx，不允许监听端口）
# ==================================================

def render_ui():
    """Streamlit UI 渲染函数（Cloud / 本地通用）"""
    st.title("每日股票分析系统")
    st.caption("Cloud / 本地 / Docker 统一 UI 层")

    # TODO: 把你原来 main() 里所有 st.xxx 代码完整搬到这里


# ==================================================
# 原 HTTP Server 启动逻辑（仅本地 / Docker 使用）
# ==================================================

def _start_http_server(host, port, handler):
    server = ThreadingHTTPServer((host, port), handler)
    server.serve_forever()


# ==================================================
# 主入口（已 Cloud 安全化）
# ==================================================

def main():
    # ① 永远先画 UI
    render_ui()

    # ② Cloud 环境：立刻返回，禁止任何端口监听
    if IS_STREAMLIT_CLOUD:
        return

    # ③ 本地 / Docker：如果你需要 HTTP Server，在这里显式开启
    # 示例（按你原项目参数填写）：
    # host = "0.0.0.0"
    # port = 8000
    # handler = _Handler
    # _start_http_server(host, port, handler)


# ==================================================
# Streamlit Cloud 标准调用入口
# ==================================================

def render_webui():
    return main()


# ==================================================
# 本地 / Docker 直接运行支持
# ==================================================
if __name__ == "__main__":
    main()
