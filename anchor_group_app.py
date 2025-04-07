
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

# 錨栓型號及其參數
bolt_data = {
    '型號': ['HST3 M8', 'HST3 M10', 'HST3 M12', 'HST3 M16', 'HST3 M20', 'HKV M10', 
             'RE500V3 M10', 'RE500V3 M12', 'RE500V3 M16', 'HY200V3 M10', 'HY200V3 M12', 
             'HY200V3 M16', 'HY200V3 M20', 'HY200V3 M24', 'HY200V3 M27'],
    '螺栓直徑 (cm)': [0.8, 1, 1.2, 1.6, 2, 1, 1.2, 1.2, 1.6, 1, 1.2, 1.6, 2, 2.4, 2.7],
    '有效埋深 (cm)': [4.7, 6, 7.1, 8.5, 10.1, 4.7, 11, 11, 12.5, 4.7, 7.1, 8.5, 10, 10, 27],
    '開裂 kc': [7.1, 7.1, 7.1, 7.1, 7.1, 7.1, 11, 11, 11, 7.1, 7.1, 7.1, 7.1, 7.1, 7.1],
    '非開裂 kc': [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
    'kcp': [1, 1, 2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2, 2, 2],
    'τuncr (2500psi)': [10000, 10000, 10000, 10000, 10000, 10000, 167.33, 161.71, 155.38, 10000, 155.38, 156.08, 156.08, 137.87, 125.85],
    'τucr (2500psi)': [10000, 10000, 10000, 10000, 10000, 10000, 89.99, 89.99, 88.57, 10000, 88.57, 90.69, 97.02, 82.96, 82.96],
    'Vsa': [1315, 1947, 2813, 4852, 6554, 815, 1913, 4454, 635, 1913, 2134, 4454, 4454, 913, 1913]
}

df_bolts = pd.DataFrame(bolt_data)

# Streamlit 介面設置
st.set_page_config(page_title="Anchor Layout (Fixed Spacing + Plate Size)", layout="centered")
st.title("🔩 錨栓配置圖（自訂 X / Y 間距 + 四個角落距邊 25mm + 自動底版大小）")

st.markdown("此版本讓四個角落的錨栓距離底版邊緣 25mm，並根據錨栓位置自動設置底版大小，排版樣式不變，並即時更新圖形。")

# 錨栓型號選擇
st.sidebar.header("⚙️ 錨栓型號選擇")
selected_bolt = st.sidebar.selectbox("選擇錨栓型號", df_bolts['型號'])

# 顯示選擇的錨栓型號對應參數
selected_data = df_bolts[df_bolts['型號'] == selected_bolt].iloc[0]
st.sidebar.subheader(f"選擇的錨栓型號：{selected_bolt}")
st.sidebar.write(f"螺栓直徑 (cm): {selected_data['螺栓直徑 (cm)']}")
st.sidebar.write(f"有效埋深 (cm): {selected_data['有效埋深 (cm)']}")
st.sidebar.write(f"開裂 kc: {selected_data['開裂 kc']}")
st.sidebar.write(f"非開裂 kc: {selected_data['非開裂 kc']}")
st.sidebar.write(f"kcp: {selected_data['kcp']}")
st.sidebar.write(f"τuncr (2500psi): {selected_data['τuncr (2500psi)']}")
st.sidebar.write(f"τucr (2500psi): {selected_data['τucr (2500psi)']}")
st.sidebar.write(f"Vsa (kgf): {selected_data['Vsa']}")

# 使用者參數：錨栓直徑、間距設定
diameter = selected_data['螺栓直徑 (cm)'] * 10  # 改成 mm
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

# 預設邊距 25mm
corner_offset = 25
edge_left = st.sidebar.number_input("左邊距 (mm)", 25, 1000, 50)
edge_top = st.sidebar.number_input("上邊距 (mm)", 25, 1000, 50)

# 計算底版大小
plate_width = sum(x_spacings) + 2 * corner_offset
plate_height = sum(y_spacings) + 2 * corner_offset

# 顯示自動計算的底版大小
st.sidebar.write(f"自動計算底版寬度：{plate_width:.0f} mm")
st.sidebar.write(f"自動計算底版高度：{plate_height:.0f} mm")

# 畫圖設置
offset_spacing = 30
inter_label_gap = 40  # 單段與總距離的排距
label_fontsize = 7
label_text_offset = 10

fig, ax = plt.subplots()
anchor_radius = diameter / 2

# 座標起點（四角錨栓預設為距邊緣 25mm）
x_start = corner_offset
y_start = plate_height - corner_offset

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

# 標註距離參數
offset_spacing = 30
inter_label_gap = 40  # 單段與總距離的排距
label_fontsize = 7
label_text_offset = 10

# X方向、Y方向間距標註
# 單段 X spacing 標註
if len(x_coords) > 1:
    y_spacing_line = y_coords[-1] - offset_spacing
    for j in range(len(x_coords) - 1):
        x0, x1 = x_coords[j], x_coords[j+1]
        x_mid = (x0 + x1) / 2
        ax.annotate("", xy=(x0, y_spacing_line), xytext=(x1, y_spacing_line), arrowprops=dict(arrowstyle='<->'))
        ax.text(x_mid, y_spacing_line - label_text_offset, f"{x1 - x0:.0f} mm", ha='center', va='top', fontsize=label_fontsize)

# 總距離 X spacing
if len(x_coords) > 1:
    x0 = x_coords[0]
    x1 = x_coords[-1]
    y_total = y_spacing_line - inter_label_gap
    total_x = x1 - x0
    ax.annotate("", xy=(x0, y_total), xytext=(x1, y_total), arrowprops=dict(arrowstyle='<->'))
    ax.text((x0 + x1) / 2, y_total - label_text_offset, f"{total_x:.0f} mm", ha='center', va='top', fontsize=9)

# 單段 Y spacing 標註
if len(y_coords) > 1:
    x_spacing_line = x_coords[-1] + offset_spacing
    for i in range(len(y_coords) - 1):
        y0, y1 = y_coords[i], y_coords[i+1]
        y_mid = (y0 + y1) / 2
        ax.annotate("", xy=(x_spacing_line, y0), xytext=(x_spacing_line, y1), arrowprops=dict(arrowstyle='<->'))
        ax.text(x_spacing_line + label_text_offset, y_mid, f"{y0 - y1:.0f} mm", va='center', fontsize=label_fontsize, rotation=90)

# 總距離 Y
if len(y_coords) > 1:
    y0 = y_coords[0]
    y1 = y_coords[-1]
    x_total = x_spacing_line + 40
    total_y = y0 - y1
    ax.annotate("", xy=(x_total, y0), xytext=(x_total, y1), arrowprops=dict(arrowstyle='<->'))
    ax.text(x_total + label_text_offset, (y0 + y1) / 2, f"{total_y:.0f} mm", va='center', rotation=90, fontsize=9)

ax.set_aspect('equal')
ax.set_xlim(0, plate_width + 100)
ax.set_ylim(0, plate_height + 100)
ax.axis('off')
st.pyplot(fig)
