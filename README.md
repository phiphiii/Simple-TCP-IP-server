# Multi-User Asynchronous Chat with ASCII-Art Conversion

A Python-based networking application consisting of a server and a client capable of asynchronous communication via TCP/IP.

## Core Features

* **User Nicknames**: Upon starting the client, users are prompted to enter a custom nickname, which identifies them to all other participants in the chat.
* **Asynchronous Communication**: Implemented using the `threading` module to ensure that the input prompt is never blocked. Users can send and receive messages simultaneously at any time.
* **Multi-Client Server**: The server architecture supports an arbitrary number of simultaneous connections, managing each user in a dedicated thread.
* **ASCII-Art Image Transfer**: Features a specialized command to convert local image files into ASCII-art strings using the `ascii_magic` library, which are then broadcast to all connected peers.
* **Localhost Simulation**: Designed for easy testing by running multiple client instances on 127.0.0.1.



## Technical Specifications

* **Networking**: Built on the `socket` library using `AF_INET` (IPv4) and `SOCK_STREAM` (TCP).
* **Concurrency**: 
    * **Client**: Utilizes a background daemon thread for continuous message reception (`get_msg`) while the main thread handles user input.
    * **Server**: Uses a main loop to accept connections (`server.accept()`) and spawns new threads to handle individual client logic (`send_msg` / `handle_client`).
* **Data Handling**: 
    * Messages are encoded and decoded using UTF-8.
    * Optimized buffer size to handle large ASCII-art character blocks.

## Installation & Usage

1. **Install dependencies**:
   ```bash
   pip install ascii_magic
