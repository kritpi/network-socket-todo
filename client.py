import socket

def run_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = "127.0.0.1"
    server_port = 9000
    client.connect((server_ip, server_port))

    while True:
        print("Todo-List Application")
        msg = input("Enter command[ add <todo-list> | view | remove <todo-list id> | close ]: ")
        client.send(msg.encode("utf-8"))

        response = client.recv(1024).decode("utf-8")
        print(f"Server response: {response}")
        
        if response.lower() == "closed":
            break

    client.close()
    print("Connection to server closed")

run_client()
