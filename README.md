# comp-7118-project
Project for COMP 7118

## Description
Movie rating system with users. Has a web, movie, and user component that allows one to rate and add movies. An administrator component allows movies to be added and complete statistics displayed. A user can rank movies, recieve recomendations, and pick genres and titles. Initialization uses datasets in the same format as movieLens: a movies.csv file and a ratings.csv file. 

### 1. Input/Backend
From the groupLens site, the movieLens data set is at http://files.grouplens.org/datasets/movielens/ml-20m.zip
The headers are as follows:
#### Movie List
Contains 3 columns:
- Movie IDs: Identifies the movie.
- Movie Titles: Title of that movie.
- Movie Genres:Genres associated with that movie, in pipe, "|", seperated list.
#### User Ratings
Contains 3 columns:
- User IDs: Identifies the user.
- Movie ID: Identifies the movie that is rated by identified user.
- User Ratings: Rating given by the identified user.

### 2. Output/Stats
The ratings are aggregated via sklearn to predict 'likeness' among movies rated and movies watch by users.This lets us perform statistics on the following:
#### User recommendations
Based on similar choices among users.
#### Popular
What is the most popular overall, in a genre, or most watched.
#### Similar Movies
Movies with similar genres.

### 3. Web interface/Frontend
Utilizes Flask from python. Has two modes:
#### User
Can only rate, select, and recieve recomendations.
#### Administrator
Can read complete statistics.

## Building
Run 'pipenv install' installs the packages required for python. And running 'pipenv shell' will start the shell.

## Running
After running 'pipenv shell', the interface can be set up with...

> python sampleCSV.py --input=filename.csv --number=nSamples --seed=seedNumber

where:
- --input specifies the csv file to sample.
- --number specifies the number of samples to make.
- --seed specifies a seed for the sampling shuffle.
Output: filename_NnSamples_SseedNumber.csv

