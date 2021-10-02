def transform(self, x, y):
        return self.transformPerspective(x, y)
        # return self.transform2D(x,y)

def transform2D(self, x, y):
    return int(x), int(y)

def transformPerspective(self, x, y):
    # sets 3d y coordinate
    linearY = y * self.perspecitvePointY / self.height
    # limits y to the perspective point
    if linearY > self.perspecitvePointY:
        linearY = self.perspecitvePointY

    # calculates distance to the perspective point
    diffX = x - self.perspecitvePointX
    diffY = self.perspecitvePointY - linearY

    # gets proportional distance
    factorY = diffY/self.perspecitvePointY
    factorY = pow(factorY, 4)

    # calculates x based on proportional distance of y
    transformedX = self.perspecitvePointX + diffX * factorY
    transformedY = (1- factorY) *self.perspecitvePointY

    return int(transformedX), int(transformedY)