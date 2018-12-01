import pandas
import sys
import getopt

#----------------------------------------------------------------
# Class for user movie ratings. Yay!
#----------------------------------------------------------------
class ratings():
    #------------------------------------------------------------------
    # Initialize our ratings. self.movies and self.ratings.
    # asdfasdfasdf 
    #------------------------------------------------------------------
    def __init__(self, initialMovies, initialRatings):
        # These structures will probably be merged into a pandas 
        # dataFrame 
        ######################### This part doesn't work yet #################
        print(initialMovies.columns)
        try:
            if all(['movieId', 'title', 'genres']) in initialMovies.columns:
                self.movies=initialMovies
                print("No movies in initialMovies.")
                raise
            else:
                print("Wrong pandas dataframe header in initialMovies:")
                raise KeyError
        except:
            print("initialMovies is the wrong type.")
            raise
        try:
            if len(initialRatings.loc['userId'])>0 and len(initialRatings.loc['movieId'])>0 and len(initialRatings.loc['rating'])>0 and len(initialRatings.loc['timestamp'])>0:
                self.ratings=initialRatings
            else:
                print("No ratings in initialRatings")
                raise
        except KeyError:
            print("Wrong pandas dataframe header in initialRatings:")
            print(initialRatings)
            raise KeyError
        except:
            print("initialRatings is the wrong type.")
            raise
    
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
    
    ############## Maybe in a seperate ui class #######################
    #------------------------------------------------------------------
    # Display graph.
    #------------------------------------------------------------------
    def displayGraph(stuff):
        pass
    
    #------------------------------------------------------------------
    # Display horizontal scrolling movies.
    #------------------------------------------------------------------
    def displayHorizontalMovies(movies):
        pass
    
    #------------------------------------------------------------------
    # Display verticle scrolling movies.
    #------------------------------------------------------------------
    def displayVerticalMovies(movies):
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
