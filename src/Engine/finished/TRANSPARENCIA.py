import pygame as py
import win32api
import win32con
import win32gui

py.init()
# initialize the pygame window
window_screen = py.display.set_mode((400, 400))
# for borderless window use pygame.Noframe
# size of the pygame window will be of width 700 and height 450
hwnd = py.display.get_wm_info()["window"]
# Getting information of the current active window
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong( hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)

win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(255, 0, 128), 0, win32con.LWA_COLORKEY)
# This will set the opacity and transparency color key of a layered window
font = py.font.SysFont("Times New Roman", 54)
# declare the size and font of the text for the window
text = []
# Declaring the array for storing the text
text.append((font.render("Transparent Window", 0, (255, 100, 0)), (20, 10)))
text.append((font.render("Press Esc to close the window", 0, (255, 100, 100)), (20, 250)))
# Appending the text in the array

# Function to display the text
def show_text():
	for t in text:
	# For loop for calling every element in the text
		window_screen.blit(t[0], t[1])
		# Blit is for block transfer

# Main while loop for the program
done = 0
while not done:
	# Accessing the event if any occurred
	for event in py.event.get():
		# Checking if quit button is pressed or not
		if event.type == py.QUIT:
			# If quit then store true
			done = 1
		# Checking if the escape button is pressed or not
		if event.type == py.KEYDOWN:
			# If the escape button is pressed then store true in the variable
			if event.key == py.K_ESCAPE:
				done = 1
	# Transparent background
	window_screen.fill((255,0,128))
	# Calling the show_text function
	show_text()
	# Checking for the update in the display
	py.display.update()
