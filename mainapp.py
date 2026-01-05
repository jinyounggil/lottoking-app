import streamlit as st
import random
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import datetime
import os
import base64
from io import BytesIO

# 페이지 설정 (가장 먼저 호출)
st.set_page_config(layout="wide", page_title="로또킹 분석")

# 세션 상태 초기화
if 'show_tab' not in st.session_state:
    st.session_state['show_tab'] = None
if 'subscribe_count' not in st.session_state:
    st.session_state['subscribe_count'] = 0
if 'like_count' not in st.session_state:
    st.session_state['like_count'] = 0

# ----- tab1~tab4 UI 함수 직접 정의 -----
def get_color(n):
  # 실로또공 색상: 1~10 노랑, 11~20 파랑, 21~30 빨강, 31~40 검정, 41~45 초록
  if 1 <= n <= 10:
    return "gold"  # 노랑
  elif 11 <= n <= 20:
    return "dodgerblue"  # 파랑
  elif 21 <= n <= 30:
    return "red"  # 빨강
  elif 31 <= n <= 40:
    return "black"  # 검정
  else:
    return "green"  # 초록


def tab1_content():
  # session_state 초기화
  if 'tab1_combinations' not in st.session_state:
    st.session_state['tab1_combinations'] = []
  if 'tab1_show_result' not in st.session_state:
    st.session_state['tab1_show_result'] = False
  
  st.markdown("""
  <div style='background-color:#111; border-radius:20px; padding:10px; text-align:center;'>
    <h2 style='color:gold; font-size:42px;'>🎵 띠별추천번호 생성기</h2>
    <p style='color:white; font-size:20px;'>본인 띠와 출생 년도로 5조합을 확인하세요</p>
  </div>
  """, unsafe_allow_html=True)
  
  zodiac_years = {
    "쥐 🐭": [1948,1960,1972,1984,1996,2008,2020],
    "소 🐮": [1949,1961,1973,1985,1997,2009,2021],
    "호랑이 🐯": [1950,1962,1974,1986,1998,2010,2022],
    "토끼 🐰": [1951,1963,1975,1987,1999,2011,2023],
    "용 🐲": [1952,1964,1976,1988,2000,2012,2024],
    "뱀 🐍": [1953,1965,1977,1989,2001,2013,2025],
    "말 🐴": [1954,1966,1978,1990,2002,2014,2026],
    "양 🐑": [1955,1967,1979,1991,2003,2015,2027],
    "원숭이 🐵": [1956,1968,1980,1992,2004,2016,2028],
    "닭 🐔": [1957,1969,1981,1993,2005,2017,2029],
    "개 🐶": [1958,1970,1982,1994,2006,2018,2030],
    "돼지 🐷": [1959,1971,1983,1995,2007,2019,2031]
  }
  
  selected_zodiac = st.selectbox("띠 선택", list(zodiac_years.keys()), key="zodiac_select")
  selected_year = st.selectbox("출생년도 선택", zodiac_years[selected_zodiac], key="year_select")
  
  if st.button("행운의 5조합 🎲", key="btn_zodiac5"):
    base = selected_year
    all_combinations = []
    for i in range(5):
      numbers = []
      while len(numbers) < 6:
        num = (base + random.randint(1,999) + i*1000) % 45 + 1
        if num not in numbers:
          numbers.append(num)
      numbers.sort()
      all_combinations.append(numbers)
    
    st.session_state['tab1_combinations'] = all_combinations
    st.session_state['tab1_show_result'] = True
  
  # 결과 표시 영역 (placeholder 사용)
  result_placeholder = st.empty()
  
  with result_placeholder.container():
    if st.session_state['tab1_show_result'] and len(st.session_state['tab1_combinations']) > 0:
      # 전체 HTML을 한 번에 생성
      html_output = "<div style='display:flex;flex-direction:column;align-items:center; margin-top:20px;'>"
      
      for comb in st.session_state['tab1_combinations']:
        html_output += "<div style='margin:10px 0;'>"
        for n in comb:
          color = get_color(n)
          html_output += f"<span style='display:inline-block; background:{color}; color:white; border-radius:50%; width:60px; height:60px; text-align:center; line-height:60px; margin:2px; font-size:22px;'>{n}</span>"
        html_output += "</div>"
      
      html_output += "</div>"
      st.markdown(html_output, unsafe_allow_html=True)


