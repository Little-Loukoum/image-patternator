#!/usr/bin/env python
from PIL import Image, ImageDraw
from math import sqrt, pi, log
from random import randrange
import sys

def black_ring(ctx, i, j, square_size, avg, adjusted = True):
	r = square_size*sqrt(avg)/2
	if adjusted:
		r *= pi/4
	d = square_size/2 - r
	box = [(i*square_size, j*square_size), ((i+1)*square_size, (j+1)*square_size)]
	small = [(i*square_size+d, j*square_size+d), ((i+1)*square_size-d, (j+1)*square_size-d)]

	ctx.ellipse(box, fill=0)
	ctx.ellipse(small, fill=255)

def black_circle(ctx, i, j, square_size, avg):
	r = square_size*sqrt(1-avg)/2
	d = square_size/2 - r
	small = [(i*square_size+d, j*square_size+d), ((i+1)*square_size-d, (j+1)*square_size-d)]
	ctx.ellipse(small, fill=0)

def black_square(ctx, i, j, square_size, avg):
	c = square_size*sqrt(1-avg)
	d = (square_size - c)/2
	small = [(i*square_size+d, j*square_size+d), ((i+1)*square_size-d, (j+1)*square_size-d)]
	ctx.rectangle(small, 0)

def black_square_ring(ctx, i, j, square_size, avg):
	c = square_size*sqrt(avg)
	d = (square_size - c)/2
	box = [(i*square_size, j*square_size), ((i+1)*square_size, (j+1)*square_size)]
	small = [(i*square_size+d, j*square_size+d), ((i+1)*square_size-d, (j+1)*square_size-d)]
	ctx.rectangle(box,0)
	ctx.rectangle(small, 255)

def black_lines(ctx, i, j, square_size, avg):
	c = square_size*(1-avg)
	d = (square_size - c)/2
	small = [(i*square_size, j*square_size+d), ((i+1)*square_size, (j+1)*square_size-d)]
	ctx.rectangle(small, 0)

def black_columns(ctx, i, j, square_size, avg):
	c = square_size*(1-avg)
	d = (square_size - c)/2
	small = [(i*square_size+d, j*square_size), ((i+1)*square_size-d, (j+1)*square_size)]
	ctx.rectangle(small, 0)


def white_diagonal_cross(ctx, i, j, square_size, avg):
	c = square_size*sqrt(1-avg)
	d = (square_size - c)/2
	demi = square_size/2

	x0, y0, x1, y1 = i*square_size, j*square_size, (i+1)*square_size, (j+1)*square_size

	ctx.polygon([(x0+d, y0), (x1-d, y0), (x0+demi, y0+demi)], 0)
	ctx.polygon([(x0, y0+d), (x0, y1-d), (x0+demi-d, y0+demi)], 0)
	ctx.polygon([(x0+d, y1), (x1-d, y1), (x0+demi, y1-demi+d)], 0)
	ctx.polygon([(x1, y0+d), (x1, y1-d), (x1-demi+d, y0+demi)], 0)

def white_vertical_cross(ctx, i, j, square_size, avg):
	c = square_size*sqrt(1-avg)
	d = (square_size - c)/2
	demi = square_size/2
	x0, y0 = i*square_size, j*square_size
	box = [(i*square_size, j*square_size), ((i+1)*square_size, (j+1)*square_size)]

	ctx.rectangle(box, 0)
	ctx.rectangle((x0+demi-d, y0, x0+demi+d, y0+square_size), 255)
	ctx.rectangle((x0, y0+demi-d, x0+square_size, y0+demi+d), 255)

def black_crosshatch(ctx, i, j, square_size, avg, chaotic = False, adjusted = True):
	if adjusted:
		avg = log(avg+1, 2)
	n = round(square_size*(1-avg))
	if chaotic:
		d = 1/sqrt(1-avg)
	else:
		d = square_size/n if n != 0 else square_size/2
	x0, y0 = i*square_size, j*square_size
	for it in range(n-1):
		ctx.line([(x0+it*d+d, y0), (x0+it*d+d, y0+square_size)], 0, 1)
		ctx.line([(x0, y0+it*d+d), (x0+square_size, y0+it*d+d)], 0, 1)

def black_stipples(ctx, i, j, square_size, avg):
	n = round((1-avg) * (square_size)**2 / 4)
	x0, y0 = i*square_size, j*square_size
	for _ in range(n):
		x, y = x0+randrange(square_size), y0+randrange(square_size)
		ctx.ellipse( [(x-1, y-1), (x+1, y+1)], 0)

patterns = {
	"Rings": black_ring,
	"Discs": black_circle,
	"Squares": black_square,
	"Square rings": black_square_ring,
	"Horizontal lines": black_lines,
	"Vertical lines": black_columns,
	"Xs": white_diagonal_cross,
	"Plus": white_vertical_cross,
	"Crosshatch": black_crosshatch,
	"Stippling": black_stipples
}

