import pandas as pd
import dash
#import dash_core_components as dcc
from dash import dcc
#import dash_html_components as html
from dash import html
#import dash_table as dt
from dash import dash_table as dt
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
from dash.exceptions import PreventUpdate
import requests
import re
from bs4 import BeautifulSoup
import spacy
from spacy import displacy
import json
import dash_bootstrap_components as dbc
import dash_loading_spinners as dls


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED]) # theme needed for thr spinner graphic
server = app.server # Expose Flask instance for gunicorn command 
#proxies = {'https': 'http://x.x.x.x:x'}
#session = requests.Session()
#session.proxies.update(proxies)


#markdown_text = '''### Dash and Markdown'''

def blank_fig(): #https://stackoverflow.com/questions/66637861/how-to-not-show-default-dcc-graph-template-in-dash
	fig = go.Figure(go.Bar(x=[], y = []))
	fig.update_layout(template = None)
	fig.update_xaxes(showgrid = False, showticklabels = False, zeroline=False)
	fig.update_yaxes(showgrid = False, showticklabels = False, zeroline=False)
	return fig
	
app.layout = html.Div(children=[
    html.H1('Logical Connectives in the UK Statute Book', style={'margin-left':'50px', 'position': 'absolute', 'top': '35px'}),
	html.Div(
        id='app-page-content',
        className='app-body',
        children=[
			html.Div([ 
				dbc.Row(dbc.Col(
					dbc.Spinner(spinner_style={"width": "3rem", "height": "3rem", 'margin-right':'-400px','top': '300px', 'position': 'absolute'}, children=[html.Div(id='text-out', style={'border':'1px black solid', 'width': '800px', 'height': '600px', 'overflowY': 'auto', 'margin-left':'550px', 'margin-right':'-500px', 'position': 'absolute',  'top': '50px'}), #https://dash-bootstrap-components.opensource.faculty.ai/docs/components/spinner/

			html.Div([
				dcc.Graph(id='graph', figure = blank_fig(), style={'border':'1px black solid', 'width': '400px', 'height': '600px', 'position': 'relative',  'margin-left':'1450px', 'margin-right':'-500px', 'position': 'absolute',  'top': '50px'})
				]), 
			], color="#435278"), 
					width={'size': 12, 'offset': 0}),
				),
			]),
		
			html.Div([ 
				dbc.Row(dbc.Col(
					dbc.Spinner(spinner_style={"width": "3rem", "height": "3rem", 'margin-right':'-400px','top': '1000px', 'position': 'absolute'}, children=[dcc.Graph(id='plot2', style={'border':'1px black solid', 'width': '1300px', 'height': '400px', 'overflowY': 'auto', 'margin-left':'550px', 'margin-right':'-500px', 'position': 'absolute',  'top': '700px'}, figure = blank_fig()), 

			html.Div([
				dcc.Graph(id='plot3', figure = blank_fig(), style={'border':'1px black solid', 'width': '1300px', 'height': '250px', 'overflowY': 'auto', 'margin-left':'550px', 'margin-right':'-500px', 'position': 'absolute',  'top': '1150px'})
				]), 
			], color="#435278"), 
					width={'size': 12, 'offset': 0}),
				),
			]),
			
			html.Div(
				id="table1", style={'border':'1px black solid', 'width': '1300px', 'height': '300px', 'margin-left':'550px', 'margin-right':'-500px', 'position': 'absolute', 'top': '1450px'}
				),
				html.Div(
					id='app-page-content-control-tabs',
					className='control-tabs',
					children=[
						dcc.Tabs(id='control-tabs', value='what-is', children=[
							dcc.Tab(
								label='About',
								value='what-is',
								children=html.Div(className='control-tab', children=[
									html.H4(className='Visualising', children='Visualising logic in statutes'),
									html.P('This web app provides a statute tally of logical connectives and predicts a measure of logical complexity based on a trained named-entity recogniser (NER). Visualising logical connectives and complexity in statutes may help identify patterns of uncertainty to eliminate from future legislation and derive optimum interpretation.'),
								
									html.Div(style={'position': 'relative', 'top': '150px'},
										title='Select a statute',
										className='app-controls-block',
										children=[
											html.H4(className='what-is', children='What are logical connectives?'),
											html.P('A logical connective is a constant used to connect two or more formulas to create complex sentences with context-free language 𝐿1. For instance, the binary connective "∧" joining two atomic formulas P and Q  renders the formula (P ∧ Q) which can represent the statement e.g "[Lords Spiritual] and [Temporal]". The definable approximations for English connectives can be summarised like this:'),
											html.P(dcc.Markdown(children='''| 𝐿1 symbol				  	  | Word                | Connective                  |          
																			|-----------------------------|---------------------|-----------------------------|
																			| *P* ∧ *Q*              	  | and                 | Conjunction                 |
																			| *P* ∨ *Q*                	  | or                  | Disjunction                 |
																			| ¬ *P*                       | not                 | Negation                    |
																			| *P* ← *Q*                   | if                  | Converse implication        |
																			| *P* ↓ *Q*                   | nor                 | Joint denial	              |''')),
										],
									),

									html.Div(style={'position': 'relative', 'top': '250px'},
										title='Select a statute',
										className='app-controls-block',
										children=[
											html.H4(className='Research', children='Research'),
											html.I('"Propositions are like the sticks in a Tinker Toy set; without the round spools or connector blocks, you can do very little with the sticks. Operators are like the connector blocks; by adding them to propositions we get more complex structures..."'), 
											html.P("- Rudy Engholm, 'Logic and Laws: Relief from Statutory Obfuscation'"),
											html.Br(),
											html.P(['A report on the development of the NER model used for this web app is ', html.A('here', href='https://lcituksb.s3.us-east-2.amazonaws.com/index.htm', target='_blank')]),#https://community.plotly.com/t/how-to-make-a-linebreak-in-html-p/28317	
										],
									),
								])
							),
							dcc.Tab(
								label='Use',
									children=html.Div(className='control-tab', children=[

									html.H4(className='Visualising', children='Overview'),
									html.P('Select a statute to view logical connectives and their count nunber.'),
									html.P('Discover how complex statutes are in comparison with others and obtain data.'),

										html.Div(style={'position': 'relative', 'top': '150px'},
											title='Select a statute',
											className='app-controls-block',
											children=[
												html.H4(className='Visualising', 	
														children='View logical connectives'),
												html.Div(className='fullwidth-app-controls-name',
														 children='Select a statute'),
												dcc.Dropdown(id='data-dropdown', options=[
													{'label': 'Official Secrets Act 1911', 'value': 'Official Secrets Act 1911'},
													{'label': 'Easter Act 1928', 'value': 'Easter Act 1928'},
													{'label': 'Ireland Act 1949', 'value': 'Ireland Act 1949'},
													{'label': 'Hotel Proprietors Act 1956', 'value': 'Hotel Proprietors Act 1956'},
													{'label': 'Hovercraft Act 1968', 'value': 'Hovercraft Act 1968'},
													{'label': 'Oil and Pipelines Act 1985', 'value': 'Oil and Pipelines Act 1985'},
													{'label': 'Computer Misuse Act 1990', 'value': 'Computer Misuse Act 1990'},
													{'label': 'Intelligence Services Act 1994', 'value': 'Intelligence Services Act 1994'},
													{'label': 'Identity Documents Act 2010', 'value': 'Identity Documents Act 2010'},
													{'label': 'National Citizen Service Act 2017', 'value': 'National Citizen Service Act 2017'} 
												], placeholder="Select a statute"),
												html.Button(
												id='submit-button',
												n_clicks=0,
												children='View',
												style={'position': 'relative', 'top': '50px'}
												),

										html.Div(
											style={'position': 'relative', 'top': '250px'},
											title='Select a statute',
											className='app-controls-block',
											children=[
												html.H4(className='Visualising', 	
														children='Compare logical complexity'),
												html.Div(className='fullwidth-app-controls-name',
														 children='Select many statutes'
												),
												dcc.Dropdown(id='multiVariableDropdown',  options=[
													{'label': 'Official Secrets Act 1911', 'value': 'Official Secrets Act 1911'},
													{'label': 'Easter Act 1928', 'value': 'Easter Act 1928'},
													{'label': 'Ireland Act 1949', 'value': 'Ireland Act 1949'},
													{'label': 'Hotel Proprietors Act 1956', 'value': 'Hotel Proprietors Act 1956'},
													{'label': 'Hovercraft Act 1968', 'value': 'Hovercraft Act 1968'},
													{'label': 'Oil and Pipelines Act 1985', 'value': 'Oil and Pipelines Act 1985'},
													{'label': 'Computer Misuse Act 1990', 'value': 'Computer Misuse Act 1990'},
													{'label': 'Intelligence Services Act 1994', 'value': 'Intelligence Services Act 1994'},
													{'label': 'Identity Documents Act 2010', 'value': 'Identity Documents Act 2010'},
													{'label': 'National Citizen Service Act 2017', 'value': 'National Citizen Service Act 2017'}
												], placeholder="Select up to ten statutes",
												value=[],
												style={'position': 'relative', 'margin-top':'0px'},
												multi=True),

											html.Button(
											id='submit-button2',
											n_clicks=0,
											children='Compare',
											style={'position': 'relative', 'top': '50px'}
											),
											html.Div([
												html.Button(id='submit-button3',                
														children='View data',
														style={'position': 'relative', 'top': '100px'}
													),
												]), 
											]
										)
									])
								]
							)
						)
					])
				]
			)	
		]
	)
])

