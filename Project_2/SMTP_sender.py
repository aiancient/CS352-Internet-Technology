from sys import argv
import socket
import argparse
import time
parser=argparse.ArgumentParser(description="""This is an SMTP sender""")
parser.add_argument('email_file', type=str, help='this is the filename of the email body',action='store')
parser.add_argument('subject_line', type=str, help='this is the email\'s subject line, remeber to include " " around the subject',action='store')
parser.add_argument('destination_email_address', type=str, help='This is the destination email address, includes only gmail addresses for now',action='store')
parser.add_argument('source_username', type=str, help='This is the username of the source email the end is implied to be the current machine',action='store')
parser.add_argument('-s', type=str, dest='dest_serv', help='This is the destination SMTP server, defaults to gmails',action='store', default='gmail-smtp-in.l.google.com.')
args = parser.parse_args(argv[1:])

# Create a socket connection
out_sock = socket.socket()
out_sock.connect((args.dest_serv, 25))

# Receive and print the server greeting
print("From Server:", out_sock.recv(1024).decode())

# Send HELO command
out_sock.send(f"HELO {socket.gethostname()}\r\n".encode())
print("To Server:", f"HELO {socket.gethostname()}\r\n")

# Receive and print the server response
print("From Server:", out_sock.recv(1024).decode())

# Send MAIL FROM command
out_sock.send(f"MAIL FROM:<{args.source_username}@{socket.gethostname()}>\r\n".encode())
print("To Server:", f"MAIL FROM:<{args.source_username}@{socket.gethostname()}>\r\n")

# Receive and print the server response
print("From Server:", out_sock.recv(1024).decode())

# Send RCPT TO command
out_sock.send(f"RCPT TO:<{args.destination_email_address}>\r\n".encode())
print("To Server:", f"RCPT TO:<{args.destination_email_address}>\r\n")

# Receive and print the server response
print("From Server:", out_sock.recv(1024).decode())

# Send DATA command
out_sock.send("DATA\r\n".encode())
print("To Server:", "DATA\r\n")

# Receive and print the server response
print("From Server:", out_sock.recv(1024).decode())

# Generate Message-ID header
message_id = f"<{int(time.time())}@{socket.gethostname()}>"

# Construct and send email headers
headers = [
    f"From: <{args.source_username}@{socket.gethostname()}>",
    f"Message-ID: {message_id}",
    f"To: <{args.destination_email_address}>",
    f"Subject: {args.subject_line}"
]

for header in headers:
    out_sock.send(f"{header}\r\n".encode())
    print("To Server:", f"{header}\r\n")

# Read and send email body from file
with open(args.email_file, "r") as email_file:
    email_body = email_file.read()
    out_sock.send(email_body.encode())

# Send the end-of-email marker
out_sock.send("\r\n.\r\n".encode())
print("To Server:", "\r\n.\r\n")

# Receive and print the server response
print("From Server:", out_sock.recv(1024).decode())

# Send QUIT command
out_sock.send("QUIT\r\n".encode())
print("To Server:", "QUIT\r\n")

# Receive and print the server response
print("From Server:", out_sock.recv(1024).decode())

# Close the socket connection
out_sock.close()