def grid(image, size, square_size, abyss):
	avgs = []
	width, height = size

	for y_0 in range(0, height, square_size):
		squares = [0]*(width//square_size)
		for y_delta in range(square_size):
			for x in range(width):
				try:
					squares[x//square_size] += image.getpixel((x, y_0+y_delta))
				except IndexError:
					if abyss == 'black':
						pass
					elif abyss == 'white':
						squares[int(x/sq)] += 255

		ligne = map(lambda y: y/(square_size*square_size), squares)
		avgs.append(list(ligne))

	return avgs

def patterner(image, square_size, pattern = black_ring, quality = 8, abyss='crop'):
	if abyss == 'crop':
		height = (image.height//square_size)*square_size
		width = (image.width//square_size)*square_size
	else:
		width, height = image.size

	columns = image.width//square_size
	rows = image.height//square_size
	print("Calculating grid...")
	averages = grid(image, (width, height), square_size, abyss)
	print("Done.")

	square_size *= quality
	res = Image.new("L", (width*quality, height*quality), 255)
	ctx = ImageDraw.Draw(res)
	print("Drawing pattern...")
	for i in range(columns):
		for j in range(rows):
			avg = averages[j][i]/255
			pattern(ctx, i, j, square_size, avg)
	print("Done.")

	return res

def scale_and_save(image, size, name = 'pattern.jpg'):
	image = image.resize(size, Image.Resampling.LANCZOS)
	image.save(name)

if __name__ == "__main__":
	try:
		im = Image.open(sys.argv[1])
	except:
		im = Image.open("bisou.jpeg")

	print("LittleLoukoum's patternator")
	print("Enter image name on the next line.")
	correct = False
	while not correct:
		filename = input('> ')
		try:
			image = Image.open(filename)
		except FileNotFoundError:
			print('Oops, we can\'t find that image. Did you move it to the same folder? If yes, check the spelling and enter correct name:')
		else:
			correct = True

	colour = False

	if image.mode != 'L':
		print("It appears this is a colour image. What would you like to do?")
		print("1) Convert to black and white")
		print("2) Keep colour and treat channels separately")
		correct = False
		while not correct:
			choice = int(input("> "))
			if choice == 1:
				image = image.convert('L')
				print('Image has been converted to B&W.')
				correct = True
			elif choice == 2:
				colour = True
				print("Colour has been kept. You will choose a pattern for each channel.")
				correct = True
			else:
				print("Please enter 1 or 2.")

	pattern_names = list(sorted(patterns.keys()))

	if colour:
		chosen_patterns = []
		for c in ["red", "green", "blue"]:
			print(f"Select a pattern for {c} channel (type corresponding number and enter):")
			for i, name in enumerate(pattern_names):
				print(f'{i+1}) {name}')

			correct = False
			while not correct:
				pattern = input("> ")
				try:
					pattern_name = pattern_names[int(pattern)-1]
					assert(int(pattern) > 0)
					chosen_patterns.append(patterns[pattern_name])
				except:
					print(f"Incorrect value. Please enter a number between 1 and {len(pattern_names)}")
				else:
					correct = True
	else:
		print("Select a pattern (type corresponding number and enter):")
		for i, name in enumerate(pattern_names):
			print(f'{i+1}) {name}')
		correct = False
		while not correct:
			pattern = input("> ")
			try:
				pattern_name = pattern_names[int(pattern)-1]
				assert(int(pattern) > 0)
				pattern = patterns[pattern_name]
			except:
				print(f"Incorrect value. Please enter a number between 1 and {len(pattern_names)}")
			else:
				correct = True

	correct = False
	print("Enter a grid size (higher = more stylised, lower = more detailed). Leave empty (press enter) for default.")
	while not correct:
		square_size = input("> ").strip()
		try:
			if square_size == "":
				square_size = round(sqrt(image.width*image.height)/100)
			else:
				square_size = int(square_size)
			assert(square_size > 0)
		except:
			print("Please enter a positive number")
		else:
			correct = True

	if colour:
		red, green, blue = image.split()
		red = patterner(red, square_size, chosen_patterns[0])
		green = patterner(green, square_size, chosen_patterns[1])
		blue = patterner(blue, square_size, chosen_patterns[2])
		result = Image.merge("RGB", (red, green, blue))
	else:
		result = patterner(image, square_size, pattern)

	print("Enter the name of the file to save to. Please specify a file extension, e.g. png, jpg, jpeg or webm.")
	correct = False
	while not correct:
		out_name = input("> ")
		try:
			scale_and_save(result, image.size, out_name)
		except:
			print("Something went wrong. Please try again. The name should look something like this: cool_pattern.jpg")
		else:
			correct = True
