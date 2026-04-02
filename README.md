# Streamlit 실습 튜토리얼

Streamlit을 활용한 데이터 시각화 및 웹 앱 개발 실습 저장소입니다.

## 환경 설정

```bash
# uv 환경 생성 및 의존성 설치 (권장)
uv sync
```

uv가 없는 경우, Python 3.12 환경에서 아래 명령어로 설치해주세요.

```bash
pip install -U streamlit pandas numpy matplotlib seaborn plotly
```



### 주요 라이브러리

| 라이브러리 | 용도 |
|-----------|------|
| streamlit | 웹 앱 프레임워크 |
| pandas | 데이터 처리 |
| numpy | 수치 연산 |
| matplotlib | 정적 시각화 |
| seaborn | 통계 시각화 |
| plotly | 인터랙티브 시각화 |

## 실습 구성

### 1회차 - Streamlit 기초

> 폴더: [`1_streamlit_기초/`](1_streamlit_기초/)

Streamlit의 핵심 기능을 익히는 기초 실습입니다.

| 파일 | 내용 | 실행 |
|------|------|------|
| `01_hello.py` | 첫 번째 앱 만들기 | `streamlit run 1_streamlit_기초/01_hello.py` |
| `02_basic_output.py` | 텍스트, 데이터, 메트릭 출력 | `streamlit run 1_streamlit_기초/02_basic_output.py` |
| `03_input_widgets.py` | 입력 위젯 (텍스트, 슬라이더, 버튼 등) | `streamlit run 1_streamlit_기초/03_input_widgets.py` |
| `04_feedback.py` | 상태 표시, 진행률, 알림 | `streamlit run 1_streamlit_기초/04_feedback.py` |
| `05_widget_tips.py` | Session State, Form, 조건부 위젯 | `streamlit run 1_streamlit_기초/05_widget_tips.py` |
| `06_charts.py` | 차트 시각화 (Matplotlib, Seaborn, Plotly) | `streamlit run 1_streamlit_기초/06_charts.py` |


## 1회차 실행 방법

```bash
# 01. 첫 번째 앱 만들기
streamlit run 1_streamlit_기초/01_hello.py

# 02. 텍스트, 데이터, 메트릭 출력
streamlit run 1_streamlit_기초/02_basic_output.py

# 03. 입력 위젯
streamlit run 1_streamlit_기초/03_input_widgets.py

# 04. 상태 표시, 진행률, 알림
streamlit run 1_streamlit_기초/04_feedback.py

# 05. Session State, Form, 조건부 위젯
streamlit run 1_streamlit_기초/05_widget_tips.py

# 06. 차트 시각화
streamlit run 1_streamlit_기초/06_charts.py
```
