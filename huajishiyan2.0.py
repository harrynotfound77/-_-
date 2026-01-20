import time
import gradio as gr
import numpy as np

# 后端固定输出（按你的要求：无论什么图都输出“一般”）
FIXED_RESULT = "混合程度一般"
RESULT_OPTIONS = ["混合程度良好", "混合程度一般", "混合程度较差"]

def assess_mixing(image):
    if image is None:
        return "请先上传/拍摄一张图片"
    time.sleep(1)          # 点击后加载 1s
    _ = np.mean(image)     # 占位
    return FIXED_RESULT

CUSTOM_CSS = """
:root{
  --bg: #f6f7fb;
  --card: #ffffff;
  --text: #111827;
  --muted: #6b7280;
  --border: #e5e7eb;
  --shadow: 0 8px 24px rgba(17,24,39,.08);
  --radius: 18px;
}

/* 整体背景与字体 */
.gradio-container{
  background: var(--bg) !important;
  color: var(--text);
  font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, "Apple Color Emoji","Segoe UI Emoji";
}

/* 控制页面最大宽度，让布局更像作品页 */
#page-wrap{
  max-width: 1050px;
  margin: 0 auto;
}

/* 顶部封面卡片 */
.hero{
  background: linear-gradient(135deg, #ffffff 0%, #f3f6ff 100%);
  border: 1px solid var(--border);
  box-shadow: var(--shadow);
  border-radius: var(--radius);
  padding: 22px 24px;
  margin-bottom: 16px;
}
.hero-title{
  font-size: 30px;
  font-weight: 800;
  letter-spacing: .2px;
  margin: 0 0 8px 0;
}
.hero-sub{
  margin: 0;
  color: var(--muted);
  font-size: 14px;
  line-height: 1.55;
}
.badges{
  margin-top: 12px;
  display:flex;
  gap:10px;
  flex-wrap: wrap;
}
.badge{
  font-size: 12px;
  padding: 6px 10px;
  border-radius: 999px;
  border: 1px solid var(--border);
  background: rgba(255,255,255,.7);
}

/* 卡片统一风格 */
.card{
  background: var(--card);
  border: 1px solid var(--border);
  box-shadow: var(--shadow);
  border-radius: var(--radius);
  padding: 16px;
}

/* 结果展示更醒目 */
#result_box textarea{
  font-size: 22px !important;
  font-weight: 800 !important;
  text-align: center !important;
  padding: 18px 14px !important;
  border-radius: 14px !important;
  border: 1px solid var(--border) !important;
  background: #f8fafc !important;
}

/* 主按钮美化 */
#run_btn{
  border-radius: 14px !important;
  padding: 12px 16px !important;
  font-weight: 800 !important;
}
#run_btn:hover{
  transform: translateY(-1px);
  transition: .15s ease;
}

/* Markdown 标题间距优化 */
h2{
  margin-top: 10px !important;
}
"""

def build_demo():
    with gr.Blocks(title="搅拌混合程度评价", css=CUSTOM_CSS) as demo:
        with gr.Column(elem_id="page-wrap"):
            # 顶部封面区：用 HTML 更容易排版
            gr.HTML(
                """
                <div class="hero">
                  <div class="hero-title">搅拌萃取实验 · 搅拌混合程度评价</div>
                  <p class="hero-sub">
                    领军二班 · 第一组<br/>
                    杨艺睿 / 赵诗琪 / 杨加迪 / 张扬
                  </p>
                  <div class="badges">
                    <span class="badge">上传图片 / 摄像头拍摄</span>
                    <span class="badge">1 秒评估延迟（模拟计算）</span>
                    <span class="badge">输出：良好 / 一般 / 较差</span>
                  </div>
                  <p class="hero-sub" style="margin-top:12px;">
                    请上传实验图片或调用摄像头拍摄图片，点击“开始测验”获得混合程度评价。
                  </p>
                </div>
                """
            )

            # 中间主区：左右双卡片
            with gr.Row():
                with gr.Column(scale=7):
                    with gr.Group(elem_classes=["card"]):
                        gr.Markdown("## 输入图片")
                        img_in = gr.Image(
                            sources=["upload", "webcam"],
                            type="numpy",
                            label="上传文件或摄像头拍摄"
                        )

                with gr.Column(scale=5):
                    with gr.Group(elem_classes=["card"]):
                        gr.Markdown("## 评价结果")
                        out = gr.Textbox(
                            label="",
                            placeholder="点击“开始测验”后显示结果",
                            interactive=False,
                            elem_id="result_box",
                            lines=2
                        )
                        btn = gr.Button("开始测验", elem_id="run_btn")

            btn.click(fn=assess_mixing, inputs=img_in, outputs=out)

            # 下方标准区：卡片化呈现
            with gr.Group(elem_classes=["card"]):
                gr.Markdown(
                    "## 打分标准\n"
                    "评价依据为样品在搅拌后**宏观混合均匀性**与**相分离/团聚特征**。"
                    "综合图像中颜色/灰度分布的一致性、局部浓度波动幅度，以及是否存在可见分层界面、"
                    "条带状梯度或絮团等现象进行分级：\n\n"
                    "- **混合程度良好**：整体外观均一，颜色/灰度分布连续且一致；无明显分层界面、条带状浓度梯度或块状团聚。\n"
                    "- **混合程度一般**：基本混匀但存在轻微不均一；可见局部浓度斑块、弱分层迹象或少量团聚，不均一主要局限于局部区域。\n"
                    "- **混合程度较差**：混合不充分；存在明显分层界面、显著条带状梯度或大面积团聚/絮凝，整体均匀性较低。\n"
                )

            gr.Markdown(
                "<div style='text-align:center;color:#6b7280;font-size:12px;margin-top:10px;'>"
                "© 搅拌萃取实验 · 计算机视觉辅助评价（演示版）"
                "</div>"
            )

    return demo

if __name__ == "__main__":
    demo = build_demo()
    # 本机访问更稳（摄像头权限也更不容易出问题）
    demo.launch(server_name="localhost", server_port=7860)
