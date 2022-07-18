from PIL import Image, ImageDraw, ImageFont
from colorama import Fore, Back, Style, init

try:
	from .colors import get_color
except ImportError:
	from colors import get_color

import os, random, math



init()

_chess_font_colors = {
	'green': 
		{
			0: (238, 238, 210),
			1: (118, 150, 86)
		},
	'wood':
		{
			0: (190, 156, 120),
			1: (141, 101, 69)
		},
	'light':
		{
			0: (230, 230, 230),
			1: (123, 123, 123)
		},
	'glass':
		{
			0: (100, 116, 134),
			1: (37, 44, 57)
		},
	'tournament':
		{
			0: (184, 168, 158),
			1: (56, 107, 80)
		},
	'newspaper':
		{
			0: (10, 10, 10),
			1: (10, 10, 10)
		},
	'blue':
		{
			0: (107, 135, 157),
			1: (60, 97, 126)
		},
	'8bit':
		{
			0: (215, 219, 220),
			1: (117, 162, 79)
		},
	'lolz':
		{
			0: (255, 255, 255),
			1: (109, 122, 127)
		},
	'neon':
		{
			0: (154, 156, 155),
			1: (49, 50, 50)
		},
	'metal':
		{
			0: (210, 210, 210),
			1: (79, 79, 79)
		},
	'graffiti':
		{
			0: (68, 74, 68),
			1: (164, 129, 88)
		}
}



_2048_dict = {
	"2": {
		'square_rgb':(236, 226, 216),
		'font_size':50,
		'letter_color':(119, 110, 101)
	},
	"4": {
		'square_rgb':(236, 223, 199),
		'font_size':50,
		'letter_color':(119, 110, 101)
	},
	"8": {
		'square_rgb':(241, 176, 120),
		'font_size':50,
		'letter_color':(249, 246, 242)
	},
	"16": {
		'square_rgb':(244, 148, 99),
		'font_size':50,
		'letter_color':(249, 246, 242)
	},
	"32": {
		'square_rgb':(245, 123, 94),
		'font_size':50,
		'letter_color':(249, 246, 242)
	},
	"64": {
		'square_rgb':(245, 93, 58),
		'font_size':50,
		'letter_color':(249, 246, 242)
	},
	"128": {
		'square_rgb':(235, 205, 112),
		'font_size':40,
		'letter_color':(249, 246, 242)
	},
	"256": {
		'square_rgb':(235, 202, 95),
		'font_size':40,
		'letter_color':(249, 246, 242)
	},
	"512": {
		'square_rgb':(235, 198, 79),
		'font_size':40,
		'letter_color':(249, 246, 242)
	},
	"1024": {
		'square_rgb':(235, 195, 61),
		'font_size':30,
		'letter_color':(249, 246, 242)
	},
	"2048": {
		'square_rgb':(235, 192, 45),
		'font_size':30,
		'letter_color':(249, 246, 242)
	}
}

_minesweeper_dict = {
	'1':0x1976d2,
	'2':0x388e3c,
	'3':0xd32f2f,
	'4':0x8027a2,
	'5':0xdeaa1f,
	'6':0x0998a6,
	'7':0x4b4947,
	'8':0x9e9e9e,
	'bomb1':{
		'color': 0xed44b5,
		'darker_color': 0x9a2c76
	},
	'bomb2':{
		'color': 0xb648f2,
		'darker_color': 0x762f9d
	},
	'bomb3':{
		'color': 0x4885ed,
		'darker_color': 0x2f569a
	},
	'bomb4':{
		'color': 0xefbe0d,
		'darker_color': 0x9f7e08
	},
	'bomb5':{
		'color': 0x48e6f1,
		'darker_color': 0x2f969d
	},
	'bomb6':{
		'color': 0xf4840d,
		'darker_color': 0x9f5608
	},
}

def _convert_to_coor(num, numeric_coordinates, alpha_coordinates):
	if numeric_coordinates:
		return str(num+1)
	elif alpha_coordinates:
		return chr(num+ord('a'))
	return ''

