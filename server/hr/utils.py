import pandas as pd
import numpy as np
import tensorflow as tf
import joblib
import nltk
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from PyPDF2 import PdfReader
from gensim import corpora
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from pymystem3 import Mystem

train_path = "hr/data/cleaned"

def get_train_data(path):
  print("get_train_data")
  train_df = pd.read_csv(path)
  docs = [str(train_df.keywords[i]).split() for i in range(len(train_df))]
  return docs

def parse_pdf(path):
    print("parse_pdf")
    reader = PdfReader(path)
    page = reader.pages[0]
    page = page.extract_text()
    temp_df = pd.DataFrame({"raw":[page]})
    return temp_df

def remove_numbers(documents):
  return [''.join([i for i in doc if not i.isdigit()]) for doc in documents]

def remove_strange_char(documents):
  return [re.sub(r'[^a-zA-Z0-9\#_+-]', r' ', doc) for doc in documents]

def make_tokenize(documents):
  return [doc.lower().split() for doc in documents]

useless_words_path = "hr/data/useless_words.csv"

useless_words = np.loadtxt(useless_words_path, delimiter=',', dtype='str')

def get_stopset(documents):
  unigrams = [word for doc in documents for word in doc if len(word)==1]
  std_stop = stopwords.words('english')
  return set(unigrams + std_stop + useless_words.tolist())

def remove_stopwords(documents):
  stopset=get_stopset(documents)
  return [[word for word in doc if word not in stopset] for doc in documents]

def lemmetization(documents):
  lemm=Mystem()
  return [[''.join(lemm.lemmatize(word)).replace('\n', '') for word in doc] for doc in documents]

def clean(df, col):
  """
  returns array of array containing keywords from the df
  """
  print("clean")

  docs = df[col].fillna('').tolist()
  docs = remove_strange_char(docs)
  print("removing numbers")
  docs = remove_numbers(docs)
  print("making tokens")
  docs = make_tokenize(docs)
  # print("lemma")
  # docs = lemmetization(docs)
  print("removing stopwords")
  docs = remove_stopwords(docs)
  print("done cleaning")
  return docs

def init_vectorizer():
  print("init_vectorizer")
  nltk.download('stopwords')
  print("done downloading nltk")
  def dummy(doc):
    return doc
  vectorizer=TfidfVectorizer(ngram_range=(1, 2), 
                             max_df=0.5,
                             min_df=0.05, 
                             tokenizer=dummy,
                             token_pattern=None, 
                             preprocessor=dummy)
  docs = get_train_data(train_path)
  vectorizer.fit(docs)
  return vectorizer

def get_keywords(pdf_path):
    docs = clean(parse_pdf(pdf_path), "raw")
    return docs

def full_parse(docs, vectorizer):
    print("full_parse")
    print(docs)
    transformed = vectorizer.transform(docs).toarray()
    transformed = np.pad(transformed, (0, 33), 'constant')
    
    print("done parsing")
    return transformed

def get_employee(employee_path):
  print("get_employee")
  employee_df = pd.read_csv(employee_path)
  employee_features, employee_score = employee_df.drop(['average'], axis=1), employee_df.loc[:, ['average']]
  return employee_features, employee_score





