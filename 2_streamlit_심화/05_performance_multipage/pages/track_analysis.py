import streamlit as st
import pandas as pd
from utils.database import get_connection, load_overview

st.header("🎵 트랙 분석")

# 공통 데이터: DB 전체 요약
conn = get_connection()
overview = load_overview()
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("총 트랙 수", f"{overview['total_tracks']:,}곡")
with col2:
    st.metric("총 아티스트 수", f"{overview['total_artists']:,}명")
with col3:
    st.metric("총 앨범 수", f"{overview['total_albums']:,}장")
st.success(f"✅ DB 연결 (id: {id(conn)})")


# 트랙 데이터 로드 (이 페이지 전용)
@st.cache_data
def load_tracks():
    """트랙 데이터 로드 (캐싱)"""
    conn = get_connection()
    df = pd.read_sql("""
        SELECT t.TrackId, t.Name as TrackName, a.Title as Album,
               ar.Name as Artist, g.Name as Genre,
               t.Milliseconds / 1000 as Seconds, t.UnitPrice
        FROM tracks t
        JOIN albums a ON t.AlbumId = a.AlbumId
        JOIN artists ar ON a.ArtistId = ar.ArtistId
        JOIN genres g ON t.GenreId = g.GenreId
    """, conn)
    return df


tracks_df = load_tracks()
st.write(f"**{len(tracks_df):,}개 트랙 로드됨**")

st.divider()

# -----------------------------------------------------------------------------
# Fragment로 필터링
@st.fragment
def track_filter():
    col1, col2 = st.columns(2)
    with col1:
        genres = tracks_df['Genre'].unique().tolist()
        selected_genre = st.selectbox("장르 선택", genres, key="genre")
    with col2:
        max_price = st.slider("최대 가격", 0.0, 2.0, 1.0, key="price")

    filtered = tracks_df[
        (tracks_df['Genre'] == selected_genre) &
        (tracks_df['UnitPrice'] <= max_price)
    ]

    st.write(f"**필터링 결과:** {len(filtered):,}곡")
    st.dataframe(filtered.head(20), width='stretch', hide_index=True)

track_filter()

st.divider()

# -----------------------------------------------------------------------------
# 차트
@st.fragment
def track_chart():
    chart_type = st.radio("차트", ["장르별 트랙 수", "가격 분포"], horizontal=True, key="chart")

    if chart_type == "장르별 트랙 수":
        st.bar_chart(tracks_df['Genre'].value_counts().head(10))
    else:
        st.bar_chart(tracks_df['UnitPrice'].value_counts().sort_index())

track_chart()
