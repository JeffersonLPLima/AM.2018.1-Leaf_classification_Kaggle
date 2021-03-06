import numpy as np
import pandas as pd
from  scipy import ndimage
from scipy import misc
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedShuffleSplit

from matplotlib import pyplot as plt



train = pd.read_csv('train.csv')
test = pd.read_csv('test.csv')


img_dir = 'images/'
n_images = 1584
rows = int(467*0.2)
cols = int(526*0.2)
def encode(train, test):
    label_encoder = LabelEncoder().fit(train.species)
    labels = label_encoder.transform(train.species)
    classes = list(label_encoder.classes_)

    train = train.drop(['species', 'id'], axis=1)
    test = test.drop('id', axis=1)

    return train, labels, test, classes




def load_image_data():
    _2d_images=[]
    img_data = np.vstack([misc.imresize(arr= ndimage.imread(img_dir+str(i+1)+'.jpg'), size= (rows, cols), interp='bilinear', mode=None).reshape(-1,)  for i in range(n_images)])

    for i in range(n_images):
        _2d_images.append(misc.imresize(arr= ndimage.imread(img_dir+str(i+1)+'.jpg'), size= (rows, cols), interp='bilinear', mode=None))

    return img_data, _2d_images

train, labels, test, classes = encode(train, test)
train = train.values

img_data, _2d_images = load_image_data()


##plt.imshow(_2d_images[0])#, interpolation='nearest')
##plt.show()
#img_data = np.array(img_data)
##img_data = img_data.reshape(1584, rows,cols)
print("data loaded")

# splittrain data into train and validation
sss = StratifiedShuffleSplit(test_size=0.2, random_state=23)
for train_index, valid_index in sss.split(train, labels):
    X_train, X_valid = train[train_index], train[valid_index]
    y_train, y_valid = labels[train_index], labels[valid_index]
    X_train_img, X_valid_img = img_data[train_index], img_data[valid_index]
    
X_test = test.values

  
print("Done")
##
##scaler = StandardScaler()
##X_train = scaler.fit(X_train).transform(X_train)
##X_valid = scaler.fit(X_valid).transform(X_valid)

## Classifying

from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

from sklearn import tree
neigh = KNeighborsClassifier(n_neighbors=1)
neigh.fit(X_train, y_train)
p_n = neigh.predict_proba(X_valid)#, y_valid)

svm = SVC(probability=True)
svm.fit(X_train, y_train)
p_svm = svm.predict_proba(X_valid)


tree = tree.DecisionTreeClassifier()
tree.fit(X_train, y_train)
p_tree = tree.predict_proba(X_valid)


##############################################
###       CNN  ##

