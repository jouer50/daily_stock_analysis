# streamlit_app.py
import streamlit as st

# ✅ 必须是第一条 Streamlit 命令
st.set_page_config(
    page_title="每日股票分析",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get help": None,
        "Report a Bug": None,
        "About": None,
    },
)

# ========= Streamlit Cloud 入口适配层 =========
def _call_first_existing(obj, names):
    """在模块 obj 上，按顺序找函数并调用"""
    for name in names:
        fn = getattr(obj, name, None)
        if callable(fn):
            return fn
    return None


def main():
    try:
        import webui  # 你的仓库里已经有 webui.py
    except Exception as e:
        st.error("无法导入 webui.py（依赖/路径/导入错误）")
        st.exception(e)
        st.stop()

    # 兼容不同写法：你原项目里 webui 可能叫 render_webui / main / run / app 等
    entry = _call_first_existing(
        webui,
        [
            "render_webui",  # ✅ 推荐你最终统一成这个
            "render",
            "run",
            "app",
            "main",
            "webui",
        ],
    )

    if entry is None:
        st.error("webui.py 中未找到可调用的 UI 入口函数。")
        st.info("请在 webui.py 里提供 render_webui() 或 main() 之类的函数。")
        st.stop()

    try:
        entry()
    except TypeError:
        # 有些项目把入口写成 webui.main(args) 之类，兜底提示
        st.error("找到入口函数，但调用参数不匹配。")
        st.info("请把 webui.py 的入口整理成无参函数：render_webui()")
        st.stop()
    except Exception as e:
        st.error("webui UI 渲染过程中报错（请看下方异常栈）")
        st.exception(e)
        st.stop()


if __name__ == "__main__":
    main()
