# ------- Bolierplate Code Start -----
import socket
from  threading import Thread
IP_ADDRESS = '127.0.0.1'
PORT = 8080   #1024 min


SERVER = None
clients = {}
BUFFER_SIZE=4096

def handle_show_list(client):
    global clients
    counter=0;
    for c in clients:
        counter+=1
        client_address=clients[c]['addr']
        connected_with=clients[c]['connected_with']
        msg=''

        if connected_with:
            msg=f'{counter}, {c} , {client_address}, connected with {connected_with}, tiul,\n'
        else:
            msg=f'{counter}, {c}, {client_address} , available, tiul,\n'
        print(msg)
        client.send(msg.encode("utf-8"))

def handle_messages(client,msg,client_name):
    if msg=='show list':
        handle_show_list(client)

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
