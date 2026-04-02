import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

# =============================================================================
# 운영체제별 한글 폰트 설정 (matplotlib에서 한글이 깨지지 않도록)
# =============================================================================
import platform

def set_korean_font():
    """운영체제에 따라 적절한 한글 폰트 설정"""
    system = platform.system()

    if system == 'Darwin':  # macOS
        plt.rcParams['font.family'] = 'AppleGothic'
    elif system == 'Windows':  # Windows
        plt.rcParams['font.family'] = 'Malgun Gothic'
    else:  # Linux 또는 기타
        plt.rcParams['font.family'] = 'DejaVu Sans'

    # 마이너스 폰트 깨짐 방지
    plt.rcParams['axes.unicode_minus'] = False

# 폰트 설정 적용
set_korean_font()

# =============================================================================
# 데이터 로드 및 전처리
# =============================================================================

# 캐시 데코레이터: 데이터를 한 번만 로드하고 메모리에 저장해서 성능 향상
@st.cache_data
def load_california_housing():
    """
    캘리포니아 주택 데이터셋 로드 및 전처리

    Returns:
        pd.DataFrame: 전처리된 주택 데이터
    """
    try:
        # CSV 파일에서 데이터 읽기
        df = pd.read_csv('california_housing.csv')

        # 컬럼명을 한글로 변경
        df.columns = ['중위소득', '주택연수', '평균방수', '평균침실수',
                      '인구', '평균거주자수', '위도', '경도', '주택가격']

        # 가격 단위 변환: 원래 단위(10만 달러)에서 이해하기 쉬운 단위로
        df['주택가격'] = df['주택가격'] * 10  # 10만 달러 단위로 표시

        return df

    except FileNotFoundError:
        st.error("❌ 데이터 파일을 찾을 수 없습니다. 'california_housing.csv' 파일이 있는지 확인하세요.")
        return pd.DataFrame()  # 빈 데이터프레임 반환

# 데이터 로드
df = load_california_housing()

# 데이터가 제대로 로드되었는지 확인
if df.empty:
    st.stop()  # 데이터가 없으면 앱 실행 중단

# =============================================================================
# 데이터 개요 및 기본 정보 표시
# =============================================================================

st.header("📊 캘리포니아 주택 데이터 개요")

# 4개 열로 나누어 주요 통계 정보 표시
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("총 데이터 수", f"{len(df):,}개")
with col2:
    # 주택가격 평균을 소수점 1자리까지 표시
    st.metric("평균 주택가격", f"${df['주택가격'].mean():.1f}만")
with col3:
    st.metric("중위소득 평균", f"${df['중위소득'].mean():.1f}만")
with col4:
    st.metric("평균 주택연수", f"{df['주택연수'].mean():.1f}년")

# 확장 가능한 섹션으로 데이터 샘플 표시
if st.expander("데이터 샘플 보기"):
    st.dataframe(df.head(10), use_container_width=True)

# =============================================================================
# Streamlit 네이티브 지도 시각화 (st.map)
# =============================================================================
st.header("Streamlit 내장 시각화 활용 - 지도 시각화")

# st.map을 위한 데이터 준비
st.subheader("캘리포니아 주택 위치 분포")

# st.map은 'lat'과 'lon' 컬럼명을 기대하므로 컬럼명 변경
map_df = df[['위도', '경도']].copy()
map_df.columns = ['lat', 'lon']

# 가격대별 지도 시각화
st.subheader("가격대별 주택 분포")

# 가격대 선택 슬라이더
price_range = st.slider(
    "주택가격 범위 선택 (10만 달러 단위)",
    min_value=float(df['주택가격'].min()),
    max_value=float(df['주택가격'].max()),
    value=(float(df['주택가격'].quantile(0.25)), float(df['주택가격'].quantile(0.75))),
    step=0.5
)

# 선택된 가격 범위에 해당하는 데이터 필터링
filtered_df = df[(df['주택가격'] >= price_range[0]) & (df['주택가격'] <= price_range[1])].copy()
st.text(f"선택된 가격 범위: ${price_range[0]:.1f}만 ~ ${price_range[1]:.1f}만 (총 {len(filtered_df):,}개)")

# 필터링된 데이터로 지도 표시
if len(filtered_df) > 0:
    map_filtered = filtered_df[['위도', '경도']].copy()
    map_filtered.columns = ['lat', 'lon']
    st.map(map_filtered, zoom=5)
else:
    st.warning("선택된 가격 범위에 해당하는 주택이 없습니다.")

