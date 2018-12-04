import pandas
import sys
import getopt

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
        self.parse_ratings(initialMoviesFile)
    
    ################# Accumulation methods ############################
    #------------------------------------------------------------------
    # Add a rating
    #------------------------------------------------------------------
    def addRating(self, userId, movieId, rating, timestamp):
        try:
            self.ratings.append({'userId':userId,'movieId':movieId,'rating':rating,'timestamp':timestamp})
        except:
            print("Bad rating:")
            print(userId,' ',movieId,' ',rating,' ',timestamp)
            raise
    
    #------------------------------------------------------------------
    # Add a movie
    #------------------------------------------------------------------
    def addMovie(self, movieId,title,genres):
        try:
            self.movies.append({'movieId':movieId,'title':title,'genres':genres})
        except:
            print("Bad movie:")
            print(movieId,' ',title,' ',genres)
            raise
    
    #------------------------------------------------------------------
    # Add a user. Probably don't need this...
    #------------------------------------------------------------------
    def addUser(self, user):
        pass
    
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
                    if not int(row[0]) in ratings_by_user_id:
                        ratings_by_user_id[int(row[0])] = []
                    self.ratings_by_user_id[int(row[0])].append({
                        "movie_id": int(row[1]),
                        "rating": float(row[2]),
                        "timestamp": int(row[3])
                    })
                    if not int(row[1]) in ratings_by_movie_id:
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
                            if genre.lower() not in movies_by_genre:
                                self.movies_by_genre[genre.lower()] = []
                            self.movies_by_genre[genre.lower()].append(int(row[0]))
                    self.movies[int(row[0])] = {
                        "title": row[1],
                        "genres": genres
                    }
    
    ############# End Accumulation methods ############################
    
    ############# Find/recommend methods ##############################
    #------------------------------------------------------------------
    # Find similar movies for a user, based on a given movie. HARD
    #------------------------------------------------------------------
    def similarMovie(self, user, movieId): 
        pass
    
    #------------------------------------------------------------------
    # Find similar movies by genres.
    #------------------------------------------------------------------
    def similarGenres(self,user,genres):
        pass
    
    #------------------------------------------------------------------
    # Find a similar movies for a user, based on other users. HARD
    #------------------------------------------------------------------
    def similarUser(self, user):
        pass
  
    #------------------------------------------------------------------
    # Most popular movies by both rating and frequency. EASY
    #------------------------------------------------------------------
    def popularMovies(self):
        pass
    
    #------------------------------------------------------------------
    # Top Rated movies with highest rating. EASY
    #------------------------------------------------------------------
    def topRated(self):
        pass
    
    #------------------------------------------------------------------
    # Most frequently number of times rated regardless of ratings. EASY
    #------------------------------------------------------------------
    def frequentlyRatedRecently(self, timestamp):
        pass
    
    #------------------------------------------------------------------
    # Most number of times rated. EASY
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
    initialMovies=pandas.read_csv(movieFilename)
    initialRatings=pandas.read_csv(ratingFilename)
    rData=ratings(initialMovies,initialRatings)
    rData.addRating(9783, 245, 3, time.clock())
    rData.addMovie(9999999,'Sharknado 10','comedy|romance|parody|crap')

if __name__ == "__main__":
    main()
    ############## End of Stand alone section ##########################
