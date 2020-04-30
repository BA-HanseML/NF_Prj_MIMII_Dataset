print('Load anomaly_detection_models')

# main imports
from sklearn.covariance import EllipticEnvelope
from sklearn.ensemble import IsolationForest
from sklearn.mixture import GaussianMixture
from sklearn.svm import OneClassSVM
from sklearn.metrics import roc_auc_score

# model_class_definition
class uni_EllipticEnvelope(EllipticEnvelope):
    def __init__(self, 
                 store_precision=True, 
                 assume_centered=False,
                 support_fraction=None, 
                 contamination=0.1,
                 random_state=None, 
                 def_threshold=0):
        
        # most of the keywords are being routed directly to the mother
        super().__init__(store_precision=store_precision,
            assume_centered=assume_centered,
            support_fraction=support_fraction,
            contamination=contamination,
            random_state=random_state)

        self.def_threshold=def_threshold
        self.roc_auc = None

    # fit inherited
    # predict inherited

    def predict_score(self, data):
        return self.decision_function(data)

    def eval_roc_auc(self, data_test, y_true):
        return roc_auc_score(y_true, self.predict_score(data_test))

class uni_IsolationForest(IsolationForest):
    pass

class uni_OneClassSVM(OneClassSVM):
    pass