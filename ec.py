
# Reference: https://bitcointalk.org/index.php?topic=23241.0
import random
# Class for declaring an Elliptic Curve of the form y^2 = x^3 + ax + b (mod p)
class CurveFp( object ):
	def __init__( self, p, a, b ):

# Declaring values of parameters `a`, `b`, `p` in the Elliptic Curve- y^2 = x^3 + ax + b (mod p)

		self.__p = p
		self.__a = a
		self.__b = b

	def p( self ):
		return self.__p

	def a( self ):
		return self.__a

	def b( self ):
		return self.__b

	def contains_point( self, x, y ):
		return ( y * y - ( x * x * x + self.__a * x + self.__b ) ) % self.__p == 0

class Point( object ):
	def __init__( self, curve, x, y, order = None ):
		self.__curve = curve
		self.__x = x
		self.__y = y
		self.__order = order
		if self.__curve:
			assert self.__curve.contains_point( x, y )
		if order:
			assert self * order == INFINITY

	def __add__( self, other ):
		if other == INFINITY: return self
		if self == INFINITY: return other
		assert self.__curve == other.__curve
		if self.__x == other.__x:
            		if ( self.__y + other.__y ) % self.__curve.p() == 0:
                		return INFINITY
            		else:
                		return self.double()

		p = self.__curve.p()
		l = ( ( other.__y - self.__y ) * inverse_mod( other.__x - self.__x, p ) ) % p
		x3 = ( l * l - self.__x - other.__x ) % p
		y3 = ( l * ( self.__x - x3 ) - self.__y ) % p
		return Point( self.__curve, x3, y3 )

	def __mul__( self, other ):
		def leftmost_bit( x ):
			assert x > 0
			result = 1
			while result <= x: result = 2 * result
			return result / 2

		e = int(other)
		if self.__order: e = e % self.__order
		if e == 0: return INFINITY
		if self == INFINITY: return INFINITY
		assert e > 0
		e3 = int(3 * e)
		negative_self = Point( self.__curve, self.__x, -self.__y, self.__order )
		i = leftmost_bit( e3 ) / 2
		result = self
		while i > 1:
			result = result.double()
			if ( e3 & int(i) ) != 0 and ( e & int(i) ) == 0: result = result + self
			if ( e3 & int(i) ) == 0 and ( e & int(i) ) != 0: result = result + negative_self
			i = i / 2
		return result

	def __rmul__( self, other ):
		return self * other

	def __str__( self ):
		if self == INFINITY: return "infinity"
		return "(%d,%d)" % ( self.__x, self.__y )

	def double( self ):
		if self == INFINITY:
			return INFINITY

		p = self.__curve.p()
		a = self.__curve.a()
		l = ( ( 3 * self.__x * self.__x + a ) * inverse_mod( 2 * self.__y, p ) ) % p
		x3 = ( l * l - 2 * self.__x ) % p
		y3 = ( l * ( self.__x - x3 ) - self.__y ) % p
		return Point( self.__curve, x3, y3 )

	def x( self ):
		return self.__x

	def y( self ):
		return self.__y

	def curve( self ):
		return self.__curve

	def order( self ):
		return self.__order

INFINITY = Point( None, None, None )

def inverse_mod( a, m ):
	if a < 0 or m <= a: a = a % m
	c, d = a, m
	uc, vc, ud, vd = 1, 0, 0, 1
	while c != 0:
		q, c, d = divmod( d, c ) + ( c, )
		uc, vc, ud, vd = ud - q*uc, vd - q*vc, uc, vc
	assert d == 1
	if ud > 0: return ud
	else: return ud + m
def generate_curve():
	p = 2**160 - 2**32 -  2**14 - 2**12 - 2**9 - 2**8 - 2**7 - 2**3 - 2**2 -1
	a = 1
	b = 7
	E = CurveFp(p, a, b)
	Gx = 1312070859336953328235792006245642608194004626015
	Gy = 183286360807308303108180027093052510417499316608

	G = Point(E, Gx, Gy)

	return E, G
def gen_curve(x, y):
	p = 2**160 - 2**32 -  2**14 - 2**12 - 2**9 - 2**8 - 2**7 - 2**3 - 2**2 -1
	a = 1
	b = 7
	E = CurveFp(p, a, b)

	G = Point(E, x, y)
	return E, G
