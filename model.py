from distutils.command.config import dump_file
from tabnanny import verbose
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from surprise import Reader
from surprise import Dataset 
from surprise import KNNBasic
from surprise import dump
from surprise.model_selection import cross_validate
from surprise import SVD
from collections import defaultdict


RATINGS_FILE='u.data'
MOVIES_FILE='u.item'
USERS_FILE='u.user'
SVD_FILE='predictions_svd'
KNN_FILE='predictions_knn'

def test_score(test_data, actual_data: pd.DataFrame):
    users_to_movies = list(zip(test_data['movie_id'], test_data['user_id']))

    print(len(users_to_movies))

    predicted_ratings = []

    """
        This should take time, have some coffe and chill..
    """
    for (movie, user) in users_to_movies:
        rating = weighted_avg_predict(actual_data, movie, user)
        predicted_ratings.append(rating)
    

    actual = X_test['rating']


    #return the root_mean_sq_error.
    return np.sqrt(mean_squared_error(np.array(actual), np.array(predicted_ratings)))




def get_top_predictions(predictions: list, n = 10):
    top_n = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        top_n[uid].append((iid, est))

    # Then sort the predictions for each user and retrieve the k highest ones.
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:n]

    return top_n




    
"""
    Predicts the rating score for a given <user_id, movie_id> pair based on the KNN algorithm.
"""
def predict_items(ratings: pd.DataFrame, algo: str, file: str):

    allowed_algos = ['knn', 'svd']

    if algo not in allowed_algos:
        return None

    #exclude unused column, KNNBasic() function needs data purified to work
    ratings = ratings.drop(columns='timestamp')

    """
        Defining/Creating the dataset.
    """
    reader = Reader()

    data = Dataset.load_from_df(ratings, reader)

    """
        Train, fit, predict..
    """

    trainset = data.build_full_trainset()
    algo = KNNBasic() if algo == 'knn' else SVD()
    algo.fit(trainset)

    #predict ratings for all pairs (user, item/movie) that are NOT in the training set.
    testset = trainset.build_anti_testset()
    predictions = algo.test(testset)

    """
        Write result on file.
    """       
    dump.dump(file, predictions, verbose= 1)

    return predictions



"""
    Predicts the rating score for a given <user_id, movie_id> pair based on cosine similarity of the weights.
"""
def weighted_avg_predict(ratings: pd.DataFrame, movie_id: int, user_id: int): 
    #cache the ratings dataframe
    ratings_cp = ratings.copy().fillna(0)

    #create a similarity matrix
    sim_grid = cosine_similarity(ratings_cp, ratings_cp)

    #make it a dataframe
    sim_grid_df = pd.DataFrame(sim_grid, index= ratings.index, columns= ratings.index)
    if user_id in ratings and movie_id in ratings:
        

        try:
            #similarity of user_id with other users.
            user_similarity_scores = sim_grid_df[user_id]

            #ratings of other users for movie_id
            user_ratings = ratings[movie_id]
            """
                Exclude users who havent rated <movie_id> even if similar.
            """
            index_non_rated = user_ratings[user_ratings.isnull()].index

            user_ratings = user_ratings.dropna()

            user_similarity_scores = user_similarity_scores.drop(index_non_rated)

            """
                Weight the mean of ratings and cosine score o users who have actually rated the movie.
            """

            ratings_movie = np.dot(user_ratings, user_similarity_scores)/user_similarity_scores.sum()

            return ratings_movie
        except:
            return 2.5

    else: 
        return 2.5  
        

"""
    Reads data from a csv.
    Arguments:
        - file_name: csv's file name.
        - collumns: a list of collumns.
        - sep: collumns separator on csv.
    Note: 
        Acts a wrapper for pandas.read_csv to perform checks before reading. 
"""

def read_from_csv(file_name: str, collumns: list, sep: str):
    try:
        data = pd.read_csv(file_name, sep = sep, names = collumns, encoding= 'latin-1')
        return data
    except:
        print("Exception occured on file: ["+file_name+"]" )



def read_ratings_from_file():
    
    return read_from_csv(
        './movie_data/'+RATINGS_FILE,
        ['user_id', 'movie_id', 'rating', 'timestamp'],
        '\t'
    )

def read_movies_from_file():
    return read_from_csv(
        './movie_data/'+MOVIES_FILE,
        ['movie_id', 'title' ,'release date','video release date', 'IMDb URL', 'unknown', 'Action', 'Adventure',
        'Animation', 'Children\'s', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy',
        'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western'],
        '|'
    )

def read_users_from_file():
    return read_from_csv(
        './movie_data/'+USERS_FILE,
        ['user_id', 'age', 'sex', 'occupation', 'zip_code'],
        '|'
    )

def predict_top_for_user(uid: int, prediction_file: str, len: int):

    predictions = dump.load(prediction_file)[0]


    if len <= 0 or not predictions:
        return None

    items = []

    print("Reached here..")
    top_n = get_top_predictions(predictions, len)

    

    # List the recommended items for each user
    for u, user_ratings in top_n.items():
        if uid == u:
            for el in user_ratings:
                items.append(el[0])

    print(items)
    return items






    
    
    