DEFAULT_LABEL_COLORS = {'(¬ P)':'lightgreen', '(P ∨ Q)':'orange', '(P ∧ Q)':'lightblue', '(P → Q)':'grey', '(P ↓ Q)':'salmon', '(P ← Q)':'purple'}

def entname(name):
    return html.Span(name, style={
        "font-size": "0.8em",
        "font-weight": "bold",
        "line-height": "2",
        "border-radius": "0.35em",
        "text-transform": "uppercase",
        "vertical-align": "middle",
        "margin-left": "0.5rem",
    })


def entbox(children, color):
    return html.Mark(children, style={
        "background": color,
        "padding": "0.45em 0.6em",
        "margin": "0 0.25em",
        "line-height": "2",
        "border-radius": "0.35em",
    })


def entity(children, name):
    if type(children) is str:
        children = [children]

    children.append(entname(name))
    color = DEFAULT_LABEL_COLORS[name]
    return entbox(children, color)


def render(doc):
    children = []
    last_idx = 0
    for ent in doc.ents:
        children.append(doc.text[last_idx:ent.start_char])
        children.append(
            entity(doc.text[ent.start_char:ent.end_char], ent.label_))
        last_idx = ent.end_char
    children.append(doc.text[last_idx:])
    return children

#def statute(value):
	#if value == 'Parliament (Qualification of Women) Act 1918':
		#url = "https://www.legislation.gov.uk/ukpga/Geo5/8-9/47/enacted/data.html"
	#elif value== 'Easter Act 1928':
		#url = "https://www.legislation.gov.uk/ukpga/Geo5/18-19/35/enacted/data.html"
	#elif value is None:
		#raise PreventUpdate
	#return url

