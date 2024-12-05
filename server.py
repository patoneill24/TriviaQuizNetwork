import socket
import threading
# import time

# Current issues: Not all of the questions are being sent to the client and formatting is off
# Next step: Fix the formatting of the questions and answers and find a way to provide different answers for each question (dictionary?)

Questions_dictionary = {
    'Which planet in our solar system is the hottest?\nA. Mercury\nB. Venus\nC. Mars\nD. Jupiter': 'B',
    'Which planet in our solar system is the smallest?\nA. Mercury\nB. Venus\nC. Mars\nD. Earth': 'A',
    'Which planet in our solar system is the largest?\nA. Mercury\nB. Venus\nC. Jupiter\nD. Earth': 'C'
}

scores= []

def handle_client(client_socket):   
    global disconnection_count
    try:
        while True:
            start = client_socket.recv(1024).decode()
            if(start == "no"):
                print("Client connection closed")
                break
            for question, answer in Questions_dictionary.items():
                client_socket.sendall(f"{question}\nChoose the correct answer: ".encode())
                data = client_socket.recv(1024).decode()
                # print(f" Answer Received: {data}")
                if not data:
                    print("Client connection closed")
                    break
                print(f"Received: {data}")
                if(data == answer):
                    client_socket.sendall("Correct!".encode())
                    client_socket.recv(1024).decode()
                    # client_socket.sendall(str(50).encode())
                else:
                    client_socket.sendall("Incorrect!".encode())
                    client_socket.recv(1024).decode()
                    # client_socket.sendall(str(0).encode())
            client_socket.send("No more questions".encode())
            score = client_socket.recv(1024).decode()
            print(f"Final score: {score}")
            scores.append(score)
            if(len(scores) == 1):
                client_socket.sendall(f"Waiting for second player to finish".encode())
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
        client_socket.close()

def start_server(port):
    # AF_INET is the address family for IPv4 and SOCK_STREAM is the socket type for TCP connections
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # server will only accept connections from the same machine
    server_socket.bind(('localhost', port))
    server_socket.listen(5)
    print(f"Server listening on port {port}")
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connected to {addr} on port {port}")
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

def main():
    port1 = 5050
    port2 = 8001

    thread1 = threading.Thread(target=start_server, args=(port1,))
    thread2 = threading.Thread(target=start_server, args=(port2,))


    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

if __name__ == "__main__":
    main()