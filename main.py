#!/usr/bin/env python
import os.path as path, sys
from os import getcwd
from tiles import *

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
	print("LittleLoukoum's patternator")

	cwd = getcwd()
	script_dir = path.dirname(path.realpath(__file__))
	image_paths = [path.abspath(cwd), path.abspath(path.join(cwd, 'images'))]
	if not path.samefile(cwd, script_dir):
		image_paths += [path.abspath(script_dir), path.abspath(path.join(script_dir, 'images'))]

	try:
		with open('paths.txt', 'r') as f:
			custom_dirs = f.read().split()
			print(custom_dirs)
			for c_dir in custom_dirs:
				c_dir = path.abspath(c_dir)
				print(c_dir)
				if not (path.exists(c_dir) and path.isdir(c_dir)):
					print(path.exists(c_dir), path.isdir(c_dir))
					print("Warning : some or all custom image directories in paths.txt may be incorrect.")
					continue
				if all(map(lambda y: not path.samefile(c_dir, y), image_paths)):
					image_paths.append(c_dir)
	except FileNotFoundError:
		pass

	print(image_paths)
	print("Enter image name on the next line.")
	correct = False
	while not correct:
		filename = input('> ')
		for image_dir in image_paths:
			try:
				image = Image.open(path.join(image_dir,filename))
			except FileNotFoundError:
				continue
			else:
				correct = True
				break
		if not correct:
			print('Oops, we can\'t find that image. Did you move it to the same folder? If yes, check the spelling and enter correct name:')

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
				image = image.convert('RGB')
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
			result_dir = path.join(script_dir, 'results')
			scale_and_save(result, image.size, path.join(result_dir, out_name))
		except BaseException as e:
			print(e)
			print("Something went wrong. Please try again. The name should look something like this: cool_pattern.jpg")
		else:
			correct = True