##import keras
##from keras.datasets import mnist
##from keras.models import Sequential
##from keras.layers import Dense, Dropout, Flatten
##from keras.layers import Conv2D, MaxPooling2D, AveragePooling2D
##from keras import backend as K
##from keras.callbacks import ReduceLROnPlateau, EarlyStopping
##
##batch_size = 128
##num_classes = len(classes)
##epochs = 20
##input_shape = (rows, cols, 1)  #definindo o tamanho da entrada da rede
##
##
##print(batch_size, num_classes, epochs)
##y_train = keras.utils.to_categorical(y_train, num_classes)  #convertendo as classes em vetores binários (one hot encoding)
##y_val = keras.utils.to_categorical(y_valid, num_classes)  
##
##model = Sequential()      #Criando o modelo
##model.add(Conv2D(32, (3, 3), activation='relu', input_shape=input_shape))         #Camada de convolução 2d, com janela 3x3, e Adcionando a ativação relu.
##model.add(Conv2D(64, (3, 3), activation='relu'))  	 #Camada de convolução 2d, com janela 3x3, e Adcionando a ativação relu.
##model.add(AveragePooling2D(pool_size=(2, 2)))        #Camada de Pooling 2d, de tamanho 2x2, através da média. (Retira a média aritmética de janelas 2x2 na imagem, reduzindo a quantidade de características 4->1 por janela)
##model.add(Dropout(0.25))       #Camada de Dropout para evitar overfitting. Nada mais é do que desativar um neurônio. No caso a probabilidade de que isso seja feita é de 0.25, no exemplo em questão. 
##model.add(Flatten())    #Reduz a dimensão da camada. output_shape == (None, 64, 32, 32) -> Flatten() -> output_shape == (None, 65536)
##														
##model.add(Dense(128, activation='relu'))     #Camada completamente conectada
##model.add(Dense(num_classes, activation='softmax'))   #Camada de saída, com ativação softmax.
##
##model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
##
###Reduz a taxa de aprendizado
##reduce_lr = ReduceLROnPlateau(monitor='val_loss',  #observar a função de perda no conjunto de validação
##							factor=0.2,     #fator pela qual a taxa será reduzida -> nova_taxa = taxa_atual * factor
##							verbose=1, 
##							patience=1,    # número de épocas, sem redução na função de perda, que o monitor espera para agir.
##							min_lr=0.0001) 	#limite inferior da nova_taxa. Menor que isso e o monitor não irá reduzir mais a taxa.
##
###Interrompe o treinamento
##early_stopping=EarlyStopping(monitor='val_loss', #observar a função de perda no conjunto de validação
##							patience=4,    # número de épocas, sem redução na função de perda, que o monitor espera para agir.
##							verbose=1,)    
##																		
##																  #fazendo uso dos monitores criados		
##model.fit(X_train_img, y_train, batch_size=batch_size, epochs=epochs, callbacks=[reduce_lr, early_stopping], verbose=1, validation_data=(X_valid_img, y_valid))
##
####loss, accuracy = model.evaluate(x_test, y_test, verbose=0)
####
####print('Test accuracy:', accuracy)



import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D, AveragePooling2D
from keras import backend as K
from keras.callbacks import ReduceLROnPlateau, EarlyStopping


batch_size = 128
num_classes = len(classes)
epochs = 100


y_train_cat = keras.utils.to_categorical(y_train, num_classes)  #convertendo as classes em vetores binários (one hot encoding)
y_valid_cat = keras.utils.to_categorical(y_valid, num_classes)  


print("to_categorical")

model = Sequential()
model.add(Dense(512, activation='relu', input_shape=(X_train.shape[1],)))
model.add(Dropout(0.2))
model.add(Dense(512, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(num_classes, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

  
# monitores para o treinamento da rede
#https://keras.io/callbacks/

#Reduz a taxa de aprendizado
reduce_lr = ReduceLROnPlateau(monitor='val_loss',  #observar a função de perda no conjunto de validação
							factor=0.2,     #fator pela qual a taxa será reduzida -> nova_taxa = taxa_atual * factor
							verbose=1, 
							patience=1,    # número de épocas, sem redução na função de perda, que o monitor espera para agir.
							min_lr=0.0001) 	#limite inferior da nova_taxa. Menor que isso e o monitor não irá reduzir mais a taxa.

#Interrompe o treinamento
early_stopping=EarlyStopping(monitor='val_loss', #observar a função de perda no conjunto de validação
							patience=4,    # número de épocas, sem redução na função de perda, que o monitor espera para agir.
							verbose=1,)    

															  #fazendo uso dos monitores criados		
history= model.fit(X_train, y_train_cat, batch_size=batch_size, epochs=epochs, callbacks=[reduce_lr, early_stopping], verbose=1, validation_data=(X_valid, y_valid_cat))

print("1-NN: ",1-neigh.score(X_valid, y_valid))
print("SVM: ",1-svm.score(X_valid, y_valid))
print('Tree: ',1-tree.score(X_valid, y_valid))
print("MLP:", 1-model.evaluate(X_valid, y_valid_cat, verbose=0)[1])





plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.show()
# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.show()
