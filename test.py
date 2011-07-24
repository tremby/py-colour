from colour import Colour
import colour
import cgi
import sys

def head(title, level=2):
	print "<h%s>%s</h%s>\n" % (level, title, level)

def test(code, name=None):
	if name is not None:
		print "%s: " % name
	print "<code>%s</code> " % cgi.escape(code)
	print eval(code)
	print "<br>"

def main():
	print """<html><head>
		<style type="text/css">
			.blobset {
				display: inline-block;
				margin: 4px;
			}
			.blob {
				display: inline-block;
				height: 12px;
				width: 12px;
			}
			.reallybig {
				font-size: 200%;
				font-weight: bold;
				font-family: "Impact", sans-serif;
			}
		</style></head><body>"""
	head("Colour class test", level=1)
	print "Colour version %s<br>" % colour.VERSION

	head("constructor")

	head("empty", 3)
	test('Colour().swatch()')

	head("shade of grey", 3)
	for x in range(11):
		test("Colour(%f).swatch()" % (x / 10.0))

	head("RGB values", 3)
	for x in ["(0.2, 0.8, 0.7)", "(0.0, 0.1, 1.0)", "(1.0, 0.2, 0.9)"]:
		test("Colour(%s).swatch()" % x)

	head("hex RGB string", 3)
	for x in ["12f", "ffCF00", "#399", "#012345"]:
		test("Colour(\"%s\").swatch()" % x)

	head("named CSS3 colour", 3)
	for x in ["goldenrod", "slateblue", "SPRINGGREEN", "darkorchid"]:
		test("Colour(\"%s\").swatch()" % x)

	head("existing Colour object", 3)
	for x in ["goldenrod", "midnightblue", "c09"]:
		test("Colour(Colour(\"%s\")).swatch()" % x)

	head("rgb methods")

	head("rgb", 3)
	test("Colour().rgb((0, 0.2, 1)).swatch()")
	test("Colour().rgb((1, 0.8, 0.4221)).swatch()")
	test("Colour((1, 1, 0.5)).rgb((1, None, 0)).swatch()")
	test("Colour().rgb((255, 23, 0), max=255).swatch()")
	test("Colour().rgb((30, 77, 100), max=100).swatch()")
	test("Colour().rgb((4, 6.9, 3.5), min=3.5, max=7.0).swatch()")
	test("Colour(\"goldenrod\").rgb()")
	test("Colour(\"goldenrod\").rgb(min=10, max=30)")
	test("Colour(\"goldenrod\").rgb(min=10.0, max=30.0)")

	head("rgb255", 3)
	test("Colour().rgb255((0, 55, 199)).swatch()")
	test("Colour().rgb255((255, 0, 0)).swatch()")
	test("Colour(\"goldenrod\").rgb255((None, 255, None)).swatch()")
	test("Colour(\"goldenrod\").rgb255()")

	head("rgb100", 3)
	test("Colour().rgb100((0, 55, 88)).swatch()")
	test("Colour().rgb100((100, 0, 0)).swatch()")
	test("Colour(\"goldenrod\").rgb100((None, 100, None)).swatch()")
	test("Colour(\"goldenrod\").rgb100()")

	head("hsv/hsl methods")

	head("hsv", 3)
	test("Colour().hsv((0, 0.2, 1)).swatch()")
	test("Colour().hsv((300, 0.8, 0.4221)).swatch()")
	test("Colour((1, 1, 0.5)).hsv((0, None, 0.5)).swatch()")
	test("Colour().hsv((250, 88, 200), svmax=255).swatch()")
	test("Colour().hsv((180, 77, 40), svmax=100).swatch()")
	test("Colour().hsv((0.9, 0.5, 0.5), hmin=0.0, hmax=1.0).swatch()")
	test("Colour(\"blue\").hsv((30, None, None)).swatch()")
	test("Colour(\"blue\").hsv((30, None, None), perceptual=True).swatch()")
	test("Colour(\"goldenrod\").hsv()")
	test("Colour(\"goldenrod\").hsv(hmin=10, hmax=30, svmin=0, svmax=50)")
	test("Colour(\"goldenrod\").hsv(hmin=10.0, hmax=30.0, svmin=0.0, svmax=50.0)")

	head("hsl", 3)
	test("Colour().hsl((0, 0.2, 1)).swatch()")
	test("Colour().hsl((300, 0.8, 0.4221)).swatch()")
	test("Colour((1, 1, 0.5)).hsl((0, None, 0.5)).swatch()")
	test("Colour().hsl((250, 88, 200), slmax=255).swatch()")
	test("Colour().hsl((180, 77, 40), slmax=100).swatch()")
	test("Colour().hsl((0.9, 0.5, 0.5), hmin=0.0, hmax=1.0).swatch()")
	test("Colour(\"blue\").hsl((30, None, None)).swatch()")
	test("Colour(\"blue\").hsl((30, None, None), perceptual=True).swatch()")
	test("Colour(\"goldenrod\").hsl()")
	test("Colour(\"goldenrod\").hsl(hmin=10, hmax=30, slmin=0, slmax=50)")
	test("Colour(\"goldenrod\").hsl(hmin=10.0, hmax=30.0, slmin=0.0, slmax=50.0)")

	head("hs[vl]255", 3)
	test("Colour().hsv255((90, 45, 255)).swatch()")
	test("Colour().hsl255((90, 45, 255)).swatch()")
	test("Colour().hsv255((270, 255, 180)).swatch()")
	test("Colour().hsl255((270, 255, 180)).swatch()")
	test("Colour(\"goldenrod\").hsv255()")
	test("Colour(\"goldenrod\").hsl255()")

	head("hs[vl]100", 3)
	test("Colour().hsv100((90, 45, 100)).swatch()")
	test("Colour().hsl100((90, 45, 100)).swatch()")
	test("Colour().hsv100((270, 100, 44)).swatch()")
	test("Colour().hsl100((270, 100, 44)).swatch()")
	test("Colour(\"goldenrod\").hsv100()")
	test("Colour(\"goldenrod\").hsl100()")

	head("yiq")

	test("Colour().yiq((0.5, -0.2, 1)).swatch()")
	test("Colour().yiq((1, 0.8, -0.4221)).swatch()")
	test("Colour((1, 1, 0.5)).yiq((0, None, 0.5)).swatch()")
	test("Colour().yiq((0.75, -185, -20), iqmin=-255, iqmax=255).swatch()")
	test("Colour().yiq((0.4, -100, -88), iqmin=-100, iqmax=100).swatch()")
	test("Colour().yiq((45, -1, 0.5), ymin=40, ymax=60).swatch()")
	test("Colour(\"goldenrod\").yiq()")

	head("hex")

	test("Colour().hex(\"abc\").swatch()")
	test("Colour().hex(\"#DEf\").swatch()")
	test("Colour().hex(\"#007bcc\").swatch()")
	test("Colour().hex(\"9000f0\").swatch()")
	test("Colour(\"goldenrod\").hex()")
	test("Colour(\"goldenrod\").hex(hash=False)")
	test("Colour(\"goldenrod\").hex(allowshort=True)")
	test("Colour(\"goldenrod\").hex(forceshort=True)")
	test("Colour(\"red\").hex()")
	test("Colour(\"red\").hex(allowshort=True)")

	head("css3")

	test("Colour().css3(\"goldenrod\").swatch()")
	test("Colour().css3(\"GOLDENrod\").swatch()")
	test("Colour().css3(\"wheat\").swatch()")
	test("Colour((0.8, 1, 0.1)).css3()")
	test("Colour(\"daa520\").css3()")

	head("grey")

	for x in range(8):
		test("Colour().grey(%f).swatch()" % (x / 7.0))
	test("Colour(\"goldenrod\").grey()")
	test("Colour(\"grey\").grey()")

	head("hash")

	for x in ["tremby", "yappy", "mon", "bill"]:
		test("Colour().hash(\"%s\").swatch()" % x)
	for x in ["tremby", "yappy", "mon", "bill"]:
		test("Colour().hash(\"%s\", minh=-15, maxh=15).swatch()" % x)
	for x in ["tremby", "yappy", "mon", "bill"]:
		test("Colour().hash(\"%s\", mins=0, maxs=0.3).swatch()" % x)
	for x in ["tremby", "yappy", "mon", "bill"]:
		test("Colour().hash(\"%s\", miny=0, maxy=0.2).swatch()" % x)
	for x in ["1", "9.22", "\"blah\"", "None", "Colour(\"goldenrod\")", "Colour(\"red\")", "[2, 3, 3]"]:
		test("Colour().hash(%s).swatch()" % x)

	head("hue methods")

	head("hue", 3)
	test("Colour(\"goldenrod\").hue(340).swatch()")
	test("Colour(\"goldenrod\").hue(340, perceptual=True).swatch()")
	test("Colour(\"goldenrod\").hue(30).swatch()")
	test("Colour(\"goldenrod\").hue(-30).swatch()")
	test("Colour(\"goldenrod\").hue()")
	test("Colour(\"slateblue\").hue()")

	head("shifthue", 3)
	test("Colour(\"goldenrod\").shifthue(340).swatch()")
	test("Colour(\"goldenrod\").shifthue(340, perceptual=True).swatch()")
	test("Colour(\"goldenrod\").shifthue(30).swatch()")
	test("Colour(\"goldenrod\").shifthue(-30).swatch()")

	head("saturation methods")

	head("saturation_hs[vl]", 3)
	for x in range(8):
		test("Colour(\"goldenrod\").saturation_hsv(%f).swatch()" % (x / 7.0))
	for x in range(8):
		test("Colour(\"goldenrod\").saturation_hsv(%f, perceptual=True).swatch()" % (x / 7.0))
	for x in range(8):
		test("Colour(\"goldenrod\").saturation_hsl(%f).swatch()" % (x / 7.0))
	for x in range(8):
		test("Colour(\"goldenrod\").saturation_hsl(%f, perceptual=True).swatch()" % (x / 7.0))
	test("Colour(\"goldenrod\").saturation_hsv()")
	test("Colour(\"goldenrod\").saturation_hsl()")

	head("shiftsaturation_hs[vl]", 3)
	for x in range(8):
		test("Colour(\"goldenrod\").shiftsaturation_hsv(%f).swatch()" % (x / 3.5 - 1))
	for x in range(8):
		test("Colour(\"goldenrod\").shiftsaturation_hsv(%f, perceptual=True).swatch()" % (x / 3.5 - 1))
	for x in range(8):
		test("Colour(\"goldenrod\").shiftsaturation_hsl(%f).swatch()" % (x / 3.5 - 1))
	for x in range(8):
		test("Colour(\"goldenrod\").shiftsaturation_hsl(%f, perceptual=True).swatch()" % (x / 3.5 - 1))

	head("lightness methods")

	head("intensity", 3)
	for x in range(8):
		test("Colour(\"darkblue\").intensity(%f).swatch()" % (x / 7.0))
	test("Colour(\"goldenrod\").intensity()")
	test("Colour(\"darkblue\").intensity()")

	head("shiftintensity", 3)
	for x in range(8):
		test("Colour(\"darkblue\").shiftintensity(%f).swatch()" % (x / 3.5 - 1))

	head("value", 3)
	for x in range(8):
		test("Colour(\"darkblue\").value(%f).swatch()" % (x / 7.0))
	test("Colour(\"goldenrod\").value()")
	test("Colour(\"darkblue\").value()")

	head("shiftvalue", 3)
	for x in range(8):
		test("Colour(\"darkblue\").shiftvalue(%f).swatch()" % (x / 3.5 - 1))

	head("lightness", 3)
	for x in range(8):
		test("Colour(\"darkblue\").lightness(%f).swatch()" % (x / 7.0))
	test("Colour(\"goldenrod\").lightness()")
	test("Colour(\"darkblue\").lightness()")

	head("shiftlightness", 3)
	for x in range(8):
		test("Colour(\"darkblue\").shiftlightness(%f).swatch()" % (x / 3.5 - 1))

	head("luma", 3)
	for x in range(8):
		test("Colour(\"darkblue\").luma(%f).swatch()" % (x / 7.0))
	test("Colour(\"goldenrod\").luma()")
	test("Colour(\"darkblue\").luma()")

	head("shiftluma", 3)
	for x in range(8):
		test("Colour(\"darkblue\").shiftluma(%f).swatch()" % (x / 3.5 - 1))

	head("mix")
	for x in range(8):
		test("Colour(\"goldenrod\").mix(Colour(\"darkblue\"), %f).swatch()" % (x / 7.0))

	head("swatch")

	test("Colour(\"goldenrod\").swatch()")
	test("Colour(\"goldenrod\").swatch(showhex=False)")
	test("Colour(\"goldenrod\").swatch(cssclass=\"reallybig\")")

	head("conversion functions")
	test("colour.rgbtohsv((0.2, 0.8, 0))")
	test("colour.rgbtohsl((0.2, 0.8, 0))")
	test("colour.rgbtoyiq((0.2, 0.8, 0))")
	test("colour.hsvtorgb((88, 0.8, 0.4))")
	test("colour.hsltorgb((88, 0.8, 0.4))")
	test("colour.yiqtorgb((0.7, -0.8, 0.4))")
	test("colour.hextorgb(\"#342\")")
	test("colour.rgbtohex((0.2, 0.8, 0))")

	head("cubes")

	head("RGB", 2)
	for r in range(7):
		print "<div class=\"blobset\">"
		for g in range(7):
			for b in range(7):
				sys.stdout.write("<div class=\"blob\" style=\"background-color: %s\"></div>" % Colour((r / 6.0, g / 6.0, b / 6.0)))
			print "<br>"
		print "</div>"

	head("HSV", 3)
	for h in range(12):
		print "<div class=\"blobset\">"
		for s in range(7):
			for v in range(7):
				sys.stdout.write("<div class=\"blob\" style=\"background-color: %s\"></div>" % Colour(hsv=(h * 30.0, s / 6.0, v / 6.0)))
			print "<br>"
		print "</div>"
	
	head("HSL", 3)
	for h in range(12):
		print "<div class=\"blobset\">"
		for s in range(7):
			for l in range(7):
				sys.stdout.write("<div class=\"blob\" style=\"background-color: %s\"></div>" % Colour(hsl=(h * 30.0, s / 6.0, l / 6.0)))
			print "<br>"
		print "</div>"

	head("YIQ", 3)
	for y in range(13):
		print "<div class=\"blobset\">"
		for i in range(7):
			for q in range(7):
				sys.stdout.write("<div class=\"blob\" style=\"background-color: %s\"></div>" % Colour(yiq=(y / 12.0, i / 3.0 - 1, q / 3.0 - 1)))
			print "<br>"
		print "</div>"

	print "</body></html>"

if __name__ == "__main__":
	main()
