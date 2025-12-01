class XY:
	def __init__(self, x, y):
		self.x = x
		self.y = y
	def __repr__(self):
		return f"({self.x}, {self.y})"

	def value(self):
		return (self.x, self.y)


class AABB:
	def __init__(self, center, halfDimension):
		self._cnt = center
		self._hlfDim = halfDimension


	# Checks if point is in  boundary of the axis align bounding box
	def containsPoint(self, point: XY):
		return (self._cnt.x - self._hlfDim <= point.x <= self._cnt.x + self._hlfDim) and (self._cnt.y - self._hlfDim <= point.y <= self._cnt.y + self._hlfDim)

	def divide(self):
		x = self._cnt.x /2
		y = self._cnt.y /2
		hlfDim = self._hlfDim /2
		return AABB(XY(x, y), hlfDim)

	def intersectsAABB(self, other):
		return (abs(self._cnt.x - other._cnt.x) <= (self._hlfDim + other._hlfDim)) and (abs(self._cnt.y - other._cnt.y) <= (self._hlfDim + other._hlfDim))

	def value(self):
		return (self._cnt.x, self._cnt.y, self._hlfDim)


class QuadTree:
	QT_NODE_CAPACITY = 4
	BOXES = []
	def __init__(self, boundary: AABB):
		self._boundary = boundary
		self._points = []

		self.northWest = None
		self.northEast = None
		self.southWest = None
		self.southEast = None
		self.BOXES.append(boundary.value())

	def insert(self, p: XY):
		if not self._boundary.containsPoint(p):
			return False	# object cannot be added

		if (len(self._points) < self.QT_NODE_CAPACITY and self.northWest == None):
			self._points.append(p)

			return True
		if (self.northWest == None):
			self.subdivide()

		if (self.northWest.insert(p)): return True
		if (self.northEast.insert(p)): return True
		if (self.southWest.insert(p)): return True
		if (self.southEast.insert(p)): return True

		return False

	def subdivide(self):
		div = self._boundary._hlfDim / 2
		x = self._boundary._cnt.x
		y = self._boundary._cnt.y

		ne = AABB(XY(x - div, y - div), div)
		nw = AABB(XY(x + div, div), div)
		se = AABB(XY(div, y + div), div)
		sw = AABB(XY(x + div, y + div), div)

		self.northEast = QuadTree(ne)
		self.northWest = QuadTree(nw)
		self.southEast = QuadTree(se)
		self.southWest = QuadTree(sw)


	def queryRange(self, rnge: AABB):
		pointsInRange = []
		if not self._boundary.intersectsAABB(rnge):
			return pointsInRange

		for p in self._points:
			if (rnge.containsPoint(p)):
				pointsInRange.append(p)

		if (self.northWest == None):
			return pointsInRange

		pointsInRange.extend(self.northWest.queryRange(rnge))
		pointsInRange.extend(self.northEast.queryRange(rnge))
		pointsInRange.extend(self.southWest.queryRange(rnge))
		pointsInRange.extend(self.southEast.queryRange(rnge))

		return pointsInRange



if __name__ == '__main__':
	point = XY(350, 350)
	boundary = AABB(XY(250, 250), 250)
	# print(boundary.containsPoint(point))
	qt = QuadTree(boundary)
	qt.insert(point)
	qt.insert(XY(10, 10))
	qt.insert(XY(100, 100))
	qt.insert(XY(50, 50))
	qt.insert(XY(400, 125))
	qt.insert(XY(450, 100))
	qt.insert(XY(400, 400))
	qt.insert(XY(150, 400))
	qt.insert(XY(200, 350))

	print(qt.queryRange(boundary))
	print(qt.BOXES)
