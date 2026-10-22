import os
import joblib
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_DIR = os.path.join(BASE_DIR, 'dataset')
SAVED_MODEL_DIR = os.path.join(BASE_DIR, 'model', 'saved')

os.makedirs(SAVED_MODEL_DIR, exist_ok=True)

def train_url_model():
    print("--> Training URL Phishing Classification Model...")
    df = pd.read_csv(os.path.join(DATASET_DIR, 'urls.csv'))
    X = df['url']
    y = df['label']

    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(analyzer='char_wb', ngram_range=(3, 5), max_features=5000)),
        ('clf', RandomForestClassifier(n_estimators=100, random_state=42))
    ])

    pipeline.fit(X, y)
    preds = pipeline.predict(X)
    acc = accuracy_score(y, preds)
    print(f"URL Model Accuracy: {acc * 100:.2f}%")
    print(classification_report(y, preds))

    model_path = os.path.join(SAVED_MODEL_DIR, 'url_phishing_model.pkl')
    joblib.dump(pipeline, model_path)
    print(f"URL Model saved to: {model_path}\n")

def train_sms_model():
    print("--> Training SMS Smishing Classification Model...")
    df = pd.read_csv(os.path.join(DATASET_DIR, 'sms.csv'))
    X = df['message']
    y = df['label']

    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(ngram_range=(1, 2), max_features=3000, stop_words='english')),
        ('clf', RandomForestClassifier(n_estimators=80, random_state=42))
    ])

    pipeline.fit(X, y)
    preds = pipeline.predict(X)
    acc = accuracy_score(y, preds)
    print(f"SMS Model Accuracy: {acc * 100:.2f}%")
    print(classification_report(y, preds))

    model_path = os.path.join(SAVED_MODEL_DIR, 'sms_phishing_model.pkl')
    joblib.dump(pipeline, model_path)
    print(f"SMS Model saved to: {model_path}\n")

def train_email_model():
    print("--> Training Email Phishing Classification Model...")
    df = pd.read_csv(os.path.join(DATASET_DIR, 'emails.csv'))
    # Combine sender, subject, and content
    X = df['sender'].fillna('') + " " + df['subject'].fillna('') + " " + df['content'].fillna('')
    y = df['label']

    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(ngram_range=(1, 2), max_features=4000, stop_words='english')),
        ('clf', RandomForestClassifier(n_estimators=80, random_state=42))
    ])

    pipeline.fit(X, y)
    preds = pipeline.predict(X)
    acc = accuracy_score(y, preds)
    print(f"Email Model Accuracy: {acc * 100:.2f}%")
    print(classification_report(y, preds))

    model_path = os.path.join(SAVED_MODEL_DIR, 'email_phishing_model.pkl')
    joblib.dump(pipeline, model_path)
    print(f"Email Model saved to: {model_path}\n")

if __name__ == '__main__':
    print("=== Training AI CYBER SHIELD Machine Learning Models ===")
    train_url_model()
    train_sms_model()
    train_email_model()
    print("All models trained and exported successfully!")
