
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Anchor Layout (Spacing Label Fixed)", layout="centered")
st.title("🔩 錨栓配置工具（間距標註修正）")

st.markdown("本版本修正 X 方向間距標註文字，顯示實際段長（跨多間距），與圖形箭頭一致。")

# 輸入參數
st.sidebar.header("⚙️ 錨栓參數設定")
diameter = st.sidebar.number_input("錨栓直徑 d (mm)", 6.0, 50.0, 15.0)

st.sidebar.header("📐 錨栓配置")
n_x = st.sidebar.number_input("橫向錨栓數量（X 方向）", 1, 20, 3)
n_y = st.sidebar.number_input("縱向錨栓數量（Y 方向）", 1, 20, 2)
spacing_x = st.sidebar.number_input("X 方向間距 (mm)", 30, 1000, 300)
spacing_y = st.sidebar.number_input("Y 方向間距 (mm)", 30, 1000, 150)

st.sidebar.header("🧱 底板設定")
plate_width = st.sidebar.number_input("底版寬度 (mm)", 100, 3000, 700)
plate_height = st.sidebar.number_input("底板高度 (mm)", 100, 3000, 500)

st.sidebar.header("📏 錨栓邊距")
edge_left = st.sidebar.number_input("左邊距 (mm)", 0, 1000, 50)
edge_top = st.sidebar.number_input("上邊距 (mm)", 0, 1000, 50)

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

# 標註 X 間距（顯示總長度）
if n_x > 1:
    x0 = x_start
    x1 = x_start + (n_x - 1) * spacing_x
    y_annot = y_start - (n_y - 1) * spacing_y - 30
    span_length_x = x1 - x0
    ax.annotate("", xy=(x0, y_annot), xytext=(x1, y_annot),
                arrowprops=dict(arrowstyle='<->'))
    ax.text((x0 + x1) / 2, y_annot - 15, f"{span_length_x:.0f} mm", ha='center')

# 標註 Y 間距
if n_y > 1:
    y0 = y_start
    y1 = y_start - (n_y - 1) * spacing_y
    x_annot = plate_width - 20
    span_length_y = y0 - y1
    ax.annotate("", xy=(x_annot, y0), xytext=(x_annot, y1),
                arrowprops=dict(arrowstyle='<->'))
    ax.text(x_annot + 15, (y0 + y1) / 2, f"{span_length_y:.0f} mm", va='center', rotation=90)

ax.set_aspect('equal')
ax.set_xlim(-30, plate_width + 30)
ax.set_ylim(-30, plate_height + 50)
ax.axis('off')
st.pyplot(fig)

st.caption("※ 標註數值已更新為實際跨距段長，與箭頭位置對齊。")
