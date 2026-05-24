# ==============================================================================
# 🏛️ HONG KONG GEOPOLITICAL REFERENDUM SIMULATOR: PRC/CCP FRAMEWORK (FIXED v20.6)
# ==============================================================================
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# 1. 網頁全螢幕與架構配置
st.set_page_config(layout="wide", page_title="香港主權與PRC/CCP體制公投模擬系統 v20.6", page_icon="🌐")
st.title("🏛️ 香港地緣主權民意公投模擬與戰略兵棋推演系統 (v20.6)")
st.subheader("📊 雙軌獨立意向追蹤：大英框架意向 (Option 1) vs 中華人民共和國/CCP 體制意向 (Option 2)")
st.markdown("---")

# 2. 核心大數據資料庫（【終極修復】嚴格填入香港 18 區真實常住人口，絕不留空）
raw_referendum_matrix = {
    "District": ["中西區", "灣仔區", "東區", "南區", "油尖旺區", "深水埗區", "九龍城區", "黃大仙區", "觀塘區", "葵青區", "荃灣區", "屯門區", "元朗區", "北區", "大埔區", "沙田區", "西貢區", "離島區"],
    "Population": [235100, 172600, 521200, 263100, 317100, 422000, 418700, 407000, 672000, 484700, 313100, 495000, 650000, 315000, 307000, 691000, 471000, 182000],
    "Base_Opt1_Yes": [0.55, 0.54, 0.44, 0.47, 0.49, 0.42, 0.46, 0.38, 0.35, 0.41, 0.50, 0.45, 0.34, 0.36, 0.51, 0.53, 0.52, 0.32],
    "Base_Opt2_Yes": [0.35, 0.36, 0.46, 0.43, 0.41, 0.48, 0.44, 0.52, 0.55, 0.49, 0.40, 0.45, 0.56, 0.54, 0.39, 0.37, 0.38, 0.58],
    "Region": ["香港島", "香港島", "香港島", "香港島", "九龍", "九龍", "九龍", "九龍", "九龍", "新界", "新界", "新界", "新界", "新界", "新界", "新界", "新界", "離島"],
    "Demographics": ["高級中產區", "高級中產區", "基層與閩籍", "中產南區", "商業搖擺區", "基層老區", "舊區與新發展", "傳統公屋區", "大型公屋區", "勞工公屋區", "新市鎮中產", "大西北新區", "圍村鄉事派", "邊境鄉郊區", "科學園科技中產", "全港最大新城", "將軍澳新中產", "離島鄉郊與東涌"]
}
df_ref = pd.DataFrame(raw_referendum_matrix)

# 3. 側邊控制面板
st.sidebar.header("🎛️ 選項一：留在英治歷史框架意向")
uk_sentiment_wave = st.sidebar.slider("🇬🇧 國際地緣風向 / 泛英情感波動 %", -20, 20, 0, step=1)
middle_class_turnout = st.sidebar.slider("🏙️ 都會中產與知識選民投票率倍數", 0.5, 1.5, 1.0, step=0.05)

st.sidebar.markdown("---")
st.sidebar.header("🎛️ 選項二：全面轉向 PRC/CCP 體制治理意向")
prc_regime_policy_wave = st.sidebar.slider("🇨🇳 國家主權認同 / 大灣區深化政策利多 %", -20, 20, 0, step=1)
prc_regime_mobilization = st.sidebar.slider("🚌 左派愛國社團 / 基層組織動員效率 %", -15, 20, 0, step=1)

# 4. 雙軌矩陣動態演算核心
sim_df = df_ref.copy()

# 定義地緣政治群組遮罩
mid_class_mask = sim_df['Demographics'].isin(["高級中產區", "科學園科技中產", "將軍澳新中產", "全港最大新城"])
grassroot_mask = sim_df['Demographics'].isin(["傳統公屋區", "大型公屋區", "勞工公屋區", "基層老區"])
rural_mask = sim_df['Demographics'].isin(["圍村鄉事派", "邊境鄉郊區", "離島鄉郊與東涌"])

# A. 運算選項一（Option 1）最終「同意率」
sim_df['Final_Opt1_Yes'] = sim_df['Base_Opt1_Yes'] + (uk_sentiment_wave / 100.0)
sim_df.loc[mid_class_mask, 'Final_Opt1_Yes'] += ((middle_class_turnout - 1.0) * 0.1)
sim_df['Final_Opt1_Yes'] = sim_df['Final_Opt1_Yes'].clip(0.0, 1.0)
sim_df['Opt1_Result'] = np.where(sim_df['Final_Opt1_Yes'] > 0.50, "同意 (PASS)", "反對 (FAIL)")

# B. 運算選項二（Option 2：PRC/CCP Regime Framework）最終「同意率」
sim_df['Final_Opt2_Yes'] = sim_df['Base_Opt2_Yes'] + (prc_regime_policy_wave / 100.0) + (prc_regime_mobilization * 0.3 / 100.0)
sim_df.loc[grassroot_mask, 'Final_Opt2_Yes'] += (prc_regime_mobilization * 0.2 / 100.0)
sim_df.loc[rural_mask, 'Final_Opt2_Yes'] += 0.02
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
st.subheader("📋 全港 18 區雙軌主權公投詳細動態數據報表")

report_df = pd.DataFrame({
    "區議會行政區": sim_df['District'],
    "社會人口結構分類": sim_df['Demographics'],
    "🇬🇧 Option 1 預估結果": sim_df['Opt1_Result'],
    "🇬🇧 Option 1 同意率": (sim_df['Final_Opt1_Yes'] * 100).round(1).astype(str) + "%",
    "🇨🇳 Option 2 預估結果": sim_df['Opt2_Result'],
    "🇨🇳 Option 2 同意率": (sim_df['Final_Opt2_Yes'] * 100).round(1).astype(str) + "%",
    "區域常住人口基數": sim_df['Population'].map('{:,}'.format)
})

t1, t2 = st.tabs(["🔥 全港 18 區公投總表", "🏙️ 地理分區交叉對照"])
with t1:
    st.dataframe(report_df, height=650, use_container_width=True, hide_index=True)
with t2:
    st.markdown("##### 港島/九龍都會核心區區表")
    st.dataframe(report_df[sim_df['Region'].isin(["香港島", "九龍"])], height=350, use_container_width=True, hide_index=True)
    st.markdown("##### 新界與離島偏鄉區表")
    st.dataframe(report_df[sim_df['Region'].isin(["新界", "離島"])], height=350, use_container_width=True, hide_index=True)

