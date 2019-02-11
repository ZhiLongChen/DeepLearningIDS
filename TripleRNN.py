import pandas as pd
import numpy as np
from sklearn import metrics
from keras.models import Sequential
from keras.layers.core import Dense
from keras.layers.recurrent import SimpleRNN
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping
from DataPreProcessing import exclude_inf, standardizing, load_data

LR = 0.001
LAYERS = 50
EPOCHS = 100
BATCH_SIZE = 5


if __name__ == '__main__':
    file_path = './Dataset/3class/data1.csv'
    data = pd.read_csv(file_path)
    data = exclude_inf(data)

    label = 'marker'
    data, class_number = standardizing(data, label)
    # display 5 rows
    data.dropna(inplace=True, axis=1)

    # Break into X (predictors) & y (prediction)

    (x_train, y_train), (x_test, y_test) = load_data(data, label)

    # print("x_train.shape={}".format(x_train.shape))
    # print("y_train.shape={}".format(y_train.shape))

    model = Sequential()

    model.add(SimpleRNN(units=50, input_shape=(1, x_train.shape[2])))

    model.add(Dense(units=class_number, kernel_initializer='normal', activation='softmax'))
    # 編譯: 選擇損失函數、優化方法及成效衡量方式

    adam = Adam(LR)

    model.compile(loss='categorical_crossentropy', optimizer=adam, metrics=['accuracy'])

    monitor = EarlyStopping(monitor='val_loss', min_delta=1e-3, patience=5, verbose=1, mode='auto')

    model.fit(x_train, y_train, batch_size=BATCH_SIZE, validation_data=(x_test, y_test), callbacks=[monitor], verbose=1,
              epochs=EPOCHS)

    # print(model.get_config())

    # Measure accuracy
    pred = model.predict(x_test)
    pred = np.argmax(pred, axis=1)
    y_eval = np.argmax(y_test, axis=1)
    accuracy = metrics.accuracy_score(y_eval, pred)

    precision, recall, f_score, _ = metrics.precision_recall_fscore_support(y_eval, pred, average='macro')

    print("Accuracy: {0:.2f}%".format(accuracy * 100))
    print("Precision: {0:.2f}%".format(precision * 100))
    print("Recall: {0:.2f}%".format(recall * 100))
    print("F-Measure: {}".format(f_score))

