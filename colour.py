"""
colour
Bart Nagel <bart@tremby.net>
https://github.com/tremby/py-colour
licensed under the Gnu GPL version 3

Originally ported from Colour.php, a colour manipulation class for PHP by the 
same author, but now quite different.

Provides a Colour class and various supporting functions, plus the list of CSS3 
named colours.

Colours are internally stored as float RGB values. RGB values are the 
intensities of the red, green and blue channels.

RGB
---

Conceptually RGB colour space can be thought of as a cube along whose three axes 
the intensities of red, green and blue increase, respectively. The best way to 
think of the RGB colour cube is balancing on its point, so the black corner as 
at the bottom and the white corner is at the top. Shades of grey are then in a 
column up the middle. Colours get more intense as we move upwards through the 
cube.

The RGB color cube is not so useful for thinking about and transforming colours. 
For that we can more intuitively use other models.

HSV
---

The HSV model is best thought of as the RGB colour cube on its point but 
deformed so that the middle six corners (red, yellow, green, cyan, blue, 
magenta) are all in the same horizontal plane as the top corner (white). This 
makes a hexagonal cone. Just like the RGB cube, black is still at the point at 
the bottom, and shades of grey are still in a column in the centre. It's easiest 
to think of it then as stretched out sideways into a cylinder, where the whole 
bottom face is black and the top face has bright colours around the edge, all 
fading to white at a point in its centre.

All the primary and secondary colours, then, are on the circumference of the top 
face of the cylinder. The angle from the red primary, in the direction of 
yellow, is called the hue (the H in HSV) and is measured in degrees.

As we move inwards from the circumference of the cylinder towards the central 
vertical axis, colour is lost. The distance outwards from grey to the colour is 
called the saturation (the S in HSV) -- 0 at grey and 1 at the edge of the 
cylinder.

Moving upwards from the bottom face gives lighter colours, but since we could be 
at the top and not be at white (white is only in the centre of the top), the 
vertical axis can't very well be called "lightness". So the distance upwards is 
called the value (the V in HSV).

HSL
---

The HSL model is similar to HSV but instead of moving the primaries and 
secondaries up to the same horizontal plane as white, the primaries are moved up 
a little and the secondaries down a little so that they are all in a horizontal 
plane half way up the model. This results in a double hexagonal cone. Stretch 
this out into a cylinder again and we have the HSL model. The bottom face is 
still all black and now the top face is all white.

Hue is the same as in HSV, but obviously the primaries and secondaries are now 
in a plane halfway up the model rather than at the top.

Saturation is similar to in the HSV model -- it is still the distance from the 
central vertical axis to the colour -- but most colours will have different 
saturation values in the HSV and HSL models. The difference is particularly 
large for very light colours, since that is where the two models are most 
different.

The distance up the vertical axis running from black to white is then called 
lightness (the L in HSL), and now it is a fitting name since we will always end 
up with white if we increase it enough.

YIQ
---

The YIQ model is mostly used in broadcasting, particularly in the NTSC standard.

Its lightness metric is called luma and has the abbreviation Y. This is useful 
to have in broadcasting since it is all the information a black and white TV set 
needs. It is called luma rather than lightness since it measures the perceived 
lightness of the colour rather than an intensity based on the actual amounts of 
light. This is important since the eye perceives the same amount of light of 
different colours as different lightnesses -- for instance, we see #0f0 (the 
green primary) as being much brighter than #00f (the blue primary), though both 
have the same lightness according to the metrics of RGB (average intensity), HSV 
(value) and HSL (lightness). In the YIQ model, the green has a much higher luma 
than the blue.

Luma is calculated by weighting the red, green and blue channels by finely tuned 
coefficients and then summing.

Colour information, then (called chrominance), is in the other two channels, I 
and Q. (I and Q stand for "in-phase" and "quadrature", which have something to 
do with how they are modulated for broadcast transmission.) These are simply two 
axes of colour space. With luma at 0.5 the IQ plane would look like a plane 
halfway up the HSL cylinder (grey in the centre, colours towards the edges) but 
rotated somewhat and with all points appearing to be at the same lightness. (In 
the HSL plane some parts would look lighter than others, such as yellow looking 
brighter than blue).
"""

NAME = "py-colour"
DESCRIPTION = "Colour manipulation class"
AUTHOR = "Bart Nagel"
AUTHOR_EMAIL = "bart@tremby.net"
URL = "https://github.com/tremby/py-colour"
VERSION = "1.1.0"
LICENSE = "GNU GPLv3"
COPYRIGHT_YEAR = "2011~2017"

import colorsys
import re
import hashlib
from six import string_types

