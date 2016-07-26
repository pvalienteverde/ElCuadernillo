import pandas as pd
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import numpy as np
from nltk.corpus import stopwords


class ContentBased(object):
    """
    Modelo de recomendación de articulos basados en los tags con mas relevancia de cada uno de ellos.
    El modelo vectoriza cada articulo para poder calcular la similitud entre cada uno de ellos. 
    """
    def __init__(self, stop_words=None, token_pattern=None, metric='cosine', n_neighbors=5):
        if stop_words is None:
            stop_words =  stopwords.words("english")
            
        if token_pattern is None:
            token_pattern = '(?u)\\b[a-zA-Z]\\w\\w+\\b'
            
        self.tfidf_vectorizer = TfidfVectorizer(stop_words=stop_words, token_pattern=token_pattern)
        self.nearest_neigbors = NearestNeighbors(metric=metric, n_neighbors=n_neighbors, algorithm='brute')
        
    def fit(self, datos, columna_descripcion):
        """
        Entrenamos el modelo:
        1/ Vectorizacion de cada articulo (Extracción y ponderación de atributos)
        2/ Calculamos los articulos mas cercanos
        """
        self.datos = datos
        datos_por_tags = self.tfidf_vectorizer.fit_transform(datos[columna_descripcion])        
        self.nearest_neigbors.fit(datos_por_tags)
        
    def predict(self, descripcion):
        """
        Devuelve los articulos mas parecidos a la descripcion propuesta
        """
        descripcion_tags = self.tfidf_vectorizer.transform(descripcion)        
        if descripcion_tags.sum() == 0:
            return pd.DataFrame(columns=self.datos.columns)
        else:
            _, indices = self.nearest_neigbors.kneighbors(descripcion_tags)
            return self.datos.iloc[indices[0], :]



def mostrar_pesos_tags(vector,vectorizacion,descripcion = 'peso',numero=8):
    resultado=pd.DataFrame(data={descripcion:np.transpose(vector.toarray()[0])},index=vectorizacion.get_feature_names())
    resultado.index.name='tag_'+descripcion
    return resultado.sort_values([descripcion],ascending=[0]).head(numero)