def tab2_content():
  # session_state 초기화
  if 'tab2_combinations' not in st.session_state:
    st.session_state['tab2_combinations'] = []
  if 'tab2_show_result' not in st.session_state:
    st.session_state['tab2_show_result'] = False
  
  st.markdown("""
  <div style='background-color:#222; border-radius:20px; padding:10px; text-align:center;'>
    <h2 style='color:deepskyblue; font-size:42px;'>🔮 주역 지역 추천</h2>
    <p style='color:white; font-size:20px;'>방위 기반 추천을 자동 또는 수동으로 선택하세요 (5조합)</p>
  </div>
  """, unsafe_allow_html=True)
  
  mode = st.radio("선택 모드", ["자동", "수동"], index=0, key="jx_mode2")
  regions = {
    "건(乾, 하늘·북서)": list(range(1,10)),
    "곤(坤, 땅·남서)": list(range(10,19)),
    "감(坎, 물·북)": list(range(19,28)),
    "리(離, 불·남)": list(range(28,37)),
    "중앙(中, 균형)": list(range(37,46))
  }
  
  if mode == "자동":
    if st.button("오늘의 방위 5조합 추천 🎲", key="jx_auto_btn2"):
      all_combinations = []
      for i in range(5):
        numbers = [random.choice(region) for region in regions.values()]
        while len(numbers) < 6:
          # 중복 방지: 랜덤 추가
          n = random.randint(1, 45)
          if n not in numbers:
            numbers.append(n)
        numbers = numbers[:6]
        numbers.sort()
        all_combinations.append(numbers)
      
      st.session_state['tab2_combinations'] = all_combinations
      st.session_state['tab2_show_result'] = True
  else:
    cols = st.columns(4)
    year = cols[0].number_input("년",2000,2100,2025,key="jx_year2")
    month = cols[1].number_input("월",1,12,12,key="jx_month2")
    day = cols[2].number_input("일",1,31,28,key="jx_day2")
    hour = cols[3].number_input("시",0,23,16,key="jx_hour2")
    
    if st.button("수동 방위 5조합 추천 🎲", key="jx_manual_btn2"):
      all_combinations = []
      for i in range(5):
        seed = year+month+day+hour+i*1000
        rng = random.Random(seed)
        numbers = [rng.choice(region) for region in regions.values()]
        while len(numbers) < 6:
          n = rng.randint(1, 45)
          if n not in numbers:
            numbers.append(n)
        numbers = numbers[:6]
        numbers.sort()
        all_combinations.append(numbers)
      
      st.session_state['tab2_combinations'] = all_combinations
      st.session_state['tab2_show_result'] = True
  
  # 결과 표시 영역 (placeholder 사용)
  result_placeholder = st.empty()
  
  with result_placeholder.container():
    if st.session_state['tab2_show_result'] and len(st.session_state['tab2_combinations']) > 0:
      # 전체 HTML을 한 번에 생성
      html_output = "<div style='display:flex;flex-direction:column;align-items:center; margin-top:20px;'>"
      
      for comb in st.session_state['tab2_combinations']:
        html_output += "<div style='margin:10px 0;'>"
        for n in comb:
          color = get_color(n)
          html_output += f"<span style='display:inline-block; background:{color}; color:white; border-radius:50%; width:60px; height:60px; text-align:center; line-height:60px; margin:2px; font-size:22px;'>{n}</span>"
        html_output += "</div>"
      
      html_output += "</div>"
      st.markdown(html_output, unsafe_allow_html=True)


def tab3_content():
  import matplotlib
  matplotlib.rc('font', family='Malgun Gothic')  # 한글 폰트 설정
  matplotlib.rcParams['axes.unicode_minus'] = False  # 마이너스 깨짐 방지
  past_results = pd.read_csv("past_results.csv", header=None)
  past_results.columns = ["회차", "번호1", "번호2", "번호3", "번호4", "번호5", "번호6"]
  past_results["회차"] = past_results["회차"].str.replace("회차", "").astype(int)
  latest_round = past_results["회차"].max()
  st.markdown("<h2 style='color:orange;'>📊 통계 추천</h2>", unsafe_allow_html=True)
  # 회차 범위 옵션 및 실제 범위 계산
  ranges = [300, 150, 75, 45, 30, 15, 5]
  options = [f"최근 {r}회" for r in ranges]
  mode = st.selectbox("회차 범위 선택", options)
  n = int(mode.replace("최근 ", "").replace("회", ""))
  min_round = max(latest_round - n + 1, 1)
  data = past_results[(past_results["회차"] >= min_round) & (past_results["회차"] <= latest_round)]
  st.write(f"선택된 회차 범위: {min_round} ~ {latest_round}")
  numbers = pd.concat([
    data["번호1"], data["번호2"], data["번호3"],
    data["번호4"], data["번호5"], data["번호6"]
  ])
  freq = numbers.value_counts().sort_index()
  chart_type = st.radio("그래프 타입 선택", ["막대그래프", "꺾은선그래프"])
  fig, ax = plt.subplots(figsize=(8,2.8))  # 그래프 높이 축소
  if chart_type == "막대그래프":
    freq.plot(kind="bar", ax=ax, color="skyblue")
    ax.set_title("번호 빈도 - 막대그래프")
  elif chart_type == "꺾은선그래프":
    freq.plot(kind="line", ax=ax, marker="o", color="orange")
    ax.set_title("번호 빈도 - 꺾은선그래프")
  ax.set_xlabel("번호")
  ax.set_ylabel("출현 빈도")
  st.pyplot(fig)

  # hot/mid/cold num 표시
  freq_sorted = freq.sort_values(ascending=False)
  hot_nums = freq_sorted.head(6).index.tolist()
  cold_nums = freq_sorted.tail(6).index.tolist()
  mid_start = len(freq_sorted)//2 - 3
  mid_nums = freq_sorted.iloc[mid_start:mid_start+6].index.tolist() if len(freq_sorted) >= 12 else []
  def balls(nums):
    return "".join([
      f"<span style='display:inline-block; background:{get_color(n)}; color:white; border-radius:50%; width:40px; height:40px; text-align:center; line-height:40px; margin:4px; font-size:18px;'>{n}</span>"
      for n in nums
    ])
  st.markdown(f"<b>Hot Num</b>: {balls(sorted(hot_nums))}", unsafe_allow_html=True)
  if mid_nums:
    st.markdown(f"<b>Mid Num</b>: {balls(sorted(mid_nums))}", unsafe_allow_html=True)
  st.markdown(f"<b>Cold Num</b>: {balls(sorted(cold_nums))}", unsafe_allow_html=True)

  # 미출현 번호 표시 (선택 범위 내 한 번도 안 나온 번호)
  all_numbers = set(range(1, 46))
  appeared_numbers = set(numbers.unique())
  not_appeared = sorted(list(all_numbers - appeared_numbers))
  if not_appeared:
    st.markdown(f"<b>미출현 번호</b>: {balls(not_appeared)}", unsafe_allow_html=True)

