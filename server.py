import socket
import threading

# The internet works by breaking communication into layers. At the bottom is IP (Internet Protocol),
# which routes packets between machines using IP addresses. On top of that is TCP (Transmission
# Control Protocol), which provides a reliable, ordered connection between two endpoints.
# A "socket" is the programming interface to that TCP/IP stack — it's how your code sends
# and receives data over a network, just like any website or app does.

# Quiz questions stored as a dictionary: question text -> correct answer letter
Questions_dictionary = {
    'Which planet in our solar system is the hottest?\nA. Mercury\nB. Venus\nC. Mars\nD. Jupiter': 'B',
    'Which planet in our solar system is the smallest?\nA. Mercury\nB. Venus\nC. Mars\nD. Earth': 'A',
    'Which planet in our solar system is the largest?\nA. Mercury\nB. Venus\nC. Jupiter\nD. Earth': 'C'
}

scores = []
PORT = 5050

def handle_client(client_socket):
    # This function runs in its own thread for each connected client.
    # On the internet, a server (e.g. google.com) handles thousands of clients simultaneously
    # the same way — each connection gets its own handler running in parallel.
    global disconnection_count
    try:
        while True:
            # recv() blocks and waits until the client sends data — just like a web server
            # waiting for an HTTP request. The 1024 means read up to 1024 bytes at a time.
            start = client_socket.recv(1024).decode()
            if(start == "no"):
                print("Client connection closed")
                break

            # Send each question to the client and wait for their answer
            for question, answer in Questions_dictionary.items():
                # sendall() sends data to the client — like a server sending an HTTP response
                client_socket.sendall(f"{question}\nChoose the correct answer: ".encode())
                data = client_socket.recv(1024).decode()
                if not data:
                    print("Client connection closed")
                    break
                print(f"Received: {data}")

                # Check the answer and send feedback
                if(data.lower() == answer.lower()):
                    client_socket.sendall("Correct!".encode())
                    client_socket.recv(1024).decode()  # wait for client to acknowledge before continuing
                else:
                    client_socket.sendall("Incorrect!".encode())
                    client_socket.recv(1024).decode()  # wait for client to acknowledge before continuing

            # All questions done — ask client for their final score
            client_socket.send("No more questions".encode())
            score = client_socket.recv(1024).decode()
            print(f"Final score: {score}")
            scores.append(score)

            # If only one player has finished, tell them to wait for the other
            if(len(scores) == 1):
                client_socket.sendall("Waiting for second player to finish".encode())

            # Wait until both players are done, then send the final results to this client
            while True:
                if(len(scores) == 2):
                    client_socket.sendall(f"Player 1 score: {scores[0]} \nPlayer 2 score: {scores[1]}".encode())
                    print('Client Disconnected')
                    break
            if(len(scores) == 2):
                break
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Always close the client socket when done to free up OS resources.
        # On the internet, servers close connections after a response for the same reason.
        client_socket.close()

def start_server(port):
    # AF_INET means we're using IPv4 addresses (e.g. 192.168.1.1) — the same addressing
    # system used across the internet. SOCK_STREAM means TCP, which guarantees data
    # arrives in order and without loss (unlike UDP, which is faster but unreliable).
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # bind() claims a specific port on this machine. Port numbers are how the OS knows
    # which program should receive incoming data — like apartment numbers in a building.
    # Well-known ports: 80 = HTTP, 443 = HTTPS, 5050 = our custom app.
    server_socket.bind(('localhost', port))

    # listen() marks this socket as passive — it will receive connections, not initiate them.
    # The argument (5) is the backlog: how many connections can queue up waiting to be accepted.
    server_socket.listen(5)
    print(f"Server listening on port {port}")

    while True:
        # accept() blocks until a client connects. It returns a brand new socket object
        # dedicated to that one client, plus the client's (IP, port) address.
        # The original server_socket keeps listening for the next client.
        # This is exactly how real servers work — one listening socket, many client sockets.
        client_socket, addr = server_socket.accept()
        print(f"Connected to {addr} on port {port}")

        # Spawn a new thread for each client so they can be handled in parallel.
        # Without threading, the server would be stuck talking to one client at a time.
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

def main():
    start_server(PORT)

if __name__ == "__main__":
    main()
