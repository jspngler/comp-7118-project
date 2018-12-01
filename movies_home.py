import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
from imdb import IMDb

ia = IMDb()

df_ratings = pd.read_csv('ml-20m/ml-20m/ratings.csv')
df_movies = pd.read_csv('ml-20m/ml-20m/movies.csv')

app = dash.Dash()

divs = []
app.layout = html.Div([
				html.Label('Select the Category:', style={'display':'inline-block'}), 
			 dcc.Dropdown(id='group_id',
			 	options = [{'value': '0', 'label':'Popular Movies'}, {'value': '1', 'label':'Top-Rated Movies'},
				{'value': '2', 'label':'Frequently Rated Movies'}, {'value': '3', 'label':'Frequent Popular Movies'}],
			 	value = '0',
			 	style={'width':'250px', 'display':'inline-block'},),
				html.Div(divs, id='divs_id', style={'border':'2px blue solid', 'height': '200px', 'width':'auto', 'overflow-y': 'scroll'}),
				# html.Div('', id='movie_details_id', style={'height': '300px', 'width':'700px'})
			# dcc.Graph(id='graph'),
			# dcc.Dropdown(id='year-picker', options = popular_movies,)
			# 	value=df['year'].min())
])


# @app.callback(Output('movie_details_id', 'children'),
# 	[Input('movie_id', 'children')],
# )
# def get_movie_details(movie_id_value):
# 	if(ia.get_movie(movie_id_value).data.keys().__contains__('cover url')):
# 		image = ia.get_movie(movieId).data['cover url']
# 	else:
# 		image = 'Photo-Not-Available.jpg'
# 	directors = ''
# 	for director in ia.get_movie(movie_id_value).data['directors']:
# 		directors= directors +  ', ' + director
# 	div_movie = html.Div([
# 		html.Label(directors)
# 	])
# 	return div_movie



@app.callback(Output('divs_id', 'children'),
	[Input('group_id', 'value')],
	# [State('div_id', 'value'),
	# State('movie_id', 'children'),]
)
def get_movies(group_id_value):
	movies = []
	divs = []
	image = ''
	if (group_id_value == '0'):
		popular_movies_ids = df_ratings['movieId'].value_counts().head(10)
		popular_movies = {}
		for movieId in popular_movies_ids.keys():
		    popular_movies.update({movieId: df_movies[df_movies['movieId'] == movieId]['title']})
		movies = popular_movies

	elif (group_id_value == '1'):
		top_rated_movies_ids = df_ratings[df_ratings['rating'] == 5]['movieId'].value_counts().head(10)
		top_rated_movies = {}
		for movieId in top_rated_movies_ids.keys():
		    top_rated_movies.update({movieId: df_movies[df_movies['movieId'] == movieId]['title']})
		movies = top_rated_movies

	# elif (group_id_value == '2'):
	# 	frequently_rated_movies_ids = df_ratings

	for movieId in movies:
		# if (ia.get_movie(movieId).data.keys().__contains__('cover url')):
		# 	image = ia.get_movie(movieId).data['cover url']
		# else:
			# image = 'Photo-Not-Available.jpg'
		divs.append(
			html.Div([
			# html.Div([html.Img(src=image, style={'height':'100%', 'width': '150px'})], style={'height':'70%'}),
				html.Div(movies[movieId], style={'textAlign':'left','width': '150px', 'height': '20%'})
			], style={'display':'inline-block', 'height':'100%'}))
	return divs


if __name__ == '__main__':
	app.run_server()