def kvadder(statutes, values, di): #create dictionary from list

    di[statutes]=values

    return di
	

def dfobject(d):

	dict = d
    
	df = pd.DataFrame(dict) # create df from dictionary

	return df  


def plot2(selectedVariable2, stats):	

	#if stats is None:
		#raise PreventUpdate

	a=[]
	stringlist = selectedVariable2
	for i in stringlist:
		a.append(i) # adds each string in the selectedVariable2 e.g. ['The Parliament (Qualification of Women) Act 1918', 'Computer Misuse Act 1990'] to an 'a' list - is this needed?
	#statutes = ''.join(a)
	 
	b=[]
	valuelist = stats #needed?
	lists = [list(x) for x in valuelist] # as df needs a list this turns stats into a list e.g. [[0.007936507936507936, 0.023809523809523808, 0.03968253968253968], [0.0019880715705765406, 0.007952286282306162, 0.05168986083499006]]
	#https://blog.finxter.com/how-to-convert-list-of-tuples-to-list-of-lists-in-python/
	for i in lists: # is 'b' needed?
		b.append(i)
	print ('B' + str (b))
	
	di = {'Logical connectives': ['(¬ P)', '(P ∨ Q)', '(P ∧ Q)', '(P → Q)', '(P ↓ Q)', '(P ← Q)']}	# dictionary of logical connectives
	
	res1=() # added to prevent UnboundLocalError: local variable 'res1' referenced before assignment
	for f, b in zip(a, b):  # https://stackoverflow.com/questions/1663807/how-to-iterate-through-two-lists-in-parallel also see list comprehension https://www.w3schools.com/python/python_lists_comprehension.asp https://www.geeksforgeeks.org/different-ways-to-create-pandas-dataframe/  Method 5 https://towardsdatascience.com/15-ways-to-create-a-pandas-dataframe-754ecc082c17
	
		res1 = kvadder(f, b, di) # needed to create a unique dataframe object so the graph can chart at least 1 single statute and stats data
	
	df = dfobject(res1) #adds the dictionary to the df with data from a and b
				   
	traces = []
	for i in selectedVariable2:
			colors = {'Official Secrets Act 1911':'lightblue', 'Easter Act 1928':'tomato', 'Ireland Act 1949':'lightgreen', 'Hotel Proprietors Act 1956':'purple', 'Hovercraft Act 1968':'orange', 'Oil and Pipelines Act 1985':'teal', 'Computer Misuse Act 1990':'coral', 'Intelligence Services Act 1994':'green', 'Identity Documents Act 2010': 'orchid', 'National Citizen Service Act 2017':'tan'} # https://stackoverflow.com/questions/61746001/plotly-how-to-specify-colors-for-a-group-using-go-bar # https://stackoverflow.com/questions/50579783/plotly-dash-how-to-set-automated-colors-rather-than-having-blue-for-everything
			traces.append(go.Bar(x=df['Logical connectives'],
									y=df[i],
									marker_color=colors[i],
									name=i))
	fig2 = go.Figure(data=traces)
	
	fig2.update_layout(margin=dict(t=0, b=0, l=0, r=0), plot_bgcolor = 'rgba(0,0,0,0)')
	
	print (traces)
	return fig2
	
