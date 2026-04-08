# utils/database.py - 여러 페이지에서 공통으로 사용하는 함수만 작성

import streamlit as st
import sqlite3
import pandas as pd
import os

# 데이터 경로 설정
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "..", "data", "chinook.db")


@st.cache_resource
def get_connection():
    """
    DB 연결
    - 모든 페이지에서 동일한 연결 객체 공유
    - 모든 사용자/세션에서 공유
    """
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    return conn


@st.cache_data
def load_overview():
    """DB 전체 요약 통계 (공통 데이터)"""
    conn = get_connection()
    df = pd.read_sql("""
        SELECT
            (SELECT COUNT(*) FROM tracks) as total_tracks,
            (SELECT COUNT(*) FROM artists) as total_artists,
            (SELECT COUNT(*) FROM albums) as total_albums,
            (SELECT COUNT(*) FROM genres) as total_genres,
            (SELECT COUNT(*) FROM customers) as total_customers,
            (SELECT COUNT(*) FROM invoices) as total_invoices
    """, conn)
    return df.iloc[0]
