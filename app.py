import requests
import re
from bs4 import BeautifulSoup
import dash
import dash_html_components as html
import spacy
from spacy import displacy 
import json
import dash_core_components as dcc

# Initialize the application
app = dash.Dash(__name__)

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

data = requests.get("https://www.legislation.gov.uk/ukpga/Geo5/8-9/47/enacted/data.html") 
content = data.content

soup = BeautifulSoup(content, features="html.parser")
clean_content = soup.get_text()
text = clean_content

nlp = spacy.load(r".\model")
doc = nlp(text)
print("Entities:", doc.ents)
#displacy.render(doc, style="ent", options=options)

# define de app
app.layout = html.Div(
    children=render(doc)
)

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)