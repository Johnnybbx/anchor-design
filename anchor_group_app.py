
import streamlit as st
from math import sqrt, pow

st.set_page_config(page_title="Anchor Design", layout="centered")
st.title("🔩 群錨錨栓設計計算工具（互動式配置）")

st.markdown("透過下方控制元件，您可以互動式調整錨栓數量、間距與底板大小，系統將即時計算群錨總拉拔強度。")

# 基本參數輸入
st.sidebar.header("⚙️ 基本參數設定")
f_c = st.sidebar.number_input("混凝土強度 f'c (kgf/cm²)", min_value=100.0, max_value=1000.0, value=280.0)
embed_depth = st.sidebar.number_input("錨栓埋入深度 hef (mm)", min_value=40.0, max_value=500.0, value=100.0)
diameter = st.sidebar.number_input("錨栓直徑 d (mm)", min_value=6.0, max_value=50.0, value=12.0)
safety_factor = st.sidebar.number_input("安全係數 γM", min_value=1.0, max_value=3.0, value=1.5)

# 底板與錨栓配置 UI
st.subheader("📐 錨栓群配置設定")

n_x = st.slider("橫向錨栓數量（X 方向）", min_value=1, max_value=10, value=2)
n_y = st.slider("縱向錨栓數量（Y 方向）", min_value=1, max_value=10, value=2)
anchor_spacing = st.slider("錨栓中心間距 s (mm)", min_value=50, max_value=500, value=150)

plate_width = (n_x - 1) * anchor_spacing + 100  # 底板寬度預設多留邊緣
plate_height = (n_y - 1) * anchor_spacing + 100

st.write(f"🔲 自動計算底板尺寸：**{plate_width} mm × {plate_height} mm**")

# 計算單錨栓拉拔強度
phi_N_cb = 10 * pow(embed_depth, 1.5) * sqrt(f_c) / safety_factor  # 單位為 kgf

# 群錨計算
total_anchors = n_x * n_y
total_capacity = phi_N_cb * total_anchors

# 結果顯示
st.subheader("🧮 計算結果")
st.write(f"🔹 單支錨栓拉拔強度：**{phi_N_cb:.2f} kgf**")
st.write(f"🔹 錨栓總數：**{total_anchors} 支**")
st.write(f"🔹 群錨總拉拔強度（未折減）：**{total_capacity:.2f} kgf**")

# 底板簡易視覺化（文字）
st.subheader("🔍 錨栓佈局預覽（示意）")
grid = ""
for _ in range(n_y):
    grid += "🔘 " * n_x + "\n"
st.text(grid)

st.caption("※ 群錨效應尚未考慮折減因子，實際設計請參考規範。")
