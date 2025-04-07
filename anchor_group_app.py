
import streamlit as st
from math import sqrt, pow

st.title("🔩 群錨錨栓設計計算工具")

st.markdown("請輸入下列參數，系統將計算單支錨栓的拉拔強度，以及整體群錨效應。")

# 使用者輸入
f_c = st.number_input("混凝土圓柱體抗壓強度 f'c (kgf/cm²)", min_value=100.0, max_value=1000.0, value=280.0)
embed_depth = st.number_input("錨栓埋入深度 hef (mm)", min_value=40.0, max_value=500.0, value=100.0)
diameter = st.number_input("錨栓直徑 d (mm)", min_value=6.0, max_value=50.0, value=12.0)
safety_factor = st.number_input("安全係數 γM", min_value=1.0, max_value=3.0, value=1.5)

st.divider()

st.subheader("📐 錨栓群設定")

anchor_spacing = st.number_input("錨栓中心間距 s (mm)", min_value=40.0, max_value=1000.0, value=150.0)
plate_width = st.number_input("底板寬度 B (mm)", min_value=100.0, max_value=3000.0, value=300.0)
plate_height = st.number_input("底板高度 H (mm)", min_value=100.0, max_value=3000.0, value=300.0)

# 計算混凝土錐體拉拔強度（以 kgf 計算）
phi_N_cb = 10 * pow(embed_depth, 1.5) * sqrt(f_c) / safety_factor  # 單位為 kgf

# 群錨配置計算
n_x = int(plate_width // anchor_spacing)
n_y = int(plate_height // anchor_spacing)
total_anchors = n_x * n_y

# 顯示結果
st.subheader("🧮 計算結果")
st.write(f"🔹 單支錨栓拉拔強度：**{phi_N_cb:.2f} kgf**")
st.write(f"🔹 錨栓配置：每行 {n_x} 支 × 每列 {n_y} 支，共 **{total_anchors} 支**")
st.write(f"🔹 群錨總拉拔強度（未考慮群效應折減）：**{phi_N_cb * total_anchors:.2f} kgf**")

st.caption("※ 群錨效應尚未考慮折減因子。詳細設計請依據規範進行。")
