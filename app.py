# ==============================================================================
# 🏛️ TAIWAN ELECTION QUANTITATIVE WAR-ROOM ENGINE (STREAMLIT STRICT v8.5)
# ==============================================================================
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# 1. 強制設定全螢幕 RWD 網頁排版
st.set_page_config(layout="wide", page_title="台灣選戰量化模擬中心 v8.5", page_icon="🏛️")
st.title("🏛️ 台灣地方公職選舉量化模擬與戰略預測系統 (戰情室完全體 v8.5)")
st.markdown("---")

# 2. 核心大數據基本盤資料庫（內建精確地理經緯度坐標，長度嚴格對齊 22 縣市）
raw_master_data = {
    "County": ["基隆市", "臺北市", "新北市", "桃園市", "新竹市", "新竹縣", "苗栗縣", "臺中市", "彰化縣", "南投縣", "雲林縣", "嘉義市", "嘉義縣", "臺南市", "高雄市", "屏東縣", "宜蘭縣", "花蓮縣", "臺東縣", "澎湖縣", "金門縣", "連江縣"],
    "Population": [360000, 2500000, 4000000, 2300000, 450000, 580000, 530000, 2800000, 1240000, 480000, 660000, 260000, 490000, 1850000, 2730000, 790000, 450000, 320000, 210000, 100000, 140000, 14000],
    "Base_KMT": [0.46, 0.44, 0.43, 0.41, 0.26, 0.46, 0.48, 0.41, 0.43, 0.46, 0.38, 0.44, 0.31, 0.29, 0.31, 0.34, 0.42, 0.55, 0.56, 0.41, 0.65, 0.72],
    "Base_DPP": [0.38, 0.36, 0.37, 0.35, 0.30, 0.26, 0.26, 0.35, 0.39, 0.36, 0.47, 0.41, 0.54, 0.55, 0.54, 0.51, 0.41, 0.24, 0.23, 0.44, 0.09, 0.05],
    "Base_TPP": [0.16, 0.20, 0.20, 0.24, 0.44, 0.28, 0.26, 0.24, 0.18, 0.18, 0.15, 0.15, 0.15, 0.16, 0.15, 0.15, 0.17, 0.21, 0.21, 0.15, 0.26, 0.23],
    "Is_Six_Metro": [0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    "Is_Swing_Zone": [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    "Lat": [25.12, 25.03, 25.01, 24.99, 24.81, 24.82, 24.56, 24.23, 23.95, 23.83, 23.70, 23.48, 23.45, 23.14, 22.99, 22.54, 24.60, 23.75, 22.98, 23.56, 24.44, 26.15],
    "Lon": [121.74, 121.56, 121.46, 121.31, 120.96, 121.01, 120.82, 120.94, 120.48, 120.98, 120.43, 120.45, 120.57, 120.25, 120.44, 120.62, 121.63, 121.35, 120.98, 119.61, 118.37, 119.92]
}
df_master = pd.DataFrame(raw_master_data)
df_master['Seats'] = 1

party_pro_colors = {"KMT": "#01579B", "DPP": "#2E7D32", "TPP": "#00B8D4", "none": "#455A64"}

# 3. 左側獨立控制面板 (Slider 命名與範圍嚴格規範)
st.sidebar.header("🎛️ 戰情室核心因子控制台")
kmt_f = st.sidebar.slider("🔵 國民黨大勢增減 %", -20, 20, 0, step=1)
dpp_f = st.sidebar.slider("🟢 民進黨大勢增減 %", -20, 20, 0, step=1)
tpp_f = st.sidebar.slider("⚪ 民眾黨棄保/爆發 %", -20, 20, 0, step=1)
ind_f = st.sidebar.slider("🔸 中間選民流向偏好 %", -15, 15, 0, step=1)
young_r = st.sidebar.slider("👥 青年投票率加權倍數", 0.3, 1.7, 1.0, step=0.1)

# 4. 多因子量化聯動演算引擎公式
sim_df = df_master.copy()
sim_df['Final_KMT'] = sim_df['Base_KMT'] + (kmt_f / 100.0) + (ind_f * 0.4 / 100.0)
sim_df['Final_DPP'] = sim_df['Base_DPP'] + (dpp_f / 100.0) + (ind_f * 0.4 / 100.0)
sim_df['Final_TPP'] = (sim_df['Base_TPP'] * young_r) + (tpp_f / 100.0) + (ind_f * 0.2 / 100.0)

# 區域政治敏感度微調
metro_mask = sim_df['Is_Six_Metro'] == 1
sim_df.loc[metro_mask, 'Final_TPP'] += (tpp_f * 0.15 / 100.0)
sim_df.loc[sim_df['County'] == "新竹市", 'Final_TPP'] += 0.05

# 數據極致標準化 (Sum to 100%)
total_matrix = sim_df['Final_KMT'] + sim_df['Final_DPP'] + sim_df['Final_TPP']
sim_df['Final_KMT'] /= total_matrix
sim_df['Final_DPP'] /= total_matrix
sim_df['Final_TPP'] /= total_matrix

# 勝負矩陣判定
decisions = [
    (sim_df['Final_KMT'] > sim_df['Final_DPP']) & (sim_df['Final_KMT'] > sim_df['Final_TPP']),
    (sim_df['Final_DPP'] > sim_df['Final_KMT']) & (sim_df['Final_DPP'] > sim_df['Final_TPP']),
    (sim_df['Final_TPP'] > sim_df['Final_KMT']) & (sim_df['Final_TPP'] > sim_df['Final_DPP'])
]
sim_df['Winner'] = np.select(decisions, ['KMT', 'DPP', 'TPP'], default='none')
calc_seats = sim_df.groupby('Winner').size().reindex(party_pro_colors.keys(), fill_value=0)
calc_pops = sim_df.groupby('Winner')['Population'].sum().reindex(party_pro_colors.keys(), fill_value=0)

# ==============================================================================
# 🏙️ 網頁佈局：強制左右對分，完全阻絕元件衝突
# ==============================================================================
col1, col2 = st.columns([0.55, 0.45])

with col1:
    st.subheader("🗺️ 全台 22 縣市戰略人口分佈圖")
    
    fig_map = go.Figure()
    
    for party, color in party_pro_colors.items():
        p_data = sim_df[sim_df['Winner'] == party]
        if not p_data.empty:
            hover_labels = p_data.apply(lambda r: f"<b>🏛️ {r['County']}</b><br>----------------------------<br>🗳️ 勝出: {r['Winner']}<br>🔵 國民黨: {r['Final_KMT']*100:.1f}%<br>🟢 民進黨: {r['Final_DPP']*100:.1f}%<br>⚪ 民眾黨: {r['Final_TPP']*100:.1f}%<br>👥 人口: {r['Population']:,} 人", axis=1)
            
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
                name=f"{party} 勝出"
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
    st.subheader("📊 戰情即時量化統計指標")
    
    # 指標一：總席次直方圖 (帶有 12 席過半紅線)
    fig_seats = go.Figure()
    fig_seats.add_trace(go.Bar(
        x=["中國國民黨", "民主進步黨", "台灣民眾黨"], 
        y=[calc_seats['KMT'], calc_seats['DPP'], calc_seats['TPP']], 
        marker_color=[party_pro_colors['KMT'], party_pro_colors['DPP'], party_pro_colors['TPP']], 
        text=[f"<b>{calc_seats['KMT']} 席</b>", f"<b>{calc_seats['DPP']} 席</b>", f"<b>{calc_seats['TPP']} 席</b>"], 
        textposition='auto'
    ))
    fig_seats.add_shape(type="line", x0=-0.5, x1=2.5, y0=12, y1=12, line=dict(color="#FF1744", width=3, dash="dash"))
    fig_seats.update_layout(template="plotly_dark", title="預估席次總和對決 (紅線過半: 12 席)", height=230, margin=dict(l=10, r=10, t=40, b=10))
    st.plotly_chart(fig_seats, use_container_width=True)
    
    # 指標二：地方執政覆蓋人口比例圓餅圖
    fig_pie = go.Figure(data=[go.Pie(
        labels=["藍營覆蓋", "綠營覆蓋", "白營覆蓋"], 
        values=[calc_pops['KMT'], calc_pops['DPP'], calc_pops['TPP']], 
        marker=dict(colors=[party_pro_colors['KMT'], party_pro_colors['DPP'], party_pro_colors['TPP']]), 
        hole=0.45, 
        textinfo='percent+label'
    )])
    fig_pie.update_layout(template="plotly_dark", title="各黨地方執政覆蓋人口總和比例", height=230, margin=dict(l=10, r=10, t=40, b=10), showlegend=False)
    st.plotly_chart(fig_pie, use_container_width=True)
    
    # 指標三：核心戰區拉鋸戰堆疊圖
    fig_zones = go.Figure()
    focus_zones = sim_df[(sim_df['Is_Six_Metro'] == 1) | (sim_df['Is_Swing_Zone'] == 1)]
    fig_zones.add_trace(go.Bar(name='國民黨', x=focus_zones['County'], y=focus_zones['Final_KMT']*100, marker_color=party_pro_colors['KMT']))
    fig_zones.add_trace(go.Bar(name='民進黨', x=focus_zones['County'], y=focus_zones['Final_DPP']*100, marker_color=party_pro_colors['DPP']))
    fig_zones.add_trace(go.Bar(name='民眾黨', x=focus_zones['County'], y=focus_zones['Final_TPP']*100, marker_color=party_pro_colors['TPP']))
    fig_zones.update_layout(template="plotly_dark", title="都市 vs 搖擺：核心戰區拉鋸戰", height=230, margin=dict(l=10, r=10, t=40, b=10), barmode='stack', showlegend=False)
    st.plotly_chart(fig_zones, use_container_width=True)

