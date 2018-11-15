# comp-7118-project
Project for COMP 7118

## Description
Movie rating system with users. Has a web, movie, and user component that allows one to rate and add movies. An administrator component allows movies to be added and complete statistics displayed. A user can rank movies, recieve recomendations, and pick genres and titles. Initialization uses datasets in the same format as movieLens: a movies.csv file and a ratings.csv file. The headers are as follows:

### Movie List
Contains 3 columns:
- Movie IDs: Identifies the movie.
- Movie Titles: Title of that movie.
- Movie Genres:Genres associated with that movie, in pipe, "|", seperated list.


### User Ratings
Contains 3 columns:
- User IDs: Identifies the user.
- Movie ID: Identifies the movie that is rated by identified user.
- User Ratings: Rating given by the identified user.

### Output
This lets us create:
#### User recommendations
#### Popular
#### Similar Movies


### Web interface
Utilizes Flask from python. Has two modes:

#### User
Can only rate, select, and recieve recomendations.

#### Administrator
Can read complete statistics.

## Building
Run 'pipenv install' installs the packages required for python. And running 'pipenv shell' will start the shell.

## Running
After running 'pipenv shell', the interface can be set up with...



