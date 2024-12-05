## Overview

**Project Title**: Trivia Game

**Project Description**: This project is a trivia game where two people can connect and play against each other. The subject of the game is about planets in our solar system. After both players have answered each question, they will be notified if they won, lost, or tied with the other player. 

**Project Goals**: To create a fun trivia game that can be played by two people. 

## Instructions for Build and Use

Steps to build and/or run the software:

1. Use pip to install the socket and threading libraries:
```bash
pip install socket
pip install threading
```
2. Run the server.py file:
```bash
python3 server.py
```
3. Run the client.py file on another terminal:
```bash
python3 client.py
```
4. Run the other client.py file on another terminal:
```bash
python3 client2.py
```

Instructions for using the software:

1. Run the server.py file, and the two client files, all on seperate terminals within the same machine.
2. You will be asked wheter or not you'd like to start the trivia game. Type 'yes' to start the game.
3. You'll be asked three multiple choice questions, and then be given a score based on how many questions you answered correctly. You'll also
be notified if you won, lost, or tied with the other player.

## Development Environment 

To recreate the development environment, you need the following software and/or libraries with the specified versions:

* Python 3 or later
* socket library
* threading library

## Useful Websites to Learn More

I found these websites useful in developing this software:

* [Building a TCP Server-Client with Sockets in Pyton](https://www.scaler.com/topics/cyber-security/build-a-tcp-server-client-with-sockets-in-python/)
* [Python socket Programming Tutorial by Digital Ocean](https://www.digitalocean.com/community/tutorials/python-socket-programming-server-client)
* [Python socket programming Youtube tutorial ](https://www.youtube.com/watch?v=3QiPPX-KeSc)

## Future Work

The following items I plan to fix, improve, and/or add to this project in the future:

* [ ] Add more questions to the trivia game and the ability to choose a category.
* [ ] Add a GUI to the game.
* [ ] Add a timer to the game.