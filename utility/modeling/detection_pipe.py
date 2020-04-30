def find_max(ch_scores):
    ''' 
    1. returns the index of the first local maximum
    2. if first or element is global maximum, returns index 0
    '''
    
    maxima = argrelextrema(np.array(ch_scores), np.greater)
    
    if ch_scores[0] == np.max(ch_scores):
        maxima = [[0]]

    return maxima[0][0]

def evaluate_clustering(model, args, X, metric='ch_score'):
    # initiate scoring lists
    _score = []
    outlier = []

    # set up cluster storing
    clusters = []

    for arg_idx, arg in enumerate(args):
        # reinitialize model with arguments
        model.__init__(**arg)

        # store predictions
        _clusters = model.fit_predict(X)
        clusters.append(_clusters)

        if len(np.unique(_clusters)) >= 2: 
            # calculate the score
            if metric == 'ch_score':
                _score.append(calinski_harabasz_score(X, _clusters))

            elif metric == 'db_score':
                _score.append(davies_bouldin_score(X, _clusters))
        else:
            # if we have only 1 cluster, the scoring fails
            # we need to address this case
            _score.append(np.NaN)

        outlier.append(np.sum(_clusters==-1))

    # get the best set of model arguments
    if metric == 'ch_score':
        best_index = find_max(_score)

    elif metric == 'db_score':
        best_index = np.argmin(_score)

    best_args = args[best_index]
    best_clusters = clusters[best_index]

    return best_clusters, best_args, _score

def evaluate_args(ch_score, args, score_label='calinski harabasz score', keyword=None):

    plt.figure(figsize=(5,5), dpi=200)

    max_clusters = len(ch_score)

    # create the plot
    plt.title('Clustering metric score')

    plt.scatter(x=[i for i in range(2,max_clusters+2)],y=ch_score,s=50, edgecolor='k')

    plt.grid(True)
    plt.xlabel("number of clusters")
    plt.ylabel(score_label)
    plt.xticks([i for i in range(2,max_clusters+1)])

    plt.show()