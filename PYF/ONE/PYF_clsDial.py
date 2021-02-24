import plotly.graph_objects as go
import numpy as np

base_chart = {
    "values": [40, 10, 10, 10, 10],
    "labels": [" ", " ", " ", " ", " ", " "],
    "domain": {"x": [0, .9]},
    "marker": {
        "colors": [
            'rgb(255, 255, 255)',
            'rgb(255, 255, 255)',
            'rgb(255, 255, 255)',
            'rgb(255, 255, 255)',
            'rgb(255, 255, 255)',
            'rgb(255, 255, 255)',
        ],
        "line": {
            "width": 0
        }
    },
    "name": "Gauge",
    "hole": .4,
    "type": "pie",
    "direction": "clockwise",
    "rotation": 90,
    "showlegend": False,
    "hoverinfo": "none",
    "textinfo": "label",
    "textposition": "outside"
}

meter_chart = {
    "values": [40, 10, 10, 10, 10, 10],
    "labels": [' ', 'NONE', 'LOW', 'MID', 'HIGH', 'PERMANENT'],
    "marker": {
        'colors': [
            'rgb(255, 255, 255)',
            'rgb(245,252,255)',
            'rgb(219,243,250)',
            'rgb(183,233,247)',
            'rgb(146,223,243)',
            'rgb(122,215,240)'
        ]
    },
    "domain": {"x": [0, 0.9]},
    "name": "Gauge",
    "hole": .3,
    "type": "pie",
    "direction": "clockwise",
    "rotation": 100,
    "showlegend": False,
    "textinfo": "label",
    "textposition": "inside",
    "hoverinfo": "none",
}

def rotate_coord(coord, degrees, origin=(0.45, 0.5)):
    radns = np.radians([degrees])[0]
    coord = coord - np.array(origin)
    coord = np.array([
        [np.cos(radns), -np.sin(radns)],
        [np.sin(radns),  np.cos(radns)]
    ]) @ np.array(coord)
    coord = coord + np.array(origin)
    return coord

def get_path(prediction, center=(0.45, 0.65)):
    # For simplicity, we only move the topmost point of the triangle 
    svg_path = lambda coord: "M 0.445 0.5 L {} {} L 0.455 0.5 Z".format(*coord)
    if prediction == "LOW":
        return svg_path(rotate_coord(center, 25))
    if prediction == "MID":
        return svg_path(rotate_coord(center, 0))
    if prediction == "HIGH":
        return svg_path(rotate_coord(center, -25))
    if prediction == "PERMANENT":
        return svg_path(rotate_coord(center, -90))
    return svg_path(rotate_coord(center, 90))

def point_to(prediction):
    return {
        'shapes': [
            {
                'type': 'path',
                'path': get_path(prediction),
                'fillcolor': 'rgba(28,104,192, 0.5)',
                'line': {
                    'width': 0.5
                },
                'xref': 'paper',
                'yref': 'paper'
            }
        ]
    }

def create_dial(prediction):
    return go.Figure([base_chart, meter_chart], layout=point_to(prediction))
