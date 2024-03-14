import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk

class ServerGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Server")
        self.root.maxsize(350, 550)
        self.root.iconbitmap('chaticon.ico')

        # Get the screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Set the width and height of the GUI
        gui_width = 350
        gui_height = 550

        # Calculate the position of the GUI window
        x_position = screen_width - gui_width - 20  # Right corner
        y_position = screen_height - gui_height - 100  # Above the taskbar

        self.root.geometry(f"{gui_width}x{gui_height}+{x_position}+{y_position}")

        self.chat_box = scrolledtext.ScrolledText(self.root, width=50, height=20)
        self.chat_box.pack(padx=10, pady=10)
        self.root.configure(bg="#FFA500")
        self.root.resizable(False, False)

        self.message_entry = tk.Entry(self.root, width=40)
        self.message_entry.pack(padx=10, pady=5)

        self.client_dropdown = ttk.Combobox(self.root, width=37, state="readonly")
        self.client_dropdown.pack(padx=10, pady=5)

        self.send_button = tk.Button(self.root, text="Send Message", width=20, command=self.send_message)
        self.send_button.pack(padx=10, pady=5)

        self.send_to_all_button = tk.Button(self.root, text="Send to All", width=20, command=self.send_to_all_clients)
        self.send_to_all_button.pack(padx=10, pady=5)

        self.clients = {}
        self.client_count = 0

        threading.Thread(target=self.run_server).start()

        self.root.mainloop()

    def run_server(self):
        server_ip = "192.168.10.217"  # Listen on all available network interfaces
        port = 8000  # server port number
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((server_ip, port))
        self.server.listen()
        self.chat_box.insert(tk.END, f"Listening on port {server_ip}:{port}\n")

        while True:
            client_socket, addr = self.server.accept()
            threading.Thread(target=self.handle_client, args=(client_socket, addr)).start()

    def handle_client(self, client_socket, addr):
        username = f"Client{self.client_count}"
        self.client_count += 1
        self.clients[username] = client_socket
        self.update_client_dropdown()  # Update client dropdown
        self.notify_client_connected(client_socket, username)

        try:
            while True:
                request = client_socket.recv(1024).decode("utf-8")
                if not request:
                    break
                self.display_received_message(username, request)
        except Exception as e:
            print(f"Error when handling client: {e}")
        finally:
            client_socket.close()
            del self.clients[username]
            self.display_server_message(f"{username} disconnected\n")
            self.update_client_dropdown()  # Update client dropdown

    def display_received_message(self, username, message):
        self.chat_box.config(state=tk.NORMAL)
        self.chat_box.insert(tk.END, f"{message}\n")
        self.chat_box.config(state=tk.DISABLED)  # Disable the text widget after insertion

    def display_server_message(self, message):
        self.chat_box.config(state=tk.NORMAL)
        self.chat_box.insert(tk.END, f"{message}\n")
        self.chat_box.config(state=tk.DISABLED)  # Disable the text widget after insertion
        self.message_entry.delete(0, tk.END)

    def send_message(self):
        recipient = self.client_dropdown.get()
        if recipient:
            message = self.message_entry.get()
            if message:
                client_socket = self.clients.get(recipient)
                if client_socket:
                    client_socket.send(f"Server: {message}".encode("utf-8"))
                    self.display_server_message(f"Server: {message} sent to {recipient} ")
                else:
                    messagebox.showerror("Error", "Selected client not found.")
            else:
                messagebox.showerror("Error", "Please enter a message.")
        else:
            messagebox.showerror("Error", "Please select a client.")

    def send_to_all_clients(self):
        message = self.message_entry.get()
        if message:
            for client_socket in self.clients.values():
                client_socket.send(f"Server  {message}".encode("utf-8"))
            self.display_server_message(f"Server : {message} ")
        else:
            messagebox.showerror("Error", "Please enter a message.")

    def notify_client_connected(self, client_socket, username):
        try:
            client_socket.send(f"Connected to server as {username}".encode("utf-8"))
        except Exception as e:
            print(f"Error when sending notification to client: {e}")

    def update_client_dropdown(self):
        self.client_dropdown["values"] = list(self.clients.keys())

# Run the server GUI
ServerGUI()
