# Server-Client Chat Application

## Overview
This project implements a simple chat application using a client-server architecture. The server and client applications each have a graphical user interface (GUI) created using Tkinter. The server can handle multiple clients, and clients can send messages to the server, which can then broadcast messages to all connected clients or specific clients.

## Features
- Server:
  - GUI for monitoring and managing connected clients.
  - Ability to send messages to specific clients or broadcast to all clients.
  - Runs on a specified IP address and port.
- Client:
  - GUI for sending and receiving messages.
  - Connects to the server using a specified IP address and port.
  - Allows users to enter a username and send messages to the server.

## Requirements
- Python 3.x
- Tkinter (usually included with Python installations)
- A network connection

## Installation

### Cloning the Repository
To clone the repository, use the following steps:
1. Open a terminal or command prompt.
2. Navigate to the directory where you want to clone the repository.
3. Run the following command to clone the repository:
   ```sh
   git clone https://github.com/yourusername/Server-Client.git
Running the Server
Navigate to the project directory:
sh
Copy code
cd Server-Client
Open a terminal or command prompt.
Navigate to the directory containing the server.py file.
Run the server using the command:
sh
Copy code
python server.py
Running the Client
Open a terminal or command prompt.
Navigate to the directory containing the client.py file.
Run the client using the command:
sh
Copy code
python client.py
File Structure
server.py: The server application with a GUI for managing clients and broadcasting messages.
client.py: The client application with a GUI for connecting to the server and sending messages.
Configuration
By default, both the server and client are configured to run on the IP address 192.168.10.217 and port 8000. You can change these values in the respective Python files by modifying the server_ip and port variables.

Git Commands
Here are some basic Git commands you might find useful:

Clone a Repository

git clone https://github.com/yourusername/Server-Client.git
Check the Status of Your Repository
cd Server-Client
git status
Add Files to Staging Area

git add <filename>

# Or add all files:
git add .
Commit Changes
sh

git commit -m "Your commit message"
Push Changes to the Remote Repository

git push origin main
Pull Changes from the Remote Repository
git pull origin main
