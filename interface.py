import tkinter as tk
from tkinter import *
from tkinter.filedialog import askopenfile
import SWsender

class GUI():
    def __init__(self):
        #creare fereastra
        window = tk.Tk()
        window.title('Transfer de fisiere')

        #dimensiuni fereastra
        canvas = tk.Canvas(window, height=700, width=1200)
        canvas.pack()

        #imaginea de fundal
        background_image = tk.PhotoImage(file='img.png')
        background_label = tk.Label(window, image=background_image)
        background_label.place(relwidth=1, relheight=1)

        #casuta pentru Sender
        SenderView = tk.Frame(window, bg='#000000', bd=5)
        SenderView.place(relx=0.25, rely=0.05, relwidth=0.46, relheight=0.6, anchor='n')
        label1 = tk.Label(SenderView, text='Sender')
        label1.place(relwidth=1, relheight=1)

        #casuta pentru Receiver
        ReceiverView = tk.Frame(window, bg='#000000', bd=5)
        ReceiverView.place(relx=0.75, rely=0.05, relwidth=0.47, relheight=0.6, anchor='n')
        label = tk.Label(ReceiverView, text='Receiver')
        label.place(relwidth=1, relheight=1)

        #terminal box
        terminal_box = tk.Text(window, font='Helvetica 10')
        terminal_box.place(relx=0.1, rely=0.8, relwidth=0.8, relheigh=0.15)

        #buton de adaugare fisier
        browse = tk.StringVar()
        browse_btn = tk.Button(window, textvariable=browse, command=lambda: open_file(), font='Arial', bg='#ff9933',
                               fg='white', height=2, width=15)
        browse.set('Add file')
        browse_btn.place(relx=0.08, rely=0.7, relwidth=0.1, relheight=0.07)

        # TO DO: 
        # button for delete content from text box (between ADD file and SEND)

        # text_box = tk.Text(SenderView, height=500, width=500, padx=15, pady=15, font='Helvetica 10')
        # text_box.place(relx=0.5, rely=0.05, relwidth=0.9, relheight=0.9, anchor='n')
        entry_box = tk.Entry(SenderView, font='Helvetica 10')
        entry_box.place(relwidth=0.65, relheight=1)

        #adaugare fisier
        def open_file():
            browse.set("Se incarca...")
            file = askopenfile(parent=window, mode='rb', title='Alege un fisier', filetype=[('Fisier text', '*.txt')])
            browse.set("Incarcat")

            readFile = ''
            if file:
                readFile = file.read()

            #afisarea textului in fereastra
            entry_box.insert(END, readFile)
            terminal_box.insert(END,"Fisierul s-a incarcat!\n")
                                # text_box.tag_add('center',1.0,'end')

        #TO DO: verify how to do the first line not blank
        def send_pack_callback():
            if not entry_box.get():
                 terminal_box.insert(END, "Nothing to send!\n")
            else:
                print("-------------------\n")
                print(entry_box.get())
                print("-------------------\n")                
                SWsender.send(entry_box.get())

        # buton Send
        button_send = tk.Button(text="Send", bg='#00FF00', command=lambda: send_pack_callback())
        button_send.place(relx=0.20, rely=0.7, relwidth=0.1, relheight=0.07)

        # buton Disconnect
        buttonD = tk.Button(text="Disconnect", bg='#FF0000')
        buttonD.place(relx=0.70, rely=0.7, relwidth=0.1, relheight=0.07)

        #casuta de introdus text -> this is done with text_box from sender
        '''
        frame = tk.Frame(fereastra, bg='#ffffff', bd=5)
        frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')
        entry = tk.Entry(frame, font=40)
        entry.place(relwidth=0.65, relheight=1)
        '''
        window.mainloop()

if __name__ == "__main__":
        interface = GUI()