# =============================================================================
# 1. Matplotlib - 정적이지만 완벽한 커스터마이징
# =============================================================================

st.header("1. Matplotlib")
col1, col2 = st.columns(2)
with col1:
    st.subheader("주택가격 분포")

    # Figure 객체 생성 (크기 지정)
    plt.figure(figsize=(8, 5))

    # 히스토그램 생성
    plt.hist(df['주택가격'], bins=30,           # 30개 구간으로 나누기
             alpha=0.7,                         # 투명도 70%
             color='lightcoral',                # 연한 분홍색
             edgecolor='black')                 # 테두리는 검은색

    # 축 레이블 및 제목 설정
    plt.xlabel('주택가격 (10만 달러)', fontsize=12)
    plt.ylabel('주택 수', fontsize=12)
    plt.title('캘리포니아 주택가격 분포', fontsize=14, fontweight='bold')

    # 격자 표시 (투명도 30%)
    plt.grid(True, alpha=0.3)

    # 평균값에 수직선 추가 (통계적 의미 강조)
    mean_price = df['주택가격'].mean()
    plt.axvline(mean_price, color='red', linestyle='--',
                label=f'평균: ${mean_price:.1f}만')
    plt.legend()  # 범례 표시

    # Streamlit에 matplotlib 차트 표시
    st.pyplot(plt.gcf())  # 현재 figure 객체 가져오기
    plt.clf()  # 메모리 정리

with col2:
    st.subheader("소득 vs 주택가격 관계")

    plt.figure(figsize=(8, 5))

    # 성능 최적화: 전체 데이터 대신 1000개 샘플만 사용
    sample_df = df.sample(n=1000, random_state=42)  # 재현 가능한 랜덤 샘플링

    # 산점도 생성 (색상으로 주택연수 표현)
    scatter = plt.scatter(sample_df['중위소득'], sample_df['주택가격'],
                         c=sample_df['주택연수'],    # 색상 매핑할 변수
                         cmap='viridis',            # 색상 팔레트
                         alpha=0.6,                 # 투명도
                         s=30)                      # 점 크기

    plt.xlabel('중위소득 (만 달러)', fontsize=12)
    plt.ylabel('주택가격 (10만 달러)', fontsize=12)
    plt.title('소득 vs 주택가격 (색상: 주택연수)', fontsize=14, fontweight='bold')

    # 컬러바 추가 (색상의 의미 설명)
    cbar = plt.colorbar(scatter)
    cbar.set_label('주택연수 (년)', rotation=270, labelpad=15)
    plt.grid(True, alpha=0.3)

    st.pyplot(plt.gcf())  # 현재 figure 객체 가져오기
    plt.clf()  # 메모리 정리

# =============================================================================
# 2. Seaborn - 빠르게 이쁜 시각화 완성
# =============================================================================
st.header("2. Seaborn")

col1, col2 = st.columns(2)

with col1:
    st.subheader("주택연수별 가격 분포")

    # 주택연수를 의미있는 구간으로 분류
    df_age = df.copy()
    df_age['연수구간'] = pd.cut(df_age['주택연수'],
                             bins=[0, 10, 25, 40, 100],  # 구간 경계값
                             labels=['신축(0-10년)', '보통(11-25년)',
                                   '오래됨(26-40년)', '매우오래됨(40년+)'])

    plt.figure(figsize=(8, 5))

    # 박스플롯: 각 그룹의 분포를 상자그림으로 표현
    sns.boxplot(data=df_age, x='연수구간', y='주택가격',
                palette='Set2')  # Set2 색상 팔레트 사용

    plt.title('주택연수별 가격 분포', fontsize=14, fontweight='bold')
    plt.ylabel('주택가격 (10만 달러)')
    plt.xlabel('주택연수 구간')

    # x축 레이블 회전 (긴 텍스트가 겹치지 않도록)
    plt.xticks(rotation=45)
    plt.tight_layout()  # 레이아웃 자동 조정

    st.pyplot(plt.gcf())
    plt.clf()  # 메모리 정리

