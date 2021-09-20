def getPercentageFromAngle(input, max, min):
    if input > max or input < min: return 0
    return ((abs(input - min)) * 100) / abs(max - min)


while True:
    inpAngle = (int)(input("Enter inp"))
    minAngle = (int)(input("Enter min"))
    maxAngle = (int)(input("Enter max"))
    print(getPercentageFromAngle(inpAngle, maxAngle, minAngle))
