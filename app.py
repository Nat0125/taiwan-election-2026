# ==============================================================================
# 🏛️ HONG KONG 2023 ELECTORAL SIMULATOR: STRICT FIXED MODEL (v17.5)
# ==============================================================================
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# 1. 網頁全螢幕與架構配置
st.set_page_config(layout="wide", page_title="2023 香港選戰模擬中心 v17.5", page_icon="🇭🇰")
st.title("🏛️ 2023 香港地方選舉量化模擬與戰略推演系統 (v17.5)")
st.subheader("📊 民主派 vs 建制派：18 區五五波（5-5）割喉大盤兵棋推演")
st.markdown("---")

# 2. 核心大數據基本盤資料庫（嚴格對齊香港 18 區所有人口數據與長度）
raw_hk_data = {
    "District": ["中西區", "灣仔區", "東區", "南區", "油尖旺區", "深水埗區", "九龍城區", "黃大仙區", "觀塘區", "葵青區", "荃灣區", "屯門區", "元朗區", "北區", "大埔區", "沙田區", "西貢區", "離島區"],
    "Population": [250000, 170000, 530000, 260000, 310000, 430000, 420000, 410000, 680000, 500000, 310000, 490000, 660000, 310000, 310000, 690000, 470000, 180000],
    "Base_Democracy": [0.50] * 18,
    "Base_Establishment": [0.50] * 18,
    "Region": ["香港島", "香港島", "香港島", "香港島", "九龍", "九龍", "九龍", "九龍", "九龍", "新界", "新界", "新界", "新界", "新界", "新界", "新界", "新界", "離島"],
    "Sensitivity_Type": ["中產自主", "中產自主", "鐵票傳統", "基層混合", "核心搖擺", "老區基層", "發展新區", "公屋鐵票", "公屋大本營", "勞工基層", "新市鎮中產", "通勤新區", "鄉事圍村", "跨境邊境", "科技中產", "大型新市鎮", "將軍澳中產", "離島鄉郊"]
}
df_hk = pd.DataFrame(raw_hk_data)
df_hk['Seats'] = 1

party_pro_colors = {"Democracy": "#2E7D32", "Establishment": "#01579B"}

# 3. 側邊控制面板
st.sidebar.header("🎛️ 2023 香港戰情核心控制台")
democracy_wave = st.sidebar.slider("🟢 民主派政治海嘯 / 社會氛圍加成 %", -15, 15, 0, step=1)
establishment_mobilization = st.sidebar.slider("🔵 建制派地區組織 / 街坊同鄉會催票率 %", -15, 15, 0, step=1)
middle_voter_turnout = st.sidebar.slider("🔸 中間游離選民投票意願 (正值利民主派 %)", -10, 10, 0, step=1)
region_leverage = st.sidebar.slider("⚡ 核心激戰區（公屋與新市鎮）民意放大倍數", 1.0, 2.5, 1.0, step=0.1)

# 4. 聯動演算核心矩陣公式
sim_df = df_hk.copy()

dem_mod = democracy_wave / 100.0
est_mod = establishment_mobilization / 100.0
mid_mod = middle_voter_turnout / 100.0

# 計算兩軍最終得票
sim_df['Final_Dem'] = sim_df['Base_Democracy'] + dem_mod + (mid_mod * 0.6)
sim_df['Final_Est'] = sim_df['Base_Establishment'] + est_mod - (mid_mod * 0.4)

# 地緣政治敏感度加權
estate_mask = sim_df['Sensitivity_Type'].isin(["公屋鐵票", "公屋大本營", "勞工基層"])
town_mask = sim_df['Sensitivity_Type'].isin(["新市鎮中產", "大型新市鎮", "將軍澳中產"])

sim_df.loc[estate_mask, 'Final_Est'] += (est_mod * (region_leverage - 1.0) * 0.3)
sim_df.loc[town_mask, 'Final_Dem'] += (dem_mod * (region_leverage - 1.0) * 0.3)

# 數據標準化歸一化
total_share = sim_df['Final_Dem'] + sim_df['Final_Est']
sim_df['Final_Dem'] /= total_share
sim_df['Final_Est'] /= total_share

# 判定勝負
sim_df['Winner'] = np.where(sim_df['Final_Dem'] > sim_df['Final_Est'], 'Democracy', 'Establishment')

calc_seats = sim_df.groupby('Winner').size().reindex(party_pro_colors.keys(), fill_value=0)
calc_pops = sim_df.groupby('Winner')['Population'].sum().reindex(party_pro_colors.keys(), fill_value=0)