with col2:
    st.subheader("변수간 상관관계")

    # 분석에 중요한 수치형 변수들만 선택
    correlation_cols = ['중위소득', '주택연수', '평균방수', '주택가격']
    correlation_data = df[correlation_cols].corr()  # 상관계수 행렬 계산

    plt.figure(figsize=(6, 5))

    # 히트맵: 상관계수를 색상으로 표현 (시인성 좋은 색상으로 변경)
    sns.heatmap(correlation_data,
                annot=True,              # 수치값 표시
                cmap='coolwarm',         # 시원한 파랑-빨강 색상
                center=0,               # 0을 중심으로 색상 조정
                square=True,            # 정사각형 셀
                linewidths=0.5,         # 셀 경계선 두께
                fmt='.2f',              # 소수점 2자리 표시
                annot_kws={'size': 10}) # 숫자 크기 조정

    plt.title('주요 변수 상관관계', fontsize=14, fontweight='bold')
    plt.tight_layout()

    st.pyplot(plt.gcf())
    plt.clf()  # 메모리 정리

# =============================================================================
# 3. Plotly - 인터랙티브 시각화
# =============================================================================

st.header("3. Plotly")

# 인터랙티브 산점도 - 지리적 분석
st.subheader("캘리포니아 주택 지리적 분포")

# 성능 최적화: 전체 5000개 데이터 중 2000개만 시각화
sample_df = df.sample(n=2000, random_state=42)

# Plotly Express를 사용한 인터랙티브 산점도
fig = px.scatter(sample_df,
                x='경도', y='위도',           # 지리적 좌표를 x, y축으로
                color='주택가격',             # 점 색상: 주택가격
                size='중위소득',              # 점 크기: 중위소득
                hover_data=['주택연수', '평균방수'],  # 마우스 오버시 추가 정보
                title='캘리포니아 주택 위치별 가격 분포',
                labels={'경도': '경도', '위도': '위도', '주택가격': '주택가격 (10만$)'},
                color_continuous_scale='Viridis')  # 색상 스케일

fig.update_layout(height=500)  # 차트 높이 설정
st.plotly_chart(fig, use_container_width=True)  # 컨테이너 너비에 맞춤

# 소득 vs 가격 인터랙티브 분석
st.subheader("소득 vs 주택가격 인터랙티브 분석")

fig = px.scatter(sample_df,
                x='중위소득', y='주택가격',
                color='주택연수',             # 점 색상: 주택연수
                size='평균방수',              # 점 크기: 평균방수
                hover_data=['위도', '경도', '인구'],  # 호버 정보
                title='중위소득 vs 주택가격 (색상: 주택연수, 크기: 평균방수)',
                labels={'중위소득': '중위소득 (만$)', '주택가격': '주택가격 (10만$)'},
                color_continuous_scale='RdYlBu')  # 빨강-노랑-파랑 그라데이션

fig.update_layout(height=500)
st.plotly_chart(fig, use_container_width=True)

# 3D 산점도 - 소득, 가격, 주택연수
st.subheader("3D 주택 분석")

# 3D 차트는 더 적은 데이터 포인트 사용 (성능 고려)
sample_3d = df.sample(n=1000, random_state=42)

# Plotly Graph Objects를 사용한 3D 산점도
fig = go.Figure(data=[go.Scatter3d(
    x=sample_3d['중위소득'],         # X축: 중위소득
    y=sample_3d['주택가격'],         # Y축: 주택가격
    z=sample_3d['주택연수'],         # Z축: 주택연수
    mode='markers',                 # 점만 표시
    marker=dict(
        size=5,                     # 점 크기
        color=sample_3d['평균방수'], # 점 색상: 평균방수
        colorscale='RdYlBu',       # 색상 팔레트
        showscale=True,             # 컬러바 표시
        colorbar=dict(
            title="평균방수",
        ),
        opacity=0.8,                # 투명도 추가로 겹치는 점들 구분
        cmin=sample_3d['평균방수'].quantile(0.05),  # 하위 5% 값을 최소로
        cmax=sample_3d['평균방수'].quantile(0.95)   # 상위 5% 값을 최대로 (색상 범위 확장)

    ),
    # 호버 텍스트 커스터마이징
    text=[f"소득: ${row['중위소득']:.1f}만<br>가격: ${row['주택가격']:.1f}만<br>연수: {row['주택연수']:.0f}년"
          for _, row in sample_3d.iterrows()],
    hovertemplate='%{text}<extra></extra>'  # 호버 템플릿
)])

# 3D 차트 레이아웃 설정
fig.update_layout(
    title='3D 주택 분석: 소득-가격-연수 (색상: 평균방수)',
    scene=dict(
        xaxis_title='중위소득 (만$)',
        yaxis_title='주택가격 (10만$)',
        zaxis_title='주택연수 (년)'
    ),
    height=600
)
st.plotly_chart(fig, use_container_width=True)