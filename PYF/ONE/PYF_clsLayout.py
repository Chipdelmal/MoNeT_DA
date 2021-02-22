import dash_html_components as html
import dash_core_components as dcc

def get_marks(start, end, step, norm=None):
    marks = dict()
    for i in range(start, end, step):
        if norm:
            if i == start or i == end - 1:
                marks[int(i / norm)] = str(int(i / norm))
            else:
                marks[i / norm] = str(i / norm)
        else:
            marks[i] = str(i)
    return marks

def mdl_div(model_keys):
    if len(model_keys) == 0: raise ValueError("Found 0 models to use!")
    mink = min(model_keys)
    maxk = max(model_keys)
    return html.Div([
        html.H5('Threshold:'),
        dcc.Slider(
            id='mdl-slider',
            min=mink,
            max=maxk,
            step=None,
            value=10,
            marks={k: str(k) for k in model_keys}
        )
    ])

pop_div = html.Div([
    html.H5('Population:'),
    dcc.Input(
        id="pop-input",
        type="number",
        value=20
    )
])

ren_div = html.Div([
    html.H5('Releases Number:'),
    dcc.Input(
        id="ren-input",
        type="number",
        value=20
    )
])

res_div = html.Div([
    html.H5('Released Fraction:'),
    dcc.Slider(
        id='res-slider',
        min=0,
        max=1,
        step=0.15,
        value=1,
        marks=get_marks(0, 10 + 1, 1, 10)
    )
])

mad_div = html.Div([
    html.H5('Adult Mortality:'),
    dcc.Slider(
        id='mad-slider',
        min=0,
        max=0.5,
        step=0.01,
        value=0.15,
        marks=get_marks(0, 100+1, 5, 100)
    )
])

mat_div = html.Div([
    html.H5('Mating Reduction:'),
    dcc.Slider(
        id='mat-slider',
        min=0,
        max=0.5,
        step=0.01,
        value=0.1,
        marks=get_marks(0, 100+1, 5, 100)
    )
])

qnt_div = html.Div([
    html.H5('Quantile:'),
    dcc.Slider(
        id='qnt-slider',
        min=0,
        max=95,
        step=5,
        value=50,
        marks=get_marks(0, 100, 5)
    )
])

prd_div = html.Div([
    html.H5('Prediction:'),
    html.Div(id='prediction')
])
