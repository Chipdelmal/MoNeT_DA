def labelTranslate(className):
    label = "None"
    if className == 1:
        label = "Low"
    elif className == 2:
        label = "Mid"
    elif className == 3:
        label = "High"
    elif className == 4:
        label = "Semi-Permanent"
    elif className == 5:
        label = "Permanent"
    return label

def sexTranslate(sexValue):
    sexes = [True, False, False]
    if sexValue == 1:
        sexes = [False, True, False]
    elif sexValue == 1:
        sexes = [False, False, True]
    return sexes
