import socket
import threading
import pickle

class SchiperEggliSandoz:
    def __init__(self, process_id, total_processes, port, ports):
        self.process_id = process_id
        self.total_processes = total_processes
        self.port = port
        self.ports = ports
        self.vector_clock = [0] * total_processes
        self.message_buffer = []
        self.s_buffer = []

    def start_server(self):
        """Starts a thread that listens for incoming messages."""
        server_thread = threading.Thread(target=self.receive_message, daemon=True)
        server_thread.start()

    def receive_message(self):
        """Handles incoming messages and updates the vector clock correctly."""
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(("127.0.0.1", self.port))
        server_socket.listen(10)
        print(f"Process {self.process_id} listening on port {self.port}")

        while True:
            client_socket, addr = server_socket.accept()
            data = pickle.loads(client_socket.recv(1024))
            if data:
                received_clock = data["clock"]
                sender_id = data["sender"]
                s_buffer = data["s_buffer"]

                print(f"Received Message from Process-{sender_id} with Clock {received_clock}")
                
                # Process message delivery condition
                if self.delivery_condition(s_buffer):
                    self.deliver(data)
                    self.check_buffer()
                else:
                    print("Buffered message due to missing causal messages.")
                    self.message_buffer.append(data)
            
            client_socket.close()

    def send_message(self, destination):
        """Sends a message to the specified process."""
        if destination >= self.total_processes or destination < 0:
            print("Invalid process ID!")
            return

        self.vector_clock[self.process_id] += 1  # Increment clock on sending
        message = input("Enter your message: ")

        # Clone s_buffer for sending
        s_buffer_copy = list(self.s_buffer)

        message_data = {
            "sender": self.process_id,
            "clock": self.vector_clock[:],
            "s_buffer": s_buffer_copy,
            "message": message
        }

        try:
            send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            send_socket.connect(("127.0.0.1", self.ports[destination]))
            send_socket.send(pickle.dumps(message_data))
            send_socket.close()

            print(f"Sent message to Process-{destination} with Clock: {self.vector_clock}")
        except Exception as e:
            print(f"Failed to send message to Process-{destination}: {e}")

    def delivery_condition(self, incoming_s_buffer):
        """Checks if the message can be delivered based on S-buffer conditions."""
        for s in incoming_s_buffer:
            if s["process"] == self.process_id and s["timestamp"] > self.vector_clock[self.process_id]:
                return False
        return True

    def deliver(self, message_data):
        """Delivers a message and updates the vector clock correctly."""
        sender_id = message_data["sender"]
        received_clock = message_data["clock"]

        print(f"Delivered Message from Process-{sender_id} with Clock: {received_clock}")

        # Merge vector clocks
        self.vector_clock = [max(self.vector_clock[i], received_clock[i]) for i in range(self.total_processes)]

        # **Increment clock AFTER receiving and merging clocks**
        self.vector_clock[self.process_id] += 1  

        # Merge S-buffer knowledge
        self.s_buffer.append({"process": sender_id, "timestamp": received_clock[sender_id]})

        print(f"Updated Vector Clock: {self.vector_clock}")

    def check_buffer(self):
        """Checks the buffer for messages that can now be delivered."""
        for message_data in self.message_buffer:
            if self.delivery_condition(message_data["s_buffer"]):
                self.deliver(message_data)
                self.message_buffer.remove(message_data)
                self.check_buffer()
                break

def main():
    total_processes = int(input("Enter total number of processes: "))
    process_id = int(input(f"Enter process ID (0 to {total_processes-1}): "))
    ports = [int(input(f"Enter port for Process-{p}: ")) for p in range(total_processes)]

    process = SchiperEggliSandoz(process_id, total_processes, ports[process_id], ports)
    process.start_server()

    while True:
        action = input("Choose action: (s)end or (r)eceive: ").strip().lower()
        if action == "s":
            dest = int(input("Enter destination process ID: "))
            process.send_message(dest)
        elif action == "r":
            print("Listening for messages...")
        else:
            print("Invalid action. Choose 's' or 'r'.")

if __name__ == "__main__":
    main()