class Colour:
	"""
	Colours can be made from CSS3 named colours, hex strings, RGB values, HSV 
	values, HSL values, YIQ values, lightness (for shades of grey), arbitrary 
	bits of data (through hashing their string representations) or copied from 
	other Colour objects.

	They can be manipulated in various ways -- setting or shifting luma, hue, 
	value, saturation and so on, or mixing with other colours.

	Colours can be output as hex strings, 3-tuples of RGB, HSV, HSL or YIQ 
	values and HTML colour swatches.

	Very basic examples:
		# Import the library
		from colour import Colour

		# Print a hex representation of a CSS3 named colour
		print(Colour("red"))

		# To produce modified versions of a base colour (in this case shifted in 
		# lightness towards black or white) we can make a start Colour object
		green = Colour("#006310")

		# ...then make modified copies by putting the start colour through the 
		# constructor and then calling one of its colour modification methods
		darkgreen = Colour(green).shiftluma(-0.5)
		lightgreen = Colour(green).shiftluma(0.5)

		# If we hadn't used the constructor to make copies the original Colour 
		# object would have been modified.

		# Instead of shifting by a proprtion we can produce shades of a colour 
		# on an absolute scale
		verydarkgreen = Colour(green).luma(0.1)
		verylightgreen = Colour(green).luma(0.9)

		# Produce a rainbow by repeatedly shifting the hue of a Colour object
		c = Colour(hsv=(0, 0.8, 0.6))
		for x in range(12):
			print(c.shifthue(30))

		# A similar rainbow with uniform brightness (with copies of the Colour 
		# object rather than by modifying the original)
		c = Colour(hsv=(0, 0.8, 0.6))
		for x in range(12):
			print(Colour(c).shifthue(x * 30, perceptual=True))

		# An almost-grey version of our green from earlier
		almostgrey = Colour(green).saturation_hsv(0.2)

		# Another almost-grey version, but this time with a perceptually similar 
		# level of lightness
		almostgrey2 = Colour(green).saturation_hsv(0.2, perceptual=True)

		# Make a set of colours to colour-code some usernames
		usernames = ["tremby", "yappy", "mon", "bill"]
		for username in usernames:
			print("<li style=\"color: %s\">%s</li>" \\
					% (Colour(hash=username), username))

		# The same list of usernames but only allowing reds and oranges
		for username in usernames:
			print("<li style=\"color: %s\">%s</li>" \\
					% (Colour().hash(username, minh=0, maxh=30), username))

	To test the class and see lots more examples you can use the test.py script 
	(distributed with this module) which outputs HTML, then view the result in 
	your browser:
		python test.py >/tmp/colour.html
		x-www-browser /tmp/colour.html
	"""

	__colour = (0.0, 0.0, 0.0)

	def __init__(self, arg=None,
			grey=None,
			rgb=None, rgb100=None, rgb255=None,
			hsv=None, hsv100=None, hsv255=None,
			hsl=None, hsl100=None, hsl255=None,
			yiq=None,
			hex=None, css3=None, hash=None,
			colour=None):
		"""
		Constructor

		This can be called without any arguments, in which case the colour is 
		set to black.

		If the first argument is used its type and value are used to choose the 
		action to take. It can be
			a float or integer in the range 0~1
				act as if the grey argument was used
			a 3-tuple
				act as if the rgb argument was used
			a valid hex RGB string
				act as if the hex argument was used
			a string corresponding with a CSS3 named colour
				act as if the css3 argument was used
			a Colour object
				act as if the colour argument was used

		Otherwise exactly one of the other arguments must be used.
			grey=i
				Set the colour to a grey of this intensity (in the range 0~1).
			rgb=(r, g, b), rgb100=(r, g, b), rgb255=(r, g, b)
				Set colour to these RGB values (in the range 0~1, 0~100 or 0~255 
				depending on the argument used).
			hsv=(h, s, v), hsv100=(h, s, v), hsv255=(h, s, v)
			hsl=(h, s, l), hsl100=(h, s, l), hsl255=(h, s, l)
				Set the colour to these HSV or HSL values (h in degrees, s and v 
				in the range 0~1, 0~100 or 0~255 depending on the argument 
				used).
			yiq=(y, i, q)
				Set the colour to these YIQ values (y in the range 0~1, i and q 
				in the range -1~1).
			hex=string
				Set colour to this hex representation of an RGB colour. See the 
				hex() method for what is accepted.
			css3=string
				Set colour to the CSS3 named colour of this name.
			hash=something
				Convert whatever was passed to a string, hash it and make a 
				colour from the result.
			colour=colour_object
				Set colour to match the given Colour object
		"""

		# ensure there is at maximum one non-None argument
		if sum((arg is not None,
				grey is not None,
				rgb is not None, rgb100 is not None, rgb255 is not None,
				hsv is not None, hsv100 is not None, hsv255 is not None,
				hsl is not None, hsl100 is not None, hsl255 is not None,
				yiq is not None,
				hex is not None, css3 is not None, hash is not None,
				colour is not None,
				)) > 1:
			raise ValueError("expected at most one non-None argument")

		if arg is not None:
			# determine what is meant by looking at the type and value
			try:
				if arg >= 0 and arg <= 1:
					self.grey(arg)
					return
			except TypeError:
				pass
			if _is_sequence(arg) and len(arg) == 3:
				self.rgb(arg)
				return
			if _validhex(arg):
				self.hex(arg)
				return
			if isinstance(arg, string_types):
				self.css3(arg)
				return
			if isinstance(arg, self.__class__):
				self.rgb(arg.rgb())
				return
			raise ValueError("unrecognized constructor option")

		if grey is not None:
			self.grey(grey)

		elif rgb is not None:
			self.rgb(rgb)
		elif rgb100 is not None:
			self.rgb100(rgb100)
		elif rgb255 is not None:
			self.rgb255(rgb255)

		elif hsv is not None:
			self.hsv(hsv)
		elif hsv100 is not None:
			self.hsv100(hsv100)
		elif hsv255 is not None:
			self.hsv255(hsv255)

		elif hsl is not None:
			self.hsl(hsl)
		elif hsl100 is not None:
			self.hsl100(hsl100)
		elif hsl255 is not None:
			self.hsl255(hsl255)

		elif yiq is not None:
			self.yiq(yiq)

		elif hex is not None:
			self.hex(hex)
		elif css3 is not None:
			self.css3(css3)
		elif hash is not None:
			self.hash(hash)

		elif colour is not None:
			self.rgb(colour.rgb())

		else:
			# no argument was given -- default to black
			self.grey(0)

	# base methods for the various colour models
	# --------------------------------------------------------------------------

	def rgb(self, rgb=None, min=0.0, max=1.0):
		"""
		Get or set the colour as a 3-tuple of RGB values in a particular range

		Called with no rgb argument, return the object's colour.
		If both min and max are integer types rather than floats, values are 
		rounded to the nearest integer.

		Called with a 3-tuple, the colour is set to the given colour.
		Any missing channels (that is, where None is given rather than a number) 
		are not changed.
		"""

		if rgb is None:
			if min == 0.0 and max == 1.0:
				return self.__colour
			values = (min + i * (max - min) for i in self.__colour)
			if not isinstance(min, float) \
					and not isinstance(max, float):
				# round to integers
				return tuple(map(int, map(round, values)))
			return tuple(values)

		if len(rgb) != 3:
			raise ValueError("expected a 3-tuple")
		for i in rgb:
			if i is not None and (i < min or i > max):
				raise ValueError("expected values in the range %s~%s" % (min, max))

		if min == 0.0 and max == 1.0:
			newrgb = tuple(rgb[i] \
					if rgb[i] is not None else self.__colour[i] \
					for i in range(3))
		else:
			newrgb = tuple(float(rgb[i] - min) / float(max - min) \
					if rgb[i] is not None else self.__colour[i] \
					for i in range(3))

		self.__colour = newrgb
		return self
	def rgb100(self, *args, **kwargs):
		"""Same as rgb() with min set to 0 and max to 100"""
		return self.rgb(min=0, max=100, *args, **kwargs)
	def rgb255(self, *args, **kwargs):
		"""Same as rgb() with min set to 0 and max to 255"""
		return self.rgb(min=0, max=255, *args, **kwargs)

	def __hsx(self, hsl, hsx=None, perceptual=False,
			hmin=0.0, hmax=360.0, sxmin=0.0, sxmax=1.0):
		"""
		Internal method, logic behind hsv() and hsl()
		"""
		if hsx is None:
			h, s, x = rgbtohsl(self.__colour) if hsl \
					else rgbtohsv(self.__colour)
			if hmin != 0.0 or hmax != 360.0:
				h = hmin + (h / 360.0) * (hmax - hmin)
			if not isinstance(hmin, float) \
					and not isinstance(hmax, float):
				# round to integer
				h = int(round(h))

			if sxmin != 0.0 or sxmax != 1.0:
				s = sxmin + s * (sxmax - sxmin)
				x = sxmin + x * (sxmax - sxmin)
			if not isinstance(sxmin, float) \
					and not isinstance(sxmax, float):
				s = int(round(s))
				x = int(round(x))
			return (h, s, x)

		if len(hsx) != 3:
			raise ValueError("expected a 3-tuple")
		h, s, x = hsx
		if h is not None:
			h = (h - hmin) % (hmax - hmin) + hmin
		for i in [s, x]:
			if i is not None and (i < sxmin or i > sxmax):
				raise ValueError(\
						"expected saturation and %s values in the range %s~%s" \
						% ("lightness" if hsl else "value", sxmin, sxmax))

		oldhsx = self.__hsx(hsl)

		if h is None:
			h = oldhsx[0]
		elif hmin != 0.0 or hmax != 360.0:
			h = float(h - hmin) / float(hmax - hmin)

		if s is None:
			s = oldhsx[1]
		elif sxmin != 0.0 or sxmax != 1.0:
			s = float(s - sxmin) / float(sxmax - sxmin)

		if x is None:
			x = oldhsx[2]
		elif sxmin != 0.0 or sxmax != 1.0:
			x = float(x - sxmin) / float(sxmax - sxmin)

		if perceptual:
			oldluma = self.luma()

		if hsl:
			self.rgb(hsltorgb((h, s, x)))
		else:
			self.rgb(hsvtorgb((h, s, x)))

		if perceptual:
			self.luma(oldluma)

		return self

	def hsv(self, hsv=None, perceptual=False,
			hmin=0.0, hmax=360.0, svmin=0.0, svmax=1.0):
		"""
		Get or set the colour as a 3-tuple of HSV values in a particular range

		Called with no hsv argument, return the object's colour.
		If both min and max are integer types rather than floats, values are 
		rounded to the nearest integer.

		Called with a 3-tuple, the colour is set to the given colour.
		Any missing channels (that is, where None is given rather than a number) 
		are not changed.
		Hues out of the range are accepted since hue is circular.
		If the perceptual argument is True attempt to preserve the colour's luma 
		in order to retain the colour's perceived brightness.
		"""
		return self.__hsx(False, hsx=hsv, perceptual=perceptual, \
				hmin=hmin, hmax=hmax, sxmin=svmin, sxmax=svmax)
	def hsv100(self, *args, **kwargs):
		"""Same as hsv() with hmin=0, hmax=360, svmin=0, svmax=100"""
		return self.hsv(hmin=0, hmax=360, svmin=0, svmax=100, *args, **kwargs)
	def hsv255(self, *args, **kwargs):
		"""Same as hsv() with hmin=0, hmax=360, svmin=0, svmax=255"""
		return self.hsv(hmin=0, hmax=360, svmin=0, svmax=255, *args, **kwargs)

	def hsl(self, hsl=None, perceptual=False,
			hmin=0.0, hmax=360.0, slmin=0.0, slmax=1.0):
		"""
		Get or set the colour as a 3-tuple of HSL values in a particular range

		Called with no hsl argument, return the object's colour.
		If both min and max are integer types rather than floats, values are 
		rounded to the nearest integer.

		Called with a 3-tuple, the colour is set to the given colour.
		Any missing channels (that is, where None is given rather than a number) 
		are not changed.
		Hues out of the range are accepted since hue is circular.
		If the perceptual argument is True attempt to preserve the colour's luma 
		in order to retain the colour's perceived brightness.
		"""
		return self.__hsx(True, hsx=hsl, perceptual=perceptual, \
				hmin=hmin, hmax=hmax, sxmin=slmin, sxmax=slmax)
	def hsl100(self, *args, **kwargs):
		"""Same as hsl() with hmin=0, hmax=360, slmin=0, slmax=100"""
		return self.hsl(hmin=0, hmax=360, slmin=0, slmax=100, *args, **kwargs)
	def hsl255(self, *args, **kwargs):
		"""Same as hsl() with hmin=0, hmax=360, slmin=0, slmax=255"""
		return self.hsl(hmin=0, hmax=360, slmin=0, slmax=255, *args, **kwargs)

	def yiq(self, yiq=None,
			ymin=0.0, ymax=1.0, iqmin=-1.0, iqmax=1.0):
		"""
		Get or set the colour as a 3-tuple of YIQ values in a particular range

		Called with no yiq argument, return the object's colour.
		If both min and max are integer types rather than floats, values are 
		rounded to the nearest integer.

		Called with a 3-tuple, the colour is set to the given colour.
		Any missing channels (that is, where None is given rather than a number) 
		are not changed.
		"""
		if yiq is None:
			y, i, q = rgbtoyiq(self.__colour)
			if ymin != 0.0 or ymax != 1.0:
				y = ymin + y * (ymax - ymin)
			if not isinstance(ymin, float) \
					and not isinstance(ymax, float):
				# round to integer
				y = int(round(y))

			if iqmin != -1.0 or iqmax != 1.0:
				i = iqmin + i * (iqmax - iqmin)
				q = iqmin + q * (iqmax - iqmin)
			if not isinstance(iqmin, float) \
					and not isinstance(iqmax, float):
				i = int(round(i))
				q = int(round(q))
			return (y, i, q)

		if len(yiq) != 3:
			raise ValueError("expected a 3-tuple")
		y, i, q = yiq
		if y is not None and (y < ymin or y > ymax):
			raise ValueError("expected a luma value in the range %s~%s" % (ymin, ymax))
		for x in [i, q]:
			if x is not None and (x < iqmin or x > iqmax):
				raise ValueError("expected in-phase and quadrature values" \
						+ " in the range %s~%s" % (iqmin, iqmax))

		oldyiq = self.yiq()

		if y is None:
			y = oldyiq[0]
		elif ymin != 0.0 or ymax != 1.0:
			y = float(y - ymin) / float(ymax - ymin)

		if i is None:
			i = oldyiq[1]
		elif iqmin != -1.0 or iqmax != 1.0:
			i = float(i - iqmin) / float(iqmax - iqmin)

		if q is None:
			q = oldyiq[2]
		elif iqmin != -1.0 or iqmax != 1.0:
			q = float(q - iqmin) / float(iqmax - iqmin)

		return self.rgb(yiqtorgb((y, i, q)))

	# set a colour without individual values for one of the colour models
	# --------------------------------------------------------------------------

	def hex(self, hex=None, hash=True, allowshort=False, forceshort=False):
		"""
		Get or set the colour as a hex RGB string, with or without a leading 
		hash

		Called with no hex argument, return a hex representation of the object's 
		colour.
		The hash argument controls whether or not a leading hash will be 
		present.
		The allowshort argument controls whether or not a short (3-digit) 
		version is used if it can losslessly be.
		The forceshort argument forces a short (3-digit) hex representation by 
		snapping to the closest available colour.

		Called with the hex argument, attempt to parse the string as a hex RGB 
		colour and set the colour to the result. Three or six digit strings are 
		accepted.
		"""
		if hex is None:
			return rgbtohex(self.rgb(), hash=hash, allowshort=allowshort, 
					forceshort=forceshort)

		return self.rgb(hextorgb(hex))

	def css3(self, name=None):
		"""
		Get or set the colour as a CSS3 named colour

		Called with no name argument, attempt to find a CSS3 named colour equal 
		to this colour and return its name if found.

		Called with a string, the colour is set to the CSS3 named colour 
		corresponding to the given string.
		"""
		if name is None:
			rgb255 = self.rgb255()
			for key in CSS3.keys():
				if rgb255 == Colour(css3=key).rgb255():
					return key
			return None

		try:
			return self.hex(CSS3[name.lower()])
		except KeyError:
			raise ValueError("no such CSS3 named colour")

	def grey(self, i=None, min=0.0, max=1.0):
		"""
		Set the colour to a shade of grey with the given intensity, or return 
		the current intensity if this colour is a shade of grey, in a particular 
		range

		Called with no i argument, return the intensity of this colour as long 
		as the colour is a shade of gray, otherwise return False.

		Called with a number, the colour is set to a shade of grey with the 
		given intensity.
		"""
		if i is None:
			if self.saturation_hsv() != 0:
				return False
			i = min + self.intensity() * (max - min)
			if not isinstance(min, float) \
					and not isinstance(max, float):
				# round to integer
				return int(round(i))
			return i

		if i < min or i > max:
			raise ValueError("expected value in the range %s~%s" % (min, max))
		if min != 0.0 or max != 0.0:
			i = (i - min) / (max - min)

		return self.rgb((i, i, i))

	def hash(self, tohash,
			minh=None, maxh=None, mins=0.2, maxs=1.0, miny=0.3, maxy=0.7):
		"""
		Make a colour to be associated with the given input

		The tohash argument is converted to a string and then put through the 
		MD5 algorithm. The resulting hash is then used to seed a hue, saturation 
		and luma.

		Pass minh and maxh values to constrain the hues (for instance -20 
		degrees to 140 degrees, which is not the same as 140 degrees to 340 
		degrees). Default is all hues.
		Pass mins and maxs values to constrain the saturation values. By default 
		only colours close to grey are disallowed.
		Pass miny and maxy to constrain the luma. By default anything difficult 
		to see against black or white is disallowed.
		"""
		hash = hashlib.md5(str(tohash).encode('utf-8')).hexdigest()

		if maxh is None or minh is None:
			maxh = 360
			minh = 0
		else:
			while minh <= -360:
				minh += 360
			while minh >= 360:
				minh -= 360
			while maxh <= -360:
				maxh += 360
			while maxh >= 360:
				maxh -= 360

		if mins < 0 or mins > 1 or maxs < 0 or maxs > 1 \
				or miny < 0 or miny > 1 or maxy < 0:
			raise ValueError(
					"expected mins, maxs, miny and maxy to be in the range 0~1")
		if mins > maxs:
			raise ValueError("expected mins to be less than or equal to maxs")
		if miny > maxy:
			raise ValueError("expected miny to be less than or equal to maxy")

		h = minh + (maxh - minh) * int(hash[0:8], 16) / float(16**8)
		s = mins + (maxs - mins) * int(hash[8:16], 16) / float(16**8)
		y = miny + (maxy - miny) * int(hash[16:24], 16) / float(16**8)

		return self.hsv((h, s, y)).luma(y)

	# hue
	# --------------------------------------------------------------------------

	def hue(self, h=None, perceptual=False):
		"""
		Get or set the hue in degrees

		Called with no h argument, return the colour's hue in degrees.

		Called with a number in degrees, set the colour's hue.
		If the perceptual argument is True attempt to preserve the colour's luma 
		in order to retain the colour's perceived brightness.
		"""
		if h is None:
			return self.hsv()[0]
		return self.hsv((h, None, None), perceptual=perceptual)

	def shifthue(self, angle, perceptual=False):
		"""
		Shift the hue of this colour relatively by a given number of degrees

		Return a new colour like this one but with its hue shifted by the given 
		number of degrees.
		If the perceptual argument is True attempt to preserve the colour's luma 
		in order to retain the colour's perceived brightness.
		"""
		if angle == 0:
			return self
		return self.hue(self.hue() + angle, perceptual=perceptual)

	# saturation of various kinds
	# --------------------------------------------------------------------------

	def __saturation_hsx(self, hsl, s=None, perceptual=False):
		"""
		Internal method, logic behind saturation_hsv() and saturation_hsl()
		"""
		if s is None:
			return self.hsl()[1] if hsl else self.hsv()[1]
		if s < 0 or s > 1:
			raise ValueError("expected a value in the range 0~1")
		if hsl:
			method = self.hsl
		else:
			method = self.hsv
		return method((None, s, None), perceptual=perceptual)

	def saturation_hsv(self, s=None, perceptual=False):
		"""
		Get or set the saturation in HSV space in the range 0~1

		Called with no s argument, return the colour's saturation in HSV space.

		Called with a number in the range 0~1, set the colour's saturation in 
		HSV space. The hue and value are not changed.
		If the perceptual argument is True attempt to preserve the colour's luma 
		in order to retain the colour's perceived brightness.
		"""
		return self.__saturation_hsx(False, s, perceptual=perceptual)

	def saturation_hsl(self, s=None, perceptual=False):
		"""
		Get or set the saturation in HSL space in the range 0~1

		Called with no s argument, return the colour's saturation in HSL space.

		Called with a number in the range 0~1, set the colour's saturation in 
		HSL space. The hue and value are not changed.
		If the perceptual argument is True attempt to preserve the colour's luma 
		in order to retain the colour's perceived brightness.
		"""
		return self.__saturation_hsx(True, s, perceptual=perceptual)

	def __shiftsaturation_hsx(self, hsl, scale, perceptual=False):
		"""
		Internal method, logic behind shiftsaturation_hsv() and 
		shiftsaturation_hsl()
		"""
		if scale == 0:
			return self

		if scale < -1 or scale > 1:
			return ValueError("expected a value in the range -1~1")

		s = self.saturation_hsl() if hsl else self.saturation_hsv()
		if scale > 0:
			s += (1 - s) * scale
		else:
			s *= (scale + 1)
		return self.__hsx(hsl, (None, s, None), perceptual=perceptual)

	def shiftsaturation_hsv(self, scale, perceptual=False):
		"""
		Shift the saturation of this colour relatively in HSV space

		Called with a float argument in the range -1~1, return a new colour like 
		this one but shifted by the given proportion along the saturation axis 
		of HSV space.
		Passing 1 would saturate the colour completely, passing -1 would 
		desatuarate the colour completely.
		If the perceptual argument is True attempt to preserve the colour's luma 
		in order to retain the colour's perceived brightness.
		"""
		return self.__shiftsaturation_hsx(False, scale, perceptual=perceptual)

	def shiftsaturation_hsl(self, scale, perceptual=False):
		"""
		Shift the saturation of this colour relatively in HSL space

		Called with a float argument in the range -1~1, return a new colour like 
		this one but shifted by the given proportion along the saturation axis 
		of HSL space.
		Passing 1 would saturate the colour completely, passing -1 would 
		desatuarate the colour completely.
		If the perceptual argument is True attempt to preserve the colour's luma 
		in order to retain the colour's perceived brightness.
		"""
		return self.__shiftsaturation_hsx(True, scale, perceptual=perceptual)

	# lightness of various kinds
	# --------------------------------------------------------------------------

	def intensity(self, i=None):
		"""
		Get or set the colour's intensity as a float in the range 0~1
		
		The intensity of a colour is the average of its red, green and blue 
		components. So the scale of intensity for this colour ranges from black 
		with intensity 0, in a straight line in the RGB cube to this colour, 
		then in another straight line in the RGB cube towards white.

		Called with no i argument, return the colour's intensity.

		Called with a number, set the colour's intensity to the given value.
		"""
		if i is None:
			return sum(self.rgb()) / 3.0

		if i < 0 or i > 1:
			raise ValueError("expected value in the range 0~1")

		if i == 0 or i == 1:
			return self.grey(i, False)

		if i == self.intensity():
			return self

		diff = i - self.intensity()
		if diff > 0:
			scale = diff / (1 - self.intensity())
		else:
			scale = diff / self.intensity()

		return self.shiftintensity(scale)

	def shiftintensity(self, scale):
		"""
		Shift the intensity of this colour relatively towards black or white

		See intensity() for what exactly "intensity" means.

		Called with a float argument in the range -1~1, shift the colour towards 
		black (-1 <= scale < 0) or white (0 < scale <= 1) linearly in the RGB 
		cube.
		"""
		if scale == 0:
			return self

		if scale < -1 or scale > 1:
			return ValueError("expected a value in the range -1~1")

		if scale > 0:
			return self.mix(1, scale)
		return self.mix(0, -scale)

	def __value_lightness(self, hsl, x=None):
		"""
		Internal method, logic behind value() and lightness()
		"""
		if x is None:
			return self.hsl()[2] if hsl else self.hsv()[2]
		if x < 0 or x > 1:
			raise ValueError("expected a value in the range 0~1")
		if hsl:
			return self.hsl((None, None, x))
		return self.hsv((None, None, x))

	def value(self, v=None):
		"""
		Get or set the value in HSV space in the range 0~1

		Called with no v argument, return the colour's value in HSV space.

		Called with a number in the range 0~1, set the colour's value in HSV 
		space. The hue and saturation are not changed.
		"""
		return self.__value_lightness(False, v)

	def lightness(self, l=None):
		"""
		Get or set the lightness in HSL space in the range 0~1

		Called with no v argument, return the colour's lightness in HSL space.

		Called with a number in the range 0~1, set the colour's lightness in HSV 
		space. The hue and saturation are not changed.
		"""
		return self.__value_lightness(True, l)

	def __shiftvalue_lightness(self, hsl, scale):
		"""
		Internal method, logic behind shiftvalue() and shiftlightness()
		"""
		if scale == 0:
			return self

		if scale < -1 or scale > 1:
			return ValueError("expected a value in the range -1~1")

		x = self.lightness() if hsl else self.value()
		if scale > 0:
			x += (1 - x) * scale
		else:
			x *= scale + 1
		return self.__value_lightness(hsl, x)

	def shiftvalue(self, scale):
		"""
		Shift the value of this colour relatively

		Called with a float argument in the range -1~1, return a new colour like 
		this one but shifted by the given proportion along the value axis of HSV 
		space.
		Passing 1 would maximise value (but unless the colour is fully saturated 
		it will not reach white), passing 0 would cause no change and passing -1 
		would result in black.
		"""
		return self.__shiftvalue_lightness(False, scale)

	def shiftlightness(self, scale):
		"""
		Shift the lightness of this colour relatively

		Called with a float argument in the range -1~1, return a new colour like 
		this one but shifted by the given proportion along the lightness axis of 
		HSL space.
		Passing 1 would result in white, passing 0 would cause no change and 
		passing -1 would result in black.
		"""
		return self.__shiftvalue_lightness(True, scale)

	def luma(self, y=None):
		"""
		Get or set the luma of the colour in the range 0~1

		Called with no y argument, return the colour's luma.

		Called with a number in the range 0~1, set the colour's luma as close to 
		the given value as possible while keeping its colour intact.
		"""
		if y is None:
			return self.yiq()[0]
		if y < 0 or y > 1:
			raise ValueError("expected a value in the range 0~1")
		return self.yiq((y, None, None))

	def shiftluma(self, scale):
		"""
		Shift the luma of this colour relatively

		Called with a float argument in the range -1~1, return a new colour like 
		this one but brightened or darkened by the given proportion in luma.
		Passing 1 would result in the brightest possible colour for this colour, 
		passing 0 would cause no change and passing -1 would result in the 
		darkest.
		"""
		if scale == 0:
			return self

		if scale < -1 or scale > 1:
			return ValueError("expected a value in the range -1~1")

		y = self.luma()
		if scale > 0:
			y += (1 - y) * scale
		else:
			y *= scale + 1
		return self.luma(y)

	# mix colours
	# --------------------------------------------------------------------------

	def mix(self, colour, proportion):
		"""
		Mix this colour with another

		The colour argument is usually another Colour object. If it is not, it 
		is passed to the constructor to attempt to produce a new colour.
		The proportion argument is a float in the range 0~1 controlling how far 
		towards the given colour to move, so 0 is no change and 1 is a complete 
		change.
		"""
		rgb = self.rgb()
		if not isinstance(colour, self.__class__):
			colour = self.__class__(colour)
		colour = colour.rgb()
		if proportion < 0 or proportion > 1:
			return ValueError("expected a value in the range 0~1")
		return self.rgb(tuple(rgb[x] + (colour[x] - rgb[x]) * proportion \
				for x in range(3)))

	# miscellaneous output
	# --------------------------------------------------------------------------

	def __str__(self):
		"""
		Return a string representation of the object

		The hex() method is called, returning a hex RGB string with a leading 
		hash.
		"""
		return self.hex()

	def swatch(self, showhex=True, cssclass=None):
		"""
		Return an HTML colour swatch string

		Mainly useful for debugging, this returns an HTML snippet which shows a 
		small area of the colour and optionally the hex representation of the 
		colour.
		The returned element has a CSS class of "swatch" and additionally the 
		cssclass argument if given. If the cssclass argument was not given the 
		element also carries styles to set its font family and some padding.
		"""
		html = "<span class=\"swatch"
		if cssclass is not None:
			html += " %s" % cssclass
		html += "\" style=\""
		if cssclass is None:
			html += "font-family: monospace; padding: 0.3em 0.8em; "
		textcolour = "black" if self.luma() > 0.5 else "white"
		html += "background-color: %s; color: %s\">" % (self.hex(), textcolour)
		html += self.hex() if showhex else "&nbsp;" * 7
		html += "</span>"
		return html

