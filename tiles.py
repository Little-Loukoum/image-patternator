from PIL import Image, ImageDraw
from math import sqrt, pi, log
from random import randrange


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
