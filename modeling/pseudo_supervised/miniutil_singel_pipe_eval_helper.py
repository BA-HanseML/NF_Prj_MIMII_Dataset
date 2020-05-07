def Make_TTsplit_and_task(path, machines,SNRs,IDs, features,feat):
    path = BASE_FOLDER + path
    tt_split(path)
    with open(path, 'rb') as f:
        df = pickle.load(f)
        
        
    tasks = [{
        'path_descr':path, 
        'feat': feat, 
        'feat_col':feature, 
        'SNR':SNR, 
        'machine':machine, 
        'ID':ID,
        'BASE_FOLDER':BASE_FOLDER} 
        for machine in machines
        for SNR in SNRs
        for ID in IDs
        for feature in features
        ]
    # TODO keep single here and pump up later
    return df, tasks, machines[0]+IDs[0]+SNRs[0]+features[0]
    
    

def Model_Vali_Rec(m, X_train, X_test, y_train, y_test, df , name ,thres=0.5):
    fbeta=0.5
    
   
    y_ins_pred= m.predict(X_train)
    y_outs_pred= m.predict(X_test)
    y_base = np.ones(len(X_test))
    y_base0 = np.zeros(len(X_test))
    try:
        y_ins_pred_p= m.predict_proba(X_train)[:, 1]
        y_outs_pred_p= m.predict_proba(X_test)[:, 1]
        if thres!=0.5:

            y_ins_pred = [1. if e > thres else 0. for e in y_ins_pred_p]
            y_outs_pred = [1. if e > thres else 0. for e in y_outs_pred_p]
    except:
        y_ins_pred_p= y_ins_pred
        y_outs_pred_p= y_ins_pred 
        
    
    df.at['base  recall', name] = recall_score(y_test, y_base)
    df.at['test  recall', name] = recall_score(y_test, y_outs_pred)
    df.at['train recall', name] = recall_score(y_train, y_ins_pred)
    
    df.at['base  precision', name] = precision_score(y_test, y_base)
    df.at['test  precision', name] = precision_score(y_test, y_outs_pred)
    df.at['train precision', name] = precision_score(y_train, y_ins_pred)
   
    df.at['base  ROC-AUC', name] = roc_auc_score(y_test, y_base)
    df.at['test  ROC-AUC', name] = roc_auc_score(y_test, y_outs_pred_p)
    df.at['train ROC-AUC', name] = roc_auc_score(y_train, y_ins_pred_p)
    
    #df.at['base  f1', name] = f1_score(y_test, y_base)
    #df.at['test  f1', name] = f1_score(y_test, y_outs_pred)
    #df.at['train f1', name] = f1_score(y_train, y_ins_pred)
    
    #df.at[f'base  fb={fbeta}', name] = fbeta_score(y_test, y_base,fbeta)
    #df.at[f'test  fb={fbeta}', name] = fbeta_score(y_test, y_outs_pred, fbeta)
    #df.at[f'train fb={fbeta}', name] = fbeta_score(y_train, y_ins_pred, fbeta)
    
    df.at['base  accuracy', name] = accuracy_score(y_test, y_base)
    df.at['test  accuracy', name] = accuracy_score(y_test, y_outs_pred)
    df.at['train accuracy', name] = accuracy_score(y_train, y_ins_pred)
    
    #df.at['base  log loss', name] = log_loss(y_test, y_base)
    #df.at['test  log loss', name] = log_loss(y_test, y_outs_pred_p)
    #df.at['train log loss', name] = log_loss(y_train, y_ins_pred_p)
    
    #df.at['train rate truth', name] = rate(y_train)
    #df.at['test  rate truth', name] = rate(y_test)
    
   # df.at['train rate pred.', name] = rate(y_ins_pred)
   # df.at['test  rate pred.', name] = rate(y_outs_pred)
    
   # df.at['train entopy truth', name] = entropy_c(y_train)
   # df.at['test  entopy truth', name] = entropy_c(y_test)
    
   # df.at['train entopy pred.', name] = entropy_c(y_ins_pred)
   # df.at['test  entopy pred.', name] = entropy_c(y_outs_pred)
    
    cm = confusion_matrix(y_test, y_outs_pred)
    
    df.at['TN - act. norm', name] = cm[0,0]
    df.at['TP - act. abnr', name] = cm[1,1]
    df.at['FP - false alarm', name] = cm[0,1]
    df.at['FN - missed', name] = cm[1,0]

    
    base_fpr, base_tpr, base_tresh = roc_curve(y_test, y_base)
    test_fpr, test_tpr, test_tresh = roc_curve(y_test, y_outs_pred_p)
    train_fpr, train_tpr, train_tresh = roc_curve(y_train, y_ins_pred_p)
    plt.plot(base_fpr, base_tpr, 'b', label = 'baseline')
    plt.plot(test_fpr, test_tpr, 'r', label = 'model-test')
    plt.plot(train_fpr, train_tpr, 'g', label = 'model-train')
    plt.plot(train_fpr, train_tresh, 'k--', label = 'thresh')
    #print(len(train_tresh))
    plt.legend();
    plt.xlabel('False Positive Rate'); 
    plt.ylabel('True Positive Rate'); plt.title('ROC Curves');
    plt.show();
    
    
    #base_fpr, base_tpr, base_tresh = precision_recall_curve(y_test, y_base)
    #test_fpr, test_tpr, test_tresh = precision_recall_curve(y_test, y_outs_pred_p)
    #train_fpr, train_tpr, train_tresh = precision_recall_curve(y_train, y_ins_pred_p)
    #plt.plot(base_fpr, base_tpr, 'b', label = 'baseline')
    #plt.plot(test_fpr, test_tpr, 'r', label = 'model-test')
    #plt.plot(train_fpr, train_tpr, 'g', label = 'model-train')
    #plt.plot(train_fpr[1:], train_tresh, 'k--', label = 'thresh')
    ##print(len(train_tresh))
    #plt.legend();
    #plt.xlabel('precision'); 
    #plt.ylabel('recall'); plt.title('precision recall curve');
    #plt.show();
    
    
    
from sklearn.metrics import roc_auc_score,classification_report, roc_curve, \
auc,accuracy_score, confusion_matrix, precision_score, log_loss, fbeta_score, \
recall_score, make_scorer, f1_score, precision_recall_curve

def pipetask_to_metrics(p,t,df,name,thres=0.5):
    x_train, x_test = p.get_data(t)
    #x_train, x_test = p.preprocess(x_train, x_test )
    x_train, x_test = p.preprocess_post(x_train, x_test )
    
    #print(x_train.shape,x_test.shape)
    y_train = p.y_train
    y_test = p.ground_truth
    #y_pred_train = p.df_test['pred_scores']
    #y_test_pred = p.model.predict(x_test)
    #y_train_pred = p.model.predict(x_train)
    
    Model_Vali_Rec(p.model, x_train, x_test, y_train, y_test, df , name ,thres=thres)
    #print('out of sample')
    #print(confusion_matrix(y_test,y_test_pred))
    #print('out of sample')
    #print(confusion_matrix(y_train,y_train_pred))