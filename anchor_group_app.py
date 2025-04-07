
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Anchor Layout Viewer", layout="centered")
st.title("🔩 群錨錨栓配置預覽工具（真實比例）")

st.markdown("請透過下方參數調整錨栓數量、間距與直徑，系統將自動繪製真實比例錨栓配置圖，並標註尺寸。")

# 側邊輸入區
st.sidebar.header("⚙️ 錨栓參數設定")
diameter = st.sidebar.number_input("錨栓直徑 d (mm)", 6.0, 50.0, 15.0)

st.sidebar.header("📐 配置設定")
n_x = st.sidebar.number_input("橫向錨栓數量（X 方向）", 1, 20, 3)
n_y = st.sidebar.number_input("縱向錨栓數量（Y 方向）", 1, 20, 2)
spacing_x = st.sidebar.number_input("X 方向間距 (mm)", 30, 1000, 300)
spacing_y = st.sidebar.number_input("Y 方向間距 (mm)", 30, 1000, 150)

# 計算總大小（用於畫圖範圍）
layout_width = (n_x - 1) * spacing_x
layout_height = (n_y - 1) * spacing_y

# 畫圖
st.subheader("🔍 錨栓佈局預覽（真實比例）")

fig, ax = plt.subplots()
anchor_radius = diameter / 2

for i in range(n_y):
    for j in range(n_x):
        x = j * spacing_x
        y = -i * spacing_y
        circle = plt.Circle((x, y), anchor_radius, edgecolor='black', facecolor='lightgray')
        ax.add_patch(circle)

# X 方向尺寸標註
if n_x > 1:
    x0 = 0
    x1 = (n_x - 1) * spacing_x
    y_offset = -layout_height - 40
    ax.annotate("", xy=(x0, y_offset), xytext=(x1, y_offset),
                arrowprops=dict(arrowstyle='<->'))
    ax.text((x0 + x1) / 2, y_offset - 20, f"{spacing_x} mm", ha='center')

# Y 方向尺寸標註
if n_y > 1:
    y0 = 0
    y1 = -((n_y - 1) * spacing_y)
    x_offset = x1 + 50
    ax.annotate("", xy=(x_offset, y0), xytext=(x_offset, y1),
                arrowprops=dict(arrowstyle='<->'))
    ax.text(x_offset + 20, (y0 + y1) / 2, f"{spacing_y} mm", va='center', rotation=90)

ax.set_aspect('equal')
ax.set_xlim(-50, layout_width + 100)
ax.set_ylim(-layout_height - 150, 100)
ax.axis('off')
st.pyplot(fig)

st.caption("※ 本圖為依照直徑與間距繪製之真實比例示意，未進行任何強度計算。")


st.caption("※ 配置圖依照直徑與間距真實比例繪製。尚未納入群效應折減，請依規範進行詳細設計。")
