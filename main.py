import tkinter
import cv2   # pip install oprncv-python
import PIL.Image, PIL.ImageTk    # Python Image Library - pip install pillow
from functools import partial
import threading
import imutils
import time

stream = cv2.VideoCapture("clip.mp4")
flag = True

def play(speed):
    global flag
    print(f"You clicked on play. Speed is {speed}")
    
    # play the video
    frame1 = stream.get(cv2.CAP_PROP_POS_FRAMES)
    stream.set(cv2.CAP_PROP_POS_FRAMES, frame1 + speed)

    grabbed, frame = stream.read()
    if not grabbed:
        exit()
    frame = imutils.resize(frame, width = SET_WIDTH, height = SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image = frame, anchor = tkinter.NW) 
    if flag:
        canvas.create_text(134, 25, fill = "red", font = "Times 26 bold", text = "Decision Pending")
    flag = not flag


def pending(decision):
    # 1. Display decision pending image
    frame = cv2.cvtColor(cv2.imread("pending.jpg"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width = SET_WIDTH, height = SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image = frame, ancho = tkinter.NW)

    # 2. Wait for 2 second
    time.sleep(2)

    # 3. Display sponsor image
    frame = cv2.cvtColor(cv2.imread("sponsor.jpg"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width = SET_WIDTH, height = SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image = frame, ancho = tkinter.NW)

    # 4. Wait 1 second
    time.sleep(1)

    # 5. Display ipl image
    frame = cv2.cvtColor(cv2.imread("ipl.jpg"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width = SET_WIDTH, height = SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image = frame, ancho = tkinter.NW)

    # 6. Wait for 2 second
    time.sleep(2)

    # 7. Display out/notout image
    if decision == "Out":
        decisionImg = "out.jpg"
    else:
        decisionImg = "NotOut.jpg"

    frame = cv2.cvtColor(cv2.imread(decisionImg), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width = SET_WIDTH, height = SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image = frame, ancho = tkinter.NW)


def out():
    thread = threading.Thread(target = pending, args = ("Out",))
    thread.daemon = 1
    thread.start()
    print("Player is out!")

def not_out():
    thread = threading.Thread(target = pending, args = ("Not Out",))
    thread.daemon = 1
    thread.start()
    print("Player is not out!")


# Width and height of our main screen
SET_WIDTH = 650
SET_HEIGHT = 368

# Tkinter GUI starts here
window = tkinter.Tk()
window.title("Third Umpire Decision Review kit")
cv_img = cv2.cvtColor(cv2.imread("welcome.jpg"), cv2.COLOR_BGR2RGB)
canvas = tkinter.Canvas(window, width = SET_WIDTH, height = SET_HEIGHT)
photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(cv_img))
image_on_canvas = canvas.create_image(0, 0, ancho = tkinter.NW, image = photo)
canvas.pack()
 
# Buttons to control playback
btn = tkinter.Button(window, text = "<< Previous(fast)", width = 50, command = partial(play, -25))
btn.pack()

btn = tkinter.Button(window, text = "<< Previous(slow)", width = 50, command = partial(play, -2))
btn.pack()

btn = tkinter.Button(window, text = "Next(fast) >>", width = 50, command = partial(play, 25))
btn.pack()

btn = tkinter.Button(window, text = "Next(slow) >>", width = 50, command = partial(play, 2))
btn.pack()

btn = tkinter.Button(window, text = "Give Out", width = 50, command = out)
btn.pack()

btn = tkinter.Button(window, text = "Give Not Out", width = 50, command = not_out)
btn.pack()





window.mainloop()