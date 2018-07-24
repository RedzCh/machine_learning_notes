from . import main
from flask import current_app as app
from threading import Lock
from flask import Flask, render_template, session, request, Response
from jinja2 import FileSystemLoader, Environment
import os
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import Imputer

@main.route('/', methods=['GET'])
def index():
	return render_template('index.html')

@main.route('/data_sets',methods=['GET'])
def data_sets():
	return render_template('data_sets.html')

@main.route('/view_results', methods=['GET'])
def view_results():
    return render_template ("view_results.html")

def stream_template(template_name, **context):
    app.update_template_context(context)
    t = app.jinja_env.get_template(template_name)
    rv = t.stream(context)
    rv.enable_buffering(5)
    return rv

PATH = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'templates'))
DATA_PATH = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'data'))
RESULT_PATH = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'results'))

@main.route('/preprocessing', methods=['GET'])
def preprocessing():
	def inner():
	''' 
	This function generates the output to be displayed on the browser
	'''
		df = pd.read_csv(DATA_PATH + r'\train.csv')
		yield 'The Data Set has {} registers and {} features'.format(df.shape[0],df.shape[1])
		

		yield df.dropna(axis=1).columns.tolist()

		X_train_labels = df._get_numeric_data().columns.tolist()
		Numeric_labels = set(X_train_labels)
		Data_set_labels = set(df.columns.tolist())
		String_labels = Data_set_labels.difference(Numeric_labels)
		yield String_labels

		

		imr = Imputer(missing_values='NaN', strategy='mean', axis=0)
		imr = imr.fit(df.loc[:,X_train_labels[1:-1]])
		X_to_impute = df[X_train_labels[1:-1]].values
		X_train = imr.transform(X_to_impute)
		y_train = df['SalePrice'].values

		yield 'X_train and y_train ready to fit the forest'

		forest = RandomForestClassifier(n_estimators=100, random_state=0, n_jobs=-1)
		forest.fit(X_train, y_train)
		importances = forest.feature_importances_
		indices = np.argsort(importances)[::-1]

		yield 'Plotting the results '

		plt.title('Feature Importances')
		plt.bar(range(X_train.shape[1]), importances[indices], color='lightblue', align='center')
		plt.xticks(range(X_train.shape[1]), X_train_labels, rotation=90)
		plt.xlim([-1, X_train.shape[1]])
		plt.tight_layout()
		plt.savefig(RESULT_PATH + r'\result.svg', format="svg")
		#plt.show()

		yield 'Plot is saved  '


	templateLoader = FileSystemLoader(PATH)
	templateEnv = Environment(loader=templateLoader)
	TEMPLATE_FILE = "preprocessing.html"
	template = templateEnv.get_template(TEMPLATE_FILE)

	return Response(stream_template(template, result=inner()))
