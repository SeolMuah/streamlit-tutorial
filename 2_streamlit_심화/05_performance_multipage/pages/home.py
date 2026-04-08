import streamlit as st
from utils.database import get_connection, load_overview

st.title("⚡ Streamlit 성능 최적화")
st.caption("멀티 페이지 구조에서 캐싱 활용하기")

st.markdown("""
## 폴더 구조

```
05_performance_multipage/
├── main.py                     # 엔트리 포인트 (페이지 설정)
├── utils/
│   └── database.py             # 공유 DB 연결 + 공통 데이터
└── pages/
    ├── home.py                 # 홈 (현재 페이지) - 공통 데이터 기술 통계
    ├── track_analysis.py       # 트랙 분석 - 페이지 자체 데이터 로드 (@st.cache_data)
    ├── artist_analysis.py      # 아티스트 분석 - 페이지 자체 데이터 로드 (@st.cache_data)
    └── sales_analysis.py       # 매출 분석 - 페이지 자체 데이터 로드 (@st.fragment)
```

## 핵심 포인트

### 1. 공통 데이터는 `utils/database.py`에서 관리
- `get_connection()`: DB 연결 (@st.cache_resource - 모든 페이지에서 동일한 객체 공유)
- `load_overview()`: DB 전체 요약 통계 (@st.cache_data - 여러 페이지에서 재사용 가능)

### 2. 페이지별 데이터는 각 페이지에서 로드
- `track_analysis.py` → `load_tracks()` (트랙 전용 조인 데이터)
- `artist_analysis.py` → `get_artist_stats()` (아티스트 전용 집계)
- `sales_analysis.py` → `load_invoices()` (매출 전용 데이터)
""")

st.code('''# utils/database.py - 공통
@st.cache_resource
def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    return conn

@st.cache_data
def load_overview():
    conn = get_connection()
    df = pd.read_sql("SELECT COUNT(*) ... FROM tracks, artists, ...", conn)
    return df.iloc[0]

# pages/track_analysis.py - 페이지 전용
@st.cache_data
def load_tracks():
    conn = get_connection()
    df = pd.read_sql("SELECT ... FROM tracks JOIN ...", conn)
    return df''', language="python")

st.divider()

# =============================================================================
# 공통 데이터(load_overview) 기술 통계 예시
# =============================================================================
st.header("📊 DB 전체 요약 (공통 데이터)")
st.caption("utils/database.py의 load_overview()로 로드한 공통 데이터")

conn = get_connection()
overview = load_overview()

st.success(f"✅ DB 연결 (id: {id(conn)})")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("총 트랙 수", f"{overview['total_tracks']:,}곡")
    st.metric("총 아티스트 수", f"{overview['total_artists']:,}명")
with col2:
    st.metric("총 앨범 수", f"{overview['total_albums']:,}장")
    st.metric("총 장르 수", f"{overview['total_genres']:,}개")
with col3:
    st.metric("총 고객 수", f"{overview['total_customers']:,}명")
    st.metric("총 주문 수", f"{overview['total_invoices']:,}건")

st.divider()
st.info("👈 **왼쪽 사이드바에서 페이지를 선택하세요!** 각 페이지에서 DB 연결 id가 동일한지 확인해보세요.")
