import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import PYF_clsLayout as layouts
import PYF_clsModel as model
import PYF_clsDial as dial
import dash
import os
import re

MODELS = '/home/chipdelmal/Documents/WorkSims/PYF/Onetahi/sims/PAN/MODELS/'
def get_kv_pair(model_name):
    key = int(re.search(r'[0-9]+', model_name)[0])
    # print(key)
    val = model.Model(os.path.join(MODELS, model_name))
    return key, val

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
rfm = dict(get_kv_pair(model_name) for model_name in os.listdir(MODELS) if model_name[-7:] == '.joblib')

# DO NOT DELETE THIS - this is required for Heroku deployment to succeed
server = app.server

app.layout = html.Div([
    dbc.Col(html.H2('Welcome!')),
    dbc.Col(html.Hr()),
    dbc.Row([
        dbc.Col(
            dbc.Container([
                dbc.Row([
                    dbc.Col(layouts.pop_div), 
                    dbc.Col(layouts.ren_div)
                ]),
                layouts.mdl_div(rfm.keys()),
                layouts.res_div,
                layouts.mad_div,
                layouts.mat_div,
                layouts.qnt_div,
            ])
        ),
        dbc.Col(
            dbc.Container([
                dbc.Col(layouts.prd_div)
            ])
        )
    ])
])

@app.callback(
    dash.dependencies.Output('prediction', 'children'),
    # dash.dependencies.Output('dial', 'children'),    
    dash.dependencies.Input('mdl-slider', 'value'),
    dash.dependencies.Input('pop-input' , 'value'),
    dash.dependencies.Input('ren-input' , 'value'),
    dash.dependencies.Input('res-slider', 'value'),
    dash.dependencies.Input('mad-slider', 'value'),
    dash.dependencies.Input('mat-slider', 'value')
)

def update_prediction(mdl, pop, ren, res, mad, mat):
    prediction = rfm[mdl].predict(pop, ren, res, mad, mat)
    # print([pop, ren, res, mad, mat])
    return prediction

if __name__ == '__main__':
    app.run_server(debug=True)
