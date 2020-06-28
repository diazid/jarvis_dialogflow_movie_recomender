#   Motor de Recomendación
#   Elaborado por: Andrea Faúndez, Marcelo Madel, Israel Diaz
#   para la materia de INTELIGENCIA ARTIFICIAL AVANZADA
#   MAGISTER EN DATA SCIENCE
#   UNIVERSIDAD DEL DESARROLLO

# VERSION_3

import pandas as pd
import json
from scipy.sparse import csr_matrix
import pickle
from implicit.bpr import BayesianPersonalizedRanking


class Filtering():

    def __init__(self):

        self.user_col = 'ID_CLIENTE'
        self.movie_col = 'ID_GRUPO'

        # :::: LOADING DATAFRAME :::::
        self.df_interactions = pd.read_csv('data/interactions.csv', sep=';')
        self.df_interactions[self.user_col] = self.df_interactions[self.user_col].astype("category")
        self.df_interactions[self.movie_col] = self.df_interactions[self.movie_col].astype("category")
        self.m_amount_users = len(self.df_interactions[self.user_col].cat.categories)
        self.m_amount_content = len(self.df_interactions[self.movie_col].cat.categories)

        # :::: LOADING MOVIE DICTIONARY ::::
        #with open('data/dict_movies.txt', 'rb') as m_list:
        #    self.movie_dict = json.load(m_list)
        self.dict_movies = pd.read_csv('data/dict_movies.csv', sep=',')

        #::::: LOADING MODEL :::::
        with open('model/model_BPR.pkl', 'rb') as file:
            self.bpr_model = pickle.load(file)

    def associate(self):
        users = {}
        movies = {}
        for (code, cat) in enumerate(self.df_interactions[self.movie_col].cat.categories):
            movies[cat] = code
        for (code, cat) in enumerate(self.df_interactions[self.user_col].cat.categories):
            users[cat] = code
        return users, movies

    def get_rec_movie(self, user_id, k=20):

        ### sparse matrix
        df_movies_csr = csr_matrix((self.df_interactions.counts, (self.df_interactions[self.movie_col].cat.codes, self.df_interactions[self.user_col].cat.codes)), shape=(self.m_amount_content, self.m_amount_users))

        ### mappings
        movies_users, movies_content = self.associate()

        ### filtering content watched by the user
        _filter = [movies_content[idx] for idx in self.df_interactions[self.df_interactions[self.user_col] == user_id][self.movie_col].unique()]
        ### get to K movies recommendation for a user
        rec_movies = self.bpr_model.recommend(movies_users[user_id], df_movies_csr.T, N=k, filter_items=_filter)

        ### unique values
        #movies_content_id = {v: k for k, v in movies_content.items()}
        resp = set()

        for i in range(0, 5):
            aux = self.dict_movies['TX_NOMBRE'][self.dict_movies.index == rec_movies[i][0]].tolist()[0]
            resp.add(aux)

        return 'Cualquiera de estas opciones te podría gustar  :::   ' + str(resp)
