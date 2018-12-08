import pandas
from sklearn.feature_extraction import DictVectorizer
from sklearn.cluster import KMeans,Birch,AgglomerativeClustering
from scipy import sparse
import numpy as np
import sys
import getopt
import csv

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
        self.parse_movies(initialMoviesFile)
        self.parse_ratings(initialRatingsFile)
        self.user_id=0
        self.login=False
    
    #------------------------------------------------------------------
    # login a user. 
    #------------------------------------------------------------------
    def loginUser(self,user_id):
        self.user_id=user_id
        for rating in self.ratings_by_user_id:
            if rating['user_id']==user_id:
                self.login=True
        return self.login
    
    ################# Accumulation methods ############################
    #------------------------------------------------------------------
    # Add a rating
    #------------------------------------------------------------------
    def addRating(self, user_id, movie_id, rating, timestamp):
        self.ratings_by_movie_id[movie_id].append({'user_id':user_id,'movie_id':movie_id,'rating':rating,'timestamp':timestamp})
        self.ratings_by_user_id[user_id].append({'user_id':user_id,'movie_id':movie_id,'rating':rating,'timestamp':timestamp})
    
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
    
    ############# End Accumulation methods ############################
    
    ############# Clustering methods ##################################
    #------------------------------------------------------------------
    # Find similar movies for a user, based on a given movie. 
    #------------------------------------------------------------------
    #from sklearn.cluster import KMeans,Birch,AgglomerativeClustering
    def similarMovie(self, movie_id, nMovies, T, N, I, method): 
        v=DictVectorizer(sparse=True)
        print(type(self.ratings_by_movie_id))
        #print(self.ratings_by_movie_id)
        r={}
        #ratings={movieid:[userid:{rating}]}
        for i in self.ratings_by_movie_id:
            r[i]={}
            for j in self.ratings_by_movie_id[i]:
                r[i][j['user_id']]=j['rating']
        print(r)
        X=v.fit_transform(self.ratings_by_movie_id)
        #print(self.ratings_by_user_id)
        #print(self.ratings_by_movie_id)
        #X=sparse.dok_matrix((len(self.ratings_by_user_id),len(self.ratings_by_movie_id)),dtype=np.int_)
        #for i in self.ratings_by_user_id:
        #    for j in i:
        #        X[
        print(X)
        if method==KMeans:
            clusterizer=method(n_clusters=N,tol=1,max_iter=20)
        if method==Birch:
            clusterizer=method(threshold=1,branching_factor=5,n_clusters=N)
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
            clusterizer=method(n_clusters=N,affinity='euclidean',linkage='ward')
        clustering=clusterizer.fit(X)
        sMovies=0
        i=0
        #for label in clustering._labels_:
        #    if i==
    
    #------------------------------------------------------------------
    # Find similar movies by genres.
    #------------------------------------------------------------------
    def similarGenres(self,user,genres):
        pass
    
    #------------------------------------------------------------------
    # Find a similar movies for a user, based on other users. 
    #------------------------------------------------------------------
    def similarUser(self, user):
        pass
        #sklearn.
  
    #------------------------------------------------------------------
    # Most popular movies by both rating and frequency. 
    #------------------------------------------------------------------
    def popularMovies(self):
        pass
    
    #------------------------------------------------------------------
    # Top Rated movies with highest rating. 
    #------------------------------------------------------------------
    def topRated(self):
        pass
    
    #------------------------------------------------------------------
    # Most frequently number of times rated regardless of ratings. 
    #------------------------------------------------------------------
    def frequentlyRatedRecently(self, timestamp):
        pass
    
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
    rData.similarMovie(1, 10, 10, 10, 20, KMeans) 
    #def similarMovie(self, movie_id, nMovies, T, N, I, method): 
    #rData.addRating(9783, 245, 3, time.clock())
    #rData.addMovie(9999999,'Sharknado 10','comedy|romance|parody|crap')

if __name__ == "__main__":
    main()
    ############## End of Stand alone section ##########################
