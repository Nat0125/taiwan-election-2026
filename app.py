# ==============================================================================
# 🏛️ TAIWAN ELECTION QUANTITATIVE WAR-ROOM ENGINE (STREAMLIT ULTIMATE v6.0)
# ==============================================================================
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# 1. 強制設定全螢幕 RWD 網頁排版
st.set_page_config(layout="wide", page_title="台灣選戰量化模擬中心 v6.0", page_icon="🏛️")
st.title("🏛️ 台灣地方公職選舉量化模擬與戰略預測系統 (旗艦完全體 v6.0)")
st.markdown("---")

# 2. 核心大數據基本盤資料庫
raw_master_data = {
    "County": ["基隆市", "臺北市", "新北市", "桃園市", "新竹市", "新竹縣", "苗栗縣", "臺中市", "彰化縣", "南投縣", "雲林縣", "嘉義市", "嘉義縣", "臺南市", "高雄市", "屏東縣", "宜蘭縣", "花蓮縣", "臺東縣", "澎湖縣", "金門縣", "連江縣"],
    "Population": [360000, 2500000, 4000000, 2300000, 450000, 580000, 530000, 2800000, 1240000, 480000, 660000, 260000, 490000, 1850000, 2730000, 790000, 450000, 320000, 210000, 100000, 140000, 140000],
    "Base_KMT": [0.46, 0.44, 0.43, 0.41, 0.26, 0.46, 0.48, 0.41, 0.43, 0.46, 0.38, 0.44, 0.31, 0.29, 0.31, 0.34, 0.42, 0.55, 0.56, 0.41, 0.65, 0.72],
    "Base_DPP": [0.38, 0.36, 0.37, 0.35, 0.30, 0.26, 0.26, 0.35, 0.39, 0.36, 0.47, 0.41, 0.54, 0.55, 0.54, 0.51, 0.41, 0.24, 0.23, 0.44, 0.09, 0.05],
    "Base_TPP": [0.16, 0.20, 0.20, 0.24, 0.44, 0.28, 0.26, 0.24, 0.18, 0.18, 0.15, 0.15, 0.15, 0.16, 0.15, 0.15, 0.17, 0.21, 0.21, 0.15, 0.26, 0.23],
    "Is_Six_Metro": [0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    "Is_Swing_Zone": [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
}
df_master = pd.DataFrame(raw_master_data)
df_master['Seats'] = 1

# 3. 內嵌全台 22 縣市地理幾何外觀（完美修正投影）
def generate_inline_geojson():
    geo_centers = {
        "基隆市": [[[121.65,25.10],[121.80,25.10],[121.80,25.18],[121.65,25.18],[121.65,25.10]]], "臺北市": [[[121.48,25.00],[121.62,25.00],[121.62,25.12],[121.48,25.12],[121.48,25.00]]],
        "新北市": [[[121.30,24.85],[121.75,24.85],[122.00,25.05],[121.40,25.30],[121.30,24.85]]], "桃園市": [[[121.05,24.75],[121.35,24.75],[121.45,25.05],[121.10,25.15],[121.05,24.75]]],
        "新竹市": [[[120.90,24.73],[121.02,24.73],[121.02,24.83],[120.90,24.83],[120.90,24.73]]], "新竹縣": [[[121.00,24.55],[121.30,24.55],[121.30,24.85],[121.00,24.85],[121.00,24.55]]],
        "苗栗縣": [[[120.65,24.30],[121.10,24.30],[121.15,24.65],[120.65,24.65],[120.65,24.30]]], "臺中市": [[[120.45,24.05],[121.40,24.05],[121.40,24.40],[120.45,24.40],[120.45,24.05]]],
        "彰化縣": [[[120.25,23.80],[120.65,23.80],[120.65,24.15],[120.25,24.15],[120.25,23.80]]], "南投縣": [[[120.65,23.50],[121.40,23.50],[121.40,24.25],[120.65,24.25],[120.65,23.50]]],
        "雲林縣": [[[120.10,23.55],[120.70,23.55],[120.70,23.85],[120.10,23.85],[120.10,23.55]]], "嘉義市": [[[120.40,23.45],[120.50,23.45],[120.50,23.52],[120.40,23.52],[120.40,23.45]]],
        "嘉義縣": [[[120.10,23.15],[120.80,23.15],[120.80,23.60],[120.10,23.60],[120.10,23.15]]], "臺南市": [[[120.00,22.85],[120.65,22.85],[120.65,23.40],[120.00,23.40],[120.00,22.85]]],
        "高雄市": [[[120.15,22.45],[121.05,22.45],[121.05,23.45],[120.15,23.45],[120.15,22.45]]], "屏東縣": [[[120.35,21.85],[120.95,21.85],[120.95,22.85],[120.35,22.85],[120.35,21.85]]],
        "宜蘭縣": [[[121.50,24.30],[121.95,24.30],[121.95,25.00],[121.50,25.00],[121.50,24.30]]], "花蓮縣": [[[121.15,23.10],[121.75,23.10],[121.75,24.40],[121.15,24.40],[121.15,23.10]]],
        "臺東縣": [[[120.75,22.10],[121.60,22.10],[121.60,23.20],[120.75,23.20],[120.75,22.10]]], "澎湖縣": [[[119.45,23.20],[119.75,23.20],[119.75,23.80],[119.45,23.80],[119.45,23.20]]],
        "金門縣": [[[118.20,24.35],[118.55,24.35],[118.55,24.55],[118.20,24.55],[118.20,24.35]]], "連江縣": [[[119.85,26.10],[120.30,26.10],[120.30,26.35],[119.85,26.35],[119.85,26.10]]]
    }
    features = []
    for c_name, coords in geo_centers.items():
        features.append({"type": "Feature", "properties": {"COUNTYNAME": c_name}, "geometry": {"type": "Polygon", "coordinates": coords}, "id": c_name})
    return {"type": "FeatureCollection", "features": features}

inline_geojson = generate_inline_geojson()
party_pro_colors = {"KMT": "#01579B", "DPP": "#2E7D32", "TPP": "#00B8D4", "none": "#455A64"}

# 4. 左側側邊控制面板
st.sidebar.header("🎛️ 戰情室核心因子控制台")
kmt_f = st.sidebar.slider("🔵 國民黨大勢增減 %", -20, 20, 0, step=1)
dpp_f = st.sidebar.slider("🟢 民進黨大勢增減 %", -20, 20, 0, step=1)
tpp_f = st.sidebar.slider("⚪ 民眾黨棄保/爆發 %", -20, 20, 0, step=1)
ind_f = st.sidebar.slider("🔸 中間選民流向偏好 %", -15, 15, 0, step=1)
young_r = st.sidebar.slider("👥 青年投票率加權倍數", 0.3, 1.7, 1.0, step=0.1)

# 多因子量化聯動演算
sim_df = df_master.copy()
sim_df['Final_KMT'] = sim_df['Base_KMT'] + (kmt_f / 100.0) + (ind_f * 0.4 / 100.0)
sim_df['Final_DPP'] = sim_df['Base_DPP'] + (dpp_f / 100.0) + (ind_f * 0.4 / 100.0)
sim_df['Final_TPP'] = (sim_df['Base_TPP'] * young_r) + (tpp_f / 100.0) + (ind_f * 0.2 / 100.0)

metro_mask = sim_df['Is_Six_Metro'] == 1
sim_df.loc[metro_mask, 'Final_TPP'] += (tpp_f * 0.15 / 100.0)
sim_df.loc[sim_df['County'] == "新竹市", 'Final_TPP'] += 0.05

total_matrix = sim_df['Final_KMT'] + sim_df['Final_DPP'] + sim_df['Final_TPP']
sim_df['Final_KMT'] /= total_matrix; sim_df['Final_DPP'] /= total_matrix; sim_df['Final_TPP'] /= total_matrix

decisions = [
    (sim_df['Final_KMT'] > sim_df['Final_DPP']) & (sim_df['Final_KMT'] > sim_df['Final_TPP']),
    (sim_df['Final_DPP'] > sim_df['Final_KMT']) & (sim_df['Final_DPP'] > sim_df['Final_TPP']),
    (sim_df['Final_TPP'] > sim_df['Final_KMT']) & (sim_df['Final_TPP'] > sim_df['Final_DPP'])
]
sim_df['Winner'] = np.select(decisions, ['KMT', 'DPP', 'TPP'], default='none')
calc_seats = sim_df.groupby('Winner').size().reindex(party_pro_colors.keys(), fill_value=0)
calc_pops = sim_df.groupby('Winner')['Population'].sum().reindex(party_pro_colors.keys(), fill_value=0)

# ==============================================================================
# 🏙️ 網頁結構重置：使用 st.columns 全原生渲染，徹底摧毀 Plotly Subplot 的類型 Bug
# ==============================================================================
col1, col2 = st.columns([0.5, 0.5])

with col1:
    st.subheader("🗺️ 全台 22 縣市實體幾何模擬版權圖")
    hover_labels = sim_df.apply(lambda r: f"<b>🏛️ {r['County']}</b><br>----------------------------<br>🗳️ 勝出: {r['Winner']}<br>🔵 國民黨: {r['Final_KMT']*100:.1f}%<br>🟢 民進黨: {r['Final_DPP']*100:.1f}%<br>⚪ 民眾黨: {r['Final_TPP']*100:.1f}%", axis=1)
    
    fig_map = go.Figure(data=go.Choropleth(
        geojson=inline_geojson,
        locations=sim_df['County'],
        featureidkey="properties.COUNTYNAME",
        z=sim_df['Winner'].map({'KMT': 1, 'DPP': 2, 'TPP': 3, 'none': 0}),
        colorscale=[[0, '#455A64'], [0.33, '#01579B'], [0.66, '#2E7D32'], [1.0, '#00B8D4']],
        showscale=False,
        text=hover_labels,
        hoverinfo="text"
    ))
    fig_map.update_layout(template="plotly_dark", height=780, margin=dict(l=0, r=0, t=10, b=0), geo=dict(projection_type="mercator", fitbounds="locations", visible=False))
    st.plotly_chart(fig_map, use_container_width=True)

with col2:
    st.subheader("📊 戰情即時量化統計指標")
    
    # 指標一：獨立總席次對決直方圖
    fig_seats = go.Figure()
    fig_seats.add_trace(go.Bar(
        x=["中國國民黨", "民主進步黨", "台灣民眾黨"], 
        y=[calc_seats['KMT'], calc_seats['DPP'], calc_seats['TPP']], 
        marker_color=[party_pro_colors['KMT'], party_pro_colors['DPP'], party_pro_colors['TPP']], 
        text=[f"<b>{calc_seats['KMT']} 席</b>", f"<b>{calc_seats['DPP']} 席</b>", f"<b>{calc_seats['TPP']} 席</b>"], 
        textposition='auto'
    ))
    fig_seats.add_shape(type="line", x0=-0.5, x1=2.5, y0=12, y1=12, line=dict(color="#FF1744", width=3, dash="dash"))
    fig_seats.update_layout(template="plotly_dark", title="預估席次總和對決 (紅線過半: 12 席)", height=240, margin=dict(l=10, r=10, t=40, b=10))
    st.plotly_chart(fig_seats, use_container_width=True)
    
    # 指標二：獨立地方執政覆蓋人口比例圓餅圖（完全獨立，不再引發類型衝突）
    fig_pie = go.Figure(data=[go.Pie(
        labels=["藍營覆蓋", "綠營覆蓋", "白營覆蓋"], 
        values=[calc_pops['KMT'], calc_pops['DPP'], calc_pops['TPP']], 
        marker=dict(colors=[party_pro_colors['KMT'], party_pro_colors['DPP'], party_pro_colors['TPP']]), 
        hole=0.45, 
        textinfo='percent+label'
    )])
    fig_pie.update_layout(template="plotly_dark", title="各黨地方執政覆蓋人口總和比例", height=240, margin=dict(l=10, r=10, t=40, b=10), showlegend=False)
    st.plotly_chart(fig_pie, use_container_width=True)
    
    # 指標三：核心戰區拉鋸戰堆疊圖
    fig_zones = go.Figure()
    focus_zones = sim_df[(sim_df['Is_Six_Metro'] == 1) | (sim_df['Is_Swing_Zone'] == 1)]
    fig_zones.add_trace(go.Bar(name='國民黨', x=focus_zones['County'], y=focus_zones['Final_KMT']*100, marker_color=party_pro_colors['KMT']))
    fig_zones.add_trace(go.Bar(name='民進黨', x=focus_zones['County'], y=focus_zones['Final_DPP']*100, marker_color=party_pro_colors['DPP']))
    fig_zones.add_trace(go.Bar(name='民眾黨', x=focus_zones['County'], y=focus_zones['Final_TPP']*100, marker_color=party_pro_colors['TPP']))
    fig_zones.update_layout(template="plotly_dark", title="都市 vs 搖擺：核心戰區拉鋸戰", height=240, margin=dict(l=10, r=10, t=40, b=10), barmode='stack', showlegend=False)
    st.plotly_chart(fig_zones, use_container_width=True)
