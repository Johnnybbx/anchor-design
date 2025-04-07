
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Anchor Layout (互動原型)", layout="wide")
st.title("🔩 錨栓配置圖原型：手動調整每段 X 向間距")

st.markdown("這是互動式距離設定原型，可於左側手動輸入每段 X 向間距，圖會即時更新。")

# 初始間距設定（使用 session state 記憶）
default_x_spacings = st.session_state.get("x_spacings", [150, 150, 150])
updated = False

# 顯示距離設定欄位
st.sidebar.header("🔧 X 向間距調整")
for i in range(len(default_x_spacings)):
    new_val = st.sidebar.number_input(f"X{i+1}-X{i+2} 間距 (mm)", min_value=10.0, value=default_x_spacings[i], step=10.0, key=f"x_gap_{i}")
    if new_val != default_x_spacings[i]:
        default_x_spacings[i] = new_val
        updated = True

# 更新 session
st.session_state["x_spacings"] = default_x_spacings

# 計算 X 座標
x_coords = [50]
for s in default_x_spacings:
    x_coords.append(x_coords[-1] + s)

# 畫圖（靜態 matplotlib 顯示錨栓 + 間距箭頭）
fig, ax = plt.subplots(figsize=(8, 4))
y_coord = 200
bolt_radius = 6

# 畫錨栓
for x in x_coords:
    bolt = plt.Circle((x, y_coord), bolt_radius, edgecolor='black', facecolor='white', hatch='////')
    ax.add_patch(bolt)

# 畫單段距離箭頭 + 數字
arrow_y = y_coord - 30
text_y = arrow_y - 10
for i in range(len(x_coords) - 1):
    x0 = x_coords[i]
    x1 = x_coords[i+1]
    x_mid = (x0 + x1) / 2
    ax.annotate("", xy=(x0, arrow_y), xytext=(x1, arrow_y), arrowprops=dict(arrowstyle='<->'))
    ax.text(x_mid, text_y, f"{x1 - x0:.0f} mm", ha='center', fontsize=8)

# 總距離箭頭
x0 = x_coords[0]
x1 = x_coords[-1]
y_total = arrow_y - 50
ax.annotate("", xy=(x0, y_total), xytext=(x1, y_total), arrowprops=dict(arrowstyle='<->'))
ax.text((x0 + x1) / 2, y_total - 10, f"{x1 - x0:.0f} mm", ha='center', fontsize=10)

ax.set_xlim(0, x_coords[-1] + 50)
ax.set_ylim(0, 300)
ax.set_aspect('equal')
ax.axis('off')
st.pyplot(fig)

st.caption("※ 後續將進階為可點擊箭頭直接輸入距離，目前為手動調整版本原型。")
