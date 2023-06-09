import socket
from threading import Thread
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
# new
import ftplib
from ftplib import FTP
import os
import ntpath
import time

PORT  = 8080
IP_ADDRESS = '127.0.0.1'
SERVER = None
BUFFER_SIZE = 4096

filePathLabel=None
sending_file=None
downloading_file=None
name=None
textarea=None
labelchat=None
list_box=None
mainWindow=None
text_msg=None
primary_font=("calibri",10)

def browse_files():
    global filePathLabel,textarea

    try:
        filename=filedialog.askopenfilename()

        filePathLabel.configure(text=filename)

        HOSTNAME='127.0.0.1'
        USERNAME='lftpd'
        PASSWORD='lftpd'
        
        ftp_server=FTP(HOSTNAME,USERNAME,PASSWORD)
        ftp_server.encoding='utf-8'

        ftp_server.cwd('shared_files')
        fname=ntpath.basename(filename)

        with open(filename,'rb') as file:
            ftp_server.storbinary(f'STOR {fname}',file)
            ftp_server.dir()
            ftp_server.quit()

        msg=f'send {fname}'
        print(msg)

        if msg[:4]=='send':
            print("please wait")
            textarea.insert(END,'\nplease wait')
            textarea.see(END)
            
            sending_file=msg[5:]
            file_size=get_file_size('shared_files/'+sending_file)
            final_msg=f'{msg} {file_size}'

            print(final_msg)

            SERVER.send(final_msg.encode("utf-8"))
            textarea.insert(END,'\nIn Process')

    except FileNotFoundError:
        print("Cancel Button pressed")
    


def send_message():
    global text_msg,SERVER,textarea
    msg_to_send=text_msg.get()

    SERVER.send(msg_to_send.encode("utf-8"))
    textarea.insert(END,f"\nyou> {msg_to_send}")
    textarea.see(END)
    text_msg.delete(0,END)
    

def get_file_size(file_name):
    with open(file_name,'rb') as file:
        chunk=file.read()
        return len(chunk)

def browseFiles():
    pass

def recv_message():
    global SERVER,BUFFER_SIZE,textarea,list_box,labelchat
    while True:
        chunk=SERVER.recv(BUFFER_SIZE)
        try:
            if ('tiul') in chunk.decode("utf-8") and '1.0,' not in chunk.decode("utf-8"):
                letter_list=chunk.decode('utf-8').split(',')
                print(letter_list)
                list_box.insert(letter_list[0],letter_list[0]+":"+letter_list[1]+ ':' + letter_list[3])

            elif chunk.decode('utf-8')=='Access Granted':
                print('working!!!!!!!!!!!!!!!!!!!!!!!!!')

                labelchat.configure(text='')
                textarea.insert(END,'\n'+chunk.decode('utf-8'))
                textarea.see('end')

            elif chunk.decode('utf-8')=='declined your request':
                labelchat.configure(text='')
                textarea.insert(END,chunk.decode('utf-8'))
                textarea.see('end')
            
            elif 'download' in chunk.decode('utf-8'):
                print(chunk.decode('utf-8').split(' '))
                downloading_file=chunk.decode().split(' ')[6]
                buffer_size=chunk.decode().split(' ')[10]
                print(downloading_file,buffer_size)

                textarea.insert(END,f'{downloading_file} {buffer_size}')
                textarea.see('end')
            
            else:
                textarea.insert(END,"\n"+chunk.decode('ascii'))
                textarea.see('end')
        except:
            pass

def show_client_list():
    global SERVER,list_box
    list_box.delete(0,END)
    SERVER.send("show list".encode('ascii'))

def connect_server():
    global SERVER,name
    cname=name.get()
    SERVER.send(cname.encode("utf-8"))

def connectWithClient():
    global SERVER,list_box

    list_item=list_box.get(ANCHOR).split(':')
    # print(list_item)
    user=list_item[1]
    msg='connect'+user.strip()
    SERVER.send(msg.encode("utf-8"))

def disconnectWithClient():
    list_item=list_box.get(ANCHOR).split(':')
    # print(list_item)
    user=list_item[1]
    msg='disconnect'+user
    SERVER.send(msg.encode("utf-8"))


def openChatWindow():
    global primary_font,name,list_box,textarea,text_msg,filePathLabel,labelchat
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


    connect=Button(window,text='Connect',bd=1,font=primary_font,command=connectWithClient)
    connect.place(x=280,y=160)

    refresh_btn=Button(window,text='Refresh',bd=1,font=primary_font,command=show_client_list)
    refresh_btn.place(x=430,y=160)

    disconnect=Button(window,text='Disconnect',bd=1,font=primary_font,command=disconnectWithClient)
    disconnect.place(x=350,y=160)

    labelchat=Label(window,text='Chat Window',font=primary_font)
    labelchat.place(x=10,y=180)

    textarea=Text(window,width=67,height=6,font=primary_font)
    textarea.place(x=10,y=200)


    scroll_bar2=Scrollbar(textarea)
    scroll_bar2.place(relheight=1,relx=1)
    scroll_bar2.config(command=textarea.yview)


    attach_btn=Button(window,text='Attach and Send',font=primary_font,bd=1,command=browse_files)
    attach_btn.place(x=10,y=300)

    text_msg=Entry(window,width=43,font=primary_font)
    text_msg.place(x=110,y=300)

    send_btn=Button(window,text='Send',font=primary_font,bd=1,command=send_message)
    send_btn.place(x=450,y=300)

    filePathLabel=Label(window,text='',font=primary_font,fg='blue')
    filePathLabel.place(x=10,y=330)

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