def statute(value): 

	print (value) 

	uri=[]
	statutes = {
    'Official Secrets Act 1911':'https://www.legislation.gov.uk/ukpga/Geo5/1-2/28/enacted/data.html', 
    'Easter Act 1928':'https://www.legislation.gov.uk/ukpga/Geo5/18-19/35/enacted/data.html',
    'Ireland Act 1949':'https://www.legislation.gov.uk/ukpga/Geo6/12-13-14/41/enacted/data.html',
    'Hotel Proprietors Act 1956':'https://www.legislation.gov.uk/ukpga/Eliz2/4-5/62/england/enacted/data.html',
    'Hovercraft Act 1968':'https://www.legislation.gov.uk/ukpga/1968/59/enacted/data.html',
    'Oil and Pipelines Act 1985':'https://www.legislation.gov.uk/ukpga/1985/62/enacted/data.html',
    'Computer Misuse Act 1990': 'https://www.legislation.gov.uk/ukpga/1990/18/enacted/data.html',
    'Intelligence Services Act 1994':'https://www.legislation.gov.uk/ukpga/1994/13/enacted/data.html',
    'Identity Documents Act 2010':'https://www.legislation.gov.uk/ukpga/2010/40/enacted/data.html',
    'National Citizen Service Act 2017':'https://www.legislation.gov.uk/ukpga/2017/15/enacted/data.html'
	}
	uri = [statutes[i] for i in value]  # https://stackoverflow.com/questions/54482256/comparing-list-with-a-dictionary-index-and-returning-dictionary-values-based-on  matches order of input values with statutes and returns the uris in same order
	
	#cf https://stackoverflow.com/questions/42056275/comparing-list-against-dict-return-key-if-value-matches-list

	print (uri) 
	
	return uri
	
