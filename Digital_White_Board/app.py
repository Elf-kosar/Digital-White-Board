from tkinter import *
from tkinter.colorchooser import askcolor
from tkinter import ttk
import tkinter as tk

root = Tk()
root.title("White Board")
root.geometry("1050x570+150+50")
root.configure(bg="#f2f3f5")
root.resizable(False, False)

current_x = 0
current_y = 0
color = 'black'
drawing_history = []  # Çizim hareketleri kaydolacak
undone_history = []   # Geri alınanlar için liste

def locate_xy(work):
    global current_x, current_y
    current_x = work.x
    current_y = work.y

def addLine(work):
    global current_x, current_y
    line = canvas.create_line((current_x, current_y, work.x, work.y), width=float(get_current_value()), fill=color, capstyle=ROUND, smooth=TRUE)
    current_x, current_y = work.x, work.y
    return line  # Çizgiyi geri almak için döndür

# Çizim işlemi tamamlanınca (fare tuvalden kalkınca)
def stop_drawing(event):
    global drawing_history
    drawing_history.append(drawing_temp.copy())  # Geçici çizim listesini kopyalayarak kaydet
    drawing_temp.clear()  # Geçici listeyi temizle

# Yeni bir çizim başladığında
def start_drawing(event):
    global drawing_temp
    drawing_temp = []  # Yeni geçici liste başlat
    canvas.bind('<B1-Motion>', draw)

# Çizim işlemi
def draw(event):
    line = addLine(event)
    drawing_temp.append(line)  # Bu çizimi geçici listeye ekle

# Renk değiştirme
def show_color(new_color):
    global color
    color = new_color

# Silgi modu
def use_eraser():
    global color
    color = '#ffffff'  # Silgi modu: Arka plan rengine geçiş

# Tuvali temizleme
def clear_canvas():
    canvas.delete('all')  # Tüm çizimi siler
    drawing_history.clear()  # Tüm geçmişi temizle
    undone_history.clear()   # Geri alınanları da temizle
    display_pallete()  # Renk paletini tekrar göster

# Geri alma işlemi
def undo_action():
    if drawing_history:
        last_items = drawing_history.pop()  # Son çizim hareketini al
        undone_history.append(last_items)   # Geri alınanlar listesine ekle
        for item in last_items:
            canvas.itemconfig(item, state='hidden')  # Bu çizimi tuvalden gizle

# İleri alma işlemi 
def redo_action():
    if undone_history:
        restored_items = undone_history.pop()  # Geri alınan çizimleri geri getir
        drawing_history.append(restored_items) # Tekrar çizim geçmişine ekle
        for item in restored_items:
            canvas.itemconfig(item, state='normal')  # Çizimi tekrar göster

# İkonlar ve butonlar
image_icon = PhotoImage(file="C:/Users/ElfGhost/Downloads/graphic-tablet.png")
root.iconphoto(False, image_icon)

color_box = PhotoImage()
Label(root, image=color_box, bg="#f2f3f5").place(x=10, y=20)

eraser_image = PhotoImage(file="c:\\Users\\ElfGhost\\Downloads\\eraser_603546.png")
Button(root, image=eraser_image, bg="#f2f3f5", command=use_eraser).place(x=30, y=400)

clear_image = PhotoImage(file="c:\\Users\\ElfGhost\\Downloads\\delete_12236949.png")
Button(root, image=clear_image, bg="#f2f3f5", command=clear_canvas).place(x=30, y=460)

undo_image = PhotoImage(file="c:\\Users\\ElfGhost\\Downloads\\undo_12175940.png")
Button(root, image=undo_image, bg="#f2f3f5", command=undo_action).place(x=25, y=20)

redo_image = PhotoImage(file="c:\\Users\\ElfGhost\\Downloads\\undo_12176225.png")
Button(root, image=redo_image, bg="#f2f3f5", command=redo_action).place(x=50, y=20)

# Renk paleti
colors = Canvas(root, bg="#ffffff", width=37, height=305, bd=0)
colors.place(x=30, y=60)

def display_pallete():
    color_list = ['black', 'gray', 'brown4', 'red', 'orange', 'yellow', 'green', 'blue', 'purple', 'pink', 'white', 'rosy brown']
    for i, col in enumerate(color_list):
        id = colors.create_rectangle((11, 11 + i * 25, 25, 25 + i * 25), fill=col)
        colors.tag_bind(id, '<Button-1>', lambda x, color=col: show_color(color))

display_pallete()

canvas = Canvas(root, width=930, height=500, background="white", cursor="hand2")
canvas.place(x=100, y=10)

canvas.bind('<Button-1>', lambda event: (start_drawing(event), locate_xy(event)))  # Çizim başladığında
canvas.bind('<ButtonRelease-1>', stop_drawing)  # Çizim bittiğinde
canvas.bind('<B1-Motion>', addLine)

current_value = tk.DoubleVar(value=1.0)

def get_current_value():
    return current_value.get()

def slider_changed(event):
    value_label.configure(text='{:.2f}'.format(get_current_value()))

slider = ttk.Scale(root, from_=1, to=100, orient='horizontal', command=slider_changed, variable=current_value)
slider.place(x=30, y=530)

value_label = ttk.Label(root, text='{:.2f}'.format(get_current_value()))
value_label.place(x=27, y=550)

root.mainloop()
