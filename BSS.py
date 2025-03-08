import copy

def format_vector_clock(vc):
    """
    Format the vector clock dictionary into a readable string.
    Example: {0: 0, 1: 0, 2: 0, 3: 0, 4: 0} => "P0=0, P1=0, P2=0, P3=0, P4=0"
    """
    return ", ".join(f"P{pid}={val}" for pid, val in sorted(vc.items()))

class Message:
    def __init__(self, sender, content, vector_clock):
        self.sender = sender      # Process ID of the sender
        self.content = content    # Message content
        # Attach a deep copy of the sender's vector clock
        self.vector_clock = copy.deepcopy(vector_clock)
    
    def __str__(self):
        return f"Message from P{self.sender}: '{self.content}', VC: [{format_vector_clock(self.vector_clock)}]"

class Process:
    def __init__(self, pid, total_processes):
        self.pid = pid
        self.total_processes = total_processes
        # Initialize vector clock as a dictionary: {process_id: counter}
        self.vector_clock = {i: 0 for i in range(total_processes)}
        # Queue for messages waiting for delivery (due to causal constraints)
        self.message_queue = []
        # Log of delivered messages
        self.delivered_messages = []
    
    def local_event(self):
        self.vector_clock[self.pid] += 1
        print(f"\n[Process P{self.pid}] -- Local Event --")
        print(f"   Updated Vector Clock: [{format_vector_clock(self.vector_clock)}]")
    
    def send_message(self, content, recipient):
        self.vector_clock[self.pid] += 1
        msg = Message(self.pid, content, self.vector_clock)
        print(f"\n[Process P{self.pid}] -- Sending Message --")
        print(f"   Message: '{content}'")
        print(f"   To: Process P{recipient.pid}")
        print(f"   Current Vector Clock: [{format_vector_clock(self.vector_clock)}]")
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
        Delivery condition for causal ordering:
          - For the sender (i), message.vector_clock[i] must equal self.vector_clock[i] + 1.
          - For every other process j, message.vector_clock[j] must be <= self.vector_clock[j].
        """
        sender = message.sender
        if message.vector_clock[sender] != self.vector_clock[sender] + 1:
            return False
        for j in range(self.total_processes):
            if j != sender and message.vector_clock[j] > self.vector_clock[j]:
                return False
        return True
    
    def deliver_message(self, message):
        for i in range(self.total_processes):
            self.vector_clock[i] = max(self.vector_clock[i], message.vector_clock[i])
        self.delivered_messages.append(message)
        print(f"\n[Process P{self.pid}] -- Delivered Message --")
        print(f"   {message}")
        print(f"   Updated Vector Clock: [{format_vector_clock(self.vector_clock)}]")

def simulation():
    print("=" * 60)
    print("Welcome to the BSS-based Causal Ordering Simulation!")
    print("=" * 60)
    
    total = int(input("Enter number of processes: "))
    processes = [Process(pid, total) for pid in range(total)]
    
    print("\nCommands:")
    print("  local <pid>                      - Process <pid> performs a local event.")
    print("  send <sender> <recipient> <msg>  - Process <sender> sends <msg> to Process <recipient>.")
    print("  print                            - Print current vector clocks and delivered messages for all processes.")
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
                    print(f"   Vector Clock: [{format_vector_clock(proc.vector_clock)}]")
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
