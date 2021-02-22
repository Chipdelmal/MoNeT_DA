import joblib

class Model:

    def __init__(self, path_to_model):
        self.model = joblib.load(path_to_model)

    def _label_translate(self, prediction):
        prediction = prediction[0]
        if prediction == 0: return "None"
        if prediction == 1: return "Transient"
        if prediction == 2: return "Permanent"
        raise ValueError("Invalid prediction encountered: {}".format(prediction))

    def predict(self, pop, ren, res, mad, mat):
        in_probe = [[
            int(pop), int(ren), float(res), float(mad), float(mat)
        ]]
        return self._label_translate(self.model.predict(in_probe))
