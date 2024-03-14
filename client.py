import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox


class ClientGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Client")
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

        self.chat_box = scrolledtext.ScrolledText(self.root, width=50, height=20, state=tk.DISABLED)
        self.chat_box.pack(padx=10, pady=10)
        self.root.configure(bg="Grey")
        self.root.resizable(False, False)

        self.name_label = tk.Label(self.root, text="Enter your name:")
        self.name_label.pack()

        self.name_entry = tk.Entry(self.root, width=40)
        self.name_entry.pack(padx=10, pady=5)

        self.message_label = tk.Label(self.root, text="Enter your message:")
        self.message_label.pack()

        self.message_entry = tk.Entry(self.root, width=40)
        self.message_entry.pack(padx=10, pady=5)

        self.send_button = tk.Button(self.root, text="Send", width=10, command=self.send_message)
        self.send_button.pack(padx=10, pady=5)

        self.username_set = False  # Flag to track if username has been set

        threading.Thread(target=self.connect_to_server).start()

        self.root.mainloop()

    def connect_to_server(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_ip = "192.168.10.217"
            server_port = 8000
            self.client_socket.connect((server_ip, server_port))
            self.receive_username()
            threading.Thread(target=self.receive_messages).start()
        except Exception as e:
            print(f"Error: {e}")

    def receive_username(self):
        try:
            response = self.client_socket.recv(1024).decode("utf-8")
            self.insert_message(response)
        except Exception as e:
            print(f"Error: {e}")

    def receive_messages(self):
        try:
            while True:
                response = self.client_socket.recv(1024).decode("utf-8")
                self.insert_message(response)
        except Exception as e:
            print(f"Error: {e}")

    def send_message(self):
        if self.client_socket:
            if not self.username_set:  # Check if username has been set
                name = self.name_entry.get().strip()

                if not name:
                    messagebox.showerror("Error", "Please enter your name.")
                    return
                self.name_entry.config(state=tk.DISABLED)  # Disable the name entry field
                self.username_set = True  # Set username flag
            else:
                name = self.name_entry.get().strip()  # Fetch username
            message = self.message_entry.get()
            if message:
                full_message = f"{name}: {message}"
                self.client_socket.send(full_message.encode("utf-8"))
                self.message_entry.delete(0, tk.END)
                # Insert the sent message into the chat box
                self.insert_message(full_message)

    def insert_message(self, message):
        self.chat_box.config(state=tk.NORMAL)
        self.chat_box.insert(tk.END, f"{message}\n")
        self.chat_box.config(state=tk.DISABLED)


# Run the client GUI
ClientGUI()
