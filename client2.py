import socket
import time


HOST = "localhost"  # The server's hostname or IP address
PORT = 8001  

score = 0

def determineWinner(finalScore):
    finalscoreString = finalScore.split(" ")
    player1 = int(finalscoreString[3])
    player2 = int(finalscoreString[7])
    scores = [player1, player2]
    if(player1 == player2):
        print("It's a tie!")
    elif(max(scores) == score):
        print("You won!")
    else:
        print("You lost!")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    startQuiz = input("Start quiz? (yes/no): ")
    s.sendall(startQuiz.encode())
    while True:
        if(startQuiz == "no"):
            print("Disconnecting from server")
            break
        data = s.recv(1024)
        print(f"Recieved: {data.decode()}\n")
        if(data.decode() == "No more questions"):
            s.sendall(str(score).encode())
            while True:
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
        feedback = s.recv(1024).decode()
        print(feedback)
        if(feedback == "Correct!"):
            score += 50
        proceed = input("Press any key + enter to continue: ")
        s.sendall(proceed.encode())