# static colour conversion functions
# ------------------------------------------------------------------------------

def _rgbtohsx(hsl, rgb):
	"""Internal function, logic behind rgbtohsv() and rgbtohsl()"""
	if len(rgb) != 3:
		raise ValueError("expected a 3-tuple")
	for i in rgb:
		if i < 0 or i > 1:
			raise ValueError("expected values in the range 0~1")
	if hsl:
		hls = colorsys.rgb_to_hls(*rgb)
		return (hls[0] * 360, hls[2], hls[1])
	hsv = colorsys.rgb_to_hsv(*rgb)
	return (hsv[0] * 360, hsv[1], hsv[2])

def rgbtohsv(rgb):
	"""
	Convert the given colour in RGB space to HSV space

	Argument is a 3-tuple of float RGB values in the range 0~1.
	Return a 3-tuple of float HSV values in the range (0~360, 0~1, 0~1).
	"""
	return _rgbtohsx(False, rgb)

def rgbtohsl(rgb):
	"""
	Convert the given colour in RGB space to HSL space

	Argument is a 3-tuple of float RGB values in the range 0~1.
	Return a 3-tuple of float HSV values in the range (0~360, 0~1, 0~1).
	"""
	return _rgbtohsx(True, rgb)

def rgbtoyiq(rgb):
	"""
	Convert the given colour in RGB space to YIQ space

	Argument is a 3-tuple of float RGB values in the range 0~1.
	Return a 3-tuple of float YIQ values in the range (0~1, -1~1, -1~1).
	"""
	if len(rgb) != 3:
		raise ValueError("expected a 3-tuple")
	for i in rgb:
		if i < 0 or i > 1:
			raise ValueError("expected values in the range 0~1")
	return colorsys.rgb_to_yiq(*rgb)

