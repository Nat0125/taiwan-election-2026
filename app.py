# ==============================================================================
# 🏛️ TAIWAN ELECTION QUANTITATIVE ENGINE: REAL CANDIDATES MODEL (STRICT v11.0)
# ==============================================================================
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# 1. 網頁全螢幕配置
st.set_page_config(layout="wide", page_title="台灣選戰數據中心 v11.0", page_icon="📊")
st.title("🏛️ 台灣地方大選「藍白聯合陣線」量化模擬與戰略推演系統 (v11.0)")
st.subheader("📋 基於 2026 各縣市真實參選名單之大數據推射面板")
st.markdown("---")

# 2. 核心大數據資料庫（長度嚴格對齊 22 縣市，內建真實參選人與地緣基本盤）
raw_master_data = {
    "County": ["基隆市", "臺北市", "新北市", "桃園市", "新竹市", "新竹縣", "苗栗縣", "臺中市", "彰化縣", "南投縣", "雲林縣", "嘉義市", "嘉義縣", "臺南市", "高雄市", "屏東縣", "宜蘭縣", "花蓮縣", "臺東縣", "澎湖縣", "金門縣", "連江縣"],
    "Population": [360000, 2500000, 4000000, 2300000, 450000, 580000, 530000, 2800000, 1240000, 480000, 660000, 260000, 490000, 1850000, 2730000, 790000, 450000, 320000, 210000, 100000, 140000, 140000],
    "Cand_DPP": ["童子瑋", "沈伯洋", "蘇巧慧", "黃世杰", "莊競程", "─", "陳品安", "何欣純", "陳素月", "温世政", "劉建國", "王美惠", "蔡易餘", "陳亭妃", "賴瑞隆", "周春米", "林國漳", "─", "陳瑩", "陳光復", "─", "─"],
    "Cand_BlueWhite": ["謝國樑 (藍)", "蔣萬安 (藍)", "李四川 (藍)", "張善政 (藍)", "高虹安 (白)", "徐欣營 (藍)", "鍾東錦 (藍)", "江啟臣 (藍)", "魏平政/蔡壁如", "許淑華 (藍)", "張嘉郡 (藍)", "張啓楷 (白)", "未定", "謝龍介 (藍)", "柯志恩 (藍)", "蘇清泉 (藍)", "吳宗憲 (藍)", "游淑貞 (藍)", "吳秀華 (藍)", "陳振中 (藍)", "陳玉珍 (藍)", "王忠銘 (藍)"],
    "Base_DPP": [0.36, 0.35, 0.36, 0.34, 0.20, 0.15, 0.24, 0.34, 0.38, 0.34, 0.46, 0.40, 0.54, 0.53, 0.52, 0.49, 0.41, 0.15, 0.21, 0.43, 0.05, 0.03],
    "Base_BlueWhite": [0.64, 0.65, 0.64, 0.66, 0.80, 0.85, 0.76, 0.66, 0.62, 0.66, 0.54, 0.60, 0.46, 0.47, 0.48, 0.51, 0.59, 0.85, 0.79, 0.57, 0.95, 0.97],
    "Is_Six_Metro": [0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    "Is_Swing_Zone": [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    "Note": ["謝國樑戰基隆", "蔣萬安爭取連任", "民調李四川勝出", "張善政爭取連任", "藍白合禮讓高虹安", "徐欣瑩出征", "鍾東錦具優勢", "江啟臣接棒大熱", "陳素月強碰藍白", "許淑華現任優勢", "張嘉郡出馬", "民調張啓楷勝出", "綠營傳統優勢區", "謝龍介再戰陳亭妃", "柯志恩強碰賴瑞隆", "蘇清泉再戰屏東", "民調吳宗憲勝出", "民進黨禮讓張峻", "吳秀華出戰", "陳光復面臨連任考驗", "陳玉珍鐵票倉", "王忠銘守馬祖"]
}
df_master = pd.DataFrame(raw_master_data)

party_pro_colors = {"BLUE_WHITE": "#5E35B1", "DPP": "#2E7D32"}

# 3. 側邊控制面板
st.sidebar.header("🎛️ 戰情室核心因子控制台")
coalition_efficiency = st.sidebar.slider("🤝 藍白整合轉移效率 % (選票集中度)", 40, 100, 85, step=5)
dpp_counter_mobilization = st.sidebar.slider("🟢 民進黨傳統基本盤危機催票率 %", -10, 15, 5, step=1)
middle_voter_drift = st.sidebar.slider("🔸 中間選民體制抗衡偏好 (正值利藍白)", -15, 15, 0, step=1)
young_turnout_weight = st.sidebar.slider("👥 科技城/青年投票率震盪倍數", 0.5, 1.5, 1.0, step=0.05)

# 4. 聯動演算核心
sim_df = df_master.copy()

# A. 綠營催票公式（考慮中南部深綠催票加權）
sim_df['Final_DPP'] = sim_df['Base_DPP'] + (dpp_counter_mobilization * 0.4 / 100.0)
south_mask = sim_df['County'].isin(["臺南市", "高雄市", "屏東縣", "嘉義縣"])
sim_df.loc[south_mask, 'Final_DPP'] += (dpp_counter_mobilization * 0.15 / 100.0)

# B. 藍白合公式（將轉移效率與中間選民偏好套入公式）
eff_ratio = coalition_efficiency / 100.0
sim_df['Combined_Opposition'] = sim_df['Base_BlueWhite'] * eff_ratio
sim_df['Combined_Opposition'] += (middle_voter_drift * 0.5 / 100.0)

# 科技城新竹市與特殊禮讓區（花蓮）權重微調
sim_df.loc[sim_df['County'] == "新竹市", 'Combined_Opposition'] *= young_turnout_weight

# C. 標準化歸一處理
total_pool = sim_df['Combined_Opposition'] + sim_df['Final_DPP']
sim_df['Final_Blue_White'] = sim_df['Combined_Opposition'] / total_pool
sim_df['Final_DPP'] /= total_pool

# D. 勝負判定
sim_df['Winner'] = np.where(sim_df['Final_Blue_White'] > sim_df['Final_DPP'], 'BLUE_WHITE', 'DPP')

calc_seats = sim_df.groupby('Winner').size().reindex(party_pro_colors.keys(), fill_value=0)
calc_pops = sim_df.groupby('Winner')['Population'].sum().reindex(party_pro_colors.keys(), fill_value=0)

# ==============================================================================
# 🏙️ 網頁結構排版
# ==============================================================================
col1, col2 = st.columns([0.45, 0.55])

with col1:
    st.subheader("📈 聯合陣線宏觀量化指標")
    
    # 指標一：總席次直方圖
    fig_seats = go.Figure()
    fig_seats.add_trace(go.Bar(
        x=["藍白聯合陣線", "民主進步黨"], 
        y=[calc_seats['BLUE_WHITE'], calc_seats['DPP']], 
        marker_color=[party_pro_colors['BLUE_WHITE'], party_pro_colors['DPP']], 
        text=[f"<b>{calc_seats['BLUE_WHITE']} 席</b>", f"<b>{calc_seats['DPP']} 席</b>"], 
        textposition='auto'
    ))
    fig_seats.add_shape(type="line", x0=-0.5, x1=1.5, y0=12, y1=12, line=dict(color="#FF1744", width=3, dash="dash"))
    fig_seats.update_layout(template="plotly_dark", title="預估執政縣市總席次對決 (過半勝選線: 12 席)", height=240, margin=dict(l=10, r=10, t=40, b=10))
    st.plotly_chart(fig_seats, use_container_width=True)
    
    # 指標二：執政總人口覆蓋率
    fig_pie = go.Figure(data=[go.Pie(
        labels=["藍白聯合覆蓋人口", "綠營執政覆蓋人口"], 
        values=[calc_pops['BLUE_WHITE'], calc_pops['DPP']], 
        marker=dict(colors=[party_pro_colors['BLUE_WHITE'], party_pro_colors['DPP']]), 
        hole=0.45, 
        textinfo='percent+label'
    )])
    fig_pie.update_layout(template="plotly_dark", title="兩大陣營執政覆蓋全台總人口比例", height=240, margin=dict(l=10, r=10, t=40, b=10), showlegend=False)
    st.plotly_chart(fig_pie, use_container_width=True)
    
    # 指標三：核心戰區拉鋸戰
    fig_zones = go.Figure()
    focus_zones = sim_df[(sim_df['Is_Six_Metro'] == 1) | (sim_df['Is_Swing_Zone'] == 1)]
    fig_zones.add_trace(go.Bar(name='藍白聯合軍', x=focus_zones['County'], y=focus_zones['Final_Blue_White']*100, marker_color=party_pro_colors['BLUE_WHITE']))
    fig_zones.add_trace(go.Bar(name='民主進步黨', x=focus_zones['County'], y=focus_zones['Final_DPP']*100, marker_color=party_pro_colors['DPP']))
    fig_zones.update_layout(template="plotly_dark", title="核心六都與關鍵搖擺區拉鋸得票率 (%)", height=240, margin=dict(l=10, r=10, t=40, b=10), barmode='stack', showlegend=False)
    st.plotly_chart(fig_zones, use_container_width=True)

with col2:
    st.subheader("📋 全台 22 縣市真實人選即時數據報表")
    
    # 建立數據報表，直接把人名和備註抓進去
    report_df = pd.DataFrame({
        "縣市名稱": sim_df['County'],
        "預估勝出": sim_df['Winner'].map({'BLUE_WHITE': '💜 藍白聯盟', 'DPP': '💚 民進黨'}),
        "藍白人選": sim_df['Cand_BlueWhite'],
        "藍白得票率": (sim_df['Final_Blue_White'] * 100).round(1).astype(str) + "%",
        "民進黨人選": sim_df['Cand_DPP'],
        "民進黨得票率": (sim_df['Final_DPP'] * 100).round(1).astype(str) + "%",
        "選情重要備註": sim_df['Note']
    })
    
    st.dataframe(report_df, height=760, use_container_width=True, hide_index=True)
