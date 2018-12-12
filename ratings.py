#import pandas
from sklearn.feature_extraction import DictVectorizer
from sklearn.cluster import KMeans,Birch,AgglomerativeClustering
from sklearn.datasets import make_blobs
from scipy import sparse
import numpy as np
import sys
import getopt
import csv
import matplotlib.pyplot as plt

#----------------------------------------------------------------
# Class for user movie ratings.
#----------------------------------------------------------------
class ratings():
    #------------------------------------------------------------------
    # Initialize our ratings. self.movies and self.ratings.
    #------------------------------------------------------------------
    def __init__(self, initialMoviesFile, initialRatingsFile):
        # These structures will probably be merged into a pandas 
        # dataFrame 
        # going to use a dict, with movie_id as the key, for movies because movie_id has a 1-to-1 relation with movie
        self.movies = {}  # {movie_id: {genre, title}}
        # a movie_id can have multiple ratings. going to use a dict of lists
        self.ratings_by_movie_id = {}  # {movie_id: [{user_id, rating}]}
        # a user_id can have multiple ratings. going to use a dict of lists
        self.ratings_by_user_id = {}  # {user_id: [{movie_id, rating}]}
        self.movies_by_genre = {} # {genre: [movie_id]}
        
        self.ratings_by_movie_id_for_sklearn = {}  # {movie_id: {user_id: rating}}
        self.ratings_by_user_id_for_sklearn = {}  # {movie_id: {user_id: rating}}
        self.ratings_by_timestamp_for_sklearn = {}  # {movie_id: {user_id: rating}}
        self.rating_weights_by_genre_for_sklearn = {}  # {movie_id: {user_id: rating}}
        self.rating_weights_by_user_id_for_sklearn={}
        self.genres= {}
        self.average_rating_by_movie_id={}
        self.rating_frequency_by_movie_id={}
        
        self.parse_movies(initialMoviesFile)
        self.parse_ratings(initialRatingsFile)
        #self.genre_ratings()
        self.average_ratings()
        self.rating_frequency()
        self.user_id=0
        self.login=False
    
    #------------------------------------------------------------------
    # login a user. 
    #------------------------------------------------------------------
    def loginUser(self,user_id):
        self.user_id=user_id
        if user_id in self.ratings_by_user_id:
            self.login=True
        return self.login
    
    ################# Accumulation methods ############################
    #------------------------------------------------------------------
    # Add a rating
    #------------------------------------------------------------------
    def addRating(self, user_id, movie_id, rating, timestamp):
        self.ratings_by_movie_id[movie_id].append({'user_id':user_id,'movie_id':movie_id,'rating':rating,'timestamp':timestamp})
        self.ratings_by_user_id[user_id].append({'user_id':user_id,'movie_id':movie_id,'rating':rating,'timestamp':timestamp})
        if not int(movie_id) in self.ratings_by_movie_id_for_sklearn:
            self.ratings_by_movie_id_for_sklearn[movie_id] = {}
        self.ratings_by_movie_id_for_sklearn[movie_id][user_id] = float(rating)
        if not user_id in self.ratings_by_user_id_for_sklearn:
            self.ratings_by_user_id_for_sklearn[user_id] = {}
        self.ratings_by_user_id_for_sklearn[user_id][movie_id] = float(rating)
        if not timestamp in self.ratings_by_timestamp_for_sklearn:
            self.ratings_by_timestamp_for_sklearn[timestamp] = {}
        self.ratings_by_timestamp_for_sklearn[timestamp][movie_id] = float(rating)
    
    #------------------------------------------------------------------
    # Add a user. 
    #------------------------------------------------------------------
    def addUser(self):
        self.user_id=0
        for rating in self.ratings_by_user_id:
            if rating['user_id']>self.user_id:
                self.user_id=rating['user_id']+1
        return self.user_id
    
    #------------------------------------------------------------------
    # Parse the ratings file.
    #------------------------------------------------------------------
    def parse_ratings(self,ratingsFile):
        with open(ratingsFile) as csv_file:
            csv_r = csv.reader(csv_file, delimiter=",")
            line_count = 0
            for row in csv_r:
                line_count += 1
                if line_count > 1:
                    if not int(row[0]) in self.ratings_by_user_id:
                        self.ratings_by_user_id[int(row[0])] = []
                    self.ratings_by_user_id[int(row[0])].append({
                        "movie_id": int(row[1]),
                        "rating": float(row[2]),
                        "timestamp": int(row[3])
                    })
                    if not int(row[1]) in self.ratings_by_movie_id:
                        self.ratings_by_movie_id[int(row[1])] = []
                    self.ratings_by_movie_id[int(row[1])].append({
                        "user_id": int(row[0]),
                        "rating": float(row[2]),
                        "timestamp": int(row[3])
                    })
                    if not int(row[1]) in self.ratings_by_movie_id_for_sklearn:
                        self.ratings_by_movie_id_for_sklearn[int(row[1])] = {}
                    self.ratings_by_movie_id_for_sklearn[int(row[1])][int(row[0])] = float(row[2])
                    if not int(row[0]) in self.ratings_by_user_id_for_sklearn:
                        self.ratings_by_user_id_for_sklearn[int(row[0])] = {}
                    self.ratings_by_user_id_for_sklearn[int(row[0])][int(row[1])] = float(row[2])
                    if not int(row[3]) in self.ratings_by_timestamp_for_sklearn:
                        self.ratings_by_timestamp_for_sklearn[int(row[3])] = {}
                    self.ratings_by_timestamp_for_sklearn[int(row[3])][int(row[1])] = float(row[2])
    
    #------------------------------------------------------------------
    # Parse the movies file.
    #------------------------------------------------------------------
    def parse_movies(self,moviesFile):
        with open(moviesFile) as csv_file:
            csv_r = csv.reader(csv_file, delimiter=",")
            line_count = 0
            for row in csv_r:
                line_count += 1
                if line_count > 1:
                    if row[2]:
                        genres = row[2].split("|")
                        for genre in genres:
                            if genre.lower() not in self.movies_by_genre:
                                self.movies_by_genre[genre.lower()] = []
                            self.movies_by_genre[genre.lower()].append(int(row[0]))
                    self.movies[int(row[0])] = {
                        "title": row[1],
                        "genres": genres
                    }
        for i in self.movies:
            for j in self.movies[i]['genres']:
                self.genres[j]=0
        genreI=0
        for i in self.genres:
            self.genres[i]=genreI
            genreI=genreI+1
    
    ############# End Accumulation methods ############################
    
    ############# Filter methods ######################################
    
    def truncate_movies(self, movies, max_length=10):
        for movie in self.ratings_by_user_id[self.user_id]:
            for i in range(0,len(movies)):
                if movie['movie_id']==movies[i][1]:
                    del movies[i]
                    break
        newList=[]
        for i in range(0,len(movies)-1):
            count=0
            if movies[i][0]!=movies[i+1][0]:
                count=0
            if count<max_length:
                count=count+1
                newList.append(movies[i])
        return newList
                   
            
    ############# End Filter Methods ##################################
    
    ############# Update Methods ######################################
    #------------------------------------------------------------------
    # Get the weights by user id. Cosine similarity.
    #------------------------------------------------------------------
    def cosine_similarity(self, user_id1, user_id2):
        ratings_for_user1 = self.ratings_by_user_id[user_id1]  # [{movie_id, rating}]
        ratings_for_user2 = self.ratings_by_user_id[user_id2]
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
    
    #------------------------------------------------------------------
    # Get the genre ratings by movie..
    #------------------------------------------------------------------
    #def genre_ratings_weights(self):
    #    for i in self.ratings_by_movie_id:
    #        for j in self.ratings_by_movie_id[i]:
    
    #------------------------------------------------------------------
    # Get the average ratings by movie..
    #------------------------------------------------------------------
    def average_ratings(self):
        self.average_rating_by_movie_id={}
        for i in self.ratings_by_movie_id:
            self.average_rating_by_movie_id[i]=0
            for j in self.ratings_by_movie_id[i]:
                self.average_rating_by_movie_id[i]=self.average_rating_by_movie_id[i]+j['rating']
            self.average_rating_by_movie_id[i]=self.average_rating_by_movie_id[i]/len(self.ratings_by_movie_id[i])
    
    #------------------------------------------------------------------
    # Get the rating frequency by movie, normalized by total number of 
    # movies
    #------------------------------------------------------------------
    def rating_frequency(self):
        self.rating_frequency_by_movie_id={}
        for i in self.ratings_by_movie_id:
            self.rating_frequency_by_movie_id[i]=len(self.ratings_by_movie_id[i])/len(self.ratings_by_user_id)
    
    #------------------------------------------------------------------
    # Get the rating frequency by movie, normalized by total number of 
    # movies
    #------------------------------------------------------------------
    def user_rating_weights(self):
        self.rating_weights_by_user_id_for_sklearn={}
        for i in self.ratings_by_user_id:
            self.rating_weights_by_user_id_for_sklearn[i]=self.cosine_similarity(self.user_id,i)
    
    #------------------------------------------------------------------
    # Write the user file. 
    #------------------------------------------------------------------
    def write_user_file(self,header,prefix,data_to_write):
        simMov=open(prefix+'_'+self.user_id+".txt","w")
        simMov.write(header)
        for i in topSorted:
            for j in topSorted[i]:
                simMov.write(str(i)+','+str(j[0])+','+str(j[1]))
        simMov.close()
    
    ############# End Update Methods ##################################
    
    ############# Clustering methods ##################################
    #------------------------------------------------------------------
    # Find similar movies for a user, based on a given movie. 
    # from sklearn.cluster import KMeans,Birch,AgglomerativeClustering
    #------------------------------------------------------------------
    def get_clustering(self, input_data,  nClusters, iterations, method): 
        v=DictVectorizer(sparse=True)
        R=[self.ratings_by_movie_id_for_sklearn[d] for d in self.ratings_by_movie_id_for_sklearn]
        X=v.fit_transform(R)
        if method==KMeans:
            clusterizer=method(n_clusters=nClusters,max_iter=iterations,n_jobs=8)
        if method==Birch:
            clusterizer=method(n_clusters=nClusters)
        if method==AgglomerativeClustering:
            # affinity=
            #    Metric used to compute the linkage. Can be “euclidean”, 
            #“l1”, “l2”, “manhattan”, “cosine”, or ‘precomputed’. If linkage 
            #is “ward”, only “euclidean” is accepted.
            # linkage=
            #    Which linkage criterion to use. The linkage criterion 
            #determines which distance to use between sets of observation. 
            #The algorithm will merge the pairs of cluster that minimize 
            #this criterion.
            #'ward' minimizes the variance of the clusters being merged.
            #'average' uses the average of the distances of each observation of the two sets.
            #'complete' or maximum linkage uses the maximum distances between all observations of the two sets.
            #'single' uses the minimum of the distances between all observations of the two sets.
            clusterizer=method(n_clusters=nClusters,affinity='euclidean',linkage='ward')
        return clusterizer.fit_predict(X)
    
    #------------------------------------------------------------------
    # Find similar movies. 
    #------------------------------------------------------------------
    def similarMovies(self, nClusters, nMovies, iterations, method):
        clustering=self.get_clustering(self.ratings_by_movie_id_for_sklearn,nClusters,iterations,method)
        # dictionary by cluster {[movie_id,cluster,average_rating]}
        topSorted={}
        for i in range(0,nClusters):
            topSorted[i]=[]
        for i,j in zip(self.ratings_by_movie_id,range(0,len(self.ratings_by_movie_id))):
            topSorted[clustering[j]].append((i,self.average_rating_by_movie_id[i]))
        for i in topSorted:
            topSorted[i]=sorted(topSorted[i], key=lambda data: data[1],reverse=True)
        newSorted=[]
        for i in range(0,nClusters):
            for j in topSorted[i]:
                newSorted.append((i,j[0],j[1]))
        header='cluster,movieId,rating'
        prefix='similarMovies'
        return self.truncate_movies(newSorted,nMovies),prefix,header
    
    #------------------------------------------------------------------
    # Find similar movies by genres. Doesn't work
    #------------------------------------------------------------------
    def similarGenres(self,nClusters, nMovies, iterations, method):
        clustering=self.get_clustering(self.ratings_by_movie_id_for_sklearn,nClusters,iterations,method)
        # dictionary by cluster {[movie_id,cluster,average_rating]}
        topSorted={}
        for i in range(0,nClusters):
            topSorted[i]=[]
        for i,j in zip(self.ratings_by_movie_id,range(0,len(self.ratings_by_movie_id))):
            topSorted[clustering[j]].append((i,self.average_rating_by_movie_id[i]))
        for i in topSorted:
            topSorted[i]=sorted(topSorted[i], key=lambda data: data[1],reverse=True)
        newSorted=[]
        for i in range(0,nClusters):
            for j in topSorted[i]:
                newSorted.append((i,j[0],j[1]))
        header='cluster,movieId,rating'
        prefix='similarMovies'
        return self.truncate_movies(newSorted,nMovies),prefix,header
    
    #------------------------------------------------------------------
    # Find similar users.
    # Form=avgRating+rating*sum(cosineSimilarity(user_id,j))
    #------------------------------------------------------------------
    def similarUsers(self, nClusters, nMovies, iterations, method): 
        clustering=self.get_clustering(self.ratings_by_user_id_for_sklearn,nClusters,iterations,method)
        topSorted={}
        for i in range(0,nClusters):
            topSorted[i]=[]
        for i,j in zip(self.ratings_by_user_id,range(0,len(self.ratings_by_user_id))):
            topSorted[clustering[j]].append((i,self.rating_weights_by_user_for_sklearn[i]))
        for i in topSorted:
            topSorted[i]=sorted(topSorted[i], key=lambda data: data[1],reverse=True)
        newSorted=[]
        for i in range(0,nClusters):
            for j in topSorted[i]:
                newSorted.append((i,j[0],j[1]))
        header='cluster,userId,rating'
        prefix='similarUsers'
        return self.truncate_movies(newSorted),prefix,header
    
    #------------------------------------------------------------------
    # Most popular movies weighted by both rating and frequency.
    # Form=avgRating+nRating*5.0/totalNRatings
    #------------------------------------------------------------------
    def popularMovies(self,nClusters,nMovies,iterations,method):
        newSorted=[]
        for i in self.ratings_by_movie_id:
            newSorted.append((0,i,self.average_rating_by_movie_id[i]+self.rating_frequency_by_movie_id[i]*5.0))
        newSorted=sorted(newSorted, key=lambda data: data[1],reverse=True)
        header='cluster,movieId,rating'
        prefix='popularMovies'
        return self.truncate_movies(topSorted,nMovies),prefix,header
    
    #------------------------------------------------------------------
    # Top Rated movies with highest rating. 
    #------------------------------------------------------------------
    def topRated(self):
        newSorted=[]
        for i in self.ratings_by_movie_id:
            newSorted.append((0,i,self.average_rating_by_movie_id[i]))
        newSorted=sorted(newSorted, key=lambda data: data[1],reverse=True)
        header='cluster,movieId,rating'
        prefix='popularMovies'
        return topSorted,prefix,header
    
    #------------------------------------------------------------------
    # Most number of times rated. 
    #------------------------------------------------------------------
    def frequentlyRated(self):
        pass
    
    ############# End Find/recommend methods ##########################
    
    ############## For testing and fine tuning ########################
    #------------------------------------------------------------------
    # Display graph.
    #------------------------------------------------------------------
    def displayGraph(self):
        pass
    
    ############## End of seperate class? #############################
    
    ############## Stand alone section ################################
    #------------------------------------------------------------------
    # Usage for running stand-alone testing
    #------------------------------------------------------------------
    def usage():
        print("Usage for ratings:")
        print("-h or --help")
        print("      Print this messege and quit")
        print("-m [filename] or --movies=[filename]")
        print("      Read movies from [filename]. Required!")
        print("-r [filename] or --ratings=[filename]")
        print("      Read ratings from [filename]. Required!")

