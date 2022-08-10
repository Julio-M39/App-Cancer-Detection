
"""

As 7 classes de lesões de câncer de pele incluídas neste conjunto de dados são:
Melanocytic nevi (nv)
Melanoma (mel)
Benign keratosis-like lesions (bkl)
Basal cell carcinoma (bcc) 
Actinic keratoses (akiec)
Vascular lesions (vas)
Dermatofibroma (df)

"""



import numpy as np
from PIL import Image
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import load_model


def getPrediction(filename):
    
    classes = ['Actinic keratoses', 'Basal cell carcinoma', 
               'Benign keratosis-like lesions', 'Dermatofibroma', 'Melanoma', 
               'Melanocytic nevi', 'Vascular lesions']
    le = LabelEncoder()
    le.fit(classes)
    le.inverse_transform([2])
    
    
    #Carregando o model
    my_model=load_model("model/HAM10000_100epochs.h5")
    
    SIZE = 32 #Redimensionar para o mesmo tamanho das imagens de treinamento
    img_path = 'static/images/'+filename
    img = np.asarray(Image.open(img_path).resize((SIZE,SIZE)))
    
    img = img/255.      #Valores de pixel de escala
    
    img = np.expand_dims(img, axis=0)  #Prepare-o como entrada para a rede
    
    pred = my_model.predict(img) #Prever          
    
    #Converter previsão em nome de classe
    pred_class = le.inverse_transform([np.argmax(pred)])[0]
    print("Diagnosis is:", pred_class)
    return pred_class


a = getPrediction('mel.jpg')
print(a)


