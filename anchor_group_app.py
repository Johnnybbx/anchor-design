
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Anchor Layout with Styled Plate", layout="centered")
st.title("🔩 錨栓配置 + 底版預覽（美化版 + 真實比例）")

st.markdown("設定錨栓數量、間距、直徑與底版尺寸，下方將繪製真實比例配置圖。包含底板灰色填色、錨栓紅色或加 hatch 樣式。")

# 輸入參數
st.sidebar.header("⚙️ 錨栓參數設定")
diameter = st.sidebar.number_input("錨栓直徑 d (mm)", 6.0, 50.0, 15.0)

st.sidebar.header("📐 錨栓配置")
n_x = st.sidebar.number_input("橫向錨栓數量（X 方向）", 1, 20, 3)
n_y = st.sidebar.number_input("縱向錨栓數量（Y 方向）", 1, 20, 2)
spacing_x = st.sidebar.number_input("X 方向間距 (mm)", 30, 1000, 150)
spacing_y = st.sidebar.number_input("Y 方向間距 (mm)", 30, 1000, 150)

st.sidebar.header("🧱 底版設定")
plate_width = st.sidebar.number_input("底版寬度 (mm)", 100, 3000, 500)
plate_height = st.sidebar.number_input("底版高度 (mm)", 100, 3000, 400)

# 錨栓配置圖
st.subheader("🔍 配置圖（含底版，真實比例 + 美化）")

fig, ax = plt.subplots()
anchor_radius = diameter / 2

# 計算錨栓整體寬高
total_width = (n_x - 1) * spacing_x
total_height = (n_y - 1) * spacing_y

# 將錨栓置中到底板中間
x_start = (plate_width - total_width) / 2
y_start = (plate_height - total_height) / 2

# 畫底板（灰色）
plate = plt.Rectangle((0, 0), plate_width, plate_height, facecolor='lightgrey', edgecolor='black', linewidth=1.5)
ax.add_patch(plate)

# 畫錨栓（紅色或 hatch）
for i in range(n_y):
    for j in range(n_x):
        x = x_start + j * spacing_x
        y = y_start - i * spacing_y
        bolt = plt.Circle((x, y), anchor_radius, edgecolor='black', facecolor='white', hatch='////')
        ax.add_patch(bolt)

# 標註 X 方向間距
if n_x > 1:
    x0 = x_start
    x1 = x_start + (n_x - 1) * spacing_x
    y_offset = -50
    ax.annotate("", xy=(x0, y_offset), xytext=(x1, y_offset),
                arrowprops=dict(arrowstyle='<->'))
    ax.text((x0 + x1) / 2, y_offset - 20, f"{spacing_x} mm", ha='center')

# 標註 Y 方向間距
if n_y > 1:
    y0 = y_start
    y1 = y_start - (n_y - 1) * spacing_y
    x_offset = plate_width + 40
    ax.annotate("", xy=(x_offset, y0), xytext=(x_offset, y1),
                arrowprops=dict(arrowstyle='<->'))
    ax.text(x_offset + 20, (y0 + y1) / 2, f"{spacing_y} mm", va='center', rotation=90)

ax.set_aspect('equal')
ax.set_xlim(-50, plate_width + 100)
ax.set_ylim(-plate_height - 100, plate_height + 100)
ax.axis('off')
st.pyplot(fig)

st.caption("※ 錨栓已置中配置於底板。底板灰色，錨栓加上斜線樣式作為視覺強調。")
