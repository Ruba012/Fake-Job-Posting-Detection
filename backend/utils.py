import joblib
import os
import re
import string
import numpy as np
import scipy.sparse as sp

model = None
vectorizer = None


# ============================================================
# تنظيف النص قبل TF-IDF
# ============================================================
def preprocess(text: str) -> str:
    text = text.lower()

    # إزالة الأرقام من النص
    text = re.sub(r"\d+", "", text)

    # إزالة علامات الترقيم
    text = text.translate(str.maketrans("", "", string.punctuation))

    # إزالة المسافات الزائدة
    text = text.strip()

    return text


# ============================================================
# تحميل الموديل والـ vectorizer
# ============================================================
def load_models():
    global model, vectorizer

    base_dir = os.path.dirname(__file__)
    model_path = os.path.join(base_dir, "model", "best_model.pkl")
    vectorizer_path = os.path.join(base_dir, "model", "tfidf_vectorizer.pkl")

    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)


# ============================================================
# التنبؤ بالإعلان الوظيفي
# ============================================================
def predict_job(title: str, text: str):
    global model, vectorizer

    if model is None or vectorizer is None:
        raise RuntimeError("Model or vectorizer not loaded")

    if not text.strip():
        raise ValueError("Text cannot be empty")

    # دمج العنوان مع النص
    full_text = f"{title} {text}".strip()

    # تنظيف النص قبل TF-IDF
    cleaned_text = preprocess(full_text)

    # ========================================================
    # Text -> TF-IDF
    # ========================================================
    text_vector = vectorizer.transform([cleaned_text])

    # ========================================================
    # Binary features
    # لازم يكون نفس ترتيب التدريب تمامًا:
    # [has_salary_mentioned, has_company_logo, has_questions, is_remote]
    # ========================================================
    lower_text = full_text.lower()

    salary_pattern = r"\b(salary|sar|riyal|riyals|\$|per month|per week|monthly|weekly)\b"
    has_salary_mentioned = int(bool(re.search(salary_pattern, lower_text)))

    # من الواجهة الحالية هذه القيم غير موجودة فعليًا
    has_company_logo = 0
    has_questions = 0

    is_remote = int(
        "remote" in lower_text or
        "work from home" in lower_text
    )

    binary_features = sp.csr_matrix([[
        has_salary_mentioned,
        has_company_logo,
        has_questions,
        is_remote
    ]])

    # ========================================================
    # Combine TF-IDF + binary features
    # ========================================================
    X_final = sp.hstack([text_vector, binary_features], format="csr")

    # ========================================================
    # Prediction
    # ========================================================
    prediction = model.predict(X_final)[0]

    # ========================================================
    # Confidence
    # ========================================================
    confidence = _get_confidence(model, X_final, prediction)

    # ========================================================
    # Label mapping
    # 1 = Fake
    # 0 = Real
    # ========================================================
    label = "Fake" if int(prediction) == 1 else "Real"

    return label, confidence


# ============================================================
# حساب الـ confidence
# ============================================================
def _get_confidence(model_obj, X, prediction):
    try:
        if hasattr(model_obj, "predict_proba"):
            proba = model_obj.predict_proba(X)[0]
            predicted_class_idx = int(prediction)
            return float(proba[predicted_class_idx])

        elif hasattr(model_obj, "decision_function"):
            score = model_obj.decision_function(X)

            if np.isscalar(score):
                return float(1 / (1 + np.exp(-abs(score))))

            score = np.asarray(score).flatten()

            if len(score) == 1:
                return float(1 / (1 + np.exp(-abs(score[0]))))

            predicted_class_idx = int(prediction)
            selected_score = score[predicted_class_idx] if predicted_class_idx < len(score) else score[0]
            return float(1 / (1 + np.exp(-abs(selected_score))))

        else:
            return 0.75

    except Exception:
        return 0.75