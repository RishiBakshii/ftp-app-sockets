import socket
from threading import Thread
from tkinter import *
from tkinter import ttk
from tkinter import filedialog


PORT  = 8080
IP_ADDRESS = '127.0.0.1'
SERVER = None
BUFFER_SIZE = 4096

sending_file=None
name=None
textarea=None
labelchat=None
listbox=None
mainWindow=None
primary_font=("calibri",10)


def recv_message():
    global SERVER,BUFFER_SIZE,textarea,listbox
    while True:
        chunk=SERVER.recv(BUFFER_SIZE)
        print(chunk)
        try:
            if ('tiul') in chunk.decode("utf-8") and '1.0,' not in chunk.decode("utf-8"):
                letter_list=chunk.decode('utf-8').split(',')
                print(letter_list)
                listbox.insert(letter_list[0],letter_list[0]+": "+letter_list[1]+ ':' + letter_list[3] + " "+letter_list[5])
                print(letter_list[0],letter_list[0]+": "+letter_list[1]+ ':' + letter_list[3] + " "+letter_list[5])
            else:
                textarea.insert(END,"\n"+chunk.decode('ascii'))
                textarea.see('end')
                print(chunk.decode('ascii'))
        except:
            pass

def show_client_list():
    global SERVER,listbox
    SERVER.send("show list".encode('ascii'))

def connect_server():
    global SERVER,name
    cname=name.get()
    SERVER.send(cname.encode("utf-8"))


def openChatWindow():
    global primary_font,name
    window=Tk()
    window.title("Messenger")
    window.geometry("500x350")

    namelabel=Label(window,text='Enter you name',font=primary_font)
    namelabel.place(x=10,y=10)

    name=Entry(window,width=30,font=primary_font)
    name.place(x=120,y=10)
    name.focus()

    # connect button
    connect_TO_server=Button(window,text='Connect to Chat Server',bd=1,font=primary_font,command=connect_server)
    connect_TO_server.place(x=350,y=10)

    seperator=ttk.Separator(window,orient='horizontal')
    seperator.place(x=0,y=35,relwidth=1,height=0.1)

    labelUsers=Label(window,text='Active Users',font=primary_font)
    labelUsers.place(x=10,y=50)

    list_box=Listbox(window,height=5,width=70,activestyle='dotbox',font=primary_font)
    list_box.place(x=10,y=70)

    scroll_bar1=Scrollbar(list_box)
    scroll_bar1.place(relheight=1,relx=1)
    scroll_bar1.config(command=list_box.yview)


    connect=Button(window,text='Connect',bd=1,font=primary_font)
    connect.place(x=280,y=160)

    refresh_btn=Button(window,text='Refresh',bd=1,font=primary_font,command=show_client_list)
    refresh_btn.place(x=430,y=160)

    disconnect=Button(window,text='Disconnect',bd=1,font=primary_font)
    disconnect.place(x=350,y=160)

    labelchat=Label(window,text='Chat Window',font=primary_font)
    labelchat.place(x=10,y=180)

    textarea=Text(window,width=67,height=6,font=primary_font)
    textarea.place(x=10,y=200)


    scroll_bar2=Scrollbar(textarea)
    scroll_bar2.place(relheight=1,relx=1)
    scroll_bar2.config(command=textarea.yview)


    attach_btn=Button(window,text='Attach and Send',font=primary_font,bd=1)
    attach_btn.place(x=10,y=300)

    text_msg=Entry(window,width=43,font=primary_font)
    text_msg.place(x=110,y=300)

    send_btn=Button(window,text='Send',font=primary_font,bd=1)
    send_btn.place(x=450,y=300)



    window.mainloop()



def setup():
    global SERVER
    global PORT
    global IP_ADDRESS

    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.connect((IP_ADDRESS, PORT))

    recv_thread=Thread(target=recv_message)
    recv_thread.start()

    openChatWindow()

setup()
