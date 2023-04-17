import socket
from  threading import Thread
# ftp
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer


IP_ADDRESS = '127.0.0.1'
PORT = 8080   #1024 min


SERVER = None
clients = {}
BUFFER_SIZE=4096

def send_textmsg(client,msg):
    global clients
    other_client_name=clients[client]['connected_with']
    other_client_socket=clients[other_client_name]['client']

    final_msg=f'{client}> {msg}'
    print(final_msg,'234234234234243rdws')
    other_client_socket.send(final_msg.encode("utf-8"))


def handle_error_message(client):
    msg='''
    You need to connect with one of the clients before sending any message..
    Click on refresh to see all the available users
    '''

    client.send(msg.encode("utf-8"))


def connect_client(msg,client,client_name):
    global clients
    entered_client_name=msg[7:].strip()
    print(clients)

    if entered_client_name in clients:
        clients[entered_client_name]['connected_with']=client_name
        clients[client_name]['connected_with']=entered_client_name
        greet_msg=f'Hello {entered_client_name} {client_name} connected with you!'

        other_socket=clients[entered_client_name]['client']
        other_socket.send(greet_msg.encode("utf-8"))

        msg=f'You are connected with {entered_client_name}'
        client.send(msg.encode("utf-8"))

        
    else:
        other_client_name=clients[client_name]['connected_with']
        msg=f'you are already connected with {other_client_name}'
        client.send(msg.encode('utf-8'))


def disconnect_client(msg,client,client_name):
    global clients
    entered_client_name=msg[11:].strip()
    print(msg)
    print(clients)

    if entered_client_name in clients:
        clients[entered_client_name]['connected_with']=''
        clients[client_name]['connected_with']=''

        greet_msg=f'Hello {entered_client_name} you are succesfully disconnected with {client_name}'

        other_socket=clients[entered_client_name]['client']
        other_socket.send(greet_msg.encode("utf-8"))

        msg=f'You are succesfully disconnected with {entered_client_name}'
        client.send(msg.encode("utf-8"))
    

def handle_show_list(client):
    global clients
    counter=0;
    for c in clients:
        counter+=1
        client_address=clients[c]['addr'][0]
        connected_with=clients[c]['connected_with']
        msg=''

        if connected_with:
            msg=f"{counter}, {c} , {client_address}, connected with {connected_with}, tiul,\n"
        else:
            msg=f"{counter}, {c}, {client_address} , Available, tiul,\n"
        print(msg)
        client.send(msg.encode("utf-8"))

def handle_messages(client,msg,client_name):
    print(msg)
    if msg=='show list':
        handle_show_list(client)
    elif msg[:7]=='connect':
        connect_client(msg,client,client_name)
    elif msg[:10]=='disconnect':
        disconnect_client(msg,client,client_name)
    else:
        connected=clients[client_name]['connected_with']
        if connected:
            print(connected,'connected')
            send_textmsg(client,msg)
        else:
            handle_error_message(client)

def remove_client():
    pass

def handle_client(client,client_name):
    global BUFFER_SIZE
    welcome_msg=f'welcome, you are now connected to the server\nclick on refresh to see all avalialable users\nselect the user and click on connect to start chatting.'
    client.send(welcome_msg.encode('utf-8'))
    
    while True:
        try:
            BUFFER_SIZE=clients[client_name]['file_size']
            chunk=client.recv(BUFFER_SIZE)
            msg=chunk.decode('utf-8').strip().lower()
            if (msg):
                handle_messages(client,msg,client_name)
            else:
                remove_client(client)
        except:
            pass

def acceptConnections():
    global SERVER
    global clients

    while True:
        client, addr = SERVER.accept()
        client_name=client.recv(4096).decode('utf-8').lower()
        clients[client_name]={
            'client':client,
            'addr':addr,
            'connected_with':'',
            'file_name':'',
            'file_size':4096
        }
        print(clients)
        print(f'connection established with {client_name} : {addr}')
        thread=Thread(target=handle_client,args=(client,client_name))
        thread.start()


def setup():
    print("\n\t\t\t\t\t\tIP MESSENGER\n")

    # Getting global values
    global PORT
    global IP_ADDRESS
    global SERVER


    SERVER  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.bind((IP_ADDRESS, PORT))
    SERVER.listen(100)  #only hundred connections

    print("\t\t\t\tSERVER IS WAITING FOR INCOMMING CONNECTIONS...")
    print("\n")

    acceptConnections()


setup_thread = Thread(target=setup)           #receiving multiple messages
setup_thread.start()

# ------ Bolierplate Code End -----------