def _get_relative_neighbours(x, y, *, min_num = 0, max_num = 100):
	dct = {'right':(x+1, y), 'left':(x-1, y), 'down':(x, y+1), 'up':(x, y-1)}

	for key, value in dct.items():
		if not (coor in range(min_num, max_num+1)):
			dct.pop(key)
	return dct

def _get_moved_piece(fen, old_fen):

	fen = _flat(fen).split('/')
	old_fen = _flat(old_fen).split('/')

	try:
		lst = []
		for x, line in enumerate(old_fen):
			for y, char in enumerate(line):
				if old_fen[x][y] != fen[x][y]:
					lst.append((x,y))
	except IndexError:
		return [(10,10),(10,10)]
	return lst

def _flat(fen):
	fen = list(fen)
	for num, i in enumerate(fen):
		if i.isdigit():
			fen[num] = int(i)*' '
	return ''.join(fen)

def _format_board(board, *, numeric_coordinates=False, mixed_coordinates=False, alpha_coordinates=False, replacements={}, codeblock=False, filler_char=' ', prefix='', suffix='', row_prefix='', row_suffix='', vertical_join='', horizontal_join=None, join_upper_coordinates=None, join_sideways_coordinates=None, connect_coordinates_at='tl', invert_lr_coordinates=False, invert_tb_coordinates=False):
	if (numeric_coordinates and mixed_coordinates) or (numeric_coordinates and alpha_coordinates) or (mixed_coordinates and alpha_coordinates):
		return

	coordinates = bool(numeric_coordinates or mixed_coordinates or alpha_coordinates)


	if join_sideways_coordinates and connect_coordinates_at in ['tl','bl']:
		horizontal_join = join_sideways_coordinates+horizontal_join
	elif join_sideways_coordinates and connect_coordinates_at in ['tr','br']:
		horizontal_join = horizontal_join+join_sideways_coordinates
	elif coordinates and connect_coordinates_at in ['tl','bl']:
		horizontal_join = '  '+horizontal_join

	if coordinates and connect_coordinates_at in ['tr','tl']:
		top_cordinates = filler_char
		top_cordinates += ''.join(replacements.get(conversion:=_convert_to_coor((len(board)-1)-num if invert_tb_coordinates else num, numeric_coordinates, mixed_coordinates or alpha_coordinates), conversion)+(join_upper_coordinates if join_upper_coordinates else vertical_join) for num in range(len(board)))
		lst = [top_cordinates]
	else:
		lst = []

	if horizontal_join:
		lst.append(horizontal_join)

	for num, row in enumerate(board):
		temp_lst = [row_prefix]

		if coordinates and connect_coordinates_at in ['tl','bl']:
			coordinate = _convert_to_coor((len(row)-1)-num if invert_lr_coordinates else num, numeric_coordinates or mixed_coordinates, alpha_coordinates)
			coordinate = replacements.get(coordinate, coordinate)
			temp_lst.append(coordinate)
			temp_lst.append(vertical_join)

		for col in row:
			temp_lst.append(replacements.get(col, col)+vertical_join)

		if coordinates and connect_coordinates_at in ['tr','br']:
			coordinate = _convert_to_coor((len(row)-1)-num if invert_lr_coordinates else num, numeric_coordinates or mixed_coordinates, alpha_coordinates)
			coordinate = replacements.get(coordinate, coordinate)
			temp_lst.append(coordinate)

		temp_lst.append(row_suffix)
		lst.append(''.join(temp_lst))
		if horizontal_join:
			lst.append(horizontal_join)

	if coordinates and connect_coordinates_at in ['br','bl']:
		bottom_coordinates = filler_char
		bottom_coordinates += ''.join(replacements.get(conversion:=_convert_to_coor((len(board)-1)-num if invert_tb_coordinates else num, numeric_coordinates, mixed_coordinates or alpha_coordinates), conversion)+(join_upper_coordinates if join_upper_coordinates else vertical_join) for num in range(len(board)))
		lst.append(bottom_coordinates)

	string = '\n'.join(lst)
	if codeblock:
		return '```\n'+prefix+string+suffix+'\n```'
	return prefix+string+suffix

