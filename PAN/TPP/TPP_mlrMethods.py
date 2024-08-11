
import numpy as np
from sklearn.pipeline import make_pipeline
from xgboost import XGBRFRegressor
from keras.layers import Dense
from keras.models import Sequential
from keras.callbacks import EarlyStopping
from keras.regularizers import L1L2
from scikeras.wrappers import KerasRegressor
from tensorflow.keras.layers import BatchNormalization
from sklearn.preprocessing import MinMaxScaler
from sklearn.tree import DecisionTreeRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor
from sklearn.ensemble import GradientBoostingRegressor, HistGradientBoostingRegressor
import TPP_aux as aux



def selectMLKeras(MOI, QNT='50', inDims=8):
    if QNT:
        if (MOI=='CPT'):
            print("* CPT Topology")
            (batchSize, epochs) = (128, 300)
            def build_model():
                rf = Sequential()
                rf.add(Dense(
                    16, activation= "tanh", input_dim=inDims,
                    kernel_regularizer=L1L2(l1=1e-5, l2=2.25e-4)
                ))
                rf.add(Dense(
                    32, activation= "LeakyReLU",
                    kernel_regularizer=L1L2(l1=1e-5, l2=2.25e-4)
                ))
                rf.add(Dense(
                    32, activation= "LeakyReLU",
                    kernel_regularizer=L1L2(l1=1e-5, l2=2.25e-4)
                ))
                rf.add(Dense(
                    1, activation='sigmoid'
                ))
                rf.compile(
                    loss= "mean_squared_error" , 
                    optimizer="adam", 
                    metrics=["mean_squared_error"]
                )
                return rf
            rf = KerasRegressor(build_fn=build_model, verbose=0)
        elif (MOI=='TTI') or (MOI=='TTO'):
            print("* TTI/TTO Topology")
            (batchSize, epochs) = (128, 1000)
            def build_model():
                rf = Sequential()
                rf.add(Dense(
                    32, activation= "tanh", input_dim=inDims,
                    kernel_regularizer=L1L2(l1=1e-5, l2=2.75e-4)
                ))
                rf.add(Dense(
                    32, activation= "LeakyReLU",
                    kernel_regularizer=L1L2(l1=1e-5, l2=2.75e-4)
                ))
                rf.add(Dense(
                    1, activation='sigmoid'
                ))
                rf.compile(
                    loss= "mean_squared_error" , 
                    optimizer="adam", 
                    metrics=["mean_squared_error"]
                )
                return rf
            rf = KerasRegressor(build_fn=build_model, verbose=0)
        elif (MOI=='WOP'):
            print("* WOP Topology")
            (batchSize, epochs) = (128, 300)
            def build_model():
                rf = Sequential()
                rf.add(Dense(
                    16, activation= "tanh", input_dim=inDims,
                    kernel_regularizer=L1L2(l1=1e-5, l2=2.75e-4)
                ))
                rf.add(Dense(
                    16, activation= "tanh",
                    kernel_regularizer=L1L2(l1=1e-5, l2=2.75e-4)
                ))
                rf.add(Dense(
                    16, activation= "tanh",
                    kernel_regularizer=L1L2(l1=1e-5, l2=2.75e-4)
                ))
                rf.add(Dense(
                    1, activation='sigmoid'
                ))
                rf.compile(
                    loss= "mean_squared_error" , 
                    optimizer="adam", 
                    metrics=["mean_squared_error"]
                )
                return rf
            rf = KerasRegressor(build_fn=build_model, verbose=0)
    else:
        if (MOI=='CPT'):
            print("* CPT Optimizer")
            (batchSize, epochs) = (128*2, 100)
            def build_model():
                rf = Sequential()
                rf.add(Dense(
                    16, activation= "tanh", input_dim=inDims,
                    kernel_regularizer=L1L2(l1=1e-5, l2=2.75e-4)
                ))
                rf.add(Dense(
                    16, activation= "tanh",
                    kernel_regularizer=L1L2(l1=1e-5, l2=2.75e-4)
                ))
                rf.add(Dense(
                    16, activation= "tanh",
                    kernel_regularizer=L1L2(l1=1e-5, l2=2.75e-4)
                ))
                rf.add(Dense(
                    1, activation='sigmoid'
                ))
                rf.compile(
                    loss= "mean_squared_error" , 
                    optimizer="adam", 
                    metrics=["mean_squared_error"]
                )
                return rf
            rf = KerasRegressor(build_fn=build_model)
        elif (MOI=='WOP'):
            print("* WOP Optimizer")
            (batchSize, epochs) = (128*2, 150)
            def build_model():
                rf = Sequential()
                rf.add(Dense(
                    16, activation= "tanh", input_dim=inDims,
                    kernel_regularizer=L1L2(l1=1e-5, l2=2.75e-4)
                ))
                rf.add(Dense(
                    32, activation= "LeakyReLU",
                    kernel_regularizer=L1L2(l1=1e-5, l2=4.25e-4)
                ))
                rf.add(Dense(
                    32, activation= "LeakyReLU",
                    kernel_regularizer=L1L2(l1=1e-5, l2=4.25e-4)
                ))
                rf.add(Dense(
                    1, activation='sigmoid'
                ))
                rf.compile(
                    loss= "mean_squared_error" , 
                    optimizer="adam", 
                    metrics=["mean_squared_error"]
                )
                return rf
            rf = KerasRegressor(build_fn=build_model)   
    return (epochs, batchSize, rf)
        

