# ==============================================================================
# 🏛️ TAIWAN ELECTION QUANTITATIVE ENGINE: PURE DATA & STATS (v12.0)
# ==============================================================================
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# 1. 網頁全螢幕配置
st.set_page_config(layout="wide", page_title="台灣選戰數據中心 v12.0", page_icon="📊")
st.title("🏛️ 台灣地方大選「藍白聯合陣線」量化模擬與戰略推演系統 (v12.0)")
st.subheader("📊 核心民意因子微調與政黨席次即時推射面板")
st.markdown("---")

# 2. 核心大數據資料庫（長度嚴格對齊 22 縣市）
raw_master_data = {
    "County": ["基隆市", "臺北市", "新北市", "桃園市", "新竹市", "新竹縣", "苗栗縣", "臺中市", "彰化縣", "南投縣", "雲林縣", "嘉義市", "嘉義縣", "臺南市", "高雄市", "屏東縣", "宜蘭縣", "花蓮縣", "臺東縣", "澎湖縣", "金門縣", "連江縣"],
    "Population": [360000, 2500000, 4000000, 2300000, 450000, 580000, 530000, 2800000, 1240000, 480000, 660000, 260000, 490000, 1850000, 2730000, 790000, 450000, 320000, 210000, 100000, 140000, 140000],
    "Base_KMT": [0.48, 0.45, 0.44, 0.42, 0.28, 0.48, 0.50, 0.42, 0.44, 0.48, 0.38, 0.45, 0.32, 0.31, 0.33, 0.35, 0.42, 0.56, 0.57, 0.42, 0.68, 0.75],
    "Base_DPP": [0.36, 0.35, 0.36, 0.34, 0.28, 0.24, 0.24, 0.34, 0.38, 0.34, 0.46, 0.40, 0.52, 0.53, 0.52, 0.49, 0.41, 0.22, 0.21, 0.43, 0.07, 0.03],
    "Base_TPP": [0.16, 0.20, 0.20, 0.24, 0.44, 0.28, 0.26, 0.24, 0.18, 0.18, 0.16, 0.15, 0.16, 0.16, 0.15, 0.16, 0.17, 0.22, 0.22, 0.15, 0.25, 0.22],
    "Is_Six_Metro": [0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    "Is_Swing_Zone": [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
}
df_master = pd.DataFrame(raw_master_data)

party_pro_colors = {"KMT_TPP": "#5E35B1", "DPP": "#2E7D32"}

# 3. 側邊控制面板
st.sidebar.header("🎛️ 戰情室核心因子控制台")
coalition_efficiency = st.sidebar.slider("🤝 藍白整合轉移效率 % (選票集中度)", 40, 100, 75, step=5)
dpp_counter_mobilization = st.sidebar.slider("🟢 民進黨傳統基本盤危機催票率 %", -10, 15, 8, step=1)
middle_voter_drift = st.sidebar.slider("🔸 中間選民體制抗衡偏好 (正值利藍白)", -15, 15, -2, step=1)
young_turnout_weight = st.sidebar.slider("👥 科技城/青年投票率震盪倍數", 0.5, 1.5, 0.95, step=0.05)

# 4. 聯動演算核心
sim_df = df_master.copy()

# 綠營催票與藍白整合公式
sim_df['Final_DPP'] = sim_df['Base_DPP'] + (dpp_counter_mobilization * 0.4 / 100.0)
south_mask = sim_df['County'].isin(["臺南市", "高雄市", "屏東縣", "嘉義縣"])
sim_df.loc[south_mask, 'Final_DPP'] += (dpp_counter_mobilization * 0.15 / 100.0)

eff_ratio = coalition_efficiency / 100.0
sim_df['Combined_Opposition'] = (sim_df['Base_KMT'] + (sim_df['Base_TPP'] * young_turnout_weight)) * eff_ratio
sim_df['Combined_Opposition'] += (middle_voter_drift * 0.5 / 100.0)

north_kmt_stronghold = sim_df['County'].isin(["基隆市", "臺北市", "新北市", "新竹縣", "苗栗縣"])
sim_df.loc[north_kmt_stronghold, 'Combined_Opposition'] += 0.03

# 標準化歸一處理
total_pool = sim_df['Combined_Opposition'] + sim_df['Final_DPP']
sim_df['Final_Blue_White'] = sim_df['Combined_Opposition'] / total_pool
sim_df['Final_DPP'] /= total_pool

# 勝負判定
sim_df['Winner'] = np.where(sim_df['Final_Blue_White'] > sim_df['Final_DPP'], 'KMT_TPP', 'DPP')

calc_seats = sim_df.groupby('Winner').size().reindex(party_pro_colors.keys(), fill_value=0)
calc_pops = sim_df.groupby('Winner')['Population'].sum().reindex(party_pro_colors.keys(), fill_value=0)

# ==============================================================================
# 🏙️ 網頁結構：全新排版（左側顯示宏觀統計，右側顯示 22 縣市詳細數值報表）
# ==============================================================================
col1, col2 = st.columns([0.45, 0.55])

with col1:
    st.subheader("📈 戰略量化三大核心指標")
    
    # 指標一：總席次直方圖
    fig_seats = go.Figure()
    fig_seats.add_trace(go.Bar(
        x=["藍白聯合陣線", "民主進步黨"], 
        y=[calc_seats['KMT_TPP'], calc_seats['DPP']], 
        marker_color=[party_pro_colors['KMT_TPP'], party_pro_colors['DPP']], 
        text=[f"<b>{calc_seats['KMT_TPP']} 席</b>", f"<b>{calc_seats['DPP']} 席</b>"], 
        textposition='auto'
    ))
    fig_seats.add_shape(type="line", x0=-0.5, x1=1.5, y0=12, y1=12, line=dict(color="#FF1744", width=3, dash="dash"))
    fig_seats.update_layout(template="plotly_dark", title="預估執政縣市總席次對決 (勝選線: 12 席)", height=240, margin=dict(l=10, r=10, t=40, b=10))
    st.plotly_chart(fig_seats, use_container_width=True)
    
    # 指標二：執政總人口覆蓋率圓餅圖
    fig_pie = go.Figure(data=[go.Pie(
        labels=["藍白聯合覆蓋人口", "綠營執政覆蓋人口"], 
        values=[calc_pops['KMT_TPP'], calc_pops['DPP']], 
        marker=dict(colors=[party_pro_colors['KMT_TPP'], party_pro_colors['DPP']]), 
        hole=0.45, 
        textinfo='percent+label'
    )])
    fig_pie.update_layout(template="plotly_dark", title="聯合陣線 vs DPP 執政覆蓋人口比例", height=240, margin=dict(l=10, r=10, t=40, b=10), showlegend=False)
    st.plotly_chart(fig_pie, use_container_width=True)
    
    # 指標三：核心戰區拉鋸戰堆疊圖
    fig_zones = go.Figure()
    focus_zones = sim_df[(sim_df['Is_Six_Metro'] == 1) | (sim_df['Is_Swing_Zone'] == 1)]
    fig_zones.add_trace(go.Bar(name='藍白聯合軍', x=focus_zones['County'], y=focus_zones['Final_Blue_White']*100, marker_color=party_pro_colors['KMT_TPP']))
    fig_zones.add_trace(go.Bar(name='民主進步黨', x=focus_zones['County'], y=focus_zones['Final_DPP']*100, marker_color=party_pro_colors['DPP']))
    fig_zones.update_layout(template="plotly_dark", title="核心六都與關鍵搖擺區拉鋸得票率 (%)", height=240, margin=dict(l=10, r=10, t=40, b=10), barmode='stack', showlegend=False)
    st.plotly_chart(fig_zones, use_container_width=True)

with col2:
    st.subheader("📋 全台 22 縣市即時預測數據報表")
    
    # 建立一個乾淨、易懂的 DataFrame 供使用者查看
    report_df = pd.DataFrame({
        "縣市名稱": sim_df['County'],
        "預估勝出者": sim_df['Winner'].map({'KMT_TPP': '💜 藍白聯合軍', 'DPP': '💚 民主進步黨'}),
        "藍白陣線得票率": (sim_df['Final_Blue_White'] * 100).round(1).astype(str) + "%",
        "民進黨得票率": (sim_df['Final_DPP'] * 100).round(1).astype(str) + "%",
        "縣市人口數": sim_df['Population'].map('{:,}'.format)
    })
    
    # 使用 Streamlit 的專業級表格組件，支援搜尋與排序
    st.dataframe(report_df, height=760, use_container_width=True, hide_index=True)
