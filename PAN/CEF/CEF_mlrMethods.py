
from sklearn.pipeline import make_pipeline
from xgboost import XGBRFRegressor
from sklearn.preprocessing import MinMaxScaler
from sklearn.tree import DecisionTreeRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor
from sklearn.ensemble import GradientBoostingRegressor, HistGradientBoostingRegressor
import CEF_aux as aux


def selectML(method, MOI):
    if method=='rf':
        modID = 'rdf'
        rf = RandomForestRegressor(
            n_estimators=100, max_depth=None, max_features="sqrt",
            oob_score=True, criterion='squared_error',
            n_jobs=aux.JOB_DSK*2, 
            verbose=True
        )
    elif method=='ada':
        rf = AdaBoostRegressor(
            DecisionTreeRegressor(max_depth=50), 
            loss='linear', n_estimators=100
        )
    elif method=='gb':
        rf = GradientBoostingRegressor(
            n_estimators=100, max_leaf_nodes=75, max_depth=30, 
            verbose=True
        )
    elif method=='hgb':
        modID = 'hgb'
        if MOI=='CPT':
            mono = aux.SA_MONOTONIC_CPT
        else:
            mono = aux.SA_MONOTONIC_WOP
        rf = HistGradientBoostingRegressor(
            loss='quantile', quantile=.25, 
            max_iter=1000, max_leaf_nodes=75, max_depth=None, 
            max_bins=255,
            monotonic_cst=list(mono.values()),
            verbose=True
        )
    if method=='rfg':
        rf_o = RandomForestRegressor(
            oob_score=True, criterion='squared_error',
            n_jobs=aux.JOB_DSK*2, 
            verbose=False
        )
        param_grid = [{
            'n_estimators': [50, 100, 200], 
            'max_depth':    [20, 25, 30, 50, None],
            'max_features': ['sqrt', 'log2', None]
        }]
        rf = GridSearchCV(
            estimator=rf_o, param_grid=param_grid,
            n_jobs=8, verbose=2
        )
    elif method=='gbg':
        rf_o = GradientBoostingRegressor()
        param_grid = [{
            'n_estimators':     [50, 100, 200], 
            'max_leaf_nodes':   [20, 30, 50, 75, None],
            'max_depth':        [20, 30, None]
        }]
        rf = GridSearchCV(
            estimator=rf_o, param_grid=param_grid,
            n_jobs=8, verbose=2
        )
    elif method=='xgb':
        if MOI=='CPT':
            mono = aux.SA_MONOTONIC_CPT
        else:
            mono = aux.SA_MONOTONIC_WOP
        rf = XGBRFRegressor(
            n_jobs=aux.JOB_DSK*2,
            n_estimators=500, max_depth=None,
            tree_method='hist',
            max_bin=5000,
            objective='reg:squarederror',
            eval_metric='mae',
            verbose=2
        )
    elif method=='mlp':
        modID = 'mlp'
        rf = make_pipeline(
            MinMaxScaler(),
            MLPRegressor(
                hidden_layer_sizes=(100, 50), 
                verbose=True
            )
        )
    return (rf, modID)