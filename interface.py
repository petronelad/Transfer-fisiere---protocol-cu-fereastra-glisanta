import threading
import tkinter as tk
from tkinter import *
from tkinter.filedialog import askopenfile
from tokenize import String
import SWsender
import SWreceiver

global text_box2
def GUI():

    # creare fereastra
    window = tk.Tk()
    window.title('Transfer de fisiere')

    # dimensiuni fereastra
    canvas = tk.Canvas(window, height=700, width=1200)
    canvas.pack()

    # imaginea de fundal
    background_image = tk.PhotoImage(file='img.png')
    background_label = tk.Label(window, image=background_image)
    background_label.place(relwidth=1, relheight=1)

    # casuta pentru Sender
    SenderView = tk.Frame(window, bg='#000000', bd=5)
    SenderView.place(relx=0.25, rely=0.05, relwidth=0.46, relheight=0.6, anchor='n')
    label1 = tk.Label(SenderView, text='Sender')
    label1.place(relwidth=1, relheight=1)

    # casuta pentru Receiver
    ReceiverView = tk.Frame(window, bg='#000000', bd=5)
    ReceiverView.place(relx=0.75, rely=0.05, relwidth=0.47, relheight=0.6, anchor='n')
    label = tk.Label(ReceiverView, text='Receiver')
    label.place(relwidth=1, relheight=1)

    # terminal box
    terminal_box = tk.Text(window, font='Helvetica 10')
    terminal_box.place(relx=0.1, rely=0.8, relwidth=0.8, relheigh=0.15)

    # buton de adaugare fisier
    browse = tk.StringVar()
    browse_btn = tk.Button(window, textvariable=browse, command=lambda: open_file(), font='Arial', bg='#ff9933',
                           fg='white', height=2, width=15)
    browse.set('Add file')
    browse_btn.place(relx=0.08, rely=0.7, relwidth=0.1, relheight=0.07)


    text_box = tk.Text(SenderView, height=500, width=500, padx=15, pady=15, font='Helvetica 10')
    text_box.place(relx=0.5, rely=0.05, relwidth=0.9, relheight=0.9, anchor='n')

    text_box2 = tk.Text(ReceiverView, height=500, width=500, padx=15, pady=15, font='Helvetica 10')
    text_box2.place(relx=0.5, rely=0.05, relwidth=0.9, relheight=0.9, anchor='n')

    # adaugare fisier
    def open_file():
        browse.set("Loading...")
        file = askopenfile(parent=window, mode='rb', title='Choose a file', filetype=[('Fisier text', '*.txt')])
        browse.set("Loaded")
        readFile = ''
        if file:
            readFile = file.read()
            print(readFile)
            print(readFile.decode())

        # afisarea textului in fereastra
        text_box.insert(END, readFile.decode())
        terminal_box.insert(END, "File loaded!\n")

    def send_pack_callback():
        if not text_box.get("1.0", "end-1c"):
            terminal_box.insert(END, "Nothing to send!\n")
        else:
            if connect_var.get()=="Connected":
                file = open("file_intermediate.txt", "wb")
                file.write(text_box.get("1.0", "end-1c").encode())
                t = threading.Thread(target=SWsender.send("file_intermediate.txt"))
                t.start()

                terminal_box.insert(END, "File sent!\n")
                file.close()
            else:
                terminal_box.insert(END, "Firstly connect!\n")


    def clear():
            browse.set('Add file')
            text_box.delete("1.0", END)
            text_box2.delete("1.0", END)
            terminal_box.delete("1.0", END)

    # clear Text Box
    button_clear = tk.Button(text="Clear", bg='#4169E1', command=clear,
                             font='Arial', fg='white', height=2, width=15)
    button_clear.place(relx=0.70, rely=0.7, relwidth=0.1, relheight=0.07)

    # buton Send
    button_send = tk.Button(text="Send", bg='#964B00', command=lambda: threading.Thread(target=send_pack_callback).start(),
                            font='Arial', fg='white', height=2, width=15)
    button_send.place(relx=0.32, rely=0.7, relwidth=0.1, relheight=0.07)

    def receive_pack_callback():
        terminal_box.insert(END, "Connected\n")
        connect_var.set("Connected")
        t = threading.Thread(target=SWreceiver.receive('file_received.txt'))
        t.start()
        terminal_box.insert(END, "End connection\n")


    # buton Connnect
    connect_var = StringVar()
    button_connect = tk.Button(textvariable=connect_var, command=lambda : threading.Thread(target=receive_pack_callback).start(),
                               font = 'Arial', bg='#00FF00', fg = 'white', height = 2, width = 15)
    connect_var.set("Connect")
    button_connect.place(relx = 0.20, rely = 0.7, relwidth = 0.1, relheight = 0.07)

    '''
    frame = tk.Frame(fereastra, bg='#ffffff', bd=5)
    frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')
    entry = tk.Entry(frame, font=40)
    entry.place(relwidth=0.65, relheight=1)
    '''
    window.mainloop()


if __name__ == "__main__":
    GUI()