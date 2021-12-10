import tkinter as tk
from tkinter import *
from tkinter.filedialog import askopenfile

class GUI():
    def __init__(self):
        #creare fereastra
        window = tk.Tk()
        window.title('Transfer de fisiere')

        #dimensiuni fereastra
        canvas = tk.Canvas(window, height=500, width=1000)
        canvas.pack()

        #imaginea de fundal
        background_image = tk.PhotoImage(file='img.png')
        background_label = tk.Label(window, image=background_image)
        background_label.place(relwidth=1, relheight=1)

        #casuta pentru Sender
        SenderView = tk.Frame(window, bg='#000000', bd=5)
        SenderView.place(relx=0.25, rely=0.05, relwidth=0.45, relheight=0.5, anchor='n')
        label1 = tk.Label(SenderView, text='Sender')
        label1.place(relwidth=1, relheight=1)

        #casuta pentru Receiver
        ReceiverView = tk.Frame(window, bg='#000000', bd=5)
        ReceiverView.place(relx=0.75, rely=0.05, relwidth=0.45, relheight=0.5, anchor='n')
        label = tk.Label(ReceiverView, text='Receiver')
        label.place(relwidth=1, relheight=1)

        #buton Connect
        buttonC = tk.Button(text="Send", bg='#00FF00')
        buttonC.place(relx=0.35, rely=0.6, relwidth=0.1, relheight=0.1)

        #buton Disconnect
        buttonD = tk.Button(text="Disconnect", bg='#FF0000')
        buttonD.place(relx=0.55, rely=0.6, relwidth=0.1, relheight=0.1)

        #buton de adaugare fisier
        browse = tk.StringVar()
        browse_btn = tk.Button(window, textvariable=browse, command=lambda: open_file(), font='Arial', bg='#ff9933',
                               fg='white', height=2, width=15)
        browse.set('Adauga fisier')
        browse_btn.place(relx=0.44, rely=0.8, relwidth=0.15, relheight=0.15)

        #adaugare fisier
        def open_file():
            print("Fisierul s-a deschis!")
            browse.set("Se incarca...")
            file = askopenfile(parent=window, mode='rb', title='Alege un fisier', filetype=[('Fisier text', '*.txt')])
            browse.set("Incarcat")

            #flag=0

            if file:
                #print("Fisierul s-a incarcat.")
                readFile = file.read();
                #print(citireFisier)

            #afisarea textului in fereastra
            text_box = tk.Text(SenderView, height=500, width=500, padx=15, pady=15)
            text_box.insert(1.0, readFile)
            text_box.tag_configure('center', justify='center')
            text_box.tag_add('center',1.0,'end')
            text_box.place(relx=0.5, rely=0.05, relwidth=0.9, relheight=0.9, anchor='n')

            #casuta de introdus text
            '''
            frame = tk.Frame(fereastra, bg='#ffffff', bd=5)
            frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')
            entry = tk.Entry(frame, font=40)
            entry.place(relwidth=0.65, relheight=1)
            '''
        window.mainloop()

if __name__ == "__main__":
        interface = GUI()