def labelTranslate(className):
    label = "None"
    if className == 1:
        label = "Low"
    elif className == 2:
        label = "Mid"
    elif className == 3:
        label = "High"
    elif className == 4:
        label = "Permanent"
    return str(className)

def sexTranslate(sexValue):
    sexes = [True, False, False]
    if sexValue == 1:
        sexes = [False, True, False]
    elif sexValue == 1:
        sexes = [False, False, True]
    return sexes