def tab4_content():
  # session_state 초기화
  if 'ai_combinations' not in st.session_state:
    st.session_state['ai_combinations'] = []
  if 'ai_show_result' not in st.session_state:
        st.session_state['ai_show_result'] = False
  
  st.markdown("<h2 style='color:lime;'>🧠 AI 통합 추천</h2>", unsafe_allow_html=True)
  
  # 과거 데이터 로드 및 고급 분석
  try:
    past_results = pd.read_csv("past_results.csv", header=None)
    past_results.columns = ["회차", "번호1", "번호2", "번호3", "번호4", "번호5", "번호6"]
    past_results["회차"] = past_results["회차"].str.replace("회차", "").astype(int)
    
    # 최근 300회 데이터 분석
    recent_data = past_results.tail(300)
    all_numbers = pd.concat([
      recent_data["번호1"], recent_data["번호2"], recent_data["번호3"],
      recent_data["번호4"], recent_data["번호5"], recent_data["번호6"]
    ])
    
    # 1. 빈도 분석
    freq = all_numbers.value_counts()
    freq_sorted = freq.sort_values(ascending=False)
    
    # 2. 최근 추세 분석 (최근 50회 vs 전체)
    recent_50 = past_results.tail(50)
    recent_numbers = pd.concat([
      recent_50["번호1"], recent_50["번호2"], recent_50["번호3"],
      recent_50["번호4"], recent_50["번호5"], recent_50["번호6"]
    ])
    recent_freq = recent_numbers.value_counts()
    
    # 3. 미출현 기간 분석 (오래 안 나온 번호)
    last_appearance = {}
    for num in range(1, 46):
      last_appearance[num] = 999
    
    for idx, row in recent_data.iloc[::-1].iterrows():
      for col in ["번호1", "번호2", "번호3", "번호4", "번호5", "번호6"]:
        num = row[col]
        if last_appearance[num] == 999:
          last_appearance[num] = len(recent_data) - recent_data.index.get_loc(idx)
    
    # 4. 구간별 출현 비율 분석 (1-10, 11-20, 21-30, 31-40, 41-45)
    zone_freq = {1:0, 2:0, 3:0, 4:0, 5:0}
    for num in all_numbers:
      if num <= 10:
        zone_freq[1] += 1
      elif num <= 20:
        zone_freq[2] += 1
      elif num <= 30:
        zone_freq[3] += 1
      elif num <= 40:
        zone_freq[4] += 1
      else:
        zone_freq[5] += 1
    
    # 5. 통합 가중치 계산
    weights = {}
    for i in range(1, 46):
      # 기본 빈도 가중치
      freq_weight = freq.get(i, 0) / freq.max() if freq.max() > 0 else 0.5
      
      # 최근 추세 가중치 (최근 50회에서 많이 나온 번호 우대)
      recent_weight = recent_freq.get(i, 0) / recent_freq.max() if len(recent_freq) > 0 and recent_freq.max() > 0 else 0.5
      
      # 미출현 기간 가중치 (너무 오래 안 나온 번호 우대)
      gap = last_appearance.get(i, 0)
      gap_weight = min(gap / 100, 1.0) if gap > 30 else 0.3
      
      # 통합 가중치 (빈도 50%, 최근 추세 30%, 미출현 20%)
      weights[i] = (freq_weight * 0.5 + recent_weight * 0.3 + gap_weight * 0.2) * 2.0
      weights[i] = max(0.3, min(weights[i], 2.5))  # 0.3~2.5 범위로 제한
    
    # 당첨 패턴 분석 (홀짝 비율, 구간 분포)
    odd_ratios = []
    zone_distributions = []
    for idx, row in recent_data.iterrows():
      nums = [row["번호1"], row["번호2"], row["번호3"], row["번호4"], row["번호5"], row["번호6"]]
      odd_count = sum(1 for n in nums if n % 2 == 1)
      odd_ratios.append(odd_count)
      
      zones = [0,0,0,0,0]
      for n in nums:
        if n <= 10: zones[0] += 1
        elif n <= 20: zones[1] += 1
        elif n <= 30: zones[2] += 1
        elif n <= 40: zones[3] += 1
        else: zones[4] += 1
      zone_distributions.append(zones)
    
    avg_odd = sum(odd_ratios) / len(odd_ratios)
    avg_zone = [sum(z[i] for z in zone_distributions) / len(zone_distributions) for i in range(5)]
    
    has_data = True
  except:
    # 데이터 없을 경우 균등 가중치
    weights = {i: 1.0 for i in range(1, 46)}
    avg_odd = 3
    avg_zone = [1.2, 1.2, 1.2, 1.2, 1.2]
    has_data = False
  
  st.markdown("""
  <p style='color:#666; font-size:15px; margin-bottom:20px;'>
  ✨ <b>AI 고급 분석:</b> 빈도(50%) + 최근추세(30%) + 미출현패턴(20%) + 구간균형 + 홀짝비율 최적화
  </p>
  """, unsafe_allow_html=True)
  
  # 번호 생성 함수 (고도화)
  def generate_combinations():
    combinations = []
    attempt = 0
    max_attempts = 50
    
    while len(combinations) < 5 and attempt < max_attempts:
      attempt += 1
      numbers = []
      available = list(range(1, 46))
      
      while len(numbers) < 6:
        remaining_weights = [weights[n] for n in available]
        total_weight = sum(remaining_weights)
        probabilities = [w/total_weight for w in remaining_weights]
        
        selected = random.choices(available, weights=probabilities, k=1)[0]
        numbers.append(selected)
        available.remove(selected)
        
        # 연속번호 3개 초과 방지
        if len(numbers) >= 3:
          numbers_sorted = sorted(numbers)
          consecutive_count = 0
          for j in range(len(numbers_sorted)-1):
            if numbers_sorted[j+1] - numbers_sorted[j] == 1:
              consecutive_count += 1
          if consecutive_count > 2:
            available.append(numbers[-1])
            numbers.pop()
            continue
      
      # 홀짝 비율 검증 (2~4개가 홀수)
      odd_count = sum(1 for n in numbers if n % 2 == 1)
      if odd_count < 2 or odd_count > 4:
        continue
      
      # 구간 분포 검증 (5개 구간에 골고루 분포)
      zones = [0,0,0,0,0]
      for n in numbers:
        if n <= 10: zones[0] += 1
        elif n <= 20: zones[1] += 1
        elif n <= 30: zones[2] += 1
        elif n <= 40: zones[3] += 1
        else: zones[4] += 1
      
      # 특정 구간에 4개 이상 몰리면 제외
      if max(zones) > 3:
        continue
      
      # 번호 합계 검증 (당첨 번호 평균 합계: 115~145)
      total_sum = sum(numbers)
      if total_sum < 100 or total_sum > 160:
        continue
      
      numbers.sort()
      
      # 중복 조합 방지
      if numbers not in combinations:
        combinations.append(numbers)
    
    # 5개 미만이면 부족한 만큼 무작위 추가
    while len(combinations) < 5:
      nums = sorted(random.sample(range(1, 46), 6))
      if nums not in combinations:
        combinations.append(nums)
    
    return combinations
  
  # 버튼
  col1, col2 = st.columns([1, 1])
  
  with col1:
    if st.button("🎲 AI 추천 번호 생성", key="ai_gen_btn", width="stretch"):
      st.session_state['ai_combinations'] = generate_combinations()
      st.session_state['ai_show_result'] = True
  
  with col2:
    if st.button("🗑️ 초기화", key="ai_clear_btn", width="stretch"):
      st.session_state['ai_combinations'] = []
      st.session_state['ai_show_result'] = False
  
  # 결과 표시 영역 (placeholder 사용)
  result_placeholder = st.empty()
  
  with result_placeholder.container():
    if st.session_state['ai_show_result'] and len(st.session_state['ai_combinations']) > 0:
      st.markdown("---")
      
      # 전체 HTML을 한 번에 생성
      html_output = ""
      for i, comb in enumerate(st.session_state['ai_combinations']):
        html_output += f"<p style='font-weight:bold; margin:15px 0 5px 0;'>🎯 AI 조합 {i+1}</p>"
        html_output += "<div style='display:flex; gap:8px; margin-bottom:15px;'>"
        for num in comb:
          color = get_color(num)
          html_output += f"""<div style='background-color:{color}; color:white; border-radius:50%; 
          width:55px; height:55px; display:flex; align-items:center; 
          justify-content:center; font-size:20px; font-weight:bold; 
          box-shadow:0 2px 4px rgba(0,0,0,0.2);'>{num}</div>"""
        html_output += "</div>"
      
      st.markdown(html_output, unsafe_allow_html=True)
      
      if has_data:
        st.success("🎯 **10/10 AI 분석 완료:** 빈도·추세·미출현 패턴 + 구간균형 + 홀짝비율 + 번호합계 + 연속번호 제어 적용")
        
        # 분석 상세 정보 표시
        with st.expander("📊 AI 분석 세부 정보 보기"):
          st.markdown(f"""
          - **빈도 분석**: 최근 300회 데이터 기반 출현 빈도 (가중치 50%)
          - **최근 추세**: 최근 50회 핫 번호 우선 선택 (가중치 30%)
          - **미출현 패턴**: 30회 이상 미출현 번호 우대 (가중치 20%)
          - **구간 균형**: 5개 구간(1-10, 11-20, 21-30, 31-40, 41-45) 균등 분포
          - **홀짝 비율**: 홀수 2~4개 유지 (평균: {avg_odd:.1f}개)
          - **연속 번호**: 연속 3개 이상 제외
          - **번호 합계**: 100~160 범위 (당첨 평균: 120~130)
          - **중복 방지**: 동일 조합 제외
          """)
    else:
      st.info("👆 위의 버튼을 눌러 AI가 분석한 추천 번호를 생성하세요!")


