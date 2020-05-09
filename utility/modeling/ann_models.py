print('Load tensorflow models')

# main imports
import numpy as np
from sklearn.metrics import roc_auc_score
import tensorflow as tf

class uni_AutoEncoder(object):
    def __init__(self,optimizer='adam',loss='mean_squared_error',metrics=None,epochs=50,batch_size=512,shuffle=True,
                 shuffle_buffer_size=2048,validation_split=0.2,verbose=1,
                 inter_layers=[(tf.keras.layers.Dense, {'units':64, 'activation':tf.nn.relu}),
                               (tf.keras.layers.Dense, {'units':64, 'activation':tf.nn.relu}),
                               (tf.keras.layers.Dense, {'units':8, 'activation':tf.nn.relu}),
                               (tf.keras.layers.Dense, {'units':64, 'activation':tf.nn.relu}),
                               (tf.keras.layers.Dense, {'units':64, 'activation':tf.nn.relu})],
                 def_threshold=10):
        self.inter_layers = inter_layers
        self.optimizer = optimizer
        self.loss = loss
        self.metrics = metrics
        self.epochs = epochs
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.shuffle_buffer_size = shuffle_buffer_size
        self.validation_split = validation_split
        self.verbose = verbose
        self.def_threshold = def_threshold
        self.roc_auc = None
        self.name = 'AutoEnc'
        self.sufix = 'x'.join([str(layer[1]['units']) for layer in inter_layers])

    def preprocess_data(self, data):
        data = data.astype('float32')
        data_tensor = tf.data.Dataset.from_tensor_slices((data, data))
        data_tensor = data_tensor.shuffle(self.shuffle_buffer_size).batch(self.batch_size)
        return data_tensor
    
    def build_keras_model(self, inputDim):
        """
        define the keras model
        the model based on the simple dense auto encoder (64*64*8*64*64)
        """
        inputLayer = tf.keras.layers.Input(shape=(inputDim,))
        
        for i, layer in enumerate(self.inter_layers):
            layer_type = layer[0]
            layer_kwargs = layer[1]
            if i == 0:
                h = layer_type(**layer_kwargs)(inputLayer)
            else:
                h = layer_type(**layer_kwargs)(h)
                
            h = tf.keras.layers.Dense(inputDim, activation=None)(h)

        return tf.keras.Model(inputs=inputLayer, outputs=h)
    
    def fit(self, data_train, y=None):
        # build model
        inputDim = data_train.shape[1]
        self.model = self.build_keras_model(inputDim)
        
        # compile and fit model
        self.model.compile(optimizer=self.optimizer, loss=self.loss, metrics=self.metrics)
        data_train = self.preprocess_data(data_train)
        self.model.fit(data_train,
                       epochs = self.epochs,
                       #validation_split = self.validation_split,
                       verbose = self.verbose)

    def predict_raw(self, data):
        return self.model.predict(data.astype('float32'))
    
    def predict(self, data):
        pred_label = np.array([-1 if i>self.def_threshold else 1 for i in self.predict_score(data)])
        return pred_label
    
    def predict_score(self, data):
        pred_score = -np.mean(np.square(data - self.predict_raw(data)), axis=1)
        return pred_score
        
    def eval_roc_auc(self, data_test, y_true):
        return roc_auc_score(y_true, self.predict_score(data_test))