def format_tictactoe_board(board, *, image=False, bg_color=(210,210,210), x_color=(255, 0, 0), o_color=(0, 0, 255), font_color=(0,0,0), line_color=(0,0,0), strikethrough=None, strikethrough_color=None, font='bahnschrift.ttf', **kwargs):
	if image:
		numeric_coordinates = kwargs.get('numeric_coordinates')
		mixed_coordinates = kwargs.get('mixed_coordinates')
		alpha_coordinates = kwargs.get('alpha_coordinates')

		if (numeric_coordinates and mixed_coordinates) or (numeric_coordinates and alpha_coordinates) or (mixed_coordinates and alpha_coordinates):
			return

		bg_color = get_color(bg_color)
		x_color = get_color(x_color)
		o_color = get_color(o_color)
		font_color = get_color(font_color)
		line_color = get_color(line_color)
		strikethrough_color = get_color(strikethrough_color)

		font = ImageFont.truetype(os.path.join(os.path.dirname(__file__), 'fonts', font), 20)

		im = Image.new('RGB', (600, 600), color = bg_color)
		draw = ImageDraw.Draw(im)

		draw.line((0, im.size[1]/3) + (im.size[0], im.size[1]/3), fill=line_color, width=10)
		draw.line((0, im.size[1]/3*2) + (im.size[0], im.size[1]/3*2), fill=line_color, width=10)

		draw.line((im.size[1]/3, 0) + (im.size[1]/3, im.size[0]), fill=line_color, width=10)
		draw.line((im.size[1]/3*2, 0) + (im.size[1]/3*2, im.size[0]), fill=line_color, width=10)

		for y, col in enumerate(board):
			for x, row in enumerate(col):
				if x == 0:
					coor = _convert_to_coor(y, numeric_coordinates, alpha_coordinates or mixed_coordinates)
					xy = ((im.size[1]/3)*y)-25+im.size[1]/3, 3
					draw.text(xy, coor, fill=font_color, font=font)
				if y == 0:
					coor = _convert_to_coor(x, numeric_coordinates or mixed_coordinates, alpha_coordinates)
					xy = 5, ((im.size[1]/3)*x)+(im.size[1]/3)-30
					draw.text(xy, coor, fill=font_color, font=font)

				if row == 'x':
					size = (im.size[0]/3)-30
					x_ = im.size[0]/3*x
					y_ = im.size[1]/3*y

					x_offset = 30
					y_offset = 30

					draw.line([(x_+x_offset, y_+y_offset), (x_+size, y_+size)], fill=x_color, width=12)
					draw.line([(x_+size, y_+y_offset), (x_+x_offset, y_+size)], fill=x_color, width=12)
				elif row == 'o':
					size = (im.size[0]/3)-30
					x_ = im.size[0]/3*x
					y_ = im.size[1]/3*y

					x_offset = 16
					y_offset = 15
					draw.ellipse([(x_+x_offset, y_+y_offset), (x_+x_offset+size, y_+y_offset+size)], outline=o_color, width=12)
		if strikethrough:
			draw.line(strikethrough, fill=strikethrough_color or line_color, width=10)
		return im
	else:
		return _format_board(board, **kwargs)

def format_hangman_game(errors, *, image=False, dead_face=False, word=None):
	if image:
		file_path = os.path.join(os.path.dirname(__file__), 'hangman')
		file_name = f"hangman{errors}{'_' if (errors==6 and dead_face) else ''}.png"

		im = Image.open(file_path+'/'+file_name)
		return im
	else:
		head = "()" if errors > 0 else "  "
		torso = "||" if errors > 1 else "  "
		left_arm = "/" if errors > 2 else " "
		right_arm = "\\" if errors > 3 else " "
		left_leg = "/" if errors > 4 else " "
		right_leg = "\\" if errors > 5 else " "

		string = f" {head}\n{left_arm}{torso}{right_arm}\n {left_leg}{right_leg}"
		string += '\n\n'+' '.join(word) if word else ''
		return string

