
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Anchor Layout (Unified Spacing Offset)", layout="centered")
st.title("🔩 錨栓配置圖（距離標註統一 + 無重疊）")

st.markdown("本圖統一所有標註距離與錨栓的垂直間距，並解決 X 向總距離與單段距離的重疊問題。")

# 使用者輸入參數
st.sidebar.header("⚙️ 錨栓參數設定")
diameter = st.sidebar.number_input("錨栓直徑 d (mm)", 6.0, 50.0, 15.0)

st.sidebar.header("📐 錨栓配置")
n_x = st.sidebar.number_input("橫向錨栓數量（X 方向）", 1, 20, 3)
n_y = st.sidebar.number_input("縱向錨栓數量（Y 方向）", 1, 20, 3)
spacing_x = st.sidebar.number_input("X 方向間距 (mm)", 30, 1000, 150)
spacing_y = st.sidebar.number_input("Y 方向間距 (mm)", 30, 1000, 150)

st.sidebar.header("🧱 底板設定")
plate_width = st.sidebar.number_input("底版寬度 (mm)", 100, 3000, 600)
plate_height = st.sidebar.number_input("底版高度 (mm)", 100, 3000, 600)

st.sidebar.header("📏 錨栓邊距")
edge_left = st.sidebar.number_input("左邊距 (mm)", 0, 1000, 50)
edge_top = st.sidebar.number_input("上邊距 (mm)", 0, 1000, 50)

# 固定標註箭頭與錨栓中心的距離
offset_spacing = 30  # mm

fig, ax = plt.subplots()
anchor_radius = diameter / 2

x_start = edge_left
y_start = plate_height - edge_top

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

# 單段 X spacing 標註（統一高度）
if n_x > 1:
    y_spacing_line = y_start - (n_y - 1) * spacing_y - offset_spacing
    for j in range(n_x - 1):
        x0 = x_start + j * spacing_x
        x1 = x_start + (j + 1) * spacing_x
        x_mid = (x0 + x1) / 2
        ax.annotate("", xy=(x0, y_spacing_line), xytext=(x1, y_spacing_line), arrowprops=dict(arrowstyle='<->'))
        ax.text(x_mid, y_spacing_line - 10, f"{spacing_x:.0f} mm", ha='center', fontsize=8)

# 總距離 X（拉開距離避免重疊）
if n_x > 1:
    x0 = x_start
    x1 = x_start + (n_x - 1) * spacing_x
    y_total = y_spacing_line - 2 * offset_spacing
    total_x = x1 - x0
    ax.annotate("", xy=(x0, y_total), xytext=(x1, y_total), arrowprops=dict(arrowstyle='<->'))
    ax.text((x0 + x1) / 2, y_total - 12, f"{total_x:.0f} mm", ha='center', fontsize=10)

# 單段 Y spacing 標註（統一水平位置）
if n_y > 1:
    x_spacing_line = x_start + (n_x - 1) * spacing_x + offset_spacing
    for i in range(n_y - 1):
        y0 = y_start - i * spacing_y
        y1 = y_start - (i + 1) * spacing_y
        y_mid = (y0 + y1) / 2
        ax.annotate("", xy=(x_spacing_line, y0), xytext=(x_spacing_line, y1), arrowprops=dict(arrowstyle='<->'))
        ax.text(x_spacing_line + 10, y_mid, f"{spacing_y:.0f} mm", va='center', fontsize=8, rotation=90)

# 總距離 Y（靠右一點）
if n_y > 1:
    y0 = y_start
    y1 = y_start - (n_y - 1) * spacing_y
    x_total = x_spacing_line + offset_spacing
    total_y = y0 - y1
    ax.annotate("", xy=(x_total, y0), xytext=(x_total, y1), arrowprops=dict(arrowstyle='<->'))
    ax.text(x_total + 12, (y0 + y1) / 2, f"{total_y:.0f} mm", va='center', rotation=90)

ax.set_aspect('equal')
ax.set_xlim(-30, plate_width + 100)
ax.set_ylim(-50, plate_height + 100)
ax.axis('off')
st.pyplot(fig)

st.caption("※ 單段與總距離標註已統一與錨栓距離，無交錯，排版清晰整齊。")