# ==============================================================================
# 🏙️ 網頁結構：全新 RWD 順暢直向「滾動排版」
# ==============================================================================
st.subheader("📊 第一維度：2023 香港大選宏觀量化指針")

stat_col1, stat_col2, stat_col3 = st.columns([0.34, 0.33, 0.33])

with stat_col1:
    fig_seats = go.Figure()
    fig_seats.add_trace(go.Bar(
        x=["民主派 陣營", "建制派 陣營"], y=[calc_seats['Democracy'], calc_seats['Establishment']], 
        marker_color=[party_pro_colors['Democracy'], party_pro_colors['Establishment']], 
        text=[f"<b>{calc_seats['Democracy']} 區</b>", f"<b>{calc_seats['Establishment']} 區</b>"], textposition='auto'
    ))
    fig_seats.add_shape(type="line", x0=-0.5, x1=1.5, y0=9, y1=9, line=dict(color="#FF1744", width=3, dash="dash"))
    fig_seats.update_layout(template="plotly_dark", title="預估控制區議會席次 (紅線過半: 10 區)", height=220, margin=dict(l=10, r=10, t=40, b=10))
    st.plotly_chart(fig_seats, use_container_width=True)

with stat_col2:
    fig_pie = go.Figure(data=[go.Pie(labels=["民主派覆蓋人口", "建制派覆蓋人口"], values=[calc_pops['Democracy'], calc_pops['Establishment']], marker=dict(colors=[party_pro_colors['Democracy'], party_pro_colors['Establishment']]), hole=0.45, textinfo='percent+label')])
    fig_pie.update_layout(template="plotly_dark", title="各陣營控制區域總人口比例", height=220, margin=dict(l=10, r=10, t=40, b=10), showlegend=False)
    st.plotly_chart(fig_pie, use_container_width=True)

with stat_col3:
    fig_zones = go.Figure()
    urban_df = sim_df[sim_df['Region'].isin(["香港島", "九龍"])]
    fig_zones.add_trace(go.Bar(name='民主派', x=urban_df['District'], y=urban_df['Final_Dem']*100, marker_color=party_pro_colors['Democracy']))
    fig_zones.add_trace(go.Bar(name='建制派', x=urban_df['District'], y=urban_df['Final_Est']*100, marker_color=party_pro_colors['Establishment']))
    fig_zones.update_layout(template="plotly_dark", title="市區核心（港島/九龍）兩軍得票率拉鋸 (%)", height=220, margin=dict(l=10, r=10, t=40, b=10), barmode='stack', showlegend=False)
    st.plotly_chart(fig_zones, use_container_width=True)

st.markdown("---")
st.subheader("📋 第二維度：香港 18 區民意動態投射大數據報表 (支援直向無限滑動滾動)")

# 建立極度詳細之香港 18 區推演報表
report_df = pd.DataFrame({
    "區議會行政區": sim_df['District'],
    "地理大區分類": sim_df['Region'],
    "地緣選民特性": sim_df['Sensitivity_Type'],
    "🔮 系統預估勝出陣營": sim_df['Winner'].map({'Democracy': '💚 民主派陣營', 'Establishment': '🔵 建制派陣營'}),
    "民主派預估得票率": (sim_df['Final_Dem'] * 100).round(1).astype(str) + "%",
    "建制派預估得票率": (sim_df['Final_Est'] * 100).round(1).astype(str) + "%",
    "區域總常住人口數": sim_df['Population'].map('{:,}'.format)
})

tab1, tab2, tab3, tab4 = st.tabs(["🔥 全港 18 區總覽", "🏙️ 香港島核心", "⚡ 九龍核心戰區", "🌲 新界及離島大盤"])

with tab1:
    st.markdown("##### 💡 操盤提示：目前基本盤完全對齊 50%:50%！任何一端只要有 1% 的細微游離，就會引發骨牌翻盤效應。")
    st.dataframe(report_df, height=650, use_container_width=True, hide_index=True)
with tab2:
    st.dataframe(report_df[report_df['地理大區分類'] == "香港島"], height=400, use_container_width=True, hide_index=True)
with tab3:
    st.dataframe(report_df[report_df['地理大區分類'] == "九龍"], height=400, use_container_width=True, hide_index=True)
with tab4:
    st.dataframe(report_df[report_df['地理大區分類'].isin(["新界", "離島"])], height=400, use_container_width=True, hide_index=True)
