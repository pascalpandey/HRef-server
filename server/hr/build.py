from hr.utils import init_vectorizer, get_employee
from hr.model import score_predictor
from sklearn.decomposition import PCA
from sklearn.cluster import Birch
import tensorflow as tf
import pandas as pd
import pickle

vectorizer_path = 'hr/data/vectorizer_2.pkl'
employee_path = 'hr/data/employee.csv'

def inference(n_components=1201):
    print("inference")
    model = tf.keras.Sequential([
      tf.keras.layers.Input(shape=(n_components, )),
      tf.keras.layers.Dense(64, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(3e-4)),
      tf.keras.layers.Dense(32, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(3e-4)),
      tf.keras.layers.Dense(32, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(3e-4)),
      tf.keras.layers.Dense(32, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(3e-4)),
      tf.keras.layers.Dense(1, activation='relu')
    ])

    weights = "hr/data/nn_model.h5"
    model.load_weights(weights)
    return model

def reduce_dim(employee_path,n_components=1201):
    print("reduce_dim")
    employee_features, employee_score = get_employee(employee_path)
    
    reducer_1 = PCA(n_components=2)
    reducer_1.fit(employee_features)

    reduced_features = reducer_1.transform(employee_features)
    reduced_features = pd.DataFrame(reduced_features, columns=['PCA1', 'PCA2'])
    reduced_features = pd.concat([reduced_features, employee_score], axis=1)

    reducer_2 = PCA(n_components=2)
    reducer_2.fit(reduced_features)

    employee_final = reducer_2.transform(reduced_features)
    employee_final = pd.DataFrame(employee_final, columns=['x','y'])

    cluster_model = Birch(n_clusters=5, threshold=0.1)
    cluster_model.fit(employee_final)
    clusters = cluster_model.predict(employee_final)

    employee_final['clusters'] = clusters
    employee_final = pd.concat([employee_final, employee_score], axis=1)
    return reducer_1, reducer_2, cluster_model, employee_final


def upload_employee(employee_final):
  res = []

  for i in range(len(employee_final)):
    res.append({
      "color": str(employee_final.iloc[i,2]),
      "score": employee_final.iloc[i,3],
      "x": employee_final.iloc[i,0],
      "y": employee_final.iloc[i,1],
    })

  return res

vectorizer = init_vectorizer()
model = inference()
reducer_1, reducer_2, cluster_model, employee_final = reduce_dim(employee_path)