def format_chess_board(fen, *, image=False, past_fen=None, ansi_color=False, board_theme='green', peice_theme='green', font='bahnschrift.ttf', flip=False, **kwargs):
	if image:
		ansi_color = False
	if past_fen:
		moved_peice = _get_moved_piece(fen, past_fen)
	else:
		moved_peice = []

	fen_ = []
	style_dict = {True:Style.BRIGHT,False:Fore.BLACK}
	for x, row in enumerate(_flat(fen).split('/')):
		tmp_lst = []
		for y, col in enumerate(row):
			if col == ' ':
				tmp_lst.append(Back.YELLOW+f' \033[39m'+Back.RESET if (x,y) in moved_peice and ansi_color else ' ')
			else:
				if ansi_color:
					style = style_dict[col.isupper()]
					if (x,y) in moved_peice:
						style += Back.YELLOW
					style += col
					style += Back.RESET
					tmp_lst.append(style+'\033[39m')
				else:
					tmp_lst.append(col)
		fen_.append(tmp_lst)

	fen_ = [i[::-1] for i in fen_][::-1] if flip else fen_

	if image:
		numeric_coordinates = kwargs.get('numeric_coordinates')
		mixed_coordinates = kwargs.get('mixed_coordinates')
		alpha_coordinates = kwargs.get('alpha_coordinates')

		if (numeric_coordinates and mixed_coordinates) or (numeric_coordinates and alpha_coordinates) or (mixed_coordinates and alpha_coordinates):
			return

		font = ImageFont.truetype(os.path.join(os.path.dirname(__file__), 'fonts', font), 25)

		board_path = os.path.join(os.path.dirname(__file__), 'chess', board_theme)
		peice_path = os.path.join(os.path.dirname(__file__), 'chess', peice_theme)
		im = Image.open(board_path+'/'+board_theme+'.png').convert('RGBA')

		draw = ImageDraw.Draw(im)

		if past_fen:
			highlight = Image.open(os.path.join(os.path.dirname(__file__), 'chess', 'chess_highlight.png')).convert('RGBA')
			moved_peice = _get_moved_piece(fen[::-1] if flip else fen, past_fen[::-1] if flip else past_fen)
			for x, y in moved_peice:
				x = x*im.size[0]//8
				y = y*im.size[1]//8

				im.paste(highlight, (y, x), highlight)

		for x in range(len(fen_)):
			for y in range(len(fen_[x])):

				x_, y_ = y*(im.size[1]//8), x*(im.size[0]//8)

				if x == 0:
					color = _chess_font_colors[board_theme][y%2]
					coor = _convert_to_coor(7-y if flip else y, numeric_coordinates, alpha_coordinates or mixed_coordinates)
					draw.text((x_+(im.size[0]//8)-25, y_+im.size[1]-25), coor, fill=color, font=font)
				if y == 0:
					color = _chess_font_colors[board_theme][0 if(x%2)else 1]
					coor = _convert_to_coor(x if flip else 7-x, numeric_coordinates or mixed_coordinates, alpha_coordinates)
					draw.text((x_+5, y_+5), coor, fill=color, font=font)

				if fen_[x][y] != ' ':
					peice = fen_[x][y]
					peice = Image.open(f"{peice_path}/{'w' if peice.isupper() else 'b'}{peice.lower()}.png").convert('RGBA')
					im.paste(peice, (x_, y_), peice)
		return im
	else:
		kwargs['connect_coordinates_at'] = 'bl'
		if flip:
			kwargs['invert_tb_coordinates'] = True
		else:
			kwargs['invert_lr_coordinates'] = True
		return _format_board(fen_, **kwargs)

def format_chess_captures(captures, *, bg_color=(0,0,0,0), theme='green', image=False, add_gap=True, ansi_color=False, sort_captures=True, extra_value_diff=0, overlap=True, font='bahnschrift.ttf', font_color=(0,0,0), other_captures=None):
	values = {'p':1, 'n':3, 'b':4, 'r':5, 'q':9, 'k':float('inf')} # Even tho a bishop and a knight have the same value i am forced to give them different values to avoid sorting problems
	if isinstance(captures, str):
		captures = list(captures)

	value_diff = 0
	if other_captures:
		if isinstance(other_captures, str):
			other_captures = list(other_captures)
		captures_copy = ''.join(captures.copy()).replace('b','n').replace('B', 'N')
		other_captures_copy = ''.join(other_captures.copy()).replace('b','n').replace('B', 'N')

		value_diff = sum([values[i.lower()] for i in captures_copy]) - sum([values[i.lower()] for i in other_captures_copy])


	if sort_captures:
		captures = sorted(captures, key=lambda i: values[i.lower()])

	if add_gap:
		for num, capture in enumerate(captures):
			try:
				if captures[num+1] != capture and capture != ' ':
					captures.insert(num+1, ' ')
			except IndexError:
				pass
	if image:
		bg_color = get_color(bg_color)
		font_color = get_color(font_color)

		image_size = 150

		width = 0

		if value_diff:
			width += int(math.log10(abs(value_diff))+1)*image_size

		if overlap:
			image_size //= 2
			width += image_size
		width += image_size*len(captures)

		im = Image.new('RGBA', (width, 150), color=bg_color)
		peice_path = os.path.join(os.path.dirname(__file__), 'chess', theme)
		font = ImageFont.truetype(os.path.join(os.path.dirname(__file__), 'fonts', font), 150)

		for x, capture in enumerate(captures):
			if capture != ' ':
				peice = Image.open(f"{peice_path}/{'w' if capture.isupper() else 'b'}{capture.lower()}.png").convert('RGBA')
				im.paste(peice, (x*image_size, 0), peice)

		draw = ImageDraw.Draw(im)
		draw.text(((x+2)*image_size, 10), f"{'+' if value_diff+extra_value_diff > 0 else ''}{value_diff+extra_value_diff}" if value_diff+extra_value_diff else "", fill=font_color, font=font)
		return im
	else:
		style_dict = {True:Style.BRIGHT,False:Fore.BLACK}
		return ''.join([style_dict[char.isupper()]+char+'\033[39m' if ansi_color and char != ' ' else char for char in captures]) + (f" {'+' if value_diff+extra_value_diff > 0 else ''}{value_diff+extra_value_diff}" if value_diff+extra_value_diff else "")

def format_2048_board(board, *, image=False, custom_2048_dict={}, font='ClearSans-Bold.ttf', empty_color=(205, 193, 180), **kwargs):
	if image:
		empty_color = get_color(empty_color)

		im = Image.new('RGBA', (519,519), color=(0,0,0,0))
		draw = ImageDraw.Draw(im)

		draw.rounded_rectangle((0, 0, 519, 519), radius=25, width=0, fill=(187, 173, 160))

		size = 106
		offset = 19

		font = ImageFont.truetype(os.path.join(os.path.dirname(__file__), 'fonts', font), 10)

		_2048_dict_copy = _2048_dict.copy()
		_2048_dict_copy.update(custom_2048_dict)

		for y, row in enumerate(board):
			for x, col in enumerate(row):
				x_, y_ = (x*size)+(offset*(x+1)), (y*size)+(offset*(y+1))

				if col in [' ', 0, '0', '']:
					draw.rounded_rectangle((x_, y_, x_+size, y_+size), radius=5, width=0, fill=empty_color)
				elif isinstance(col, int) or col.isdigit:
					color = _2048_dict_copy.get(str(col), {}).get('square_rgb', (58, 56, 48))
					font_size = _2048_dict_copy.get(str(col), {}).get('font_size', 30)
					letter_color = _2048_dict_copy.get(str(col), {}).get('letter_color', (249, 246, 242))

					color = get_color(color)
					letter_color = get_color(letter_color)

					font = font.font_variant(size=font_size)
					draw.rounded_rectangle((x_, y_, x_+size, y_+size), radius=5, width=0, fill=color)
					draw.text((x_+(size//2), y_+(size//2)), str(col), fill=letter_color, anchor='mm', font=font)
		return im
	else:
		return _format_board(board, **kwargs)

def format_minesweeper_board(board, *, image=False, theme='custom', dark_unclicked=0xa2d149, light_unclicked=0xaad751, light_clicked=0xe5c29f, dark_clicked=0xd7b899, custom_minesweeper_dict={}, font='Roboto-Medium.ttf', **kwargs):
	if image:
		cell_size = 150
		width = len(board)*cell_size
		height = len(board[0])*cell_size
		font = ImageFont.truetype(os.path.join(os.path.dirname(__file__), 'fonts', font), 120)
		flag_path = os.path.join(os.path.dirname(__file__), 'minesweeper', f'{theme}_flag.png')
		flag = Image.open(flag_path).convert('RGBA')

		im = Image.new('RGBA', (width, height), (0,0,0,0))
		draw = ImageDraw.Draw(im)

		_minesweeper_dict_copy = _minesweeper_dict.copy()
		_minesweeper_dict_copy.update(custom_minesweeper_dict)

		draw_cell = lambda x, y, col: None

		if theme == 'custom':
			dark_unclicked = get_color(dark_unclicked)
			dark_clicked = get_color(dark_clicked)
			light_unclicked = get_color(light_unclicked)
			light_clicked = get_color(light_clicked)

			bomb_dicts = [dct for name, dct in _minesweeper_dict_copy.items() if name.startswith('bomb')]

			def draw_cell(x, y, col):
				dark_or_light = (x+(y%2))%2 # 0 = light, 1 = dark
				if col in [' ', '', 'f', 'flag']:
					draw.rectangle([(x*cell_size, y*cell_size), ((x+1)*cell_size, (y+1)*cell_size)], fill=dark_unclicked if dark_or_light else light_unclicked)
				else:
					draw.rectangle([(x*cell_size, y*cell_size), ((x+1)*cell_size, (y+1)*cell_size)], fill=dark_clicked if dark_or_light else light_clicked)

				if (isinstance(col, int) or col.isdigit()) and str(col) != '0':
					color = _minesweeper_dict.get(str(col))
					color = get_color(color)
					draw.text(((x*cell_size)+(cell_size//2), (y*cell_size)+(cell_size//2)), str(col), fill=color, anchor='mm', font=font)
				elif col.lower() in ['f', 'flag']:
					im.paste(flag, (x*cell_size, y*cell_size), flag)
				elif col.lower() in ['b', 'bomb']:
					dct = random.choice(bomb_dicts)
					color = get_color(dct['color'])
					darker_color = get_color(dct['darker_color'])
					draw.rectangle([(x*cell_size, y*cell_size), ((x+1)*cell_size, (y+1)*cell_size)], fill=color)
					coors = [((x*cell_size), (y*cell_size)), (((x+1)*cell_size), ((y+1)*cell_size))]
					draw.ellipse([(coors[0][0])+cell_size//4, (coors[0][1])+cell_size//4, (coors[1][0])-cell_size//4, (coors[1][1])-cell_size//4], fill=darker_color)
		elif theme == 'windows_xp':
			mine_path = os.path.join(os.path.dirname(__file__), 'minesweeper', 'mine.png')
			mine = Image.open(mine_path).convert('RGBA')
			cell_color = get_color(0xbfbfbf)
			cell_light_line = get_color(0xf0f0f0)
			cell_dark_line = get_color(0x8b8b8c)

			def draw_cell(x, y, col):
				x_, y_ = (x*cell_size, y*cell_size)
				if col in [' ', '', 'f', 'flag']:
					draw.rectangle([(x_, y_), (x_+cell_size, y_+cell_size)], fill=cell_color)
					draw.line((x_, y_) + (x_, y_+(cell_size-5)), fill=cell_light_line, width=10)
					draw.line((x_, y_) + (x_+(cell_size-5), y_), fill=cell_light_line, width=10)
					draw.line((x_+(cell_size-8), y_) + (x_+(cell_size-8), y_+(cell_size-8)), fill=cell_dark_line, width=8)
					draw.line((x_, y_+(cell_size-8)) + (x_+(cell_size-8), y_+(cell_size-8)), fill=cell_dark_line, width=8)
				else:
					draw.rectangle([(x*cell_size, y*cell_size), ((x+1)*cell_size, (y+1)*cell_size)], fill=cell_color)

					draw.line((x_, y_) + (x_, y_+cell_size), fill=cell_dark_line, width=10)
					draw.line((x_, y_) + (x_+cell_size, y_), fill=cell_dark_line, width=10)
					draw.line((x_+cell_size, y_) + (x_+cell_size, y_+cell_size), fill=cell_dark_line, width=10)
					draw.line((x_, y_+cell_size) + (x_+cell_size, y_+cell_size), fill=cell_dark_line, width=10)

				if (isinstance(col, int) or col.isdigit()) and str(col) != '0':
					color = _minesweeper_dict.get(str(col))
					color = get_color(color)
					draw.text(((x*cell_size)+(cell_size//2), (y*cell_size)+(cell_size//2)), str(col), fill=color, anchor='mm', font=font)
				elif col.lower() in ['f', 'flag']:
					im.paste(flag, (x_, y_), flag)
				elif col.lower() in ['b', 'bomb']:
					im.paste(mine, (x_+8, y_+8), mine)


		for y, row in enumerate(board):
			for x, col in enumerate(row):
				draw_cell(x, y, col)

		return im
	else:
		return _format_board(board, **kwargs)


if __name__ == '__main__':
	print(__name__)
	# import random
	# from colors import COLORS

	# board = [['x','o','x'],['x','x','o'],['o','x','o']]
	# print(format_tictactoe_board(board, mixed_coordinates=True, vertical_join=' | ', horizontal_join='+---+---+---+', join_upper_coordinates='   ', filler_char='    ', replacements={'x':Fore.RED+'x'+Fore.RESET, 'o':Fore.BLUE+'o'+Fore.RESET}, connect_coordinates_at='tl').replace('+',Fore.BLACK+'+'+Fore.RESET))

	# im = Image.new('RGBA', (150, 150), color=(241, 231, 64, 245))
	# im.save('chess\\chess_highlight.png')
	# format_chess_board('rnbqkbnr/pppp1ppp/8/4p3/3P4/5N2/PPP1PPPP/RNBQKB1R', past_fen='rnbqkbnr/pppp1ppp/8/4p3/3P4/8/PPP1PPPP/RNBQKBNR', image=True, mixed_coordinates=True, flip=False).show()

	# print(format_chess_board('rnbqkbnr/pppp1ppp/8/4p3/3P4/5N2/PPP1PPPP/RNBQKB1R', mixed_coordinates=True, flip=False, vertical_join=' | ', horizontal_join='+---'*8+'+', join_upper_coordinates='   ', filler_char='    '))

	# color=random.choice(list(COLORS.keys()))
	# rgb = get_color(color)
	# print(color+':', rgb)
	# im = Image.new('RGBA', (200, 200), color=rgb)
	# im.show()

	# format_chess_captures('PPPPPNNBRQ', sort_captures=True, other_captures='pppppppnnbrq', image=True, theme='8bit').show()

	# format_chess_captures('pppppppnnbrq', sort_captures=True, image=True, bg_color=(40, 40, 40), theme='light', font_color=0x000000).show()

	# format_2048_board([['2','4','8','16'],['32','64','128','256'],['512','1024','2048','4096'],['8192',' ',' ',' ']], image=True).show()



	# flag_path = os.path.join(os.path.dirname(__file__), 'minesweeper', f'windows_xp_flag.png')
	# mine_path = os.path.join(os.path.dirname(__file__), 'minesweeper', f'mine.png')
	# flag = Image.open(flag_path)
	# mine = Image.open(mine_path)
	# flag = flag.resize((135, 135))
	# mine = mine.resize((135, 135))
	# flag.save(flag_path)
	# mine.save(mine_path)

	# board = [[' ' for _ in range(8)] for _ in range(8)]
	# board[0][0] = '0'
	# board[0][1] = '1'
	# board[0][2] = '2'
	# board[0][3] = '3'
	# board[0][4] = '4'
	# board[0][5] = '5'
	# board[0][6] = '6'
	# board[0][7] = '7'
	# board[1][0] = '8'
	# board[1][1] = 'f'
	# board[2][1] = '8'
	# board[1][2] = 'b'
	# board[1][3] = 'b'
	# board[1][4] = 'b'
	# board[1][5] = 'b'
	# board[1][6] = 'b'
	# board[1][7] = 'b'
	# format_minesweeper_board(board, image=True, theme='windows_xp', font='lcd.ttf').show()
