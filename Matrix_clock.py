import copy

def format_matrix(matrix):
    """Return a string representation of a matrix clock in a readable format."""
    rows = []
    for i, row in enumerate(matrix):
        row_str = ", ".join(f"P{j}={val}" for j, val in enumerate(row))
        rows.append(f"Row P{i}: [{row_str}]")
    return "\n           ".join(rows)

class MessageMC:
    def __init__(self, sender, content, matrix_clock):
        self.sender = sender      # Process ID of the sender
        self.content = content    # Message content
        # Attach a deep copy of the sender's matrix clock
        self.matrix_clock = copy.deepcopy(matrix_clock)
    
    def __str__(self):
        return f"Message from P{self.sender}: '{self.content}', Matrix Clock:\n           {format_matrix(self.matrix_clock)}"

class ProcessMC:
    def __init__(self, pid, total_processes):
        self.pid = pid
        self.total = total_processes
        # Initialize matrix clock: an n x n matrix with all entries 0.
        self.matrix_clock = [[0 for _ in range(total_processes)] for _ in range(total_processes)]
        # Queue for messages waiting for delivery (due to causal constraints)
        self.message_queue = []
        # Log of delivered messages
        self.delivered_messages = []
    
    def local_event(self):
        # Increment the local counter: row self.pid, column self.pid.
        self.matrix_clock[self.pid][self.pid] += 1
        print(f"\n[Process P{self.pid}] -- Local Event --")
        print(f"   Updated Matrix Clock:\n           {format_matrix(self.matrix_clock)}")
    
    def send_message(self, content, recipient):
        # Perform a local event before sending to capture the send event.
        self.local_event()
        msg = MessageMC(self.pid, content, self.matrix_clock)
        print(f"\n[Process P{self.pid}] -- Sending Message --")
        print(f"   Message: '{content}'")
        print(f"   To: Process P{recipient.pid}")
        print(f"   Attached Matrix Clock:\n           {format_matrix(msg.matrix_clock)}")
        recipient.receive_message(msg)
    
    def receive_message(self, message):
        print(f"\n[Process P{self.pid}] -- Message Received --")
        print(f"   {message}")
        self.message_queue.append(message)
        self.try_deliver_messages()
    
    def try_deliver_messages(self):
        delivered_any = True
        while delivered_any:
            delivered_any = False
            for msg in self.message_queue[:]:
                if self.can_deliver(msg):
                    self.message_queue.remove(msg)
                    self.deliver_message(msg)
                    delivered_any = True
    
    def can_deliver(self, message):
        """
        Delivery condition based on the sender's row in the matrix clock:
          Let i be the sender.
          For message to be deliverable at process j (self), the following must hold:
             - For the sender's own counter: 
                  message.matrix_clock[i][i] == self.matrix_clock[i][i] + 1
             - For every other process k (k != i):
                  message.matrix_clock[i][k] <= self.matrix_clock[i][k]
        """
        sender = message.sender
        # Check sender's own counter.
        if message.matrix_clock[sender][sender] != self.matrix_clock[sender][sender] + 1:
            return False
        # Check other entries in sender's row.
        for k in range(self.total):
            if k != sender and message.matrix_clock[sender][k] > self.matrix_clock[sender][k]:
                return False
        return True
    
    def deliver_message(self, message):
        # Upon delivery, update the local matrix clock by taking element-wise maximum.
        for i in range(self.total):
            for j in range(self.total):
                self.matrix_clock[i][j] = max(self.matrix_clock[i][j], message.matrix_clock[i][j])
        self.delivered_messages.append(message)
        print(f"\n[Process P{self.pid}] -- Delivered Message --")
        print(f"   {message}")
        print(f"   Updated Matrix Clock:\n           {format_matrix(self.matrix_clock)}")

def simulation():
    print("=" * 60)
    print("Welcome to the Matrix Clock-based Causal Ordering Simulation!")
    print("=" * 60)
    
    total = int(input("Enter number of processes: "))
    processes = [ProcessMC(pid, total) for pid in range(total)]
    
    print("\nCommands:")
    print("  local <pid>                      - Process <pid> performs a local event.")
    print("  send <sender> <recipient> <msg>  - Process <sender> sends <msg> to Process <recipient>.")
    print("  print                            - Print current matrix clocks and delivered messages for all processes.")
    print("  quit                             - Exit simulation.")
    print("=" * 60)
    
    while True:
        try:
            cmd = input("\nEnter command: ").strip()
            if not cmd:
                continue
            parts = cmd.split()
            command = parts[0].lower()
            
            if command == "quit":
                print("\nExiting simulation. Goodbye!")
                break
            
            elif command == "local":
                if len(parts) != 2:
                    print("Usage: local <pid>")
                    continue
                pid = int(parts[1])
                if pid < 0 or pid >= total:
                    print("Invalid process id.")
                    continue
                print("-" * 60)
                processes[pid].local_event()
                print("-" * 60)
            
            elif command == "send":
                if len(parts) < 4:
                    print("Usage: send <sender> <recipient> <message>")
                    continue
                sender = int(parts[1])
                recipient = int(parts[2])
                if sender < 0 or sender >= total or recipient < 0 or recipient >= total:
                    print("Invalid sender or recipient id.")
                    continue
                msg = " ".join(parts[3:])
                print("-" * 60)
                processes[sender].send_message(msg, processes[recipient])
                print("-" * 60)
            
            elif command == "print":
                print("-" * 60)
                for proc in processes:
                    print(f"Process P{proc.pid}:")
                    print(f"   Matrix Clock:\n           {format_matrix(proc.matrix_clock)}")
                    print("   Delivered Messages:")
                    if proc.delivered_messages:
                        for m in proc.delivered_messages:
                            print(f"      {m}")
                    else:
                        print("      None")
                    if proc.message_queue:
                        print("   Pending Message Queue:")
                        for m in proc.message_queue:
                            print(f"      {m}")
                    else:
                        print("   Pending Message Queue: None")
                    print("-" * 40)
                print("-" * 60)
            
            else:
                print("Unknown command. Available commands: local, send, print, quit.")
        
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    simulation()
