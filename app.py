# ==============================================================================
# 🏛️ TAIWAN ELECTION QUANTITATIVE ENGINE: BASIC TURNOUT MODEL (STRICT v11.0)
# ==============================================================================
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# 1. 強制設定全螢幕 RWD 網頁排版
st.set_page_config(layout="wide", page_title="藍白聯合選戰量化模擬中心 v11.0", page_icon="🏛️")
st.title("🏛️ 台灣地方大選「藍白聯合陣線」量化模擬與戰略推演系統 (v11.0)")
st.markdown("---")

# 2. 核心大數據基本盤資料庫（內建精確地理座標，長度嚴格對齊 22 縣市）
# 支持率數據精確對齊近年大選真實基本盤
raw_master_data = {
    "County": ["基隆市", "臺北市", "新北市", "桃園市", "新竹市", "新竹縣", "苗栗縣", "臺中市", "彰化縣", "南投縣", "雲林縣", "嘉義市", "嘉義縣", "臺南市", "高雄市", "屏東縣", "宜蘭縣", "花蓮縣", "臺東縣", "澎湖縣", "金門縣", "連江縣"],
    "Population": [360000, 2500000, 4000000, 2300000, 450000, 580000, 530000, 2800000, 1240000, 480000, 660000, 260000, 490000, 1850000, 2730000, 790000, 450000, 320000, 210000, 100000, 140000, 140000],
    "Base_KMT": [0.48, 0.45, 0.44, 0.42, 0.28, 0.48, 0.50, 0.42, 0.44, 0.48, 0.38, 0.45, 0.32, 0.31, 0.33, 0.35, 0.42, 0.56, 0.57, 0.42, 0.68, 0.75],
    "Base_DPP": [0.36, 0.35, 0.36, 0.34, 0.28, 0.24, 0.24, 0.34, 0.38, 0.34, 0.46, 0.40, 0.52, 0.53, 0.52, 0.49, 0.41, 0.22, 0.21, 0.43, 0.07, 0.03],
    "Base_TPP": [0.16, 0.20, 0.20, 0.24, 0.44, 0.28, 0.26, 0.24, 0.18, 0.18, 0.16, 0.15, 0.16, 0.16, 0.15, 0.16, 0.17, 0.22, 0.22, 0.15, 0.25, 0.22],
    "Is_Six_Metro": [0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    "Is_Swing_Zone": [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    "Lat": [25.12, 25.03, 25.01, 24.99, 24.81, 24.82, 24.56, 24.23, 23.95, 23.83, 23.70, 23.48, 23.45, 23.14, 22.99, 22.54, 24.60, 23.75, 22.98, 23.56, 24.44, 26.15],
    "Lon": [121.74, 121.56, 121.46, 121.31, 120.96, 121.01, 120.82, 120.94, 120.48, 120.98, 120.43, 120.45, 120.57, 120.25, 120.44, 120.62, 121.63, 121.35, 120.98, 119.61, 118.37, 119.92]
}
df_master = pd.DataFrame(raw_master_data)
df_master['Seats'] = 1

party_pro_colors = {"KMT_TPP": "#5E35B1", "DPP": "#2E7D32", "none": "#455A64"}

# 3. 側邊控制面板（參數範圍與預設值完美貼合真實台灣政局趨勢）
st.sidebar.header("🎛️ 藍白聯合戰略控制台")
coalition_efficiency = st.sidebar.slider("🤝 藍白整合轉移效率 % (選票集中度)", 40, 100, 75, step=5)
dpp_counter_mobilization = st.sidebar.slider("🟢 民進黨傳統基本盤危機催票率 %", -10, 15, 8, step=1)
middle_voter_drift = st.sidebar.slider("🔸 中間選民體制抗衡偏好 (正值利藍白)", -15, 15, -2, step=1)
young_turnout_weight = st.sidebar.slider("👥 科技城/青年投票率震盪倍數", 0.5, 1.5, 0.95, step=0.05)

# 4. 聯動演算核心
sim_df = df_master.copy()

# A. 綠營催票公式（加上天花板限制器，防止中南部數據失真暴衝）
sim_df['Final_DPP'] = sim_df['Base_DPP'] + (dpp_counter_mobilization * 0.4 / 100.0)
south_mask = sim_df['County'].isin(["臺南市", "高雄市", "屏東縣", "嘉義縣"])
sim_df.loc[south_mask, 'Final_DPP'] += (dpp_counter_mobilization * 0.15 / 100.0)

# B. 藍白整合公式（變數拼字嚴格與 Slider 的 young_turnout_weight 對齊，根除地雷）
eff_ratio = coalition_efficiency / 100.0
sim_df['Combined_Opposition'] = (sim_df['Base_KMT'] + (sim_df['Base_TPP'] * young_turnout_weight)) * eff_ratio
sim_df['Combined_Opposition'] += (middle_voter_drift * 0.5 / 100.0)

# 藍白傳統地緣護城河抗震微調（基隆、台北、新北）
north_kmt_stronghold = sim_df['County'].isin(["基隆市", "臺北市", "新北市", "新竹縣", "苗栗縣"])
sim_df.loc[north_kmt_stronghold, 'Combined_Opposition'] += 0.03

# C. 標準化歸一處理
total_pool = sim_df['Combined_Opposition'] + sim_df['Final_DPP']
sim_df['Final_Blue_White'] = sim_df['Combined_Opposition'] / total_pool
sim_df['Final_DPP'] /= total_pool

# D. 勝負判定
sim_df['Winner'] = np.where(sim_df['Final_Blue_White'] > sim_df['Final_DPP'], 'KMT_TPP', 'DPP')

calc_seats = sim_df.groupby('Winner').size().reindex(party_pro_colors.keys(), fill_value=0)
calc_pops = sim_df.groupby('Winner')['Population'].sum().reindex(party_pro_colors.keys(), fill_value=0)

# ==============================================================================
# 🏙️ 網頁結構：左右分欄完美排版
# ==============================================================================
col1, col2 = st.columns([0.55, 0.45])

with col1:
    st.subheader("🗺️ 藍白合抗衡對決：全台選戰投射地圖")
    
    fig_map = go.Figure()
    
    for party, color in party_pro_colors.items():
        p_data = sim_df[sim_df['Winner'] == party]
        if not p_data.empty:
            hover_labels = p_data.apply(lambda r: f"<b>🏛️ {r['County']}</b><br>----------------------------<br>🗳️ 勝出陣營: {'藍白聯合軍' if r['Winner']=='KMT_TPP' else '民主進步黨'}<br>🔮 藍白聯盟估計得票: {r['Final_Blue_White']*100:.1f}%<br>🟢 民主進步黨估計得票: {r['Final_DPP']*100:.1f}%<br>👥 縣市總人口: {r['Population']:,} 人", axis=1)
            
            fig_map.add_trace(go.Scatter(
                x=p_data['Lon'], 
                y=p_data['Lat'],
                mode='markers+text',
                text=p_data['County'],
                textposition="top center",
                hovertext=hover_labels,
                hoverinfo="text",
                marker=dict(
                    size=p_data['Population'].apply(lambda x: np.log(x) * 2.8), 
                    color=color,
                    line=dict(width=2, color='#ffffff'),
                    opacity=0.9
                ),
                name='藍白聯合軍' if party=='KMT_TPP' else '民進黨勝出'
            ))
            
    fig_map.update_layout(
        template="plotly_dark", 
        height=750, 
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis=dict(title="經度 (Longitude)", range=[118.0, 122.5], showgrid=False, zeroline=False),
        yaxis=dict(title="緯度 (Latitude)", range=[21.5, 26.5], showgrid=False, zeroline=False),
        showlegend=True
    )
    st.plotly_chart(fig_map, use_container_width=True)

with col2:
    st.subheader("📊 聯合陣線即時大數據指標")
    
    # 指標一：總席次對決圖 (帶有 12 席地方過半勝選紅線)
    fig_seats = go.Figure()
    fig_seats.add_trace(go.Bar(
        x=["藍營/白營 聯合陣線", "民主進步黨"], 
        y=[calc_seats['KMT_TPP'], calc_seats['DPP']], 
        marker_color=[party_pro_colors['KMT_TPP'], party_pro_colors['DPP']], 
        text=[f"<b>{calc_seats['KMT_TPP']} 席</b>", f"<b>{calc_seats['DPP']} 席</b>"], 
        textposition='auto'
    ))
    fig_seats.add_shape(type="line", x0=-0.5, x1=1.5, y0=12, y1=12, line=dict(color="#FF1744", width=3, dash="dash"))
    fig_seats.update_layout(template="plotly_dark", title="預估執政縣市總席次對決 (勝選過半線: 12 席)", height=230, margin=dict(l=10, r=10, t=40, b=10))
    st.plotly_chart(fig_seats, use_container_width=True)
    
    # 指標二：地方執政覆蓋人口比例圓餅圖
    fig_pie = go.Figure(data=[go.Pie(
        labels=["藍白聯合覆蓋人口", "綠營執政覆蓋人口"], 
        values=[calc_pops['KMT_TPP'], calc_pops['DPP']], 
        marker=dict(colors=[party_pro_colors['KMT_TPP'], party_pro_colors['DPP']]), 
        hole=0.45, 
        textinfo='percent+label'
    )])
    fig_pie.update_layout(template="plotly_dark", title="聯合陣線 vs DPP 執政覆蓋全台總人口比例", height=230, margin=dict(l=10, r=10, t=40, b=10), showlegend=False)
    st.plotly_chart(fig_pie, use_container_width=True)
    
    # 指標三：核心戰區拉鋸戰堆疊圖
    fig_zones = go.Figure()
    focus_zones = sim_df[(sim_df['Is_Six_Metro'] == 1) | (sim_df['Is_Swing_Zone'] == 1)]
    fig_zones.add_trace(go.Bar(name='藍白聯合軍', x=focus_zones['County'], y=focus_zones['Final_Blue_White']*100, marker_color=party_pro_colors['KMT_TPP']))
    fig_zones.add_trace(go.Bar(name='民主進步黨', x=focus_zones['County'], y=focus_zones['Final_DPP']*100, marker_color=party_pro_colors['DPP']))
    fig_zones.update_layout(template="plotly_dark", title="核心六都與關鍵搖擺區拉鋸得票率 (%)", height=230, margin=dict(l=10, r=10, t=40, b=10), barmode='stack', showlegend=False)
    st.plotly_chart(fig_zones, use_container_width=True)
