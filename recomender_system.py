# Motor de Recomendación
#   Elaborado por: Andrea Faúndez, Marcelo Madel, Israel Diaz
#   para la materia de INTELIGENCIA ARTIFICIAL AVANZADA
#   MAGISTER EN DATA SCIENCE
#   UNIVERSIDAD DEL DESARROLLO

# VERSION_2

# Librerias
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests
import json
from numpy import load


class Recomendacion():
    '''
    Motor de recomendación
    '''

    def __init__(self):
        '''
        Inicializa los parametros
        :param movie: string con la película a consultar.
        :param dataframe: dataframe con la base de datos de peliculas donde se buscará.
        :param movie_imdb: nombre de la pelicula en IMDB.
        '''

        self.dataframe = pd.read_csv('data/movies_combfeat.csv')
        self.cosine_sim = pd.DataFrame()
        self.indices = pd.Series()

    def obten_recomendacion(self, movie):
        '''
        Motor de recomendación mediante el calculo del cosine_similarity
        :return: devuelve 5 registros recomendados
        '''

        self.movie = movie

        api_key = '96ea9ff3'
        movie_detail = requests.get('http://www.omdbapi.com/?t={0}&apikey={1}'.format(self.movie, api_key)).content
        movie_detail = json.loads(movie_detail)
        response = movie_detail['Title']

        movie_imdb = response

        # Calculo del Cosine similarity
        #count = CountVectorizer(stop_words='english')
        #count_matrix = count.fit_transform(self.dataframe['combined_features'])
        #self.cosine_sim = cosine_similarity(count_matrix, count_matrix)
        self.indices = pd.Series(self.dataframe.index, index=self.dataframe['movie'])

        self.cosine_sim = load('data/cosine_sim.npz')['arr_0']

        # Búsqueda de recomendaciones
        try:
            idx = self.indices[movie_imdb]
            sim_scores = list(enumerate(self.cosine_sim[idx]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            sim_scores = sim_scores[1:6]
            movie_indices = [i[0] for i in sim_scores]

            return 'Cualquiera de estas opciones te podría gustar  :::   ' + str(self.dataframe['movie'].iloc[movie_indices].tolist())

        except:
            try:
                idx = self.indices[self.movie]
                sim_scores = list(enumerate(self.cosine_sim[idx]))
                sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
                sim_scores = sim_scores[1:6]
                movie_indices = [i[0] for i in sim_scores]

                return 'Cualquiera de estas opciones te podría gustar  :::   ' + str(self.dataframe['movie'].iloc[movie_indices].tolist())

            except:
                return 'No fue posible encontrar su pelicula/serie en nuestro catálogo'