def selectML(method, MOI, inDims=8):
    if method=='rf':
        modID = 'rdf'
        rf = RandomForestRegressor(
            n_estimators=100, max_depth=None, max_features="sqrt",
            oob_score=True, criterion='squared_error',
            n_jobs=aux.JOB_DSK*2, 
            verbose=True
        )
    elif method=='krs':
        modID = 'krs'
        if (MOI=='CPT'):
            def build_model():
                rf = Sequential()
                rf.add(Dense(
                    16, activation= "tanh", input_dim=inDims,
                    kernel_regularizer=L1L2(l1=1e-5, l2=2.75e-4)
                ))
                rf.add(Dense(
                    16, activation= "tanh",
                    kernel_regularizer=L1L2(l1=1e-5, l2=2.75e-4)
                ))
                rf.add(Dense(
                    16, activation= "tanh",
                    kernel_regularizer=L1L2(l1=1e-5, l2=2.75e-4)
                ))
                rf.add(Dense(
                    1, activation='sigmoid'
                ))
                rf.compile(
                    loss= "mean_squared_error" , 
                    optimizer="adam", 
                    metrics=["mean_squared_error"]
                )
                return rf
            print("* CPT Optimizer")
            rf = KerasRegressor(build_fn=build_model)
            return rf
        elif (MOI=='POE'):
            def build_model():
                rf = Sequential()
                rf.add(Dense(
                    16, activation= "sigmoid", input_dim=inDims,
                    kernel_regularizer=L1L2(l1=1e-5, l2=2.5e-4)
                ))
                rf.add(Dense(
                    16, activation= "LeakyReLU",
                    kernel_regularizer=L1L2(l1=1e-5, l2=3.125e-4)
                ))
                rf.add(Dense(
                    16, activation= "LeakyReLU",
                    kernel_regularizer=L1L2(l1=1e-5, l2=3.125e-4)
                ))
                rf.add(Dense(
                    1, activation='sigmoid'
                ))
                rf.compile(
                    loss= "mean_squared_error" , 
                    optimizer="adam", 
                    metrics=["mean_squared_error"]
                )
                return rf
            rf = KerasRegressor(build_fn=build_model)
            return rf
        elif (MOI=='WOP'):
            def build_model():
                rf = Sequential()
                rf.add(Dense(
                    15, activation= "tanh", input_dim=inDims,
                    kernel_regularizer=L1L2(l1=1e-5, l2=3e-4)
                ))
                rf.add(Dense(
                    15, activation= "tanh",
                    kernel_regularizer=L1L2(l1=1e-5, l2=3e-4)
                ))
                rf.add(Dense(
                    15, activation= "tanh",
                    kernel_regularizer=L1L2(l1=1e-5, l2=3e-4)
                ))
                rf.add(Dense(
                    1, activation='sigmoid'
                ))
                rf.compile(
                    loss= "mean_squared_error" , 
                    optimizer="adam", 
                    metrics=["mean_squared_error"]
                )
            rf = KerasRegressor(build_fn=build_model)
            return rf
    elif method=='mlp':
        modID = 'mlp'
        if (MOI=='CPT'):
            rf = make_pipeline(
                MinMaxScaler(),
                MLPRegressor(
                    hidden_layer_sizes=(10, 15, 10),
                    learning_rate='adaptive', 
                    tol=0.0001,
                    alpha=0.008,
                    verbose=False,
                    early_stopping=True,
                    activation='tanh'
                )
            )
        elif (MOI=='POE'):
            rf = make_pipeline(
                MinMaxScaler(),
                MLPRegressor(
                    hidden_layer_sizes=(10, 15, 10),
                    learning_rate='adaptive', 
                    tol=0.00001,
                    alpha=0.005,
                    verbose=False,
                    early_stopping=True,
                    activation='relu'
                )
            )
        elif (MOI=='WOP'):
            rf = make_pipeline(
                MinMaxScaler(),
                MLPRegressor(
                    hidden_layer_sizes=(10, 20, 10),
                    learning_rate='adaptive', 
                    tol=0.00001,
                    alpha=0.0035,
                    verbose=False,
                    early_stopping=True,
                    activation='relu'
                )
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
    return (rf, modID)


def unison_shuffled_copies(a, b, size=1000):
    assert len(a) == len(b)
    p = np.random.permutation(len(a))
    return a[p][:size], b[p][:size]


def getRanges(df, varNames):
    rangs = []
    for v in varNames:
        vran = (np.min(df[v]), np.max(df[v]))
        rangs.append(vran)
    return rangs


def adjRSquared(rSquared, samplesNum, featuresNum):
    rAdj = 1-(1-rSquared)*(samplesNum-1)/(samplesNum-featuresNum-1)
    return rAdj
