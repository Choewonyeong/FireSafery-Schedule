def returnTranValue(value):
    try:
        value = float(value)
    except:
        value = 0.0
    split = str(value).split('.')
    intValue = int(split[1])
    if value == 0.0:
        value = ''
    elif not intValue:
        value = str(int(value))
    else:
        value = str(value)
    return value

