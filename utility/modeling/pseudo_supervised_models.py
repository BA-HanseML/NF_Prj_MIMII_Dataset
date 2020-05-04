print('Load pseudo_supervised_models')


from sklearn.linear_model import LogisticRegression

# model_class_definition
class uni_LogisticRegression(LogisticRegression):
    def __init__(self, 
                 penalty='l2', 
                 tol=0.0001,
                 C=1.0, 
                 class_weight='balanced',
                 random_state=None, 
                 def_threshold=0):
        
        # most of the keywords are being routed directly to the mother
        super().__init__(penalty=penalty,
            tol=tol,
            C=C,
            class_weight=class_weight,
            random_state=random_state)

        self.def_threshold=def_threshold
        self.roc_auc = None

    # fit inherited
    # predict inherited

    def predict_score(self, data):
        return self.predict_proba(data)[:,1]

    def eval_roc_auc(self, data_test, y_true):
        return roc_auc_score(y_true, self.predict_score(data_test))
        
        
from sklearn.ensemble import RandomForestClassifier

class uni_RandomForestClassifier(RandomForestClassifier):
    def __init__(self, 
                 criterion='gini', 
                 max_depth=None,
                 min_samples_split=2, 
                 min_samples_leaf=1,
                 min_weight_fraction_leaf=0, 
                 max_features='auto',
                 max_leaf_nodes=None,
                 min_impurity_decrease=0.,
                 bootstrap=True,
                 random_state=25,
                 ccp_alpha=0.,
                 def_threshold=0):
        
        # most of the keywords are being routed directly to the mother
        super().__init__(criterion=criterion,
            max_depth=max_depth,
            min_samples_split=min_samples_split,
            min_samples_leaf=min_samples_leaf,
            min_weight_fraction_leaf=min_weight_fraction_leaf,
            max_features=max_features,
            max_leaf_nodes=max_leaf_nodes,
            min_impurity_decrease=min_impurity_decrease,
            bootstrap=bootstrap,
            random_state=random_state,
            ccp_alpha=ccp_alpha)

        self.def_threshold=def_threshold
        self.roc_auc = None

    # fit inherited
    # predict inherited

    def predict_score(self, data):
        return self.predict_proba(data)[:,1]

    def eval_roc_auc(self, data_test, y_true):
        return roc_auc_score(y_true, self.predict_score(data_test))
    