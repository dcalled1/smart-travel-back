import imp
from joblib import load
from nltk.corpus import stopwords

stopset = list(set(stopwords.words('spanish')))

classifier = None

def load_model():
    global classifier, stopset
    classifier = load('sentiment_model.joblib')
    stopset = list(set(stopwords.words('spanish')))

def preprocess(text):
    return dict([(word, True) for word in text.split() if word not in stopset])

def classify(text):
    if classifier == None:
        load_model()
    return classifier.classify(preprocess(text))