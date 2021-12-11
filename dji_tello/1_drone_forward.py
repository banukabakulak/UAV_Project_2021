# This example script demonstrates how to use Python to fly Tello in a box mission
# This script is part of our course on Tello drone programming
# https://learn.droneblocks.io/p/tello-drone-programming-with-python/

# Import the necessary modules
import socket
import threading
import time

# IP and port of Tello
# Drone 1: 192.168.0.100
# Drone 2: 192.168.0.101
tello1_address = ('192.168.0.101', 8889)


# IP and port of local computer
local1_address = ('', 9010)


# Create a UDP connection that we'll send the command to
sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


# Bind to the local address and port
sock1.bind(local1_address)


# Send the message to Tello and allow for a delay in seconds
def send(message, delay):
  # Try to send the message otherwise print the exception
  try:
    sock1.sendto(message.encode(), tello1_address)
    print("Sending message: " + message)
  except Exception as e:
    print("Error sending: " + str(e))

  # Delay for a user-defined period of time
  time.sleep(delay)

# Receive the message from Tello
def receive():
  # Continuously loop and listen for incoming messages
  while True:
    # Try to receive the message otherwise print the exception
    try:
      response1, ip_address = sock1.recvfrom(128)
      print("Received message: from Tello EDU #1: " + response1.decode(encoding='utf-8'))
    except Exception as e:
      # If there's an error close the socket and break out of the loop
      sock1.close()
      print("Error receiving: " + str(e))
      break

# Create and start a listening thread that runs in the background
# This utilizes our receive functions and will continuously monitor for incoming messages
receiveThread = threading.Thread(target=receive)
receiveThread.daemon = True
receiveThread.start()

# Put Tello into command mode
send("command", 3)

# Send the takeoff command
send("battery?", 0)
send("takeoff", 10)
send("rc 0 0 0 0", 2)
send("rc 0 100 0 0", 2)# command for forward
send("rc 0 0 0 0", 2)

# Land
send("land", 10)

# Print message
print("Mission completed successfully!")

# Close the socket
sock1.close()
