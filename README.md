# tic-tac-toe

Game referenced from https://medium.com/byte-tales/the-classic-tic-tac-toe-game-in-python-3-1427c68b8874

#connect-to-server

1. select one admin out of 3
2. the admin runs <server_name>.py
3. the admin shares the local ip address from the pc where the server is running to 2 other clients
4. update the client file <client_name>.py 
	at line to replace
	channel = grpc.insecure_channel('localhost:50051')
	to be
	channel = grpc.insecure_channel('<ADMIN-LAPTOP-IP-ADDRESS>:50051')
	
	in this case all clients connect to the server with the correct port and ip address.
5. now both clients can run <client_name>.py 