def clean(uri):
	data = requests.get(uri) #gets a single uri and returns the staute in html  
	#data = session.get(uri) #proxy version
	content = data.content
	soup = BeautifulSoup(content, features="html.parser") #pre-processes the html
	clean_content = soup.get_text()
	text = clean_content # assigns the pre-procssed html as clean text
	return text 

def wordcount(text):
	res2 = len(text.split())
	totalwords = res2
	return totalwords


def ner(text):
	nlp = spacy.load('model')
	doc = nlp(text)
	return doc


def nercount(doc):

	neg_count = 0
	# Iterate over all the entities
	for ent in doc.ents:
		if ("(¬ P)" in ent.label_):  # isues counting (¬ P) when 1?
			neg_count += 1
		
	dsj_count = 0 
	for ent in doc.ents:
		if ("(P ∨ Q)" in ent.label_):  
			dsj_count += 1

	cnj_count = 0
	for ent in doc.ents:
		if ("(P ∧ Q)" in ent.label_): 
			cnj_count += 1
			
	
	mimp_count = 0
	for ent in doc.ents:
		if ("(P → Q)" in ent.label_): 
			mimp_count += 1		


	jd_count = 0
	for ent in doc.ents:
		if ("(P ↓ Q)" in ent.label_):  
			jd_count += 1
				
	cimp_count = 0
	for ent in doc.ents:
		if ("(P ← Q)" in ent.label_): 
			cimp_count += 1				
			
			
	print(neg_count, dsj_count, cnj_count, mimp_count, jd_count, cimp_count)

	return neg_count, dsj_count, cnj_count, mimp_count, jd_count, cimp_count

def data(uri):

	text=[]
	for x in uri:
		text.append(clean(x)) # passes each uri to obtain html and returns it as cleaned statute text added to a 'text' list
	print(text)	
	
	countwords = []
	for x in text:
		countwords.append(wordcount(x)) #counts the number of words for each statute text and adds it to a 'countwords' list
	countwords # e.g. [126, 503] 
	print(countwords)
	
	doc = []
	for x in text:
		doc.append(ner(x)) #makes an inference using the ner model to obtain logical connectives for each staute text and adds it to a 'doc' list
	print(doc)
	
	countner = []
	for x in doc:
		countner.append(nercount(x)) #counts the number of logical connectives in each statute text in the 'doc' list and adds it to a 'countner' list
	print(countner) #countner e.g. [(1, 3, 5), (1, 4, 26)] 
	
	# res = [[] for idx in range(len(countner))]
	# for i in range(len(countner)): # len = 2 so range is 0,1 as there are two items in [(1, 3, 5), (1, 4, 26)] 
		# for j in range(3): # 3 represetns the number of types of logical connecives which are fixed
			# res[i] += [countner[i][j]  / countwords[i]] # or res[i] = res[i] + [test_list[i][j]  / mult_list[i]] 
    
	res3 = []
	for i in range(len(countwords)):
		res3.append(tuple(ti/countwords[i] for ti in countner[i])) # divide each item of items in countner (logical connectives) e.g. [(1, 3, 5), (1, 4, 26)] by each item in countwords e.g [126, 503]     
		
	return res3 #e.g.  [(0.007936507936507936, 0.023809523809523808, 0.03968253968253968, 0.0, 0.0), (0.0019880715705765406, 0.007952286282306162, 0.05168986083499006, 0.0019880715705765406, 0.003976143141153081)]

