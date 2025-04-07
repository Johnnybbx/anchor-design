
import streamlit as st
import pandas as pd

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