def _hsxtorgb(hsl, hsx):
	"""Internal function, logic behind hsvtorgb() and hsltorgb()"""
	if len(hsx) != 3:
		raise ValueError("expected a 3-tuple")
	h, s, x = hsx
	h = h % 360
	for i in [s, x]:
		if i < 0 or i > 1:
			raise ValueError("expected saturation and value to be in the range 0~1")
	if hsl:
		return colorsys.hls_to_rgb(h / 360.0, x, s)
	return colorsys.hsv_to_rgb(h / 360.0, s, x)

def hsvtorgb(hsv):
	"""
	Convert the given colour in HSV space to RGB space

	Argument is a 3-tuple of float HSV values in the range (0~360, 0~1, 0~1), 
	though hues out of the range 0~360 are accepted.
	Return a 3-tuple of float RGB values in the range 0~1.
	"""
	return _hsxtorgb(False, hsv)

def hsltorgb(hsl):
	"""
	Convert the given colour in HSL space to RGB space

	Argument is a 3-tuple of float HSL values in the range (0~360, 0~1, 0~1), 
	though hues out of the range 0~360 are accepted.
	Return a 3-tuple of float RGB values in the range 0~1.
	"""
	return _hsxtorgb(True, hsl)

def yiqtorgb(yiq):
	"""
	Convert the given colour in YIQ space to RGB space

	Argument is a 3-tuple of float YIQ values in the range (0~1, -1~1, -1~1).
	Return a 3-tuple of float RGB values in the range 0~1.
	"""
	if len(yiq) != 3:
		raise ValueError("expected a 3-tuple")
	if yiq[0] < 0 or yiq[0] > 1:
		raise ValueError("expected luma value in the range 0~1")
	for i in yiq[1:]:
		if i < -1 or i > 1:
			raise ValueError("expected chrominance values in the range 0~1")
	return colorsys.yiq_to_rgb(*yiq)

