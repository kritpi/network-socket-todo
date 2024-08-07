import socket

# Dictionary to store the to-do list
todo_list = {}
next_id = 1

def handle_request(request):
    global next_id
    response = ""
    
    command = request.split(" ", 1)
    if command[0].upper() == "ADD":
        if len(command) > 1:
            task = command[1]
            todo_list[next_id] = task
            response = f"[Status: 200 - SUCCESS]\n Task added with ID {next_id}"
            next_id += 1
        else:
            response = "[Status: 200 - SUCCESS]\n Error: No task provided"
    
    elif command[0].upper() == "VIEW":
        if todo_list:
            response = "\n".join([f"{task_id}: {task}" for task_id, task in todo_list.items()])
        else:
            response = "[Status: 200 - SUCCESS]\n To-do list is empty"
    
    elif command[0].upper() == "REMOVE":
        if len(command) > 1:
            try:
                task_id = int(command[1])
                if task_id in todo_list:
                    del todo_list[task_id]
                    response = f"[Status: 200 - SUCCESS]\n Task {task_id} removed"
                else:
                    response = "[Status: 404 - NOT FOUND]\n Error: Task ID not found"
            except ValueError:
                response = "[Status: 200 - SUCCESS]\n Error: Invalid task ID"
        else:
            response = "[Status: 200 - SUCCESS]\n Error: No task ID provided"
    
    elif command[0].upper() == "CLOSE":
        response = "closed"
    
    else:
        response = "[Status: 404 - NOT FOUND]\n Error: Unknown command"
    
    return response

def run_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = "127.0.0.1"
    port = 9000
    server.bind((server_ip, port))
    server.listen(1)
    print(f"Listening on {server_ip}:{port}")
    
    client_socket, client_address = server.accept()
    print(f"Accepted connection from {client_address[0]}:{client_address[1]}")
    
    while True:
        request = client_socket.recv(1024).decode("utf-8")
        if not request:
            break
        
        print(f"Received: {request}")
        response = handle_request(request)
        
        client_socket.send(response.encode("utf-8"))
        
        if response == "closed":
            break
    
    client_socket.close()
    server.close()
    print("Connection to client closed")
    print("Server shut down")

run_server()
