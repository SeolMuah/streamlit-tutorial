"""Iris 분류 모델 훈련 및 저장 스크립트

RandomForestClassifier로 Iris 데이터셋을 훈련하고,
학습된 모델을 joblib으로 저장합니다.

실행: python 3_streamlit_응용/train_iris_model.py
"""

from pathlib import Path

import joblib
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# 데이터 로드 및 분할
iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=0.2, random_state=42
)

# 모델 훈련
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 훈련 결과 출력
train_acc = model.score(X_train, y_train)
test_acc = model.score(X_test, y_test)
print(f"훈련 정확도: {train_acc:.4f}")
print(f"테스트 정확도: {test_acc:.4f}")

# 모델 저장
model_path = Path(__file__).parent / "iris_model.joblib"
joblib.dump(model, model_path)
print(f"모델 저장 완료: {model_path}")
