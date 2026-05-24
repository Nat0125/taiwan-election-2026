# ==============================================================================
# 🏛️ HK GEOPOLITICAL REFERENDUM: THE ULTIMATE COMPREHENSIVE ENGINE (STRICT v24.0)
# ==============================================================================
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# 1. 強制設定全螢幕 RWD 網頁排版
st.set_page_config(layout="wide", page_title="香港地緣公投終極模擬系統 v24.0", page_icon="🌐")
st.title("🏛️ 香港地緣主權民意公投模擬與戰略兵棋推演系統 (v24.0)")
st.subheader("📊 雙軌獨立意向追蹤：大英歷史框架 (Option 1) vs 全面轉向 PRC/CCP 體制 (Option 2)")
st.markdown("---")

# 2. 核心大數據資料庫（橫跨 20 年數據平滑、18區真實官方人口、2015黃藍白三營陸戰兵力分佈）
raw_referendum_matrix = {
    "District": ["中西區", "灣仔區", "東區", "南區", "油尖旺區", "深水埗區", "九龍城區", "黃大仙區", "觀塘區", "葵青區", "荃灣區", "屯門區", "元朗區", "北區", "大埔區", "沙田區", "西貢區", "離島區"],
    "Population": [235100, 174800, 529600, 263200, 310600, 422400, 407900, 406800, 686500, 490500, 311800, 495300, 642300, 309600, 310900, 691000, 457400, 180100],
    "Base_Opt1_Yes": [0.54, 0.51, 0.47, 0.49, 0.51, 0.53, 0.48, 0.47, 0.43, 0.50, 0.51, 0.51, 0.41, 0.43, 0.53, 0.55, 0.54, 0.38],
    "Base_Opt2_Yes": [0.46, 0.49, 0.53, 0.51, 0.49, 0.47, 0.52, 0.53, 0.57, 0.50, 0.49, 0.49, 0.59, 0.57, 0.47, 0.45, 0.46, 0.62],
    "Region": ["香港島", "香港島", "香港島", "香港島", "九龍", "九龍", "九龍", "九龍", "九龍", "新界", "新界", "新界", "新界", "新界", "新界", "新界", "新界", "離島"],
    "Demographics": ["高級中產區", "高級中產區", "基層與閩籍", "中產南區", "商業搖擺區", "基層老區", "舊區與新發展", "傳統公屋區", "大型公屋區", "勞工公屋區", "新市鎮中產", "大西北新區", "圍村鄉事派", "邊境鄉郊區", "科學園科技中產", "全港最大新城", "將軍澳新中產", "離島鄉郊與東涌"],
    
    # 🔵 2015 建制陣營陸戰兵力（民建聯/工聯會席次總和）與「內部搶地盤互撼」密集度
    "DAB_FTU_Count": [9, 3, 17, 4, 6, 8, 9, 13, 22, 11, 6, 9, 14, 9, 6, 9, 4, 3],
    "Est_Clash_Count": [0, 0, 1, 0, 1, 1, 1, 2, 1, 2, 2, 2, 2, 3, 2, 5, 1, 0],
    "NTAS_Force": [0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 5, 12, 22, 14, 8, 15, 6, 4],
    
    # 🟢 2015 民主陣營陸戰兵力（民主黨/新同盟席次總和）與「傘兵同路人內耗」密集度
    "DP_Neo_Count": [5, 1, 3, 3, 3, 2, 4, 4, 4, 5, 4, 5, 2, 4, 5, 14, 11, 0],
    "Dem_Clash_Count": [1, 1, 1, 1, 2, 1, 2, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    
    # ⚪ 2015 第三力量（西貢方國珊專業動力、新思維）實體席次分佈
    "Third_Force_Count": [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 11, 0]
}
df_ref = pd.DataFrame(raw_referendum_matrix)

party_pro_colors = {"Democracy": "#2E7D32", "Establishment": "#01579B", "Third_Force": "#E65100"}

# 3. 側邊控制面板
st.sidebar.header("🎛️ 🟢 民主陣營（黃營）控制參數")
uk_sentiment_wave = st.sidebar.slider("🇬🇧 國際地緣風向 / 泛英情感波動 %", -20, 20, 0, step=1)
dp_neo_enthusiasm = st.sidebar.slider("🔥 民主黨+新同盟：中產與青年公投催票率 %", -15, 20, 0, step=1)
dem_clash_penalty = st.sidebar.slider("⚔️ 傘兵與泛民「同路人撞區內耗」流失率 %", 0, 10, 4, step=1)

st.sidebar.markdown("---")
st.sidebar.header("🎛️ 🔵 建制陣營（藍營）控制參數")
prc_policy_wave = st.sidebar.slider("🇨🇳 國家主權認同 / 大灣區利多加成 %", -20, 20, 0, step=1)
dab_ftu_mobilization = st.sidebar.slider("🚌 民建聯+工聯會：公屋大巴動員效率 %", -15, 20, 0, step=1)
est_clash_penalty = st.sidebar.slider("💥 建制各政黨「內部互撼搶地盤」損耗率 %", 0, 10, 3, step=1)
ntas_phone_lock = st.sidebar.slider("☎️ 新社聯：電話固票與新界圍村動員倍數", 1.0, 2.5, 1.0, step=0.1)

st.sidebar.markdown("---")
st.sidebar.header("🎛️ ⚪ 第三力量（中間派）控制參數")
third_force_leverage = st.sidebar.slider("🔸 中間派（專業動力/新思維）吸票擴散效應 %", 0, 15, 5, step=1)

# 4. 終極多維度地緣政治聯動演算核心
sim_df = df_ref.copy()

# 變數百分比與係數化轉換
wave_ratio = uk_sentiment_wave / 100.0
prc_ratio = prc_policy_wave / 100.0
dem_clash = sim_df['Dem_Clash_Count'] * (dem_clash_penalty / 100.0)
est_clash = sim_df['Est_Clash_Count'] * (est_clash_penalty / 100.0)
third_effect = sim_df['Third_Force_Count'] * (third_force_leverage / 100.0)

# 定義地緣政治遮罩
mid_class_mask = sim_df['Demographics'].isin(["高級中產區", "科學園科技中產", "將軍澳新中產", "全港最大新城"])
grassroot_mask = sim_df['Demographics'].isin(["傳統公屋區", "大型公屋區", "勞工公屋區", "基層老區"])

# A. 運算選項一（Option 1：留在英治歷史框架）最終同意率
dem_party_effect = (sim_df['DP_Neo_Count'] * 0.003) * (dp_neo_enthusiasm / 10.0)
sim_df['Final_Opt1_Yes'] = sim_df['Base_Opt1_Yes'] + wave_ratio + dem_party_effect - dem_clash - (third_effect * 0.4)
sim_df['Final_Opt1_Yes'] = sim_df['Final_Opt1_Yes'].clip(0.0, 1.0)
sim_df['Opt1_Result'] = np.where(sim_df['Final_Opt1_Yes'] > 0.50, "同意 (PASS)", "反對 (FAIL)")

# B. 運算選項二（Option 2：全面轉向 PRC/CCP 體制）最終同意率
dab_ftu_effect = (sim_df['DAB_FTU_Count'] * 0.003) * (dab_ftu_mobilization / 10.0)
ntas_effect = (sim_df['NTAS_Force'] * 0.004) * (ntas_phone_lock - 1.0)
sim_df['Final_Opt2_Yes'] = sim_df['Base_Opt2_Yes'] + prc_ratio + dab_ftu_effect + ntas_effect - est_clash - (third_effect * 0.6)
sim_df['Final_Opt2_Yes'] = sim_df['Final_Opt2_Yes'].clip(0.0, 1.0)
sim_df['Opt2_Result'] = np.where(sim_df['Final_Opt2_Yes'] > 0.50, "同意 (PASS)", "反對 (FAIL)")

# 宏觀加總
opt1_pass_count = (sim_df['Opt1_Result'] == "同意 (PASS)").sum()
opt2_pass_count = (sim_df['Opt2_Result'] == "同意 (PASS)").sum()

# ==============================================================================
# 🏙️ 網頁結構：左右雙軌完全獨立並列
# ==============================================================================
col1, col2 = st.columns([0.5, 0.5])

with col1:
    st.header("🇬🇧 Option 1: 留在英治框架公投")
    st.markdown(f"#### 🗳️ 全港總計： **{opt1_pass_count} 個行政區** 同意通過")
    
    fig_opt1 = go.Figure()
    fig_opt1.add_trace(go.Bar(
        x=sim_df['District'], y=sim_df['Final_Opt1_Yes'] * 100,
        marker_color=np.where(sim_df['Final_Opt1_Yes'] > 0.5, '#1A237E', '#B0BEC5'),
        text=(sim_df['Final_Opt1_Yes'] * 100).round(1).astype(str) + "%", textposition='auto'
    ))
    fig_opt1.add_shape(type="line", x0=-0.5, x1=17.5, y0=50, y1=50, line=dict(color="#FF1744", width=2, dash="dash"))
    fig_opt1.update_layout(template="plotly_dark", title="各行政區 Option 1 同意率 (%)", height=320, yaxis_range=[0, 100])
    st.plotly_chart(fig_opt1, use_container_width=True)

with col2:
    st.header("🇨🇳 Option 2: 轉向 PRC/CCP 體制公投")
    st.markdown(f"#### 🗳️ 全港總計： **{opt2_pass_count} 個行政區** 同意通過")
    
    fig_opt2 = go.Figure()
    fig_opt2.add_trace(go.Bar(
        x=sim_df['District'], y=sim_df['Final_Opt2_Yes'] * 100,
        marker_color=np.where(sim_df['Final_Opt2_Yes'] > 0.5, '#B71C1C', '#B0BEC5'),
        text=(sim_df['Final_Opt2_Yes'] * 100).round(1).astype(str) + "%", textposition='auto'
    ))
    fig_opt2.add_shape(type="line", x0=-0.5, x1=17.5, y0=50, y1=50, line=dict(color="#FF1744", width=2, dash="dash"))
    fig_opt2.update_layout(template="plotly_dark", title="各行政區 Option 2 同意率 (%)", height=320, yaxis_range=[0, 100])
    st.plotly_chart(fig_opt2, use_container_width=True)

st.markdown("---")
st.subheader("📋 全港 18 區雙軌主權公投詳細動態數據報表 (直向無限滾動)")

report_df = pd.DataFrame({
    "區議會行政區": sim_df['District'],
    "選民結構分類": sim_df['Demographics'],
    "民主派(黃)實體席次": sim_df['DP_Neo_Count'].astype(str) + " 席",
    "建制派(藍)實體席次": sim_df['DAB_FTU_Count'].astype(str) + " 席",
    "中間派參選人數": sim_df['Third_Force_Count'].astype(str) + " 席",
    "泛民同路人內耗": sim_df['Dem_Clash_Count'].map(lambda x: "⚠️ 嚴重撞區" if x >= 2 else ("⚡ 輕微摩擦" if x == 1 else "✅ 完美協調")),
    "建制派派系內耗": sim_df['Est_Clash_Count'].map(lambda x: "💥 互撼搶地盤" if x >= 3 else "✅ 地區協調"),
    "🇬🇧 Option 1 預估結果": sim_df['Opt1_Result'],
    "🇬🇧 Option 1 同意率": (sim_df['Final_Opt1_Yes'] * 100).round(1).astype(str) + "%",
    "🇨🇳 Option 2 預估結果": sim_df['Opt2_Result'],
    "🇨🇳 Option 2 同意率": (sim_df['Final_Opt2_Yes'] * 100).round(1).astype(str) + "%",
    "常住人口基數": sim_df['Population'].map('{:,}'.format)
})

st.dataframe(report_df, height=650, use_container_width=True, hide_index=True)


