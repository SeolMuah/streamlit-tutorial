"""YouTube 영상 검색 앱

YouTube Data API를 사용하여 영상을 검색하고 결과를 표시합니다.
API 키는 .streamlit/secrets.toml에서 관리합니다.

실행: streamlit run 3_streamlit_응용/02_api_connection/youtube_search.py
"""

import streamlit as st
import requests

API_KEY = st.secrets["YOUTUBE_API_KEY"]
SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"

st.title("🎬 YouTube 영상 검색")


def search_youtube(query, max_results=5):
    """YouTube Data API로 영상을 검색하고 결과 리스트를 반환합니다."""
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": max_results,
        "key": API_KEY,
    }
    response = requests.get(SEARCH_URL, params=params)
    response.raise_for_status()

    return [
        {
            "video_id": item["id"]["videoId"],
            "title": item["snippet"]["title"],
            "channel": item["snippet"]["channelTitle"],
        }
        for item in response.json().get("items", [])
        if "videoId" in item.get("id", {})
    ]


def render_videos(videos):
    """영상 목록을 제목 + 채널 + 영상 플레이어로 표시합니다."""
    for video in videos:
        with st.container(border=True):
            st.markdown(f"**{video['title']}**")
            st.caption(f"채널: {video['channel']}")
            st.video(f"https://www.youtube.com/watch?v={video['video_id']}")


# 대화 기록 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 이전 대화 표시
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "user":
            st.markdown(msg["content"])
        else:
            render_videos(msg.get("videos", []))

# 사용자 입력
if query := st.chat_input("검색어를 입력하세요"):
    # 사용자 메시지 표시 및 저장
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    # YouTube API 검색
    with st.chat_message("assistant"):
        with st.spinner("검색 중..."):
            try:
                videos = search_youtube(query)
            except requests.HTTPError as e:
                st.error(f"API 요청 실패: {e}")
                videos = []

        if videos:
            render_videos(videos)
        else:
            st.warning("검색 결과가 없습니다.")

        st.session_state.messages.append({"role": "assistant", "videos": videos})
