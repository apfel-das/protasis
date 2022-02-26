from pydoc import describe
from traceback import print_tb
import numpy as np
import pandas as pd
import os
from tqdm import tqdm
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from surprise import Reader, Dataset, KNNBasic
from surprise.model_selection import cross_validate
from surprise import SVD
from dotenv import dotenv_values


config = dotenv_values(".env")

def test_score(test_data, actual_data: pd.DataFrame):
    users_to_movies = list(zip(test_data['movie_id'], test_data['user_id']))

    print(len(users_to_movies))

    predicted_ratings = []

    """
        This should take time, have some coffe and chill..
    """
    for (movie, user) in tqdm(users_to_movies, desc= "Calculating predicitions..."):
        rating = weighted_avg_predict(actual_data, movie, user)
        predicted_ratings.append(rating)
    

    actual = X_test['rating']


    #return the root_mean_sq_error.
    return np.sqrt(mean_squared_error(np.array(actual), np.array(predicted_ratings)))

     

def svd_predict(ratings: pd.DataFrame):
    #exclude unused column, KNNBasic() function needs data purified to work
    ratings = ratings.drop(columns='timestamp')

    """
        Defining/Creating the dataset.
    """
    reader = Reader()

    data = Dataset.load_from_df(ratings, reader)

    algo = SVD()

    r = cross_validate(algo, data, measures=['RMSE'], cv = 3)

    print(r)
    
    
"""
    Predicts the rating score for a given <user_id, movie_id> pair based on the KNN algorithm.
"""
def knn_predict(ratings: pd.DataFrame):

    #exclude unused column, KNNBasic() function needs data purified to work
    ratings = ratings.drop(columns='timestamp')

    """
        Defining/Creating the dataset.
    """
    reader = Reader()

    data = Dataset.load_from_df(ratings, reader)

    algo = KNNBasic()

    r = cross_validate(algo, data, measures=['RMSE', 'mae'], cv = 3)
    
    print(r)
    



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
    Samples the dataset based on a collumn.
"""
def sample_dataset(coll_name: str, data: pd.DataFrame, sample_factor: float):
    """
        No data to work with, dummies lead the way. 
    """
    try:

        #Assign X as the original ratings dataframe and y as the user_id column of ratings.
        X = data.copy()
        y = data[coll_name]
        #Split into training and test datasets, stratified along user_id
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = sample_factor, stratify=y, random_state=42)

        print("GG")
        return [X_train, X_test, y_train, y_test]

    except: 
        return None
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
        print(data)
        return data
    except:
        print("Exception occured on file: ["+file_name+"]" )


""" Discovers the actual file path.
    Arguments: 
        - relative_path: {str} A file-path to look for any file.
"""        
def discover_path(relative_path: str):
    dir = os.path.dirname(os.path.abspath(__file__))
    split_path = relative_path.split("/")
    actual_path = os.path.join(dir, *split_path)
    return actual_path

if __name__ == '__main__':
    print("Fuck off, that's a test..")


    ratings = read_from_csv(
        './movie_data/'+config['RATINGS_FILE'],
        ['user_id', 'movie_id', 'rating', 'timestamp'],
        '\t'
    )

    movies = read_from_csv(
        './movie_data/'+config['MOVIES_FILE'],
        ['movie_id', 'title' ,'release date','video release date', 'IMDb URL', 'unknown', 'Action', 'Adventure',
        'Animation', 'Children\'s', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy',
        'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western'],
        '|'
    )
    
    users = read_from_csv(
        './movie_data/'+config['USERS_FILE'],
        ['user_id', 'age', 'sex', 'occupation', 'zip_code'],
        '|'
    )

    [X_train, X_test, y_train, y_test] = sample_dataset('user_id', ratings, 0.25)
    df_ratings = X_train.pivot(index='user_id', columns='movie_id', values='rating')


    #sc = test_score(X_test, df_ratings)

    knn_predict(ratings)

    svd_predict(ratings)