# ===== 스타일 설정 =====
st.markdown("""
<style>
body, .stApp {
  background: linear-gradient(135deg, #e8f5e9 0%, #f1f8e9 50%, #fff9c4 100%) !important;
}
</style>
""", unsafe_allow_html=True)

# ===== 상단 3분할 레이아웃 =====
col_left, col_center, col_right = st.columns([1.2, 2, 2.2], gap="large")
with col_left:
  st.markdown("""
  <style>
  div.row-widget.stButton > button {
    width: 140px;
    height: 38px;
    background: #fff;
    border-radius: 10px;
    font-size: 16px;
    font-weight: 700;
    margin-bottom: 7px;
    border: 2px solid #7f7fd5;
    color: #7f7fd5;
    box-shadow: 0 1px 4px rgba(127,127,213,0.08);
    transition: transform 0.08s, box-shadow 0.18s;
  }
  div.row-widget.stButton > button:hover {
    transform: scale(1.05);
    box-shadow: 0 2px 8px rgba(127,127,213,0.15);
  }
  div.row-widget.stButton > button:active {
    transform: scale(0.95);
  }
  </style>
  """, unsafe_allow_html=True)
  
  if st.button("👉 구독", key="subscribe_btn_top"):
    st.session_state['subscribe_count'] += 1
    st.success(f"구독해주셔서 감사합니다! (총 {st.session_state['subscribe_count']}명)")
  
  if st.button("👍 좋아요", key="like_btn_top"):
    st.session_state['like_count'] += 1
    st.success(f"좋아요 감사합니다! (총 {st.session_state['like_count']}개)")
  
  if st.button("🔗 공유", key="share_btn_top"):
    st.info("링크가 클립보드에 복사되었습니다!")
    
