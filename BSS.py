import socket
import threading
import time

class Process:
    def __init__(self, process_id, total_processes, port, ports):
        self.process_id = process_id
        self.total_processes = total_processes
        self.port = port
        self.ports = ports
        self.pclock = [0] * total_processes  # Only store vector clock now
        self.buffer = []
        self.channel_delay = self.init_channel_delay()
    
    def init_channel_delay(self):
        delay = 2
        channel_delay = [0] * self.total_processes
        for ch in range(self.process_id + 1, self.total_processes):
            channel_delay[ch] = delay
            delay += 2
        print(f"Channel Delays: {channel_delay}")
        return channel_delay
    
    def start_server(self):
        server_thread = threading.Thread(target=self.receive_messages, daemon=True)
        server_thread.start()
    
    def receive_messages(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(("127.0.0.1", self.port))
        server_socket.listen(100)
        print(f"Process {self.process_id} listening on port {self.port}")
        
        while True:
            client_socket, addr = server_socket.accept()
            data = client_socket.recv(1024)
            if data:
                received_data = eval(data.decode())
                received_clock = received_data['clock']
                sender_id = received_data['sender']
                print(f"Received Message from Process-{sender_id} with Clock {received_clock}")
                self.handle_delivery(received_clock, sender_id)
            client_socket.close()
    
    def handle_delivery(self, received_clock, sender_id):
        if self.pclock[sender_id] == received_clock[sender_id] - 1:
            can_deliver = all(
                self.pclock[i] >= received_clock[i] for i in range(self.total_processes) if i != sender_id
            )
            
            if can_deliver:
                print(f"Delivered Message from Process-{sender_id} with Clock: {received_clock}")
                for i in range(self.total_processes):
                    self.pclock[i] = max(self.pclock[i], received_clock[i])
            else:
                self.buffer.append((received_clock, sender_id))
                print("Buffered message as previous messages are missing")
        else:
            self.buffer.append((received_clock, sender_id))
            print("Buffered message due to missing earlier messages")
    
    def send_broadcast(self):
        self.pclock[self.process_id] += 1
        msg = str({"clock": self.pclock, "sender": self.process_id})
        
        for p in range(self.process_id + 1, self.process_id + self.total_processes):
            target_process = p % self.total_processes
            time.sleep(self.channel_delay[target_process])
            try:
                send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                send_socket.connect(("127.0.0.1", self.ports[target_process]))
                send_socket.send(msg.encode())
                send_socket.close()
                print(f"Sent message to Process-{target_process} with Clock: {self.pclock} at Process {self.process_id}")
            except Exception as e:
                print(f"Failed to send message to Process-{target_process}: {e}")
    

def main():
    total_processes = int(input("Enter total number of processes: "))
    process_id = int(input(f"Enter process ID (0 to {total_processes-1}): "))
    ports = [int(input(f"Enter port for Process-{p}: ")) for p in range(total_processes)]
    
    process = Process(process_id, total_processes, ports[process_id], ports)
    process.start_server()
    
    while True:
        input("Press Enter to send broadcast message...")
        process.send_broadcast()
    
if __name__ == "__main__":
    main()
