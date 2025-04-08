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

# Streamlit 基本設定
st.set_page_config(page_title="Anchor Layout", layout="centered")
st.title("🔩 錨栓配置圖")
st.markdown("beta版")

# 錨栓選擇
st.sidebar.header("⚙️ 錨栓型號選擇")
selected_bolt = st.sidebar.selectbox("選擇錨栓型號", df_bolts['型號'])
selected_data = df_bolts[df_bolts['型號'] == selected_bolt].iloc[0]

# 顯示選取資訊
st.sidebar.subheader(f"選擇的錨栓型號：{selected_bolt}")
st.sidebar.write(f"螺栓直徑 (cm): {selected_data['螺栓直徑 (cm)']}")
st.sidebar.write(f"有效埋深 (cm): {selected_data['有效埋深 (cm)']}")
st.sidebar.write(f"開裂 kc: {selected_data['開裂 kc']}")
st.sidebar.write(f"非開裂 kc: {selected_data['非開裂 kc']}")
st.sidebar.write(f"kcp: {selected_data['kcp']}")
st.sidebar.write(f"τuncr (kgf/cm²): {selected_data['τuncr (2500psi)']}")
st.sidebar.write(f"τucr (kgf/cm²): {selected_data['τucr (2500psi)']}")
st.sidebar.write(f"Vsa (kgf): {selected_data['Vsa']}")

# 🧱 四角邊距（單位 cm）
st.sidebar.header("📏 四角邊距設定")
corner_offset_left = st.sidebar.number_input("左邊距 (cm)", 2.5, 100.0, 5.0)
corner_offset_top = st.sidebar.number_input("上邊距 (cm)", 2.5, 100.0, 5.0)
corner_offset_right = st.sidebar.number_input("右邊距 (cm)", 2.5, 100.0, 5.0)
corner_offset_bottom = st.sidebar.number_input("下邊距 (cm)", 2.5, 100.0, 5.0)

# 📏 間距輸入（單位 cm）
x_spacing_input = st.sidebar.text_input("X 方向間距（cm）", "15")
y_spacing_input = st.sidebar.text_input("Y 方向間距（cm）", "15")

# 轉換間距字串為數值
def parse_spacing(input_str):
    try:
        return [float(x.strip()) for x in input_str.split(",") if x.strip()]
    except:
        return []

# ✅ 轉換為 mm（實際繪圖用）
x_spacings = [x * 10 for x in parse_spacing(x_spacing_input)]
y_spacings = [y * 10 for y in parse_spacing(y_spacing_input)]
corner_offset_left *= 10
corner_offset_top *= 10
corner_offset_right *= 10
corner_offset_bottom *= 10
diameter = selected_data['螺栓直徑 (cm)'] * 10

n_x = len(x_spacings) + 1
n_y = len(y_spacings) + 1
st.sidebar.write(f"X 錨栓數量：{n_x}，Y 錨栓數量：{n_y}")

# 🧮 計算底板大小
plate_width = sum(x_spacings) + corner_offset_left + corner_offset_right
plate_height = sum(y_spacings) + corner_offset_top + corner_offset_bottom
st.sidebar.write(f"自動計算底版寬度：{plate_width / 10:.1f} cm")
st.sidebar.write(f"自動計算底版高度：{plate_height / 10:.1f} cm")

# 畫圖參數
offset_spacing = 30
label_fontsize = 7
label_text_offset = 10
inter_label_gap = 40

fig, ax = plt.subplots()
anchor_radius = diameter / 2

# 錨栓起點
x_start = corner_offset_left
y_start = plate_height - corner_offset_top

# 座標計算
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

