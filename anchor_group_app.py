
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Anchor Layout (X 向標註排距調整)", layout="centered")
st.title("🔩 錨栓配置圖（X 向單段與總距離標註排距對齊 Y 向）")

st.markdown("此版本調整 X 向標註間距，使單段距離與總距離之間的上下排距與 Y 向一致。")

# 使用者參數
st.sidebar.header("⚙️ 錨栓參數設定")
diameter = st.sidebar.number_input("錨栓直徑 d (mm)", 6.0, 50.0, 15.0)

st.sidebar.header("📐 錨栓配置")
n_x = st.sidebar.number_input("橫向錨栓數量（X 方向）", 1, 20, 3)
n_y = st.sidebar.number_input("縱向錨栓數量（Y 方向）", 1, 20, 3)
spacing_x = st.sidebar.number_input("X 方向間距 (mm)", 30, 1000, 150)
spacing_y = st.sidebar.number_input("Y 方向間距 (mm)", 30, 1000, 150)

st.sidebar.header("🧱 底板設定")
plate_width = st.sidebar.number_input("底板寬度 (mm)", 100, 3000, 600)
plate_height = st.sidebar.number_input("底板高度 (mm)", 100, 3000, 600)

st.sidebar.header("📏 錨栓邊距")
edge_left = st.sidebar.number_input("左邊距 (mm)", 0, 1000, 50)
edge_top = st.sidebar.number_input("上邊距 (mm)", 0, 1000, 50)

# 標註距離參數
offset_spacing = 30  # 與錨栓距離
inter_label_gap = 30  # 單段與總距離的排距
label_fontsize = 7
label_text_offset = 10

fig, ax = plt.subplots()
anchor_radius = diameter / 2

x_start = edge_left
y_start = plate_height - edge_top

# 畫底板
plate = plt.Rectangle((0, 0), plate_width, plate_height,
                      facecolor='lightgrey', edgecolor='black', linewidth=1.5)
ax.add_patch(plate)

# 畫錨栓
for i in range(n_y):
    for j in range(n_x):
        x = x_start + j * spacing_x
        y = y_start - i * spacing_y
        bolt = plt.Circle((x, y), anchor_radius,
                          edgecolor='black', facecolor='white', hatch='////')
        ax.add_patch(bolt)

# 單段 X spacing
if n_x > 1:
    y_spacing_line = y_start - (n_y - 1) * spacing_y - offset_spacing
    for j in range(n_x - 1):
        x0 = x_start + j * spacing_x
        x1 = x_start + (j + 1) * spacing_x
        x_mid = (x0 + x1) / 2
        ax.annotate("", xy=(x0, y_spacing_line), xytext=(x1, y_spacing_line),
                    arrowprops=dict(arrowstyle='<->'))
        ax.text(x_mid, y_spacing_line - label_text_offset,
                f"{spacing_x:.0f} mm", ha='center', va='top', fontsize=label_fontsize)

# 總距離 X spacing（拉更遠一點，與單段排距拉開）
if n_x > 1:
    x0 = x_start
    x1 = x_start + (n_x - 1) * spacing_x
    y_total = y_spacing_line - inter_label_gap
    total_x = x1 - x0
    ax.annotate("", xy=(x0, y_total), xytext=(x1, y_total),
                arrowprops=dict(arrowstyle='<->'))
    ax.text((x0 + x1) / 2, y_total - label_text_offset,
            f"{total_x:.0f} mm", ha='center', va='top', fontsize=9)

# Y 向單段 spacing（不動）
if n_y > 1:
    x_spacing_line = x_start + (n_x - 1) * spacing_x + offset_spacing
    for i in range(n_y - 1):
        y0 = y_start - i * spacing_y
        y1 = y_start - (i + 1) * spacing_y
        y_mid = (y0 + y1) / 2
        ax.annotate("", xy=(x_spacing_line, y0), xytext=(x_spacing_line, y1),
                    arrowprops=dict(arrowstyle='<->'))
        ax.text(x_spacing_line + label_text_offset, y_mid,
                f"{spacing_y:.0f} mm", va='center', fontsize=label_fontsize, rotation=90)

# 總距離 Y（不動）
if n_y > 1:
    y0 = y_start
    y1 = y_start - (n_y - 1) * spacing_y
    x_total = x_spacing_line + 40
    total_y = y0 - y1
    ax.annotate("", xy=(x_total, y0), xytext=(x_total, y1), arrowprops=dict(arrowstyle='<->'))
    ax.text(x_total + label_text_offset, (y0 + y1) / 2,
            f"{total_y:.0f} mm", va='center', rotation=90, fontsize=9)

ax.set_aspect('equal')
ax.set_xlim(-30, plate_width + 100)
ax.set_ylim(-50, plate_height + 100)
ax.axis('off')
st.pyplot(fig)

st.caption("※ X 向單段與總距離標註上下排距已加大，與 Y 向保持一致。")
