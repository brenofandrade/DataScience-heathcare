from os import path
from numpy.testing._private.utils import print_assert_equal
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
import sklearn as sk
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle
import flask

class Preprocess:
    def __init__(self,file_path):

        self.dataset = pd.read_csv(file_path)

        self.data_cleaning()
        

    def data_cleaning(self):
        
        # Remove colunas do dataset
        del self.dataset['id']
        del self.dataset['casado']
        

        novo_imc = np.where(self.dataset['imc'].isnull(), self.dataset['imc'].mean(), self.dataset['imc'])
        novo_status_tabagismo = np.where(self.dataset['status_tabagismo'].isnull(), "desconhecido", self.dataset['status_tabagismo'])
        self.dataset['status_tabagismo'] = novo_status_tabagismo

        # remove outliers
        index1 = np.where(self.dataset["media_nivel_glicose"] == max(self.dataset["media_nivel_glicose"]))
        self.dataset = self.dataset.drop(index1[0])

        self.dataset = self.dataset[self.dataset['imc'] < 60]

        #
        self.dataset['sexo'] = self.dataset['sexo'].astype('category')
        self.dataset['tipo_residencia'] = self.dataset['tipo_residencia'].astype('category')
        self.dataset['sexo'] = self.dataset['sexo'].cat.codes
        self.dataset['tipo_residencia'] = self.dataset['tipo_residencia'].cat.codes

        self.dataset = pd.get_dummies(self.dataset,columns = ['tipo_trabalho','status_tabagismo'],prefix = ["trabalho",'tabagismo'])


    def get_features_target(self):
        # Divisão dos dados em X e Y
        X = self.dataset.loc[:, self.dataset.columns != 'avc']
        y = self.dataset['avc']
        return X, y



class Modeling:
    def __init__(self, X, y):
        self.X = X
        self.y = y

    def split_dataset(self):
        seed = 7
        test_size = 0.33
        X_treino, X_teste, y_treino, y_teste = train_test_split(self.X, self.y, test_size = test_size, random_state = seed)

        return X_treino, X_teste, y_treino, y_teste

    def train_model(self):
        X_treino, X_teste, y_treino, y_teste = self.split_dataset()
    
        # Cria o classificador
        modelo = RandomForestClassifier()

        # Treina e cria o modelo
        modelo.fit(X_treino, y_treino)

        if path.exists('model/modelo.pkl'):
            print("Modelo carregado")
        else:
            pickle.dump(modelo, open('model/modelo.pkl', 'wb'), protocol = 4)

        y_pred = modelo.predict(X_teste)
        
        acuracia = accuracy_score(y_teste, y_pred)
        print("Acurácia: %.2f%%" % (acuracia * 100.0))



if __name__ == '__main__':
    
    file_str =  '../data/dataset-avc.csv'
    dataset_obj = Preprocess(file_str)

    X,y = dataset_obj.get_features_target()
    
    modelo_v1 = Modeling(X,y)
 
    modelo_v1.train_model()
   