def plot(neg, dsj, cnj, mimp, jd, cimp, value):

	lcdata= {'Logical Connective' : ['(¬ P)', '(P ∨ Q)', '(P ∧ Q)', '(P → Q)', '(P ↓ Q)', '(P ← Q)'],
        'Count':[neg, dsj, cnj, mimp, jd, cimp]}
		
	df = pd.DataFrame(lcdata)
	
	fig = go.Figure(data=[go.Pie(
				values=df['Count'], labels=df['Logical Connective']
				#text=df['Count'],
				#orientation='h',
				#text=df['Count'], #for chart lables
				#textposition='auto',
				# https://community.plotly.com/t/simply-bar-chart-without-any-aggregation/32359  searched "go.bar marker_color" in google images cf. https://community.plotly.com/t/different-colors-for-bars-in-barchart-by-their-value/6527/7 for pie charts https://stackoverflow.com/questions/63162423/map-colors-to-labels-in-plotly-go-pie-charts
			)])                                                             

	fig.update_traces(hoverinfo='label+percent', textinfo='value', marker=dict(colors=['lightgreen', 'orange', 'lightblue', 'grey', 'salmon', 'purple']))
	
	fig.update_layout(
		legend=dict(
        x=0,
        y=-.1, # https://stackoverflow.com/questions/60123611/how-to-position-legends-inside-a-plot-in-plotly
        traceorder="normal"),
		title='Logical Connectives Count',
		margin=dict(t=0, b=0, l=0, r=0)
		# https://community.plotly.com/t/how-to-increase-size-of-pie-chart/32420
		#xaxis_title='Count',
		#yaxis_title='Logical connective',
		#legend_title='Legend Title',
		#yaxis_visible=False,
		#template="simple_white" # https://plotly.com/python/pandas-backend/
		# font=dict(
			# family='arial',
			# size=18,
			# color='Black'
		# )
	)

	return fig 

def plot3(selectedVariable2, stats):

	print ('stats is' + str (stats))

	print ('plot 3' + str (selectedVariable2))
	
	q = [sum(x) for x in stats] # [0.07142857142857142, 0.06163021868787276]
	
	print ('q is ' + str (q))
	#diction = {'The Parliament (Qualification of Women) Act 1918': q1, 'Easter Act 1928': q2}
	
	global df # used for the datatable
	df = pd.DataFrame({'Statutes': selectedVariable2, 'Complexity index': q }) # https://www.datasciencelearner.com/how-to-create-a-bar-chart-from-a-dataframe-in-python/   # remove [] to get rid of ValueError: All arrays must be of the same length
	df = df.round(3) # https://www.reddit.com/r/learnpython/comments/995n7z/pandas_round_not_working/
	df = df.sort_values('Complexity index', ascending=False)
	
	print(df)
	
	# # for single charts 
	# if selectedVariable2 == ['The Parliament (Qualification of Women) Act 1918']: 
		# q1 = quotient[0]

	# elif selectedVariable2 == ['Easter Act 1928']:
		# q2 = quotient[0]

	# elif len(stats) == 2:
		# q1 = quotient[0]
		# q2 = quotient[1]

	# print ('plot 3' + str (q1))	
	# print ('plot 3' + str (q2))	

	#statute1 = selectedVariable2
	#q1, q2 = q
	
	#statute1, statute2 = selectedVariable2

	# x = selectedVariable2 # needs to be a string not list
	# y = diction['The Parliament (Qualification of Women) Act 1918'], diction['Easter Act 1928']

	#colors = {'Official Secrets Act 1911':'lightblue', 'Easter Act 1928':'tomato', 'Ireland Act 1949':'lightgreen', 'Hotel Proprietors Act 1956':'purple', 'Hovercraft Act 1968':'orange', 'Oil and Pipelines Act 1985':'teal', 'Computer Misuse Act 1990':'coral', 'Intelligence Services Act 1994':'green', 'Identity Documents Act 2010': 'orchid', 'National Citizen Service Act 2017':'tan'}

	colors = {'Official Secrets Act 1911':'lightblue', 'Easter Act 1928':'tomato', 'Ireland Act 1949':'lightgreen', 'Hotel Proprietors Act 1956':'purple', 'Hovercraft Act 1968':'orange', 'Oil and Pipelines Act 1985':'teal', 'Computer Misuse Act 1990':'coral', 'Intelligence Services Act 1994':'green', 'Identity Documents Act 2010': 'orchid', 'National Citizen Service Act 2017':'tan'} 

	col = [colors[i] for i in selectedVariable2] 
	#widths = 0.1

	fig3 = go.Figure([go.Bar(y=df['Statutes'], #https://plotly.com/python/bar-charts/ #https://plotly.com/python/graph-objects/
							x=df['Complexity index'],
							orientation='h',
							marker_color=col, #remove [] from col otherwise bars are black
							name='foo')])

	

	#fig3.update_layout(template = None)
	#fig3.update_xaxes(showgrid = False, showticklabels = False, zeroline=False)
	#fig3.update_yaxes(showgrid = False, showticklabels = False, zeroline=False)

	
	fig3.update_layout(margin=dict(t=0, b=0, l=0, r=0,), plot_bgcolor = 'rgba(0,0,0,0)') #(bargap=0.1)
	return fig3

	
