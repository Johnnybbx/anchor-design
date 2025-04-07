
import streamlit as st
from math import sqrt, pow
import matplotlib.pyplot as plt

st.set_page_config(page_title="Anchor Design", layout="centered")
st.title("🔩 群錨錨栓設計工具（圖形化配置）")

st.markdown("透過下方控制元件，設定錨栓數量、間距與直徑，並於右側圖形中直覺預覽真實比例配置與尺寸。")

# 側邊輸入區
st.sidebar.header("⚙️ 基本參數設定")
f_c = st.sidebar.number_input("混凝土強度 f'c (kgf/cm²)", 100.0, 1000.0, 280.0)
embed_depth = st.sidebar.number_input("錨栓埋入深度 hef (mm)", 40.0, 500.0, 100.0)
diameter = st.sidebar.number_input("錨栓直徑 d (mm)", 6.0, 50.0, 12.0)
safety_factor = st.sidebar.number_input("安全係數 γM", 1.0, 3.0, 1.5)

st.sidebar.markdown("---")
st.sidebar.header("📐 錨栓群配置設定")

n_x = st.sidebar.number_input("橫向錨栓數量（X 方向）", 1, 20, 3)
n_y = st.sidebar.number_input("縱向錨栓數量（Y 方向）", 1, 20, 3)
spacing_x = st.sidebar.number_input("X 方向間距 (mm)", 30, 1000, 150)
spacing_y = st.sidebar.number_input("Y 方向間距 (mm)", 30, 1000, 150)

# 底板大小估算
plate_width = (n_x - 1) * spacing_x + 100
plate_height = (n_y - 1) * spacing_y + 100

# 計算單支錨栓拉拔強度
phi_N_cb = 10 * pow(embed_depth, 1.5) * sqrt(f_c) / safety_factor
total_anchors = n_x * n_y
total_capacity = phi_N_cb * total_anchors

# 顯示計算結果
st.subheader("🧮 計算結果")
st.write(f"🔹 單支錨栓拉拔強度：**{phi_N_cb:.2f} kgf**")
st.write(f"🔹 錨栓總數：**{total_anchors} 支**")
st.write(f"🔹 群錨總拉拔強度（未折減）：**{total_capacity:.2f} kgf**")

# 顯示圖形化配置
st.subheader("🔍 錨栓佈局預覽（真實比例）")

fig, ax = plt.subplots()
anchor_radius = diameter / 2

for i in range(n_y):
    for j in range(n_x):
        x = j * spacing_x
        y = -i * spacing_y  # 向下排列
        circle = plt.Circle((x, y), anchor_radius, edgecolor='black', facecolor='lightgray')
        ax.add_patch(circle)

# 標註尺寸線（間距）
if n_x > 1:
    ax.annotate("", xy=(0, -spacing_y*(n_y-1)-30), xytext=((n_x-1)*spacing_x, -spacing_y*(n_y-1)-30),
                arrowprops=dict(arrowstyle='<->'))
    ax.text((n_x-1)*spacing_x/2, -spacing_y*(n_y-1)-50, f"{spacing_x} mm", ha='center')

if n_y > 1:
    ax.annotate("", xy=((n_x)*spacing_x+30, 0), xytext=((n_x)*spacing_x+30, -spacing_y*(n_y-1)),
                arrowprops=dict(arrowstyle='<->'))
    ax.text((n_x)*spacing_x+40, -spacing_y*(n_y-1)/2, f"{spacing_y} mm", va='center', rotation=90)

ax.set_aspect('equal')
ax.set_xlim(-50, (n_x-1)*spacing_x + 100)
ax.set_ylim(-spacing_y*(n_y) - 100, 100)
ax.axis('off')
st.pyplot(fig)

st.caption("※ 配置圖依照直徑與間距真實比例繪製。尚未納入群效應折減，請依規範進行詳細設計。")
