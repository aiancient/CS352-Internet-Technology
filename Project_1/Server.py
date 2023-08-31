import sys
import socket
    
def compute_checksum(message):
    # Internet checksum calculation
    checksum = 0
    message = b'\0\0' + message
    message_len = len(message)
        
    if message_len % 2 != 0:
        message += b'\0'  # Pad with zero byte if message length is odd
        message_len += 1
            
    for i in range(0, message_len, 2):
        if i + 1 < message_len:
            line = message[i] << 8 | message[i + 1]
            checksum += line
            checksum = (checksum & 0xFFFF) + (checksum >> 16)
                
    return ~checksum & 0xFFFF
        
def switch_cases(string):
    return string.swapcase()
        
def run_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(1)
        
    client_socket, _ = server_socket.accept()
    line = b'blah'

    while line:
        # Receive message with checksum
        line = client_socket.recv(1024)
            
        if not line:
            break
                
        # Extract checksum and message
        received_checksum = line[:2]
        message = line[2:]

        #Calculate expected sum of original sum 
        expected_checksum = compute_checksum(message)

        #Check if checksum attached to message is correct, if not send an error message
        if received_checksum != expected_checksum.to_bytes(2, byteorder='big'):
            error_message = b"\0\0ERROR\n"
            client_socket.sendall(error_message)
        
        #if checksum attached to message is correct, send swapped message w/ new checksum 
        else: 
            swapped_result = switch_cases(message)
            new_checksum = compute_checksum(swapped_result).to_bytes(2, byteorder='big')
            client_socket.sendall(new_checksum + swapped_result)
                
    client_socket.close()
    server_socket.close()
        
if __name__ == '__main__':
    port = int(sys.argv[1])
    run_server(port)