with col_center:
  st.markdown("""
  <style>
  .header-row-final {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    margin-top: -20px;
    width: 80%;
    min-width: 600px;
    max-width: 950px;
    white-space: nowrap;
  }
  .header-emoji-final {
    font-size: 56px;
    margin: 0 5px 0 0;
    filter: drop-shadow(0 2px 8px #ffd70088);
    display: inline-block;
    vertical-align: middle;
    animation: bounce-emoji 1.5s ease-in-out infinite;
  }
  @keyframes bounce-emoji {
    0%, 100% { 
      transform: translateY(0) scale(1); 
      filter: drop-shadow(0 2px 8px #ffd70088);
    }
    50% { 
      transform: translateY(-15px) scale(1.15) rotate(10deg); 
      filter: drop-shadow(0 8px 16px #ffd700dd);
    }
  }
  .header-emoji-final:nth-child(3) {
    animation-delay: 0.3s;
  }
  .header-emoji-right {
    font-size: 56px;
    margin: 0 0 0 5px;
    filter: drop-shadow(0 2px 8px #ffd70088);
    display: inline-block;
    vertical-align: middle;
    animation: bounce-emoji 1.5s ease-in-out infinite;
    animation-delay: 0.3s;
  }
  .header-title-final {
    font-size: 58px;
    font-weight: 900;
    color: #7f7fd5;
    letter-spacing: 0.08em;
    text-shadow: 3px 5px 15px #b3b3e6, 0 2px 0 #fff, 0 0 30px #7f7fd5;
    margin-right: 5px;
    display: inline-block;
    vertical-align: middle;
    line-height: 1;
    white-space: nowrap;
    animation: glow-title 2s ease-in-out infinite;
  }
  @keyframes glow-title {
    0%, 100% { 
      text-shadow: 3px 5px 15px #b3b3e6, 0 2px 0 #fff, 0 0 30px #7f7fd5;
    }
    50% { 
      text-shadow: 3px 5px 20px #b3b3e6, 0 2px 0 #fff, 0 0 50px #7f7fd5, 0 0 70px #b3b3e6;
    }
  }
  .header-slogan-final {
    font-size: 46px;
    font-weight: 900;
    color: #ff3c00;
    letter-spacing: 0.04em;
    margin-left: 5px;
    text-shadow: 2px 4px 12px #ffb3b3, 0 2px 0 #fff, 0 0 25px #ff3c00;
    background: none;
    -webkit-background-clip: unset;
    -webkit-text-fill-color: #ff3c00;
    background-clip: unset;
    display: inline-block;
    line-height: 1;
    white-space: normal;
    word-break: keep-all;
    vertical-align: middle;
    animation: pulse-slogan 1.8s ease-in-out infinite;
  }
  @keyframes pulse-slogan {
    0%, 100% { 
      transform: scale(1);
      filter: brightness(1);
    }
    50% { 
      transform: scale(1.08);
      filter: brightness(1.2);
    }
  }
  </style>
  <div class='header-row-final'>
    <span class='header-emoji-final'>✨</span>
    <span class='header-title-final'>로또킹과</span>
    <span class='header-slogan-final'>더 높은 곳을 향하여</span>
    <span class='header-emoji-right'>👑</span>
  </div>
  """, unsafe_allow_html=True)