def hextorgb(hex):
	"""
	Parse the given colour represented by a hex RGB string to RGB values

	Argument is a string of any of the following forms:
		#xxx
		#xxxxxx
		xxx
		xxxxxx
	Where x is a case-insensitive hexadecimal digit.
	Return a 3-tuple of float RGB values in the range 0~1.
	"""
	if not _validhex(hex):
		raise ValueError("invalid hex string")
	if hex[0] == "#":
		hex = hex[1:]
	if len(hex) == 3:
		hex = hex[0] * 2 + hex[1] * 2 + hex[2] * 2
	return tuple(int(hex[x * 2:(x + 1) * 2], 16) / 255.0 for x in range(3))

def rgbtohex(rgb, hash=True, allowshort=False, forceshort=False):
	"""
	Encode the given colour in RGB form to its hexadecimal representation

	Argument is a 3-tuple of float RGB values in the range 0~1.
	Return a string of the form #xxxxxx, where x is a lowercase hexadecimal 
	digit, two digits per channel.
	Pass False as the hash argument to omit the leading hash.
	The allowshort argument controls whether or not a short (3-digit) version is 
	used if it can losslessly be.
	The forceshort argument forces a short (3-digit) hex representation by 
	snapping to the closest available colour.
	"""
	h = "#" if hash else ""
	if forceshort:
		rgb = tuple(int(round(x * 15)) for x in rgb)
		return h + "%s%s%s" % tuple(hex(rgb[x])[2:] for x in range(3))
	rgb = tuple(int(round(x * 255)) for x in rgb)
	if allowshort and sum(x % 17 for x in rgb) == 0:
		return h + "%s%s%s" % tuple(hex(int(rgb[x] / 17))[2:] for x in range(3))

	return h + "%s%s%s" % tuple(hex(rgb[x])[2:].rjust(2, "0") for x in range(3))

