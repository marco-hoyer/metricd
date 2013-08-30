import argparse
import os
import socket

def parse_arguments():
        parser = argparse.ArgumentParser()
        parser.add_argument('pipe_path')
	parser.add_argument('carbon_port')
        args = parser.parse_args()
	args.carbon_port = int(args.carbon_port)
	return args

def start_metric_script(script_name, carbon_server, carbon_port, pipe_path):
	exec 'python %s %s %s %s' % (script_name, carbon_server, carbon_port, pipe_path)

def create_named_pipe(pipe_path):
	os.mkfifo(pipe_path, 0666)

def write_icinga_lines_to_pipe(pipe_path, lines):
	with open(pipe_path, 'w') as pipe:
		for l in lines:
			pipe.write(l)

def start_socket(port):
	listening_socket = socket.socket()
	listening_socket.bind(('localhost', port))
	listening_socket.listen(5)
	while True:
		(connected_socket, address) = listening_socket.accept()
		while True:
			sock = connected_socket.makefile()
			print sock.readline()

def clean_up(pipe_path):
	os.remove(pipe_path)

if __name__ == '__main__':
	args = parse_arguments()
	#create_named_pipe(args.pipe_path)

	#start_metric_script(args.script_name, args.carbon_server, args.carbon_port, args.pipe_path)

	write_icinga_lines_to_pipe(args.pipe_path, 
		['tuvtst01|Ping|rta=1.000000ms;3000.000000;5000.000000;0.000000 pl=1%;80;100;0|1',
		'tuvtst02|Ping|rta=2.000000ms;3000.000000;5000.000000;0.000000 pl=2%;80;100;0|2',
		'tuvtst03|Ping|rta=3.000000ms;3000.000000;5000.000000;0.000000 pl=3%;80;100;0|3',
		'tuvtst04|Ping|rta=4.000000ms;3000.000000;5000.000000;0.000000 pl=4%;80;100;0|4',
		'tuvtst05|Ping|rta=5.000000ms;3000.000000;5000.000000;0.000000 pl=5%;80;100;0|5',
		'tuvtst06|Ping|rta=6.000000ms;3000.000000;5000.000000;0.000000 pl=6%;80;100;0|6',
		'tuvtst07|Ping|rta=7.000000ms;3000.000000;5000.000000;0.000000 pl=7%;80;100;0|7'])


	start_socket(args.carbon_port)

	# write 10 Icinga lines to a named pipe

	# call the Metric.py script
	# open a socket
	# read 7 Carbon lines from the socket
	# kill the socket
	# write another 5 Icinga lines to the pipe
	# open a new socket (hopefully we can bind to the same port)
	# write some garbage to the pipe
	# read all remaining Carbon lines from the socket
	# assert that all expected Carbon lines have been read

	# clean up
#	clean_up(args.pipe_path)

