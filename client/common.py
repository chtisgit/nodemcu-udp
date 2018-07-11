from sys import argv, exit

def getIPPort():
	if len(argv) < 2:
		print("Usage:",argv[0],"<ip address> [port]")
		exit(1)

	ip = argv[1]
	port = 10000
	if len(argv) == 3:
		port = int(argv[2])
	
	return (ip, port)
