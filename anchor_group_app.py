
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Anchor Layout (Custom Spacing)", layout="centered")
st.title("🔩 錨栓配置圖（自訂 X / Y 間距）")

st.markdown("此版本允許自訂 X / Y 方向的錨栓間距（非等距），排版與標註樣式不變。")

# 使用者參數
st.sidebar.header("⚙️ 錨栓參數設定")
diameter = st.sidebar.number_input("錨栓直徑 d (mm)", 6.0, 50.0, 15.0)

# 🆕 自訂間距輸入
st.sidebar.header("📐 錨栓間距（逗號分隔）")
x_spacing_input = st.sidebar.text_input("X 方向間距（mm）", "150,150,150")
y_spacing_input = st.sidebar.text_input("Y 方向間距（mm）", "150,150")

# 轉換字串為數值陣列
def parse_spacing(input_str):
    try:
        return [float(x.strip()) for x in input_str.split(",") if x.strip()]
    except:
        return []

x_spacings = parse_spacing(x_spacing_input)
y_spacings = parse_spacing(y_spacing_input)
n_x = len(x_spacings) + 1
n_y = len(y_spacings) + 1

st.sidebar.write(f"X 錨栓數量：{n_x}，Y 錨栓數量：{n_y}")

st.sidebar.header("🧱 底板設定")
plate_width = st.sidebar.number_input("底板寬度 (mm)", 100, 3000, 600)
plate_height = st.sidebar.number_input("底板高度 (mm)", 100, 3000, 600)

st.sidebar.header("📏 錨栓邊距")
edge_left = st.sidebar.number_input("左邊距 (mm)", 0, 1000, 50)
edge_top = st.sidebar.number_input("上邊距 (mm)", 0, 1000, 50)

# 標註距離參數
offset_spacing = 30
inter_label_gap = 40
label_fontsize = 7
label_text_offset = 10

fig, ax = plt.subplots()
anchor_radius = diameter / 2

# 座標起點
x_start = edge_left
y_start = plate_height - edge_top

# 計算每個錨栓的座標（非等距）
x_coords = [x_start]
for s in x_spacings:
    x_coords.append(x_coords[-1] + s)

y_coords = [y_start]
for s in y_spacings:
    y_coords.append(y_coords[-1] - s)

# 畫底板
plate = plt.Rectangle((0, 0), plate_width, plate_height, facecolor='lightgrey', edgecolor='black', linewidth=1.5)
ax.add_patch(plate)

# 畫錨栓
for y in y_coords:
    for x in x_coords:
        bolt = plt.Circle((x, y), anchor_radius, edgecolor='black', facecolor='white', hatch='////')
        ax.add_patch(bolt)

# 單段 X spacing 標註
if len(x_coords) > 1:
    y_spacing_line = y_coords[-1] - offset_spacing
    for j in range(len(x_coords) - 1):
        x0, x1 = x_coords[j], x_coords[j+1]
        x_mid = (x0 + x1) / 2
        ax.annotate("", xy=(x0, y_spacing_line), xytext=(x1, y_spacing_line),
                    arrowprops=dict(arrowstyle='<->'))
        ax.text(x_mid, y_spacing_line - label_text_offset,
                f"{x1 - x0:.0f} mm", ha='center', va='top', fontsize=label_fontsize)

# 總距離 X spacing
if len(x_coords) > 1:
    x0 = x_coords[0]
    x1 = x_coords[-1]
    y_total = y_spacing_line - inter_label_gap
    ax.annotate("", xy=(x0, y_total), xytext=(x1, y_total),
                arrowprops=dict(arrowstyle='<->'))
    ax.text((x0 + x1) / 2, y_total - label_text_offset,
            f"{x1 - x0:.0f} mm", ha='center', va='top', fontsize=9)

# 單段 Y spacing 標註
if len(y_coords) > 1:
    x_spacing_line = x_coords[-1] + offset_spacing
    for i in range(len(y_coords) - 1):
        y0, y1 = y_coords[i], y_coords[i+1]
        y_mid = (y0 + y1) / 2
        ax.annotate("", xy=(x_spacing_line, y0), xytext=(x_spacing_line, y1),
                    arrowprops=dict(arrowstyle='<->'))
        ax.text(x_spacing_line + label_text_offset, y_mid,
                f"{y0 - y1:.0f} mm", va='center', fontsize=label_fontsize, rotation=90)

# 總距離 Y
if len(y_coords) > 1:
    y0 = y_coords[0]
    y1 = y_coords[-1]
    x_total = x_spacing_line + 40
    ax.annotate("", xy=(x_total, y0), xytext=(x_total, y1), arrowprops=dict(arrowstyle='<->'))
    ax.text(x_total + label_text_offset, (y0 + y1) / 2,
            f"{y0 - y1:.0f} mm", va='center', rotation=90, fontsize=9)

ax.set_aspect('equal')
ax.set_xlim(-30, plate_width + 100)
ax.set_ylim(-50, plate_height + 100)
ax.axis('off')
st.pyplot(fig)

st.caption("※ 可自由輸入每段間距，系統自動生成座標與標註，排版樣式與既定一致。")
