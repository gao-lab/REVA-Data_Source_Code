#############
'''RAEDME'''
#This is the model structure
#############
import tensorflow as tf
import tensorflow.contrib.keras as keras

'''For DNA accessibility, TF and histone modification'''
def cnn_model(filter_num,filter_len,pool_len,units):
    model = keras.models.Sequential()
    model.add(keras.layers.Conv1D(
        filter_num,
        filter_len,
        strides=1,
        input_shape=(200,4),
        padding='same'))
    model.add(keras.layers.ThresholdedReLU(theta=1e-8))
    model.add(keras.layers.MaxPool1D(pool_size=pool_len,padding='valid'))
    model.add(keras.layers.Dropout(0.5))
    
    model.add(keras.layers.Flatten())
    model.add(keras.layers.Dense(units=units))
    model.add(keras.layers.ThresholdedReLU(theta=1e-8))
    model.add(keras.layers.Dropout(0.2))
    model.add(keras.layers.Dense(units=1,activation='sigmoid'))
    return model

'''For DNA methylation'''
def cnn_model(filter_num,filter_len,pool_len,units):
    model = keras.models.Sequential()    
    model.add(keras.layers.Conv1D(
        filter_num,
        filter_len,
        strides=1,
        input_shape=(200,4),
        padding='same'))
    model.add(keras.layers.ThresholdedReLU(theta=1e-8))
    model.add(keras.layers.MaxPool1D(pool_size=pool_len,padding='valid'))
    model.add(keras.layers.Dropout(0.2))
    model.add(keras.layers.Conv1D(
        256,
        filter_len,
        strides=1,
        padding='same'))
    model.add(keras.layers.ThresholdedReLU(theta=1e-8))
    model.add(keras.layers.MaxPool1D(pool_size=pool_len,padding='valid'))
    model.add(keras.layers.Dropout(0.5))
    
    model.add(keras.layers.Flatten())
    model.add(keras.layers.Dense(units=units))
    model.add(keras.layers.ThresholdedReLU(theta=1e-8))
    model.add(keras.layers.Dropout(0.2))
    model.add(keras.layers.Dense(units=1,activation='sigmoid'))
    return model