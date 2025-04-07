
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Anchor Layout with Accurate Spacing", layout="centered")
st.title("🔩 錨栓配置工具（標註位置修正）")

st.markdown("此版本修正了 X 方向間距標註位置，確保尺寸線與錨栓列正確對齊，並維持圖形真實比例。")

# 錨栓與底板設定
st.sidebar.header("⚙️ 錨栓參數設定")
diameter = st.sidebar.number_input("錨栓直徑 d (mm)", 6.0, 50.0, 15.0)

st.sidebar.header("📐 錨栓配置")
n_x = st.sidebar.number_input("橫向錨栓數量（X 方向）", 1, 20, 3)
n_y = st.sidebar.number_input("縱向錨栓數量（Y 方向）", 1, 20, 2)
spacing_x = st.sidebar.number_input("X 方向間距 (mm)", 30, 1000, 150)
spacing_y = st.sidebar.number_input("Y 方向間距 (mm)", 30, 1000, 150)

st.sidebar.header("🧱 底板設定")
plate_width = st.sidebar.number_input("底版寬度 (mm)", 100, 3000, 500)
plate_height = st.sidebar.number_input("底版高度 (mm)", 100, 3000, 400)

st.sidebar.header("📏 錨栓邊距")
edge_left = st.sidebar.number_input("左邊距 (mm)", 0, 1000, 50)
edge_top = st.sidebar.number_input("上邊距 (mm)", 0, 1000, 50)

fig, ax = plt.subplots()
anchor_radius = diameter / 2

# 起始位置計算
x_start = edge_left
y_start = plate_height - edge_top  # 向下排

# 底板
plate = plt.Rectangle((0, 0), plate_width, plate_height, facecolor='lightgrey', edgecolor='black', linewidth=1.5)
ax.add_patch(plate)

# 畫錨栓
bolt_coords = []
for i in range(n_y):
    for j in range(n_x):
        x = x_start + j * spacing_x
        y = y_start - i * spacing_y
        bolt = plt.Circle((x, y), anchor_radius, edgecolor='black', facecolor='white', hatch='////')
        ax.add_patch(bolt)
        bolt_coords.append((x, y))

# 取最下排 Y 值作為標註基準
y_last_row = y_start - (n_y - 1) * spacing_y
y_annot = y_last_row - 30

# X 間距標註
if n_x > 1:
    x0 = x_start
    x1 = x_start + (n_x - 1) * spacing_x
    ax.annotate("", xy=(x0, y_annot), xytext=(x1, y_annot),
                arrowprops=dict(arrowstyle='<->'))
    ax.text((x0 + x1) / 2, y_annot - 15, f"{spacing_x} mm", ha='center')

# Y 間距標註
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

st.caption("※ X 方向尺寸標註將依最下排錨栓動態調整位置，避免錯位或穿出。")
