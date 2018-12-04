import time

#----------------------------------------------------------------
# Class for web interface
# ***********************
# This tracks the state of the web interface. All the movies
# selected, search queries, current movie selection, rating,
# etc... This is a view that should be pickled per userId?
#----------------------------------------------------------------
class webInterface():
    #------------------------------------------------------------------
    # Initialize our interface
    #------------------------------------------------------------------
    def __init__(self, initialData, userId=1, covers=None):
        self.data=initialData
        self.userId=userId
        if self.data.userExists(self.userId):
            self.userId=self.getUserId(self.userId)
        else:
            self.userId=self.addUser(self.userId)
        
        #####################################################################
        # Rendered First?
        #
        self.similarUserMovies=self.data.similarUser(self.userId)
        self.similarMovies=self.data.similarMovies(self.currentMovie)
        
        #--------------------------------------------------
        #   * SelectView         *                  
        #  F* ------------------ *  --------  -------
        #  l* |                | *  |Search|  |Side |
        #  o* |HorizontalBoxes0| *  |  1   |  |  C  |
        #  a* ------------------ *  |  2   |  |  u  |
        #  t* SelectView         *  |  3   |  |  r  |
        #  i* ------------------ *  |  4   |  |  r  |
        #  n* |                | *  |  5   |  |  e  |
        #  g* |HorizontalBoxes | *  |  6   |  |  n  |
        #  ?* ------------------ *  --------  |  t  |
        #   *        \?/         *            -------
        #   *         V          *            Rate   
        #--------------------------------------------------
        self.currentMovie=data.getMovie(self.userId)
        # Format: ['searchQuery',['result0','result1','result2',...,'resultN']]
        self.searchBox=[]
        # Format: ['result0','result1','result2',...,'resultN']
        self.horizontalBoxes=[]
        self.horizontalBoxes.append(self.similarUserMovies)
        self.horizontalBoxes.append(self.similarMovies)
        
        #####################################################################
        # Rendered upon event?
        # 
        self.similarGenreMovies=self.data.similarGenres(self.currentMovie)
        self.popularMovies=self.data.popularMovies()
        self.topRatedMovies=self.data.topRated()
        self.frequentlyRatedMovies=self.frequentlyRated()
        self.frequentlyRatedRecentMovies=self.frequentlyRatedRecently(time.time())
    
    #------------------------------------------------------------------
    # Select movie
    #------------------------------------------------------------------
    def setCurrentMovie(self, movie):
        self.currentMovie=movie
    
    #------------------------------------------------------------------
    # Select horizontal boxes' view
    # *****************************
    # This interfaces the horizontal boxes' states between the app and 
    # rating interface.
    #------------------------------------------------------------------
    def selectView(self, index, view):
        # Not enough boxes to view,
        #  add enough boxes to fill up to index.
        while index>=len(self.horizontalBoxes):
            self.horizontalBoxes.append([])
        
        # Change each view
        if view=='popular':
            self.horizontalBoxes[index]=self.popularMovies
        elif view=='top':
            self.horizontalBoxes[index]=self.topRated
        elif view=='frequent':
            self.horizontalBoxes[index]=self.frequentlyRatedMovies
        elif view=='recently popular':
            self.horizontalBoxes[index]=self.frequentlyRatedRecentMovies
        elif view=='similar genre':
            self.horizontalBoxes[index]=self.data.similarGenreMovies
        elif view=='random':
            self.horizontalBoxes[index]=self.data.randomMovie()
        else:
            subselect=view.split(' ')
            # Grab some genre, i.e. ['genre','action']
            if subselect[0]=='genre':
                self.horizontalBoxes[index]=self.data.popularGenre(subselect[1])
            #elif subselect[0]=='asdfasdf':
            #    self.horizontalBoxes[index]=self.data.asdfasdf(subselect[1])
    
    #------------------------------------------------------------------
    # Update selection, this should use the web interface timer
    #------------------------------------------------------------------
    def updateSelection(self):
        self.similarUserMovies=self.data.similarUser(self.userId)
        self.similarMovies=self.data.similarMovies(self.currentMovie)
        self.similarGenreMovies=self.data.similarGenres(self.currentMovie)
        self.popularMovies=self.data.popularMovies()
        self.topRatedMovies=self.data.topRated()
        self.frequentlyRatedMovies=self.frequentlyRated()
        self.frequentlyRatedRecentMovies=self.frequentlyRatedRecently(time.time())
    
    
    #------------------------------------------------------------------
    # Render a sloth
    #------------------------------------------------------------------
    def sloth(self):
        pass
    
    #------------------------------------------------------------------
    # Add a rating
    #------------------------------------------------------------------
    def addRating(self, movie, rating):
        self.data.addRating(movie,rating,self.userId)
    
    #------------------------------------------------------------------
    # Search movies.
    #------------------------------------------------------------------
    def search(self, movie)
        self.searchBox=self.data.search(movie)
   
    ###################################################################
    # Move these to an admin interface?
    #
    #------------------------------------------------------------------
    # Render statistics. Move this to admin state?
    #------------------------------------------------------------------
    def statistics(self):
        pass
    
    #------------------------------------------------------------------
    # Display graph.
    #------------------------------------------------------------------
    def displayGraph(stuff):
        pass
    
    #
    # End admin interface
    ##################################################################
