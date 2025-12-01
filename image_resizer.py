from PIL import Image
import sys


if __name__ == '__main__':
	argv = sys.argv
	if len(argv) != 3:
		print("usage: image_resizer [file_name] [scale:int]")
		exit()
	file_name= argv[1]
	img = Image.open(file_name).convert("RGB")
	w, h = img.size
	scale = int(argv[2])

	print(w, h)
	split = file_name.split('.')
	name = split[0] + '_resize.' + split[1]
	w = w//scale
	h = h//scale
	print(w, h, split,name)
	img = img.resize((w, h), Image.LANCZOS)
	img.save(name)