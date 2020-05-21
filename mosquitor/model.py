# coding: utf-8


'''
Description : 
    best predictive model for our data (Preprocessed/Raw).
    'main' class of our model:
    - fit: trains the model.
    - predict: uses the model to perform predictions.
    - save: saves the model.
    - load: reloads the model.
'''

from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from __future__ import unicode_literals

import pickle
import numpy as np
from os.path import isfile

from sklearn.base import BaseEstimator
from sklearn.base import ClassifierMixin
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

from preprocessing import PreproPreprocessed
from preprocessing import PreproRaw



__author__ = "MOSQUITO"



class ModelPreprocessed(BaseEstimator, ClassifierMixin):
    def __init__(self, classifier = RandomForestClassifier(random_state = 42, n_estimators = 760, max_depth=28)):
        '''
        Best model for classification in the preprocessed challenge
         args:
             Classifier: classifier used in our model
        '''
        self.prepro = PreproPreprocessed()
        self.StSc = StandardScaler()
        self.classifier = classifier

    def fit(self, X, y):
        '''
        Training the model.
        Args:
            X: Training data matrix of dim num_train_samples * num_feat.
            y: Training label matrix of dim num_train_samples * num_labels.
        Both inputs are numpy arrays.
        '''
        X = self.prepro.fit_transform(X, y)
        X = self.StSc.fit_transform(X, y)
        self.classifier.fit(X, y)
        return self

    def predict_proba(self, X):
        '''
        Compute probabilities to belong to given classes.
        '''
        X = self.prepro.transform(X)
        X = self.StSc.transform(X)
        y_proba = self.classifier.predict_proba(X)
        return y_proba

    def predict(self, X):
        y_proba = self.predict_proba(X)
        y_pred = np.argmax(y_proba, axis=1)
        return y_pred
    
    def save(self, path="./"):
        pickle.dump(self, open(path + '_model.pickle', "wb"))

    def load(self, path="./"):
      modelfile = path + '_model.pickle'
      if isfile(modelfile):
         with open(modelfile, 'rb') as f:
            self = pickle.load(f)
         print("Model reloaded from: " + modelfile)
      return self



class ModelRaw(BaseEstimator, ClassifierMixin):
    def __init__(self, classifier = RandomForestClassifier(random_state = 42, n_estimators = 760, max_depth=28)):
        '''
        Best model for classification in the raw challenge
         args: 
             Classifier: classifier used in our model
        '''
        self.prepro = PreproRaw()
        self.classifier = classifier

    def fit(self, X, y):
        '''
        Training the model.
        Args:
            X: Training data matrix of dim num_train_samples * num_feat.
            y: Training label matrix of dim num_train_samples * num_labels.
        Both inputs are numpy arrays.
        '''
        X = self.prepro.fit_transform(X, y)
        self.classifier.fit(X, y)
        return self

    def predict_proba(self, X):
        '''
        Compute probabilities to belong to given classes.
        '''
        X = self.prepro.transform(X)
        y_proba = self.classifier.predict_proba(X)
        return y_proba

    def predict(self, X):
        y_proba = self.predict_proba(X)
        y_pred = np.argmax(y_proba, axis=1)
        return y_pred

    def save(self, path="./"):
        pickle.dump(self, open(path + '_model.pickle', "wb"))

    def load(self, path="./"):
      modelfile = path + '_model.pickle'
      if isfile(modelfile):
         with open(modelfile, 'rb') as f:
            self = pickle.load(f)
         print("Model reloaded from: " + modelfile)
      return self


# Adpat to Codalab interface
# ModelPreprocessed for preprocessed challenge
# ModelRaw for raw challenge
model = ModelRaw
