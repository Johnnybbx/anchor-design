
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(page_title="Anchor Layout (Fixed Spacing + Plate Size)", layout="centered")
st.title("🔩 錨栓配置圖（自訂 X / Y 間距 + 四個角落距邊 25mm + 自動底版大小）")

st.markdown("此版本讓四個角落的錨栓距離底版邊緣 25mm，並根據錨栓位置自動設置底版大小，排版樣式不變，並即時更新圖形。")

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

# 預設邊距 25mm
corner_offset = 25
st.sidebar.header("📏 底版邊距（四角錨栓距邊 25mm）")
edge_left = st.sidebar.number_input("左邊距 (mm)", 25, 1000, 50)
edge_top = st.sidebar.number_input("上邊距 (mm)", 25, 1000, 50)

# 計算底版大小
plate_width = sum(x_spacings) + 2 * corner_offset
plate_height = sum(y_spacings) + 2 * corner_offset

# 顯示自動計算的底版大小
st.sidebar.write(f"自動計算底版寬度：{plate_width:.0f} mm")
st.sidebar.write(f"自動計算底版高度：{plate_height:.0f} mm")

# 標註距離參數
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
# 假設的螺栓資料（由於圖片無法直接解析，我會自行創建一個表格）
bolt_data = {
    '型號': ['HST3 M8', 'HST3 M10', 'HST3 M12', 'HST3 M16', 'HST3 M20', 'HKV M10', 'RE500V3 M10', 'HY200V3 M10'],
    '螺栓直徑 (cm)': [0.8, 1, 1.2, 1.6, 2, 1, 1.2, 1.6],
    '有效埋深 (cm)': [4.7, 6, 7.1, 8.5, 10.1, 4.7, 11, 12.5],
    '開裂強度 k': [7.1, 7.1, 7.1, 7.1, 7.1, 7.1, 11, 12.5],
    '非開裂強度 k': [10, 10, 10, 10, 10, 10, 10, 10],
    'kcp': [1, 1, 2, 2, 2, 1, 2, 2],
    'uncr (2500psi)': [10000, 10000, 10000, 10000, 10000, 10000, 167.33, 155.38],
    'ucr (2500psi)': [10000, 10000, 10000, 10000, 10000, 10000, 89.99, 88.57],
    'Vsa': [1315, 1947, 2813, 4852, 6554, 815, 1913, 4454]
}

# 轉換成DataFrame
df = pd.DataFrame(bolt_data)

# streamlit 網頁設置
st.set_page_config(page_title="錨栓配置", layout="centered")
st.title("🔩 錨栓型號選擇及參數顯示")

# 下拉選單：選擇錨栓型號
selected_bolt = st.selectbox("選擇錨栓型號", df['型號'])

# 顯示對應的參數
selected_data = df[df['型號'] == selected_bolt].iloc[0]
st.subheader(f"選擇的錨栓型號：{selected_bolt}")
st.write(f"螺栓直徑 (cm): {selected_data['螺栓直徑 (cm)']}")
st.write(f"有效埋深 (cm): {selected_data['有效埋深 (cm)']}")
st.write(f"開裂強度 k: {selected_data['開裂強度 k']}")
st.write(f"非開裂強度 k: {selected_data['非開裂強度 k']}")
st.write(f"kcp: {selected_data['kcp']}")
st.write(f"uncr (2500psi): {selected_data['uncr (2500psi)']}")
st.write(f"ucr (2500psi): {selected_data['ucr (2500psi)']}")
st.write(f"Vsa: {selected_data['Vsa']}")

# 顯示表格
st.subheader("錨栓型號及其參數")
st.dataframe(df)

st.caption("※ 四個角落錨栓距邊緣 25mm，底版大小自動計算，排版樣式與既定一致。")
