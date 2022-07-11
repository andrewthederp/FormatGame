from PIL import Image, ImageDraw, ImageFont
from colorama import Fore, Back, Style, init
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


_number_dict = {
	"2": ((236, 226, 216), 50),
	"4": ((236, 223, 199), 50),
	"8":  ((241, 176, 120), 50),
	"16": ((244, 148, 99), 50),
	"32": ((245, 123, 94), 50),
	"64": ((245, 93, 58), 50),
	"128": ((235, 205, 112), 40),
	"256": ((235, 202, 95), 40),
	"512": ((235, 198, 79), 40),
	"1024": ((235, 195, 61), 30),
	"2048": ((235, 192, 45), 30)
}

def _convert_to_coor(num, numeric_coordinates, alpha_coordinates):
	if numeric_coordinates:
		return str(num+1)
	elif alpha_coordinates:
		return chr(num+ord('a'))
	return ''

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

def _format_board(board, *, numeric_coordinates=False, mixed_coordinates=False, alpha_coordinates=False, replacments={}, codeblock=False, filler_char=None, prefix='', suffix='', row_prefix='', row_suffix='', vertical_join='', horizontal_join=''):
	if (numeric_coordinates and mixed_coordinates) or (numeric_coordinates and alpha_coordinates) or (mixed_coordinates and alpha_coordinates):
		return

	coordinates = bool(numeric_coordinates or mixed_coordinates or alpha_coordinates)
	if coordinates:
		lst = [(filler_char or ' ')+vertical_join+''.join(replacments.get(conversion:=_convert_to_coor(i, numeric_coordinates, mixed_coordinates or alpha_coordinates), conversion)+vertical_join for i in range(len(board)))]
	else:
		lst = []

	for num, row in enumerate(board):
		lst.append(replacments.get(conversion:=_convert_to_coor(num, numeric_coordinates or mixed_coordinates, alpha_coordinates), conversion)+vertical_join+''.join([replacments.get(col, col)+vertical_join for col in row]))

	string = ''.join([row_prefix+row+row_suffix+horizontal_join+'\n' for row in lst])
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

def format_hangman_game(errors, *, image=False, dead_face=False):
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
		return (
			f" {head}\n{left_arm}{torso}{right_arm}\n {left_leg}{right_leg}"
		)

def format_chess_game(fen, *, image=False, past_fen=None, ansi_color=False, board_theme='green', peice_theme='green', font_color=(0,0,0), font='bahnschrift.ttf', **kwargs):
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
			moved_peice = _get_moved_piece(fen, past_fen)
			for x, y in moved_peice:
				x = x*im.size[0]//8
				y = y*im.size[1]//8

				im.paste(highlight, (y, x), highlight)

		for x in range(len(fen_)):
			for y in range(len(fen_[x])):

				x_, y_ = y*(im.size[1]//8), x*(im.size[0]//8)

				if x == 0:
					color = _chess_font_colors[board_theme][y%2]
					coor = _convert_to_coor(y, numeric_coordinates, alpha_coordinates or mixed_coordinates)
					draw.text((x_+(im.size[0]//8)-25, y_+im.size[1]-25), coor, fill=color, font=font)
				if y == 0:
					color = _chess_font_colors[board_theme][0 if(x%2)else 1]
					coor = _convert_to_coor(7-x, numeric_coordinates or mixed_coordinates, alpha_coordinates)
					draw.text((x_+5, y_+5), coor, fill=color, font=font)

				if fen_[x][y] != ' ':
					peice = fen_[x][y]
					peice = Image.open(f"{peice_path}/{'w' if peice.isupper() else 'b'}{peice.lower()}.png").convert('RGBA')
					im.paste(peice, (x_, y_), peice)
		return im
	else:
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
		image_size = 150

		if value_diff:
			width += int(math.log10(abs(value_diff))+1)*image_size
		width = 0
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

def format_2048_board(board, *, image=False, custom_number_dict={}, font='ClearSans-Bold.ttf', **kwargs):
	if image:
		im = Image.new('RGB', (519,519), color=(187, 173, 160))
		draw = ImageDraw.Draw(im)

		size = 106
		offset = 19

		font = ImageFont.truetype(os.path.join(os.path.dirname(__file__), 'fonts', font), 10)

		number_dict = {k: custom_number_dict.get(k, v) for k, v in _number_dict.items()}

		for y, row in enumerate(board):
			for x, col in enumerate(row):
				x_, y_ = (x*size)+(offset*(x+1)), (y*size)+(offset*(y+1))

				if col in [' ', 0, '0', '']:
					draw.rounded_rectangle((x_, y_, x_+size, y_+size), radius=5, width=0, fill=(205, 193, 180))
				elif isinstance(col, int) or col.isdigit:
					try:
						color = number_dict[str(col)][0]
						font_size = number_dict[str(col)][1]
					except KeyError:
						color = (58, 56, 48)
						font_size = 30
					font = font.font_variant(size=font_size)
					draw.rounded_rectangle((x_, y_, x_+size, y_+size), radius=5, width=0, fill=color)
					draw.text((x_+(size//2), y_+(size//2)), str(col), fill=(119, 110, 101) if str(col) in ['2','4'] else (249, 246, 242), anchor='mm', font=font)
		return im
	else:
		return _format_board(board, **kwargs)

if __name__ == '__main__':
	print(__name__)
	# im = Image.new('RGBA', (150, 150), color=(255, 255, 0, 170))
	# im.save('chess\\chess_highlight.png')
	# format_chess_game('rnbqkbnr/1ppppppp/8/p7/P7/8/1PPPPPPP/RNBQKBNR', past_fen='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR', image=True, board_theme='graffiti', peice_theme='graffiti', mixed_coordinates=True).show()
	# format_chess_captures('PPPPPNNBRQ', sort_captures=True, other_captures='pppppppnnbrq', image=True, bg_color=(40, 40, 40), theme='light', font_color=(170, 170, 170)).show()
	# format_chess_captures('pppppppnnbrq', sort_captures=True, image=True, bg_color=(40, 40, 40), theme='light', font_color=(170, 170, 170)).show()
	# format_2048_board([['2','4','8','16'],['32','64','128','256'],['512','1024','2048','4096'],['8192',' ',' ',' ']], image=True).show()
