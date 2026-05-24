# ==============================================================================
# 🏛️ TAIWAN ELECTION QUANTITATIVE INTEL ENGINE: THE BLACK SWAN CRISIS (v16.5)
# ==============================================================================
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# 1. 網頁全螢幕與架構配置
st.set_page_config(layout="wide", page_title="台灣選戰黑天鵝量化模擬中心 v16.5", page_icon="🕵️")
st.title("🏛️ 台灣地方大選「黑天鵝事件與突發危機」動態兵棋推演系統 (v16.5)")
st.markdown("---")

# 2. 核心大數據基本盤資料庫（長度嚴格對齊 22 縣市，內建真實人選名單）
raw_master_data = {
    "County": ["基隆市", "臺北市", "新北市", "桃園市", "新竹市", "新竹縣", "苗栗縣", "臺中市", "彰化縣", "南投縣", "雲林縣", "嘉義市", "嘉義縣", "臺南市", "高雄市", "屏東縣", "宜蘭縣", "花蓮縣", "臺東縣", "澎湖縣", "金門縣", "連江縣"],
    "Population": [360000, 2500000, 4000000, 2300000, 450000, 580000, 530000, 2800000, 1240000, 480000, 660000, 260000, 490000, 1850000, 2730000, 790000, 450000, 320000, 210000, 100000, 140000, 140000],
    "Candidate_DPP": ["童子瑋", "沈伯洋", "蘇巧慧", "黃世杰", "—", "—", "陳品安", "何欣純", "陳素月", "溫世政", "劉建國", "—", "蔡易餘", "陳亭妃", "賴瑞隆", "周春米", "林國漳", "—", "陳瑩", "陳光復", "—", "—"],
    "Candidate_KMT": ["謝國樑", "蔣萬安", "李四川", "張善政", "—", "徐欣瑩", "鍾東錦", "江啟臣", "魏平政", "許淑華", "張嘉郡", "—", "—", "謝龍介", "柯志恩", "蘇清泉", "吳宗憲", "游淑貞", "吳秀華", "陳振中", "陳玉珍", "王忠銘"],
    "Candidate_TPP": ["—", "—", "—", "—", "高虹安", "—", "—", "—", "蔡壁如", "—", "—", "張啓楷", "—", "—", "—", "—", "—", "—", "—", "—", "—", "—"],
    "Candidate_Other": ["—", "郭璽", "—", "—", "—", "—", "—", "—", "—", "—", "—", "黃宏成...", "—", "—", "張靜", "—", "—", "張峻/魏嘉賢", "—", "葉竹林", "—", "—"],
    "Base_KMT": [0.48, 0.45, 0.44, 0.42, 0.28, 0.48, 0.50, 0.42, 0.44, 0.48, 0.38, 0.45, 0.32, 0.31, 0.33, 0.35, 0.42, 0.56, 0.57, 0.42, 0.68, 0.75],
    "Base_DPP": [0.36, 0.35, 0.36, 0.34, 0.28, 0.24, 0.24, 0.34, 0.38, 0.34, 0.46, 0.40, 0.52, 0.53, 0.52, 0.49, 0.41, 0.22, 0.21, 0.43, 0.07, 0.03],
    "Base_TPP": [0.16, 0.20, 0.20, 0.24, 0.44, 0.28, 0.26, 0.24, 0.18, 0.18, 0.16, 0.15, 0.16, 0.16, 0.15, 0.16, 0.17, 0.22, 0.22, 0.15, 0.25, 0.22],
    "Tier": ["一級激戰", "六都核心", "六都核心", "六都核心", "一級激戰", "基本盤常勝", "基本盤常勝", "六都核心", "一級激戰", "基本盤常勝", "基本盤常勝", "基本盤常勝", "基本盤常勝", "六都核心", "六都核心", "基本盤常勝", "一級激戰", "基本盤常勝", "基本盤常勝", "一級激戰", "基本盤常勝", "基本盤常勝"],
    "Is_Six_Metro": [0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    "Is_Swing_Zone": [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0],
    "Coalition_Type": ["常規整合", "常規整合", "民調勝出", "常規整合", "完全禮讓", "常規整合", "常規整合", "常規整合", "民調勝出", "常規整合", "常規整合", "民調勝出", "獨大局", "常規整合", "常規整合", "常規整合", "民調勝出", "綠營禮讓無黨", "常規整合", "三方混戰", "常規整合", "常規整合"]
}
df_master = pd.DataFrame(raw_master_data)

party_pro_colors = {"KMT_TPP": "#5E35B1", "DPP": "#2E7D32"}

# 3. 側邊控制面板：全面引入「危機突發變數群」
st.sidebar.header("🎛️ 戰情室常規政局因子")
coalition_efficiency = st.sidebar.slider("🤝 藍白整合轉移效率 %", 40, 100, 75, step=5)
dpp_counter_mobilization = st.sidebar.slider("🟢 民進黨基本盤危機催票率 %", -10, 15, 8, step=1)
middle_voter_drift = st.sidebar.slider("🔸 中間選民體制抗衡偏好", -15, 15, -2, step=1)
young_turnout_weight = st.sidebar.slider("👥 科技城/青年投票率震盪倍數", 0.5, 1.5, 0.95, step=0.05)

st.sidebar.markdown("---")
st.sidebar.header("🚨 突發黑天鵝危機事件矩陣")
event_scenario = st.sidebar.selectbox(
    "🔥 選擇選前震撼彈事件劇本：",
    [
        "🟢 劇本 A：無重大突發事件（回歸基本盤面）",
        "🔵 劇本 B：藍白陣營爆發世紀貪腐弊案（中間選民雪崩）",
        "🟢 劇本 C：綠營高層爆發國安級叛國與桃色醜聞",
        "💥 劇本 D：在野強棒選前三天突遭刺殺襲擊（悲憤狂熱催票）",
        "📉 劇本 E：全台選前爆發極端天災/經濟主權危機"
    ]
)

scandal_impact = st.sidebar.slider("☠️ 政治醜聞引發的支持度流失率 %", 0, 15, 6, step=1)
enthusiasm_boost = st.sidebar.slider("🦅 遇刺/極端事件引發的死忠悲憤催票率 %", 0, 20, 12, step=1)
swing_leverage = st.sidebar.slider("⚡ 邊緣搖擺州對危機事件的敏感放大倍數", 1.0, 2.5, 1.5, step=0.1)

# 4. 聯動演算核心矩陣公式（極端因子動態干涉演算法）
sim_df = df_master.copy()

# 初始化事件干擾權重
kmt_tpp_mod = 0.0
dpp_mod = 0.0
swing_addon = sim_df['Is_Swing_Zone'] * (swing_leverage - 1.0) * 0.02

# 根據選擇的黑天鵝劇本注入量化數值
if "劇本 B" in event_scenario:
    kmt_tpp_mod -= (scandal_impact / 100.0)
    sim_df['Base_KMT'] -= swing_addon
elif "劇本 C" in event_scenario:
    dpp_mod -= (scandal_impact / 100.0)
    sim_df['Base_DPP'] -= swing_addon
elif "劇本 D" in event_scenario:
    kmt_tpp_mod += (enthusiasm_boost / 100.0)
    sim_df['Base_KMT'] += swing_addon * 1.5
elif "劇本 E" in event_scenario:
    dpp_mod += 0.03
    kmt_tpp_mod -= 0.04

# A. 計算民進黨最終得票 (納入常規催票與事件修正)
sim_df['Final_DPP'] = sim_df['Base_DPP'] + (dpp_counter_mobilization * 0.4 / 100.0) + dpp_mod
south_mask = sim_df['County'].isin(["臺南市", "高雄市", "屏東縣", "嘉義縣"])
sim_df.loc[south_mask, 'Final_DPP'] += (dpp_counter_mobilization * 0.15 / 100.0)

# B. 計算藍白合最終得票 (【核心修復】完全對齊 young_turnout_weight 變數名稱)
eff_ratio = coalition_efficiency / 100.0
sim_df['Combined_Opposition'] = (sim_df['Base_KMT'] + (sim_df['Base_TPP'] * young_turnout_weight)) * eff_ratio
sim_df['Combined_Opposition'] += (middle_voter_drift * 0.5 / 100.0) + kmt_tpp_mod

# 北部地緣基礎護城河
north_kmt_stronghold = sim_df['County'].isin(["基隆市", "臺北市", "新北市", "新竹縣", "苗栗縣", "彰化縣"])
sim_df.loc[north_kmt_stronghold, 'Combined_Opposition'] += 0.03

# C. 標準化歸一
total_pool = sim_df['Combined_Opposition'] + sim_df['Final_DPP']
sim_df['Final_Blue_White'] = sim_df['Combined_Opposition'] / total_pool
sim_df['Final_DPP'] /= total_pool

# D. 最終決定性勝負判定
sim_df['Winner'] = np.where(sim_df['Final_Blue_White'] > sim_df['Final_DPP'], 'KMT_TPP', 'DPP')

calc_seats = sim_df.groupby('Winner').size().reindex(party_pro_colors.keys(), fill_value=0)
calc_pops = sim_df.groupby('Winner')['Population'].sum().reindex(party_pro_colors.keys(), fill_value=0)

# ==============================================================================
# 🏙️ 網頁結構：全新 RWD 順暢直向「滾動排版」
# ==============================================================================
st.subheader("📊 第一維度：全台大選宏觀量化指針")

stat_col1, stat_col2, stat_col3 = st.columns([0.34, 0.33, 0.33])

with stat_col1:
    fig_seats = go.Figure()
    fig_seats.add_trace(go.Bar(
        x=["藍白聯合陣線", "民主進步黨"], y=[calc_seats['KMT_TPP'], calc_seats['DPP']], 
        marker_color=[party_pro_colors['KMT_TPP'], party_pro_colors['DPP']], 
        text=[f"<b>{calc_seats['KMT_TPP']} 席</b>", f"<b>{calc_seats['DPP']} 席</b>"], textposition='auto'
    ))
    fig_seats.add_shape(type="line", x0=-0.5, x1=1.5, y0=12, y1=12, line=dict(color="#FF1744", width=3, dash="dash"))
    fig_seats.update_layout(template="plotly_dark", title="預估執政總席次 (紅線過半: 12 席)", height=220, margin=dict(l=10, r=10, t=40, b=10))
    st.plotly_chart(fig_seats, use_container_width=True)

with stat_col2:
    fig_pie = go.Figure(data=[go.Pie(labels=["藍白聯合覆蓋", "綠營執政覆蓋"], values=[calc_pops['KMT_TPP'], calc_pops['DPP']], marker=dict(colors=[party_pro_colors['KMT_TPP'], party_pro_colors['DPP']]), hole=0.45, textinfo='percent+label')])
    fig_pie.update_layout(template="plotly_dark", title="各陣營執政覆蓋總人口比例", height=220, margin=dict(l=10, r=10, t=40, b=10), showlegend=False)
    st.plotly_chart(fig_pie, use_container_width=True)

with stat_col3:
    fig_zones = go.Figure()
    focus_zones = sim_df[(sim_df['Is_Six_Metro'] == 1) | (sim_df['Is_Swing_Zone'] == 1)]
    fig_zones.add_trace(go.Bar(name='藍白聯合軍', x=focus_zones['County'], y=focus_zones['Final_Blue_White']*100, marker_color=party_pro_colors['KMT_TPP']))
    fig_zones.add_trace(go.Bar(name='民主進步黨', x=focus_zones['County'], y=focus_zones['Final_DPP']*100, marker_color=party_pro_colors['DPP']))
    fig_zones.update_layout(template="plotly_dark", title="核心六都與邊緣搖擺區拉鋸得票率 (%)", height=220, margin=dict(l=10, r=10, t=40, b=10), barmode='stack', showlegend=False)
    st.plotly_chart(fig_zones, use_container_width=True)

st.markdown("---")
st.subheader("📋 第二維度：全台 22 縣市危機動態投射大數據報表 (支援直向無限滑動滾動)")

# 建立極度詳細之推演報表
report_df = pd.DataFrame({
    "縣市區域": sim_df['County'],
    "選情熱度": sim_df['Tier'],
    "戰略整合型態": sim_df['Coalition_Type'],
    "🟢 民進黨參選人": sim_df['Candidate_DPP'],
    "🔵 國民黨參選人": sim_df['Candidate_KMT'],
    "⚪ 民眾黨參選人": sim_df['Candidate_TPP'],
    "🟣 其他/無黨籍": sim_df['Candidate_Other'],
    "🔮 系統預估勝出陣營": sim_df['Winner'].map({'KMT_TPP': '💜 藍白聯合軍', 'DPP': '💚 民主進步黨'}),
    "藍白預估得票率": (sim_df['Final_Blue_White'] * 100).round(1).astype(str) + "%",
    "綠營預估得票率": (sim_df['Final_DPP'] * 100).round(1).astype(str) + "%",
    "縣市總投票人口數": sim_df['Population'].map('{:,}'.format)
})

tab1, tab2, tab3, tab4 = st.tabs(["🔥 全台戰情總覽", "🏙️ 六都核心焦點", "⚡ 一級激戰區", "🌲 基本盤常勝軍"])

with tab1:
    st.markdown("##### 💡 提示：點擊各欄位（如藍白得票率）可直接進行全台排序，找出最緊繃的五五波割喉縣市")
    st.dataframe(report_df, height=750, use_container_width=True, hide_index=True)
with tab2:
    st.dataframe(report_df[report_df['選情熱度'] == "六都核心"], height=400, use_container_width=True, hide_index=True)
with tab3:
    st.dataframe(report_df[report_df['選情熱度'] == "一級激戰"], height=400, use_container_width=True, hide_index=True)
with tab4:
    st.dataframe(report_df[report_df['選情熱度'] == "基本盤常勝"], height=600, use_container_width=True, hide_index=True)
