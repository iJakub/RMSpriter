#iJ

from tkinter import filedialog
from tkinter import *
import tkinter
import os
from PIL import ImageTk, Image, ImageDraw

root = tkinter.Tk()
root.title("RMSpriter")
root.geometry("450x570")
root.resizable(False,False)
root.configure(bg='#191919')

rmxp_img = PhotoImage(file = r"img/rmxp.png")
rmvx_img = PhotoImage(file = r"img/rmvx.png")
frames_one_img = PhotoImage(file = r"img/frames1.png")
frames_all_img = PhotoImage(file = r"img/frames2.png")
output_img = PhotoImage(file = r"img/output.png")

def workplace():
    global image, bigger_parameter
    file_name = filedialog.askopenfilename(filetypes=[("Sprite", ".png")])

    if file_name == "":
        workplace_button.config(text="Click here to\n select a file", image = "", anchor="center")
        convert_button["state"] = DISABLED
        return

    image = Image.open(file_name)
    
    if (image.width >= 430) or (image.height >= 430):
        
        if image.width <= image.height:
            bigger_parameter = image.height

        elif image.width >= image.height:
            bigger_parameter = image.width

        preview_width, preview_height = (image.width)//(bigger_parameter/430), (image.height)//(bigger_parameter/430)
        preview_image = image.resize((int(preview_width), int(preview_height)))
    else:
        preview_image = image

    root.tkimage = ImageTk.PhotoImage(preview_image)
    workplace_button.config(image = root.tkimage, anchor="center")
    convert_button["state"] = NORMAL
    return image

output_directory = (os.getcwd() + "/output.png").replace("\\", "/")
default_directory = output_directory
def output():
    global default_directory, output_directory
    folder_selected = filedialog.askdirectory()
    output_directory = (folder_selected + "/output.png")

    if folder_selected == "":
        output_directory = default_directory

    output_directory_label.config(text = (" " + output_directory))
    return output_directory

current_rpgmaker = "xp"
def rpgmaker():
    global current_rpgmaker

    if current_rpgmaker == "xp":
        rpgmaker_button.config(text = "VX")
        current_rpgmaker = "vx"

    elif current_rpgmaker == "vx":
        rpgmaker_button.config(text = "XP")
        current_rpgmaker = "xp"

    return current_rpgmaker

current_frames = "one"
def frames():
    global current_frames

    if current_frames == "one":
        frames_button.config(image = frames_all_img)
        current_frames = "all"

    elif current_frames == "all":
        frames_button.config(image = frames_one_img)
        current_frames = "one"

    return current_frames

def convert():
    global current_frames, current_rpgmaker, image, bigger_parameter
    width, height = image.width, image.height

    if current_rpgmaker == "xp":
        output = Image.new('RGBA', (width*4, height*4), (255, 0, 0, 0))
        first_row = 4
        second_row = 8
        third_row = 12
        loop_range = 17

    elif current_rpgmaker == "vx":
        output = Image.new('RGBA', (width*3, height*4), (255, 0, 0, 0))
        first_row = 3
        second_row = 6
        third_row = 9
        loop_range = 13

    draw = ImageDraw.Draw(output)
    output.save(output_directory, 'PNG')
    bg = Image.open(output_directory)
    fg = image
    x = 0
    y = 0

    if current_frames == "one":
        bg.paste(fg, (x, y), fg.convert('RGBA'))

    if current_frames == "all":

        for i in range(1, loop_range):
            bg.paste(fg, (x, y), fg.convert('RGBA'))
            x = x + width

            if (i == first_row) or (i == second_row) or (i == third_row):
                x = 0
                y = y + height

    bg.save(output_directory)
    output_image = Image.open(output_directory)

    if (output_image.width >= 430) or (output_image.height >= 430):
    
        if output_image.width <= output_image.height:
            bigger_parameter = output_image.height

        elif output_image.width >= output_image.height:
            bigger_parameter = output_image.width

        output_width, output_height = (output_image.width)//(bigger_parameter/430), (output_image.height)//(bigger_parameter/430)
        output_image = output_image.resize((int(output_width), int(output_height)))

    root.tkimage = ImageTk.PhotoImage(output_image)
    workplace_button.config(image = root.tkimage, anchor="center")
    convert_button["state"] = NORMAL

rpgmaker_button = tkinter.Button(root, compound="c", relief="solid", bg="#393939", activebackground="#393939", activeforeground="white", fg="white", text="XP", font=("Bahnschrift", 20, "bold"), command=rpgmaker)
rpgmaker_button.place(x=10, y=10, height=50, width=50)

output_button = tkinter.Button(root, compound="c", relief="solid", bg="#393939", activebackground="#393939", activeforeground="white", image = output_img, command=output)
output_button.place(x=390, y=10,height=50, width=50)

frames_button = tkinter.Button(root, compound="c", relief="solid", bg="#393939", activebackground="#393939", activeforeground="white", image = frames_one_img, command=frames)
frames_button.place(x=10, y=70, height=50, width=50)

convert_button = tkinter.Button(root, compound="c", relief="solid", bg="#393939", fg="white", activebackground="#393939", activeforeground="white", state=DISABLED, text="CONVERT", font=("Bahnschrift", 20, "bold"), command=convert)
convert_button.place(x=70, y=70,height=50, width=370)

workplace_button = tkinter.Button(root, bd=2, anchor="center", relief="solid", bg="#393939", fg="white", activebackground="#393939", activeforeground="white", text="Click here to\n select a file", font=("Bahnschrift", 30, "bold"), command=workplace)
workplace_button.place(x=10, y=130 ,height=430, width=430)

output_directory_label = Label(root, bd=2, anchor="w", relief="solid", bg="#393939", fg="white", text=(" " + output_directory), font=("Bahnschrift", 13, "bold"))
output_directory_label.place(x=70, y=10 ,height=50, width=321)

root.mainloop()