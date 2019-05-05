from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
import pickle
from api.models import Etat
from sklearn.linear_model import LogisticRegression
import pyrebase
import time
from datetime import datetime, timezone
import pytz
import pandas as pd 
from scipy.io import loadmat
from os import listdir
from random import choice
from time import sleep


PATH="/home/kays/pim/seizure-detection/seizure-data/Patient_8/test/"
PATH_training="/home/kays/pim/seizure-detection/seizure-data/Patient_8/training/"

def mat_to_dataframe(path):
    mat = loadmat(path)['data']
    return pd.DataFrame(mat).transpose()


tz= pytz.timezone('Europe/Paris')
config = {

'apiKey': "AIzaSyBGWYlHu5sqFMdHALJ6rULTJlIEmKr48TA",
    'authDomain': "alertepsie.firebaseio.com/",
    'databaseURL': "https://alertepsie.firebaseio.com//",
    'projectId': "alertepsie",
    'storageBucket': "alertepsie.appspot.com"
  }

firebase = pyrebase.initialize_app(config)
database=firebase.database()
loaded_model = pickle.load(open('xgb_model.dat', 'rb'))

def getData(file,predict=True) : 
	data = mat_to_dataframe(file)
	df = data.iloc[0:100]
	for i in range(0,100) : 
		df.iloc[i] = data[i*50:(i+1)*50].mean() 
	X=pd.np.zeros(shape=(1,5000,16))
	nsamples, nx, ny = X.shape
	X = X.reshape((nsamples,nx*ny))
	if(predict) : 
		prediction=loaded_model.predict(X)[0]
		return (df,prediction)
	return df


@csrf_exempt
def home(request):
	files = listdir(PATH)
	flag = True
	file = PATH+choice(files)
	df,prediction=getData(file)
	notif_ref = database.child("eeg/data")
	data = df.transpose().to_dict()
	data["interictal"]=prediction
	new_notif = notif_ref.push(data)
	print("Sent")
	return HttpResponse("Updated")

@csrf_exempt
def ictal(request):
	print("ictal")
	files = listdir(PATH_training)
	ictal = list(filter(lambda file : "_ictal" in file ,files)) 
	flag = True
	file = PATH_training+choice(ictal)
	df=getData(file,predict=False)
	notif_ref = database.child("eeg/data")
	data = df.transpose().to_dict()
	data["interictal"]=0
	new_notif = notif_ref.push(data)
	print("Sent")
	return HttpResponse("Updated")


@csrf_exempt
def interictal(request):
	print("interictal")
	files = listdir(PATH_training)
	interictal = list(filter(lambda file : "interictal" in file ,files)) 
	file = PATH_training+choice(interictal)
	df=getData(file,predict=False)
	notif_ref = database.child("eeg/data")
	data = df.transpose().to_dict()
	data["interictal"]=1
	new_notif = notif_ref.push(data)
	print("Sent")
	return HttpResponse("Updated")

def stop(request) : 
	database.child("eeg/data").remove()
	return HttpResponse("Cleared")
