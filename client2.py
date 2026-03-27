import socket

# This is Player 2's client. It is identical to client.py in structure —
# both clients connect to the same server port (5050), but the OS gives each
# a different ephemeral source port, so the server sees them as separate TCP connections.
# This mirrors how two browser tabs can both connect to the same website simultaneously.

HOST = "localhost"
PORT = 5050

score = 0

def determineWinner(finalScore):
    # Parse the final score string sent by the server and decide the outcome
    finalScoreString = finalScore.split(" ")
    player1 = int(finalScoreString[3])
    player2 = int(finalScoreString[7])
    scores = [player1, player2]
    if(player1 == player2):
        print("It's a tie!")
    elif(max(scores) == score):
        print("You won!")
    else:
        print("You lost!")

# Create a TCP/IPv4 socket and connect to the server.
# Even though client.py also connects to port 5050, there's no conflict:
# a TCP connection is uniquely identified by (src IP, src port, dst IP, dst port).
# Each client gets a different src port from the OS, so they're distinct connections.
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    startQuiz = input("Start quiz? (yes/no): ")

    # Strings must be encoded to bytes before sending — networks transmit raw bytes,
    # not Python strings. The server decodes them back on receipt.
    s.sendall(startQuiz.encode())

    while True:
        if(startQuiz == "no"):
            print("Disconnecting from server")
            break

        # Block and wait for data from the server (up to 1024 bytes).
        # This request/response pattern is the basis of most internet protocols —
        # HTTP, FTP, SMTP all work the same way at this level.
        data = s.recv(1024)
        print(f"Received: {data.decode()}\n")

        if(data.decode() == "No more questions"):
            # Quiz is over — send our final score to the server
            s.sendall(str(score).encode())
            while True:
                # Wait for the server to confirm both players are done
                final_score = s.recv(1024).decode()
                if(final_score != "Waiting for second player to finish"):
                    print(f"Final score: {final_score}")
                    determineWinner(final_score)
                    break
            break

        answer = input(" ")
        if(answer == "exit"):
            print("Disconnecting from server")
            print(f"Final score: {score}")
            break

        s.sendall(answer.encode())

        # Wait for the server's feedback on our answer
        feedback = s.recv(1024).decode()
        print(feedback)
        if(feedback == "Correct!"):
            score += 50

        proceed = input("Press any key + enter to continue: ")
        s.sendall(proceed.encode())
