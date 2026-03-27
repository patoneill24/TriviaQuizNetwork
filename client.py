import socket

# This is Player 1's client. On the internet, a "client" is any program that initiates
# a connection to a server — your browser is a client when it connects to google.com.
# The client doesn't need a fixed port; the OS assigns it a random ephemeral port automatically.

# "localhost" means we're connecting to a server on the same machine.
# On the real internet this would be an IP address (e.g. "142.250.80.46") or domain name.
HOST = "localhost"
PORT = 5050  # The destination port on the server we want to reach

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

# Create a TCP socket using IPv4 (AF_INET) and connect to the server.
# This performs the TCP "three-way handshake" (SYN, SYN-ACK, ACK) — the same process
# your browser uses when it opens a connection to any website.
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))  # OS auto-assigns an ephemeral source port (e.g. 54321)
    startQuiz = input("Start quiz? (yes/no): ")

    # encode() converts the string to bytes — all data sent over a network is raw bytes,
    # not text. The server must decode() it back on the other end.
    s.sendall(startQuiz.encode())

    while True:
        if(startQuiz == "no"):
            print("Disconnecting from server")
            break

        # recv() blocks until the server sends something — up to 1024 bytes.
        # This back-and-forth (send/receive) is called a protocol — a agreed set of rules
        # for how client and server communicate, just like HTTP defines how browsers talk to web servers.
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
