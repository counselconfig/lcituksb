import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import requests
import re
from bs4 import BeautifulSoup
import spacy
from spacy import displacy 
import json

app = dash.Dash()

app.layout = html.Div([
    dcc.Dropdown(
    id='number-in',
    options=[
        {'label': 'Metropolitan Police Act 1839', 'value': 'MPA'},
        {'label': 'Easter Act 1928', 'value': 'EA'},
        {'label': 'Parliament (Qualification of Women) Act 1918', 'value': 'PQWA'}
    ],
    placeholder="Select a statute",
    ),
    html.Button(
        id='submit-button',
        n_clicks=0,
        children='Submit',
        style={'fontSize':28}
    ),
    html.Div(id='number-out')
])

DEFAULT_LABEL_COLORS = {"(P ∧ Q)":"lightblue", "(¬ P)":"lightgreen","(P ∨ Q)":"orange","(P ← Q)":"purple","(P ↓ Q)":"light red","(P → Q)":"grey"}

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

def ner(url):
    data = requests.get(url) 
    content = data.content
    soup = BeautifulSoup(content, features="html.parser")
    clean_content = soup.get_text()
    text = clean_content
    nlp = spacy.load(r".\model")
    doc = nlp(text)
    return render(doc)

@app.callback(
    Output('number-out', 'children'),
    [Input('submit-button', 'n_clicks')],
    [State('number-in', 'value')])
def output(n_clicks, number):
    if number == 'PQWA':
        url = "https://www.legislation.gov.uk/ukpga/Geo5/8-9/47/enacted/data.html"
    elif number == 'EA':
        url = "https://www.legislation.gov.uk/ukpga/Geo5/18-19/35/enacted/data.html"
    elif number == 'MPA':
        url = "https://www.legislation.gov.uk/ukpga/Vict/2-3/47/enacted/data.html"
    return ner(url)

if __name__ == '__main__':
    app.run_server()
