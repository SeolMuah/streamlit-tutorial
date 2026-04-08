import streamlit as st
import pandas as pd
from utils.database import get_connection, load_overview

st.header("🎤 아티스트 분석")

# 공통 데이터: DB 전체 요약
conn = get_connection()
overview = load_overview()
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("총 아티스트 수", f"{overview['total_artists']:,}명")
with col2:
    st.metric("총 앨범 수", f"{overview['total_albums']:,}장")
with col3:
    st.metric("총 트랙 수", f"{overview['total_tracks']:,}곡")
st.success(f"✅ DB 연결 (id: {id(conn)})")

st.divider()

# -----------------------------------------------------------------------------
# 아티스트 통계
@st.cache_data
def get_artist_stats():
    return pd.read_sql("""
        SELECT ar.Name as Artist, COUNT(t.TrackId) as TrackCount,
               SUM(t.Milliseconds)/1000/60 as TotalMinutes
        FROM artists ar
        JOIN albums a ON ar.ArtistId = a.ArtistId
        JOIN tracks t ON a.AlbumId = t.AlbumId
        GROUP BY ar.ArtistId
        ORDER BY TrackCount DESC
        LIMIT 20
    """, conn)

artist_stats = get_artist_stats()

col1, col2 = st.columns(2)
with col1:
    st.subheader("트랙 수 Top 10")
    st.bar_chart(artist_stats.set_index('Artist')['TrackCount'].head(10))

with col2:
    st.subheader("총 재생시간 Top 10")
    st.bar_chart(artist_stats.set_index('Artist')['TotalMinutes'].head(10))

st.divider()

# -----------------------------------------------------------------------------
# SQL 쿼리 실행기
st.subheader("🔍 SQL 쿼리 실행")

query = st.text_area("SQL", value="SELECT * FROM artists LIMIT 10", height=80, key="sql")

if st.button("실행"):
    try:
        result = pd.read_sql(query, conn)
        st.dataframe(result, width='stretch', hide_index=True)
    except Exception as e:
        st.error(f"오류: {e}")