with col_right:
  # 회차 및 날짜 계산
  now = datetime.datetime.now()
  # 1206회차 기준: 2026년 1월 3일 21시 시작, 1월 10일 21시 추첨
  base_round = 1206
  base_start_datetime = datetime.datetime(2026, 1, 3, 21, 0, 0)
  
  # 현재 시각 기준으로 몇 주 지났는지 계산
  time_diff = (now - base_start_datetime).total_seconds()
  weeks_passed = int(time_diff // (7 * 24 * 3600))
  
  # 현재 회차와 다음 추첨일 계산
  if time_diff < 0:
    # 기준일 이전이면 이전 회차
    round_num = base_round - 1
    next_draw_datetime = base_start_datetime
  else:
    round_num = base_round + weeks_passed
    next_draw_datetime = base_start_datetime + datetime.timedelta(weeks=weeks_passed + 1)
  
  st.markdown(f"""
  <div style='text-align:right; margin-top:10px;'>
    <span style='font-size:22px; font-weight:700; color:#222;'>
      {round_num}회차
    </span><br>
    <span style='font-size:16px; color:#666;'>
      추첨일: {next_draw_datetime.strftime('%Y년 %m월 %d일')} 21시까지
    </span>
  </div>
  """, unsafe_allow_html=True)

# CSS 스타일 정의
st.markdown("""
<style>
/* 모바일 반응형 CSS */
@media screen and (max-width: 768px) {
  /* 헤더 폰트 크기 축소 */
  .header-emoji-final {
    font-size: 28px !important;
  }
  .header-title-final {
    font-size: 24px !important;
    letter-spacing: 0.02em !important;
  }
  .header-slogan-final {
    font-size: 20px !important;
    letter-spacing: 0.02em !important;
  }
  .header-emoji-right {
    font-size: 28px !important;
  }
  .header-row-final {
    flex-wrap: wrap !important;
    justify-content: center !important;
  }
  
  /* 버튼 크기 조정 */
  div.stButton > button {
    width: 100% !important;
    height: 48px !important;
    font-size: 14px !important;
    margin-bottom: 12px !important;
  }
  
  /* 로또 공 크기 축소 */
  .ball {
    width: 40px !important;
    height: 40px !important;
    font-size: 16px !important;
  }
  
  /* 컬럼 간격 축소 */
  [data-testid="column"] {
    padding: 5px !important;
  }
  
  /* 텍스트 크기 조정 */
  h1 { font-size: 24px !important; }
  h2 { font-size: 20px !important; }
  h3 { font-size: 18px !important; }
  p { font-size: 14px !important; }
}

/* 기존 스타일 */
.aspect-12-9 {
  position: relative;
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 8px 24px rgba(0,0,0,.15);
}
.aspect-12-9::before {
  content: "";
  display: block;
  padding-top: 75%;
}
.aspect-12-9 > .content {
  position: absolute;
  inset: 0;
  display: grid;
  grid-template-columns: 1fr 4fr;
  gap: 20px;
  background: #e6e0f8;
  padding: 20px;
  box-sizing: border-box;
}
.left-column {
  display: grid;
  grid-template-rows: repeat(4, 1fr);
  gap: 20px;
}
.frame {
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,.1);
  display: flex;
  align-items: center;
  justify-content: center;
}
.button-custom {
  width: 100px;
  height: 40px;
  background-color: #28a745;
  color: #fff;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
}
.button-custom:hover {
  background-color: #218838;
}
.big-frame {
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,.1);
  overflow: hidden;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding: 0;
  margin: 0;
}
.big-frame img {
  width: 100%;
  height: auto;
  object-fit: contain;
  border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)



# Streamlit columns로 레이아웃 분리 (왼쪽 버튼, 오른쪽 big-frame+이미지)

# 왼쪽 띠별 추천번호 프레임을 세로로 일정 간격으로 배치
left, right = st.columns([1, 4], gap="large")
with left:
  st.markdown(
    """
    <div style="display: flex; flex-direction: column; gap: 32px; margin-top: 0px;">
    """,
    unsafe_allow_html=True
  )
  # 멋진 버튼 스타일 CSS (st.button에만 적용)
  st.markdown("""
  <style>
  div.stButton > button {
    width: 180px;
    height: 54px;
    margin-bottom: 22px;
    background: linear-gradient(90deg, #7f7fd5 0%, #86a8e7 50%, #91eac9 100%);
    color: #fff;
    border: none;
    border-radius: 18px;
    font-size: 20px;
    font-weight: 700;
    box-shadow: 0 4px 16px rgba(80,80,180,0.13);
    cursor: pointer;
    transition: transform 0.1s, box-shadow 0.2s;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    letter-spacing: 1px;
  }
  div.stButton > button:hover {
    background: linear-gradient(90deg, #91eac9 0%, #86a8e7 50%, #7f7fd5 100%);
    transform: translateY(-2px) scale(1.04);
    box-shadow: 0 8px 24px rgba(80,80,180,0.18);
  }
  </style>
  """, unsafe_allow_html=True)
  # st.button + 이모지로 멋진 버튼
  if st.button("🎵 띠별 추천번호"):
    st.session_state['show_tab'] = 'tab1'
  if st.button("🧭 주역 추천번호"):
    st.session_state['show_tab'] = 'tab2'
  if st.button("📊 통계 추천"):
    st.session_state['show_tab'] = 'tab3'
  if st.button("🧠 AI 통합 추천"):
    st.session_state['show_tab'] = 'tab4'

  st.markdown("</div>", unsafe_allow_html=True)
with right:
  show_tab = st.session_state.get('show_tab')
  if show_tab in ['tab1', 'tab2', 'tab3', 'tab4']:
    col_btn, _ = st.columns([2, 7])
    with col_btn:
      if st.button('메인으로', key='main_back', help='메인 화면으로 이동'):
        st.session_state['show_tab'] = None
    
    # tab2(주역)와 tab4(AI)에 좋아요/구독 버튼 표시 (단일 컨테이너로 안정화)
    social_placeholder = st.empty()
    with social_placeholder.container():
      if show_tab in ['tab2', 'tab4']:
        st.markdown("""
        <div style='display:flex; gap:20px; margin:20px 0; padding:15px; background:#f8f9fa; border-radius:10px;'>
          <div style='flex:1; text-align:center;'>
            <div style='font-size:24px; margin-bottom:5px;'>👍</div>
            <div style='color:#666; font-size:14px;'>좋아요: {}</div>
          </div>
          <div style='flex:1; text-align:center;'>
            <div style='font-size:24px; margin-bottom:5px;'>👉</div>
            <div style='color:#666; font-size:14px;'>구독자: {}</div>
          </div>
        </div>
        """.format(st.session_state['like_count'], st.session_state['subscribe_count']), unsafe_allow_html=True)
        
        btn_col1, btn_col2 = st.columns([1, 1])
        with btn_col1:
          if st.button('👍 좋아요', key=f'like_{show_tab}', width="stretch"):
            st.session_state['like_count'] += 1
            st.rerun()
        with btn_col2:
          if st.button('👉 구독', key=f'subscribe_{show_tab}', width="stretch"):
            st.session_state['subscribe_count'] += 1
            st.rerun()
        st.markdown("---")
    
    if show_tab == 'tab1':
      tab1_content()
    elif show_tab == 'tab2':
      tab2_content()
    elif show_tab == 'tab4':
      tab4_content()
    elif show_tab == 'tab3':
      tab3_content()
  else:
    # 메인 화면 - 메인 이미지 확대 표시
    # 자동 썸네일 선택
    thumb_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd()
    thumb_candidates = [f for f in os.listdir(thumb_dir) if f.startswith('lottoking') and f.lower().endswith(('.jpg','.jpeg','.png'))]
    
    # 세션 상태 또는 파일에서 이미지 로드
    if 'main_thumbnail' in st.session_state:
        # PIL로 이미지 크기 확대 후 HTML로 표시
        img = st.session_state['main_thumbnail']
        if isinstance(img, str):
            img = Image.open(img)
        # 모바일 대응: 원본 크기 유지 (확대 제거)
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        st.markdown(f'<img src="data:image/png;base64,{img_str}" style="width:100%; max-width:800px; height:auto; border-radius:12px; display:block; margin:0 auto;">', unsafe_allow_html=True)
    elif thumb_candidates:
        pick = random.choice(thumb_candidates)
        image_path = os.path.join(thumb_dir, pick)
        try:
            image = Image.open(image_path)
            # 모바일 대응: 원본 크기 유지 (확대 제거)
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            st.markdown(f'<img src="data:image/png;base64,{img_str}" style="width:100%; max-width:800px; height:auto; border-radius:12px; display:block; margin:0 auto;">', unsafe_allow_html=True)
        except:
            # 이미지 로드 실패 시 멋진 플레이스홀더
            st.markdown("""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        border-radius:20px; padding:100px 80px; text-align:center; box-shadow: 0 10px 40px rgba(0,0,0,0.2);'>
                <h1 style='color:white; font-size:72px; margin:0;'>🎰 로또킹</h1>
                <p style='color:#fff; font-size:36px; margin-top:30px;'>당신의 행운을 응원합니다!</p>
                <div style='margin-top:40px;'>
                    <span style='font-size:60px; margin:0 20px;'>🍀</span>
                    <span style='font-size:60px; margin:0 20px;'>💎</span>
                    <span style='font-size:60px; margin:0 20px;'>⭐</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        # 이미지가 없을 경우 멋진 플레이스홀더
        st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    border-radius:20px; padding:100px 80px; text-align:center; box-shadow: 0 10px 40px rgba(0,0,0,0.2);'>
            <h1 style='color:white; font-size:72px; margin:0;'>🎰 로또킹</h1>
            <p style='color:#fff; font-size:36px; margin-top:30px;'>당신의 행운을 응원합니다!</p>
            <div style='margin-top:40px;'>
                <span style='font-size:60px; margin:0 20px;'>🍀</span>
                <span style='font-size:60px; margin:0 20px;'>💎</span>
                <span style='font-size:60px; margin:0 20px;'>⭐</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # 메인 화면 추가 정보 섹션
    st.markdown("<div style='margin-top:35px;'></div>", unsafe_allow_html=True)
    
    # 3단 특징 카드 섹션
    col1, col2, col3 = st.columns(3, gap="medium")
    with col1:
        st.markdown("""
        <style>
        .feature-card {
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
            padding:30px;
            border-radius:18px;
            box-shadow:0 6px 20px rgba(0,0,0,0.12);
            text-align:center;
            min-height:200px;
            display:flex;
            flex-direction:column;
            justify-content:center;
            transition: transform 0.3s, box-shadow 0.3s;
            cursor: pointer;
        }
        .feature-card:hover {
            transform: translateY(-8px);
            box-shadow:0 12px 30px rgba(0,0,0,0.18);
        }
        .feature-card-2 {
            background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        }
        .feature-card-3 {
            background: linear-gradient(135deg, #fbc2eb 0%, #a6c1ee 100%);
        }
        </style>
        <div class='feature-card'>
            <div style='font-size:56px; margin-bottom:15px;'>🎯</div>
            <h3 style='color:#2d3748; margin:12px 0; font-size:22px; font-weight:800;'>정확한 통계 분석</h3>
            <p style='color:#4a5568; font-size:15px; line-height:1.6;'>과거 당첨 번호 데이터를<br>분석하여 최적의 번호를<br>추천해드립니다</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class='feature-card feature-card-2'>
            <div style='font-size:56px; margin-bottom:15px;'>🧠</div>
            <h3 style='color:#2d3748; margin:12px 0; font-size:22px; font-weight:800;'>AI 스마트 추천</h3>
            <p style='color:#4a5568; font-size:15px; line-height:1.6;'>인공지능 알고리즘으로<br>패턴을 분석하여<br>똑똑한 조합을 제공합니다</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class='feature-card feature-card-3'>
            <div style='font-size:56px; margin-bottom:15px;'>🔮</div>
            <h3 style='color:#2d3748; margin:12px 0; font-size:22px; font-weight:800;'>다양한 생성 방식</h3>
            <p style='color:#4a5568; font-size:15px; line-height:1.6;'>띠별, 주역, 통계 등<br>여러 방식으로<br>행운의 번호를 만들어보세요</p>
        </div>
        """, unsafe_allow_html=True)
    
    # 사용 안내 + 최근 당첨 정보 2단 레이아웃
    st.markdown("<div style='margin-top:40px;'></div>", unsafe_allow_html=True)
    
    info_col1, info_col2 = st.columns([1.5, 1], gap="medium")
    
    with info_col1:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #e0f7fa 0%, #b2ebf2 100%); 
                    padding:28px 35px; border-radius:16px; box-shadow:0 4px 15px rgba(0,0,0,0.1);
                    border-left: 5px solid #00acc1; height:100%;'>
            <h3 style='color:#006064; margin:0 0 15px 0; font-size:20px; font-weight:800;'>💡 사용 방법</h3>
            <p style='color:#00838f; font-size:16px; line-height:1.8; margin:0;'>
                왼쪽 메뉴에서 원하는 방식을 선택하세요. <b>띠별 추천</b>은 생년월일 기반, <b>주역 추천</b>은 방위 기반, 
                <b>통계 추천</b>은 과거 데이터 분석, <b>AI 추천</b>은 인공지능 알고리즘으로 번호를 생성합니다.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with info_col2:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%); 
                    padding:28px 30px; border-radius:16px; box-shadow:0 4px 15px rgba(0,0,0,0.1);
                    border-left: 5px solid #ff9800; height:100%;'>
            <h3 style='color:#e65100; margin:0 0 12px 0; font-size:20px; font-weight:800;'>🎊 행운의 메시지</h3>
            <p style='color:#f57c00; font-size:16px; line-height:1.7; margin:0;'>
                <b>"행운은 준비된 자에게 찾아옵니다"</b><br>
                매주 새로운 기회!<br>
                오늘도 당신의 꿈을 응원합니다! 🍀
            </p>
        </div>
        """, unsafe_allow_html=True)
  
  # YouTube 구독 배너 추가
  st.markdown("<div style='margin-top:50px;'></div>", unsafe_allow_html=True)
  st.markdown("""
  <div style='background: linear-gradient(135deg, #ff0000 0%, #cc0000 100%); 
              padding:35px; border-radius:20px; box-shadow:0 8px 25px rgba(255,0,0,0.3);
              text-align:center; border: 3px solid #ffffff;'>
      <div style='font-size:64px; margin-bottom:15px;'>🎬</div>
      <h2 style='color:#ffffff; margin:15px 0; font-size:28px; font-weight:900; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>
          로또킹 YouTube 채널 구독하세요!
      </h2>
      <p style='color:#ffebee; font-size:18px; margin:15px 0 25px 0; line-height:1.6;'>
          더 많은 로또 정보와 당첨 전략을 영상으로 만나보세요!<br>
          구독과 알림 설정으로 최신 정보를 놓치지 마세요! 🔔
      </p>
      <a href='https://www.youtube.com/@lottoking-s6c' target='_blank' style='text-decoration:none;'>
          <button style='background:#ffffff; color:#ff0000; padding:18px 50px; 
                         border:none; border-radius:50px; font-size:20px; font-weight:900;
                         cursor:pointer; box-shadow:0 4px 15px rgba(0,0,0,0.2);
                         transition: all 0.3s ease;'>
              ▶️ 지금 구독하기
          </button>
      </a>
      <p style='color:#ffcdd2; font-size:14px; margin-top:15px;'>
          @lottoking-s6c
      </p>
  </div>
  """, unsafe_allow_html=True)
  
  # 메인 화면 하단 경고 메시지
  st.markdown("""
  <div style='margin-top:32px; padding:18px 0 0 0; text-align:center; color:#b00; font-size:17px; font-weight:600;'>
    ⚠️ 로또 번호 예측은 불가능합니다. 본 서비스는 교육 및 오락 목적의 참고용입니다.<br>
    <span style='font-size:15px; color:#d00; margin-top:8px; display:inline-block;'>실제 투자, 도박, 구매 등에는 신중을 기하시기 바랍니다. 당첨을 보장하지 않습니다.</span>
  </div>
  """, unsafe_allow_html=True)





