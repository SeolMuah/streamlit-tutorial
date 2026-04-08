from pathlib import Path

import joblib
import numpy as np
import streamlit as st

# 모델 로드 (캐싱 필수!)
@st.cache_resource
def load_model():
    model_path = Path(__file__).parent / "iris_model.joblib"
    return joblib.load(model_path)

model = load_model()

st.title("🌸 붓꽃 품종 예측")

col1, col2 = st.columns(2)
with col1:
    sepal_length = st.slider("꽃받침 길이", 4.0, 8.0, 5.0)
    sepal_width = st.slider("꽃받침 너비", 2.0, 4.5, 3.0)
with col2:
    petal_length = st.slider("꽃잎 길이", 1.0, 7.0, 4.0)
    petal_width = st.slider("꽃잎 너비", 0.1, 2.5, 1.0)

# 예측
input_data = np.array([[sepal_length, sepal_width, petal_length, petal_width]])
prediction = model.predict(input_data)[0]
probabilities = model.predict_proba(input_data)[0]

species = ["Setosa", "Versicolor", "Virginica"]

# 품종별 예측 확률
st.subheader("품종별 예측 확률")
for name, prob in zip(species, probabilities):
    st.progress(prob, text=f"{name}: {prob:.1%}")

# 최종 예측 결과
st.success(f"최종 예측: **{species[prediction]}** ({probabilities[prediction]:.1%})")