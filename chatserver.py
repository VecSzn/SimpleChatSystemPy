import socket
import threading
import time
import pickle


# List to store connected clients

channels = []
#Bind Host
HOST = '0.0.0.0'

class MainChannel:
    def __init__(self, name, port):
        self.name = name
        self.port = port
        self.host = HOST
        self.clients = []

    def start_chat_server(self):
        # Server configuration

        # Create a socket object
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to a specific address and port
        server_socket.bind((self.host, self.port))

        # Listen for incoming connections
        server_socket.listen(1)
        print('Main server started on {}:{}'.format(self.host, self.port))
        sendcount = threading.Thread(target=self.keepsendinginfo,args="a",)
        sendcount.start()
        while True:
            # Accept a connection from a client
            client_socket, client_address = server_socket.accept()
            print('Client connected:', client_address)
            
            # Create a thread to handle the client
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
            client_thread.start()
    def keepsendinginfo(self, string):
        while True:

            fixedchannel=[]
            for channel in channels:
                newchannel = FixedChannel(channel.name,channel.port,channel.password)
                fixedchannel.append(newchannel)
            for client in self.clients:
                
                serialized_data = pickle.dumps(fixedchannel)
                if serialized_data:
                    client.sendall(serialized_data)
                
            time.sleep(1)


    def handle_client(self,client_socket, client_address):
        # Add the client to the list
        self.clients.append(client_socket)
        while True:
            try:
                # Receive data from the client
                client_socket.recv(1024).decode('utf-8')
            except:
                # If an error occurs, remove the client from the list and close the connection
                self.clients.remove(client_socket)
                client_socket.close()
                break


    def __str__(self):
        return f"Channel Name: {self.name}\nChannel Port: {self.port}\n"

class FixedChannel:
    def __init__(self, name, port, password):
        self.name = name
        self.port = port
        self.host = HOST
        self.password = password


class Channel:
    def __init__(self, name, port, password):
        self.name = name
        self.port = port
        self.host = HOST
        self.password = password
        self.clients = []

    def start_chat_server(self):
        # Server configuration

        # Create a socket object
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to a specific address and port
        server_socket.bind((self.host, self.port))

        # Listen for incoming connections
        server_socket.listen(1)
        print(f'[{self.name}]Chat server started on {self.host}:{self.port}')
        sendcount = threading.Thread(target=self.keepsendinginfo,args="a",)
        sendcount.start()
        while True:
            # Accept a connection from a client
            client_socket, client_address = server_socket.accept()
            print(f'[{self.name}]Client connected:', client_address)
            
            # Create a thread to handle the client
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
            client_thread.start()
    def keepsendinginfo(self, string):
        while True:
            for client in self.clients:
                chatmembercount = f'Player_Count_Update_{len(self.clients)}'
                client.sendall(chatmembercount.encode('utf-8'))
            time.sleep(1)


    def handle_client(self,client_socket, client_address):
        # Add the client to the list
        self.clients.append(client_socket)
        
        while True:
            try:
                # Receive data from the client
                data = client_socket.recv(1024).decode('utf-8')
                if data:
                    print(f'[{self.name}][{client_address}] {data}')
                    # Broadcast the received data to all other clients
                    for client in self.clients:
                        if client != client_socket:
                            client.sendall(data.encode('utf-8'))
                else:
                    # If no data received, remove the client from the list and close the connection
                    self.clients.remove(client_socket)
                    client_socket.close()
                    break
            except:
                # If an error occurs, remove the client from the list and close the connection
                self.clients.remove(client_socket)
                client_socket.close()
                break


    def __str__(self):
        return f"Channel Name: {self.name}\nChannel Port: {self.port}\n"

    


MainChannel1 = MainChannel("主频道", 11112)
MainChannel_thread = threading.Thread(target=MainChannel1.start_chat_server)
MainChannel_thread.start()

channel1 = Channel("频道 1", 49756, None)
channel1_thread = threading.Thread(target=channel1.start_chat_server)
channel1_thread.start()
channels.append(channel1)

channel2 = Channel("频道 2", 33259, None)
channel2_thread = threading.Thread(target=channel2.start_chat_server)
channel2_thread.start()
channels.append(channel2)

channel3 = Channel("频道 3", 23578, None)
channel3_thread = threading.Thread(target=channel3.start_chat_server)
channel3_thread.start()
channels.append(channel3)

channel4 = Channel("[密码]频道 4", 38293, "123456")
channel4_thread = threading.Thread(target=channel4.start_chat_server)
channel4_thread.start()
channels.append(channel4)

channel5 = Channel("[密码]频道 5", 32589, "654321")
channel5_thread = threading.Thread(target=channel5.start_chat_server)
channel5_thread.start()
channels.append(channel5)


