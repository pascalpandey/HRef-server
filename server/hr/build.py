from utils import init_vectorizer, get_employee
from model import score_predictor
from sklearn.decomposition import PCA
from sklearn.cluster import Birch
import tensorflow as tf
import pandas as pd


vectorizer_path = 'data/vectorizer.pkl'
employee_path = 'data/employee.csv'

def inference(n_components=1201):
    model = score_predictor(n_components)
    q = tf.zeros((1, n_components))
    output = score_predictor(q)

    weights = "data/nn_model.h5"
    model.load_weights(weights)
    return model

def reduce_dim(employee_path,n_components=1201):
    employee_features, employee_score = get_employee(employee_path)
    
    reducer_1 = PCA(n_components=n_components)
    reducer_1.fit(employee_features)

    reduced_features = reducer_1.transform(employee_features)
    reduced_features = pd.DataFrame(reduced_features, columns=['PCA1', 'PCA2'])
    reduced_features = pd.concat([reduced_features, employee_score], index = -1)

    reducer_2 = PCA(n_components=2)
    reducer_2.fit(reduced_features)

    employee_final = reducer_2.transform(reduced_features)
    employee_final = pd.DataFrame(employee_final, columns=['x','y'])

    cluster_model = Birch(n_clusters=5)
    cluster_model.fit(employee_final)

    employee_final['clusters'] = cluster_model.transform(employee_final)
    employee_final = pd.concat([employee_final, employee_score], axis=1)
    return reducer_1, reducer_2, cluster_model, employee_final

vectorizer = init_vectorizer(vectorizer_path)
model = inference()
reducer_1, reducer_2, cluster_model, employee_final = reduce_dim(employee_path)