# X spacing 單段標註
if len(x_coords) > 1:
    y_spacing_line = y_coords[-1] - offset_spacing
    for j in range(len(x_coords) - 1):
        x0, x1 = x_coords[j], x_coords[j + 1]
        x_mid = (x0 + x1) / 2
        ax.annotate("", xy=(x0, y_spacing_line), xytext=(x1, y_spacing_line), arrowprops=dict(arrowstyle='<->'))
        ax.text(x_mid, y_spacing_line - label_text_offset, f"{(x1 - x0)/10:.1f} cm", ha='center', va='top', fontsize=label_fontsize)

    # 總距離 X
    x0 = x_coords[0]
    x1 = x_coords[-1]
    y_total = y_spacing_line - inter_label_gap
    total_x = x1 - x0
    ax.annotate("", xy=(x1, y_total), xytext=(x0, y_total), arrowprops=dict(arrowstyle='<->', lw=1.5))
    ax.text((x0 + x1) / 2, y_total - label_text_offset, f"{total_x/10:.1f} cm", ha='center', va='top', fontsize=9)

# Y spacing 單段標註
if len(y_coords) > 1:
    x_spacing_line = x_coords[-1] + offset_spacing
    for i in range(len(y_coords) - 1):
        y0, y1 = y_coords[i], y_coords[i + 1]
        y_mid = (y0 + y1) / 2
        ax.annotate("", xy=(x_spacing_line, y0), xytext=(x_spacing_line, y1), arrowprops=dict(arrowstyle='<->'))
        ax.text(x_spacing_line + label_text_offset, y_mid, f"{(y0 - y1)/10:.1f} cm", va='center', fontsize=label_fontsize, rotation=90)

    # 總距離 Y
    y0 = y_coords[0]
    y1 = y_coords[-1]
    x_total = x_spacing_line + 40
    total_y = y0 - y1
    ax.annotate("", xy=(x_total, y0), xytext=(x_total, y1), arrowprops=dict(arrowstyle='<->'))
    ax.text(x_total + label_text_offset, (y0 + y1) / 2, f"{total_y/10:.1f} cm", va='center', rotation=90, fontsize=9)

# 👉 將錨栓座標轉換為形心為原點的座標系
bolt_positions = [(x, y) for y in y_coords for x in x_coords]
x_vals = [p[0] for p in bolt_positions]
y_vals = [p[1] for p in bolt_positions]
x_centroid = sum(x_vals) / len(x_vals)
y_centroid = sum(y_vals) / len(y_vals)

# ➕ 畫座標軸（紅色為 Y，藍色為 X）
ax.annotate('', xy=(x_centroid + 50, y_centroid), xytext=(x_centroid, y_centroid),
            arrowprops=dict(arrowstyle='->', color='blue', lw=2))
ax.annotate('', xy=(x_centroid, y_centroid + 50), xytext=(x_centroid, y_centroid),
            arrowprops=dict(arrowstyle='->', color='red', lw=2))
ax.text(x_centroid + 55, y_centroid - 5, 'x', color='blue', fontsize=12)
ax.text(x_centroid - 5, y_centroid + 55, 'y', color='red', fontsize=12)

# 🔵 在圖上顯示各錨栓在形心座標下的位置
for x, y in bolt_positions:
    x_local = x - x_centroid
    y_local = y - y_centroid
    ax.text(x, y + 10, f"({x_local/10:.1f}, {y_local/10:.1f})", fontsize=6, ha='center', color='black')
    
# 顯示圖
ax.set_aspect('equal')
ax.set_xlim(0, plate_width + 100)
ax.set_ylim(-100, plate_height + 100)
ax.axis('off')
st.pyplot(fig)

st.sidebar.header("📊 結構反力輸入 (單位：kgf / kgf-cm)")
uploaded_file = st.sidebar.file_uploader("請上傳含有 FX、FY、MX、MY 的 Excel 檔", type=["xlsx"])

if uploaded_file is not None:
    reaction_df = pd.read_excel(uploaded_file)

    # 顯示所有欄位與資料
    st.subheader("📄 匯入反力資料")
    st.dataframe(reaction_df)

    # 顯示單位提示
    with st.expander("📎 備註：欄位單位"):
        st.markdown("- **FX / FY**：kgf")
        st.markdown("- **MX / MY**：kgf-cm")

    # 額外說明
    st.success("反力資料已成功匯入，可開始進行錨栓受力分析！")
