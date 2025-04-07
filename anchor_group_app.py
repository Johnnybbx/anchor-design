
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Anchor Layout (Adjusted Arrows)", layout="centered")
st.title("🔩 錨栓配置圖（真實比例 + 內部尺寸標註）")

st.markdown("本圖顯示錨栓於底板內的配置情形，含尺寸標註，並確保標註箭頭留在底板內部，不影響視覺。")

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

# 配置計算
fig, ax = plt.subplots()
anchor_radius = diameter / 2
total_width = (n_x - 1) * spacing_x
total_height = (n_y - 1) * spacing_y

# 錨栓起始點，置中排列
x_start = (plate_width - total_width) / 2
y_start = (plate_height - total_height) / 2

# 畫底板
plate = plt.Rectangle((0, 0), plate_width, plate_height, facecolor='lightgrey', edgecolor='black', linewidth=1.5)
ax.add_patch(plate)

# 畫錨栓
for i in range(n_y):
    for j in range(n_x):
        x = x_start + j * spacing_x
        y = y_start - i * spacing_y
        bolt = plt.Circle((x, y), anchor_radius, edgecolor='black', facecolor='white', hatch='////')
        ax.add_patch(bolt)

# 修正標註位置：放在底板內側
text_offset = 20
arrow_margin = 30

# X 方向間距標註（底板內下方）
if n_x > 1:
    x0 = x_start
    x1 = x_start + (n_x - 1) * spacing_x
    y_annot = 20
    ax.annotate("", xy=(x0, y_annot), xytext=(x1, y_annot),
                arrowprops=dict(arrowstyle='<->'))
    ax.text((x0 + x1) / 2, y_annot + text_offset, f"{spacing_x} mm", ha='center')

# Y 方向間距標註（底板內右側）
if n_y > 1:
    y0 = y_start
    y1 = y_start - (n_y - 1) * spacing_y
    x_annot = plate_width - 20
    ax.annotate("", xy=(x_annot, y0), xytext=(x_annot, y1),
                arrowprops=dict(arrowstyle='<->'))
    ax.text(x_annot + 15, (y0 + y1) / 2, f"{spacing_y} mm", va='center', rotation=90)

ax.set_aspect('equal')
ax.set_xlim(-30, plate_width + 30)
ax.set_ylim(-30, plate_height + 50)
ax.axis('off')
st.pyplot(fig)

st.caption("※ 錨栓配置與標註已優化。尺寸標註位於底板內側，避免穿出外部。")
