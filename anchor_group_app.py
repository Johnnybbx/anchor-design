
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Anchor Layout (Full Spacing Labels)", layout="centered")
st.title("🔩 錨栓配置圖（單段距離標註 / 無編號）")

st.markdown("此版本已：✅移除錨栓編號、✅補上 Y 方向單段距離、✅修正 X 向箭頭與文字重疊問題。")

# 輸入
st.sidebar.header("⚙️ 錨栓參數設定")
diameter = st.sidebar.number_input("錨栓直徑 d (mm)", 6.0, 50.0, 15.0)

st.sidebar.header("📐 錨栓配置")
n_x = st.sidebar.number_input("橫向錨栓數量（X 方向）", 1, 20, 4)
n_y = st.sidebar.number_input("縱向錨栓數量（Y 方向）", 1, 20, 3)
spacing_x = st.sidebar.number_input("X 方向間距 (mm)", 30, 1000, 150)
spacing_y = st.sidebar.number_input("Y 方向間距 (mm)", 30, 1000, 150)

st.sidebar.header("🧱 底板設定")
plate_width = st.sidebar.number_input("底版寬度 (mm)", 100, 3000, 800)
plate_height = st.sidebar.number_input("底板高度 (mm)", 100, 3000, 600)

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

# 畫錨栓（無編號）
for i in range(n_y):
    for j in range(n_x):
        x = x_start + j * spacing_x
        y = y_start - i * spacing_y
        bolt = plt.Circle((x, y), anchor_radius, edgecolor='black', facecolor='white', hatch='////')
        ax.add_patch(bolt)

# 單段 X spacing 標註（避免與總距離文字重疊）
if n_x > 1:
    y_ref = y_start - (n_y - 1) * spacing_y - 40
    for j in range(n_x - 1):
        x0 = x_start + j * spacing_x
        x1 = x_start + (j + 1) * spacing_x
        x_mid = (x0 + x1) / 2
        ax.annotate("", xy=(x0, y_ref), xytext=(x1, y_ref), arrowprops=dict(arrowstyle='<->'))
        ax.text(x_mid, y_ref - 12, f"{spacing_x:.0f} mm", ha='center', fontsize=8)

# 單段 Y spacing 標註
if n_y > 1:
    x_ref = x_start + (n_x - 1) * spacing_x + 50
    for i in range(n_y - 1):
        y0 = y_start - i * spacing_y
        y1 = y_start - (i + 1) * spacing_y
        y_mid = (y0 + y1) / 2
        ax.annotate("", xy=(x_ref, y0), xytext=(x_ref, y1), arrowprops=dict(arrowstyle='<->'))
        ax.text(x_ref + 12, y_mid, f"{spacing_y:.0f} mm", va='center', fontsize=8, rotation=90)

# 總 X 間距標註
if n_x > 1:
    x0 = x_start
    x1 = x_start + (n_x - 1) * spacing_x
    y_annot = y_start - (n_y - 1) * spacing_y - 90
    total_x = x1 - x0
    ax.annotate("", xy=(x0, y_annot), xytext=(x1, y_annot), arrowprops=dict(arrowstyle='<->'))
    ax.text((x0 + x1) / 2, y_annot - 12, f"{total_x:.0f} mm", ha='center', fontsize=10)

# 總 Y 間距標註
if n_y > 1:
    y0 = y_start
    y1 = y_start - (n_y - 1) * spacing_y
    x_annot = plate_width - 20
    total_y = y0 - y1
    ax.annotate("", xy=(x_annot, y0), xytext=(x_annot, y1), arrowprops=dict(arrowstyle='<->'))
    ax.text(x_annot + 15, (y0 + y1) / 2, f"{total_y:.0f} mm", va='center', rotation=90)

ax.set_aspect('equal')
ax.set_xlim(-30, plate_width + 80)
ax.set_ylim(-50, plate_height + 80)
ax.axis('off')
st.pyplot(fig)

st.caption("※ 顯示 X / Y 每段 spacing 間距與總長，並移除編號以提升美觀。")