@app.callback([
    Output('text-out', 'children'),
    Output('graph', 'figure')], 
	[Input('submit-button', 'n_clicks')],
[State('data-dropdown', 'value')])
def multi_output(n_clicks, value):
	if value is None:
		raise PreventUpdate
		
	v=[]
	v.append(value) # convert list to string as statute() takes list
	
	uri = statute(v)
	
	list = uri
	struri = ''.join(list) # convert string to list otherwise requests.exceptions.InvalidSchema: No connection adapters were found for "['https://www.legislation.gov.uk/ukpga/Geo5/8-9/47/enacted/data.html']"
	
	print(struri)
	text=clean(struri)
	doc= ner(text)
	data = nercount(doc)
	neg, dsj, cnj, mimp, jd, cimp = data #https://note.nkmk.me/en/python-tuple-list-unpack/
	chart = plot(neg, dsj, cnj, mimp, jd, cimp, value)
	infer = render(doc)
	return infer, chart


@app.callback(Output('plot2', 'figure'), # Dabbas p.279
			Output('plot3', 'figure'), 
			Input('submit-button2', 'n_clicks'),
			State('multiVariableDropdown', 'value'))
			 
def update_graph(n_clicks, selectedVariable2): 
	#if selectedVariable2 is None:
		#raise PreventUpdate  # stops the app from processsing nothing i.e "ValueError: not enough values to unpack (expected 6, got 0)"
	print ('selectedVariable2 is ' + str (selectedVariable2))
	uri = statute(selectedVariable2) #assigns uris obtained from selectedVariables2 from statute()
	print ('uri is ' + str (uri))
	stats = data(uri) 
	print("stats : " + str(stats))
	if stats == []:
		raise PreventUpdate
	chart1 = plot2(selectedVariable2, stats)
	chart2 = plot3(selectedVariable2, stats)
	return chart1, chart2


@app.callback(Output('table1','children'),
            [Input('submit-button3','n_clicks')],
                [State('submit-button3','n_clicks')])

def update_datatable(n_clicks,csv_file):            
    if n_clicks:                            
        data = df.to_dict('records')
        columns =  [{"name": i, "id": i,} for i in (df.columns)]
        return dt.DataTable(data=data, columns=columns)


if __name__ == '__main__':
    app.run_server(debug=False, port=10000)
