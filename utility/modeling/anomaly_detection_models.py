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
    def __init__(self, 
                 n_estimators=100,
                 max_samples="auto",
                 contamination="auto",
                 max_features=1.,
                 bootstrap=False,
                 n_jobs=-1,
                 behaviour='deprecated',
                 random_state=42,
                 verbose=0,
                 warm_start=False, 
                 def_threshold=0):
        
        # most of the keywords are being routed directly to the mother
        super().__init__(n_estimators=n_estimators,
                         max_samples=max_samples,
                         contamination=contamination,
                         max_features=max_features,
                         bootstrap=bootstrap,
                         n_jobs=n_jobs,
                         behaviour=behaviour,
                         random_state=random_state,
                         verbose=verbose,
                         warm_start=warm_start)

        self.def_threshold=def_threshold
        self.roc_auc = None

    # fit inherited
    # predict inherited

    def predict_score(self, data):
        return self.decision_function(data)

    def eval_roc_auc(self, data_test, y_true):
        return roc_auc_score(y_true, self.predict_score(data_test))

class uni_OneClassSVM(OneClassSVM):
    def __init__(self, 
                 kernel='rbf', 
                 degree=3, 
                 gamma='scale',
                 coef0=0.0, 
                 tol=1e-3, 
                 nu=0.5, 
                 shrinking=True, 
                 cache_size=200,
                 verbose=False, 
                 max_iter=-1, 
                 def_threshold=0
                 ):
        
        # most of the keywords are being routed directly to the mother
        super().__init__(kernel=kernel, 
                        degree=degree, 
                        gamma=gamma,
                        coef0=coef0, 
                        tol=tol, 
                        nu=nu, 
                        shrinking=shrinking, 
                        cache_size=cache_size,
                        verbose=verbose, 
                        max_iter=-1)

        self.def_threshold=def_threshold
        self.roc_auc = None

    # fit inherited
    # predict inherited

    def predict_score(self, data):
        return self.decision_function(data)

    def eval_roc_auc(self, data_test, y_true):
        return roc_auc_score(y_true, self.predict_score(data_test))