def main():
    try:
        opts,args=getopt.getopt(sys.argv[1:],"hm:r:",
        ["help","movies=","ratings="])
    except getopt.GetoptError as err:
        print(err)
        ratings.usage()
        sys.exit(2)
    filename=''
    movieFilename=''
    ratingFilename=''
    for o,a in opts:
        if o in ("-h", "--help"):
            ratings.usage()
            sys.exit()
        elif o in ("-m", "--movies"):
            movieFilename=a
        elif o in ("-r", "--ratings"):
            ratingFilename=a
        else:
            assert False, "unhandled option"
    if len(movieFilename)==0 or len(ratingFilename)==0:
        ratings.usage()
        sys.exit()
    #initialMovies=pandas.read_csv(movieFilename)
    #initialRatings=pandas.read_csv(ratingFilename)
    rData=ratings(movieFilename,ratingFilename)
    user_id=input("Please type your login: ")
    rData.loginUser(int(user_id))
    #print(rData.truncate_movies(rData.movies))
    #clusterData=[(cluster,movie_d,ratings),...]
    if algorithm==0:
       clusterData,prefix,header=rData.similarMovies(40, 10, 5000, KMeans)
    elif algorithm==1:
       clusterData,prefix,header=rData.similarMovies(40, 10, 5000, BirchClustering)
    elif algorithm==2:
       clusterData,prefix,header=rData.similarMovies(40, 10, 5000, AgglomerativeClustering))




if __name__ == "__main__":
    main()
    ############## End of Stand alone section ##########################
