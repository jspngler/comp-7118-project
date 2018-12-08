#!/usr/bin/env python3

import math
import argparse
import csv

# going to use a dict, with movie_id as the key, for movies because movie_id has a 1-to-1 relation with movie
movies = {}  # {movie_id: {genre, title}}
# a movie_id can have multiple ratings. going to use a dict of lists
ratings_by_movie_id = {}  # {movie_id: [{user_id, rating}]}
ratings_by_movie_id_for_sklearn = {}  # {movie_id: {user_id: rating}}
# a user_id can have multiple ratings. going to use a dict of lists
ratings_by_user_id = {}  # {user_id: [{movie_id, rating}]}
movies_by_genre = {} # {genre: [movie_id]}


#This works with both the reduced data set and the large data set
def parse_ratings(ratingFile):
    with open(ratingFile) as csv_file:
        csv_r = csv.reader(csv_file, delimiter=",")
        line_count = 0
        for row in csv_r:
            line_count += 1
            if line_count > 1:
                if not int(row[0]) in ratings_by_user_id:
                    ratings_by_user_id[int(row[0])] = []
                ratings_by_user_id[int(row[0])].append({
                    "movie_id": int(row[1]),
                    "rating": float(row[2]),
                    "timestamp": int(row[3])
                })
                if not int(row[1]) in ratings_by_movie_id:
                    ratings_by_movie_id[int(row[1])] = []                
                ratings_by_movie_id[int(row[1])].append({
                    "user_id": int(row[0]),
                    "rating": float(row[2]),
                    "timestamp": int(row[3])
                })
                if not int(row[1]) in ratings_by_movie_id_for_sklearn:
                    ratings_by_movie_id_for_sklearn[int(row[1])] = {}
                ratings_by_movie_id_for_sklearn[int(row[1])][int(row[0])] = float(row[2])
    #print(ratings_by_user_id)
    #print(ratings_by_movie_id)

#This works with both the reduced data set and the large data set
def parse_movies(moviesFile):
    with open(moviesFile) as csv_file:
        csv_r = csv.reader(csv_file, delimiter=",")
        line_count = 0
        for row in csv_r:
            line_count += 1
            if line_count > 1:
                if row[2]:
                    genres = row[2].split("|")
                    for genre in genres:
                        if genre.lower() not in movies_by_genre:
                            movies_by_genre[genre.lower()] = []
                        movies_by_genre[genre.lower()].append(int(row[0]))
                movies[int(row[0])] = {
                    "title": row[1],
                    "genres": genres
                }
    #print(movies)

def find_weight(user_id1, user_id2):
    ratings_for_user1 = ratings_by_user_id[user_id1]  # [{movie_id, rating}]
    ratings_for_user2 = ratings_by_user_id[user_id2]
    """ lets create the subset list first before calculating the weight """
    set_of_movies_rated_by_both_users = {}  # {movie_id: [user1_rating, user2_rating]}
    for movie_rating1 in ratings_for_user1:
        for movie_rating2 in ratings_for_user2:
            if movie_rating1["movie_id"] == movie_rating2["movie_id"]:
                set_of_movies_rated_by_both_users[movie_rating1["movie_id"]] = []
                set_of_movies_rated_by_both_users[movie_rating1["movie_id"]].append(movie_rating1)
                set_of_movies_rated_by_both_users[movie_rating1["movie_id"]].append(movie_rating2)
                break  # no need to keep looking if we have a match

    """ lets get the avg ratings of each user in the set """
    avg_rating_for_user1 = 0
    avg_rating_for_user2 = 0
    for movie_id in set_of_movies_rated_by_both_users:
        avg_rating_for_user1 += set_of_movies_rated_by_both_users[movie_id][0]['rating']
        avg_rating_for_user2 += set_of_movies_rated_by_both_users[movie_id][1]['rating']
    if len(set_of_movies_rated_by_both_users) <= 0:
        # these users have no movies in common
        return 0
    avg_rating_for_user1 = avg_rating_for_user1 / len(set_of_movies_rated_by_both_users)
    avg_rating_for_user2 = avg_rating_for_user2 / len(set_of_movies_rated_by_both_users)

    """ now lets calculate the weight """
    # numerator
    weight_numerator = 0
    weight_denominator = 0
    user1_weighted_denominator = 0
    user2_weighted_denominator = 0
    for movie_id in set_of_movies_rated_by_both_users:
        ratings = set_of_movies_rated_by_both_users[movie_id]
        weight_numerator += (ratings[0]["rating"] - avg_rating_for_user1) * (ratings[1]["rating"] - avg_rating_for_user2)
        user1_weighted_denominator += math.pow((ratings[0]["rating"] - avg_rating_for_user1), 2)
        user2_weighted_denominator += math.pow((ratings[1]["rating"] - avg_rating_for_user2), 2)
    weight_denominator = math.sqrt(user1_weighted_denominator*user2_weighted_denominator)
    if weight_denominator <= 0:
        return 0
    else:
        weight = weight_numerator / weight_denominator
        if weight < 0:
            weight = 0
        return weight


def make_prediction(prediction_user, movie_id):
    """ get average rating for the predicted user """
    avg_rating_for_prediction_user = 0
    movie_ratings = ratings_by_user_id[prediction_user]
    for movie_rating in movie_ratings:
        avg_rating_for_prediction_user += movie_rating["rating"]
    avg_rating_for_prediction_user = avg_rating_for_prediction_user / len(movie_ratings)

    """ get all weights """
    weights = {}
    for user_id in ratings_by_user_id:
        if user_id != prediction_user:
            weights[user_id] = find_weight(prediction_user, user_id)

    """ get the top weights """
    top_weights = []
    k = round(len(weights) / 4)  # we'll make "k" = 25% of the total number of users
    for i in range(k):
        max_user_id = max(weights, key=int)
        top_weights.append({
            "user_id": max_user_id,
            "weight": weights[max_user_id]
        })
        del weights[max_user_id]

    numerator = 0
    denominator = 0
    for top_weight in top_weights:
        for user_rating in ratings_by_movie_id[movie_id]:
            if user_rating["user_id"] == top_weight["user_id"]:
                numerator += user_rating["rating"] * top_weight["weight"]
                denominator += top_weight["weight"]
                break
    if denominator is not 0:
        prediction = avg_rating_for_prediction_user + (numerator / denominator)
    else:
        prediction = 0
    if prediction < 0:
        prediction = 0
    if prediction > 5:
        prediction = prediction / 2
    return math.floor(prediction)


def main(user_id, movie_id,movieFile,ratingFile):
    # parse_file("netflix/movie_titles.txt", True)
    # parse_file("netflix/ratings.txt", False)
    parse_ratings(ratingFile)
    parse_movies(movieFile)
    print(make_prediction(user_id, movie_id))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--user", type=int, required=True)
    parser.add_argument("--movie", type=int, required=True)
    parser.add_argument("--movieFile", type=str, required=True)
    parser.add_argument("--ratingFile", type=str, required=True)
    args = parser.parse_args()
    main(args.user, args.movie, args.movieFile, args.ratingFile)
