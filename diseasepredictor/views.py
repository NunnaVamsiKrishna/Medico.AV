from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
import numpy as np
import pandas as pd
from scipy.stats import mode
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier

# Create your views here.

@login_required()
def dp(request):
    return render(request,"dp.html")

@login_required()
def result(request):
    DATA_PATH = "diseasepredictor\Training.csv"
    data = pd.read_csv(DATA_PATH).dropna(axis = 1)
    # Checking whether the dataset is balanced or not
    disease_counts = data["prognosis"].value_counts()
    temp_df = pd.DataFrame({
        "Disease": disease_counts.index,
        "Counts": disease_counts.values
    })

    # Encoding the target value into numerical
    # value using LabelEncoder
    encoder = LabelEncoder()
    data["prognosis"] = encoder.fit_transform(data["prognosis"])


    X = data.iloc[:,:-1]
    y = data.iloc[:, -1]
    X_train, X_test, y_train, y_test =train_test_split(
    X, y, test_size = 0.2, random_state = 24)

    models = {
	"SVC":SVC(),
	"Gaussian NB":GaussianNB(),
	"Random Forest":RandomForestClassifier(random_state=18)
    }

    # Training and testing SVM Classifier
    svm_model = SVC()
    svm_model.fit(X_train, y_train)
    preds = svm_model.predict(X_test)

    # Training and testing Naive Bayes Classifier
    nb_model = GaussianNB()
    nb_model.fit(X_train, y_train)
    preds = nb_model.predict(X_test)

    # Training and testing Random Forest Classifier
    rf_model = RandomForestClassifier(random_state=18)
    rf_model.fit(X_train, y_train)
    preds = rf_model.predict(X_test)

    final_svm_model = SVC()
    final_nb_model = GaussianNB()
    final_rf_model = RandomForestClassifier(random_state=18)
    final_svm_model.fit(X, y)
    final_nb_model.fit(X, y)
    final_rf_model.fit(X, y)

    # Reading the test data
    test_data = pd.read_csv("diseasepredictor\Testing.csv").dropna(axis=1)

    test_X = test_data.iloc[:, :-1]
    test_Y = encoder.transform(test_data.iloc[:, -1])

    # Making prediction by take mode of predictions
    # made by all the classifiers
    svm_preds = final_svm_model.predict(test_X)
    nb_preds = final_nb_model.predict(test_X)
    rf_preds = final_rf_model.predict(test_X)

    final_preds = [mode([i,j,k])[0][0] for i,j,
                k in zip(svm_preds, nb_preds, rf_preds)]

    symptoms = X.columns.values

    # Creating a symptom index dictionary to encode the
    # input symptoms into numerical form
    symptom_index = {}
    for index, value in enumerate(symptoms):
        symptom = " ".join([i.capitalize() for i in value.split("_")])
        symptom_index[symptom] = index

    data_dict = {
        "symptom_index":symptom_index,
        "predictions_classes":encoder.classes_
    }

    # Defining the Function
    # Input: string containing symptoms separated by commmas
    # Output: Generated predictions by models
    def predictDisease(symptoms):
        symptoms = symptoms.split(",")
        
        # creating input data for the models
        input_data = [0] * len(data_dict["symptom_index"])
        for symptom in symptoms:
            index = data_dict["symptom_index"][symptom]
            input_data[index] = 1
            
        # reshaping the input data and converting it
        # into suitable format for model predictions
        input_data = np.array(input_data).reshape(1,-1)
        
        # generating individual outputs
        rf_prediction = data_dict["predictions_classes"][final_rf_model.predict(input_data)[0]]
        nb_prediction = data_dict["predictions_classes"][final_nb_model.predict(input_data)[0]]
        svm_prediction = data_dict["predictions_classes"][final_svm_model.predict(input_data)[0]]
        
        # making final prediction by taking mode of all predictions
        final_prediction = mode([rf_prediction, nb_prediction, svm_prediction])[0][0]
        predictions = {
            final_prediction
        }
        return predictions

    v1 = request.GET['s1']
    v2 = request.GET['s2']
    v3 = request.GET['s3']
    v4 = request.GET['s4']

    # Testing the function
    disease = predictDisease("{},{},{},{}".format(v1,v2,v3,v4))

    disease = str(disease)
    disease = disease[2:len(disease)-2]+'!'

    return render(request, "result.html", {"disease":disease})