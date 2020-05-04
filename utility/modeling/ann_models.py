print('Load anomaly_detection_models')

# main imports
from sklearn.metrics import roc_auc_score
import tensorflow as tf

class MyModel(tf.keras.Model):

  def __init__(self):
    super(MyModel, self).__init__()
    #self.layers = []
    self.input_layer = tf.keras.layers.Input(shape=(400,))
    self.output_layer = tf.keras.layers.Dense(400, activation=None)
    self.dense1 = tf.keras.layers.Dense(64, activation=tf.nn.relu)
    self.dense2 = tf.keras.layers.Dense(64, activation=tf.nn.relu)
    self.dense3 = tf.keras.layers.Dense(8, activation=tf.nn.relu)
    self.dense4 = tf.keras.layers.Dense(64, activation=tf.nn.relu)
    self.dense5 = tf.keras.layers.Dense(64, activation=tf.nn.relu)

  def call(self, inputs, training=False):
    x = self.input_layer(inputs)
    x = self.dense1(x)
    x = self.dense2(x)
    x = self.dense3(x)
    x = self.dense4(x)
    x = self.dense5(x)
    return self.output_layer(x)



class uni_AutoEncoder(tf.keras.Model):
    def __init__(self,
                 # initialization parameters
                 optimizer='adam',
                 loss='mean_squared_error',
                 metrics=None,
                 # fitting parameters
                 epochs=50,
                 batch_size=24,
                 shuffle=True,
                 validation_split=0.1,
                 verbose=1,
                 inter_layers=None,
                 def_threshold=0
                 ):
        
        super().__init__()
        
        if not inter_layers:
            self.inter_layers = []
            self.inter_layers.append(tf.keras.layers.Dense(64, activation=tf.nn.relu))
            self.inter_layers.append(tf.keras.layers.Dense(64, activation=tf.nn.relu))
            self.inter_layers.append(tf.keras.layers.Dense(8, activation=tf.nn.relu))
            self.inter_layers.append(tf.keras.layers.Dense(64, activation=tf.nn.relu))
            self.inter_layers.append(tf.keras.layers.Dense(64, activation=tf.nn.relu))
        else:
            self.inter_layers = inter_layers
        
        self.optimizer = optimizer
        self.loss = loss
        
        self.epochs = epochs
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.validation_split = validation_split
        self.verbose = verbose
        
        self.def_threshold=def_threshold
        self.roc_auc = None
        self.uni_name = 'AutoEnc'
        self.sufix = '' # '{}comp'.format(self.n_components)

    # compile inherited
    
    def call(self, inputs, training):
        super().call(inputs, training)
        # h = self.input_layer(inputs)
        # return self.output_layer(h)
    
    def forward_model(self, inputDim):
        input_layer = tf.keras.layers.Input(shape=(inputDim,))
        output_layer = tf.keras.layers.Dense(inputDim, activation=None)
        
        h = input_layer
        for layer in self.inter_layers:
            h = layer(h)
        
        return input_layer, output_layer(h)
    
    def fit(self, data_train):
        # add input and output-layer
        inputDim = data_train.shape[1]
        print('im here')
        # compile and fit model
        self.input_layer, self.output_layer = self.forward_model(inputDim)
        super().__init__(inputs=self.input_layer, outputs=self.output_layer)
        print('im here')
        super().compile(optimizer=self.optimizer, loss=self.loss)
        print(self.summary)
        print('im here')
        self.history = super().fit(data_train, 
                    data_train,
                    epochs = self.epochs,
                    batch_size = self.batch_size,
                    shuffle = self.shuffle,
                    validation_split = self.validation_split,
                    verbose = self.verbose)
                
        
    # predict inherited

    def predict_score(self, data):
        error_pred = data - self.predict(data)
        return error_pred
        
    def eval_roc_auc(self, data_test, y_true):
        return roc_auc_score(y_true, self.predict_score(data_test))