# input checking
# ------------------------------------------------------------------------------

def _validhex(string):
	"""
	Return True if the given string is a valid hexadecimal representation of an 
	RGB colour

	Accepts strings of three or six case-insensitive hexadecimal digits, with or 
	without a leading hash.
	"""
	if not isinstance(string, string_types):
		return False
	return re.match("^#?([0-9a-f]{3}){1,2}$", string, re.I) is not None

def _is_numeric(f):
	"""Return True if the argument is of a numeric type"""
	return isinstance(f, int, long, float, complex)

def _is_sequence(arg):
	"""Return True if the argument is a sequence (but not a string)"""
	return not hasattr(arg, 'strip') and \
			(hasattr(arg, '__getitem__') or hasattr(arg, '__iter__'))

# CSS3 colours (from <http://www.w3.org/TR/css3-color/#svg-color>)
# ------------------------------------------------------------------------------
CSS3 = {
		"aliceblue":			"f0f8ff",
		"antiquewhite":			"faebd7",
		"aqua":					"00ffff",
		"aquamarine":			"7fffd4",
		"azure":				"f0ffff",
		"beige":				"f5f5dc",
		"bisque":				"ffe4c4",
		"black":				"000000",
		"blanchedalmond":		"ffebcd",
		"blue":					"0000ff",
		"blueviolet":			"8a2be2",
		"brown":				"a52a2a",
		"burlywood":			"deb887",
		"cadetblue":			"5f9ea0",
		"chartreuse":			"7fff00",
		"chocolate":			"d2691e",
		"coral":				"ff7f50",
		"cornflowerblue":		"6495ed",
		"cornsilk":				"fff8dc",
		"crimson":				"dc143c",
		"cyan":					"00ffff",
		"darkblue":				"00008b",
		"darkcyan":				"008b8b",
		"darkgoldenrod":		"b8860b",
		"darkgray":				"a9a9a9",
		"darkgreen":			"006400",
		"darkgrey":				"a9a9a9",
		"darkkhaki":			"bdb76b",
		"darkmagenta":			"8b008b",
		"darkolivegreen":		"556b2f",
		"darkorange":			"ff8c00",
		"darkorchid":			"9932cc",
		"darkred":				"8b0000",
		"darksalmon":			"e9967a",
		"darkseagreen":			"8fbc8f",
		"darkslateblue":		"483d8b",
		"darkslategray":		"2f4f4f",
		"darkslategrey":		"2f4f4f",
		"darkturquoise":		"00ced1",
		"darkviolet":			"9400d3",
		"deeppink":				"ff1493",
		"deepskyblue":			"00bfff",
		"dimgray":				"696969",
		"dimgrey":				"696969",
		"dodgerblue":			"1e90ff",
		"firebrick":			"b22222",
		"floralwhite":			"fffaf0",
		"forestgreen":			"228b22",
		"fuchsia":				"ff00ff",
		"gainsboro":			"dcdcdc",
		"ghostwhite":			"f8f8ff",
		"gold":					"ffd700",
		"goldenrod":			"daa520",
		"gray":					"808080",
		"green":				"008000",
		"greenyellow":			"adff2f",
		"grey":					"808080",
		"honeydew":				"f0fff0",
		"hotpink":				"ff69b4",
		"indianred":			"cd5c5c",
		"indigo":				"4b0082",
		"ivory":				"fffff0",
		"khaki":				"f0e68c",
		"lavender":				"e6e6fa",
		"lavenderblush":		"fff0f5",
		"lawngreen":			"7cfc00",
		"lemonchiffon":			"fffacd",
		"lightblue":			"add8e6",
		"lightcoral":			"f08080",
		"lightcyan":			"e0ffff",
		"lightgoldenrodyellow":	"fafad2",
		"lightgray":			"d3d3d3",
		"lightgreen":			"90ee90",
		"lightgrey":			"d3d3d3",
		"lightpink":			"ffb6c1",
		"lightsalmon":			"ffa07a",
		"lightseagreen":		"20b2aa",
		"lightskyblue":			"87cefa",
		"lightslategray":		"778899",
		"lightslategrey":		"778899",
		"lightsteelblue":		"b0c4de",
		"lightyellow":			"ffffe0",
		"lime":					"00ff00",
		"limegreen":			"32cd32",
		"linen":				"faf0e6",
		"magenta":				"ff00ff",
		"maroon":				"800000",
		"mediumaquamarine":		"66cdaa",
		"mediumblue":			"0000cd",
		"mediumorchid":			"ba55d3",
		"mediumpurple":			"9370db",
		"mediumseagreen":		"3cb371",
		"mediumslateblue":		"7b68ee",
		"mediumspringgreen":	"00fa9a",
		"mediumturquoise":		"48d1cc",
		"mediumvioletred":		"c71585",
		"midnightblue":			"191970",
		"mintcream":			"f5fffa",
		"mistyrose":			"ffe4e1",
		"moccasin":				"ffe4b5",
		"navajowhite":			"ffdead",
		"navy":					"000080",
		"oldlace":				"fdf5e6",
		"olive":				"808000",
		"olivedrab":			"6b8e23",
		"orange":				"ffa500",
		"orangered":			"ff4500",
		"orchid":				"da70d6",
		"palegoldenrod":		"eee8aa",
		"palegreen":			"98fb98",
		"paleturquoise":		"afeeee",
		"palevioletred":		"db7093",
		"papayawhip":			"ffefd5",
		"peachpuff":			"ffdab9",
		"peru":					"cd853f",
		"pink":					"ffc0cb",
		"plum":					"dda0dd",
		"powderblue":			"b0e0e6",
		"purple":				"800080",
		"red":					"ff0000",
		"rosybrown":			"bc8f8f",
		"royalblue":			"4169e1",
		"saddlebrown":			"8b4513",
		"salmon":				"fa8072",
		"sandybrown":			"f4a460",
		"seagreen":				"2e8b57",
		"seashell":				"fff5ee",
		"sienna":				"a0522d",
		"silver":				"c0c0c0",
		"skyblue":				"87ceeb",
		"slateblue":			"6a5acd",
		"slategray":			"708090",
		"slategrey":			"708090",
		"snow":					"fffafa",
		"springgreen":			"00ff7f",
		"steelblue":			"4682b4",
		"tan":					"d2b48c",
		"teal":					"008080",
		"thistle":				"d8bfd8",
		"tomato":				"ff6347",
		"turquoise":			"40e0d0",
		"violet":				"ee82ee",
		"wheat":				"f5deb3",
		"white":				"ffffff",
		"whitesmoke":			"f5f5f5",
		"yellow":				"ffff00",
		"yellowgreen":			"9acd32",
		}
