import copy

def format_history(history):
    """
    Format the causal history (a set of event IDs) as a sorted, comma-separated string.
    Example: {"P0#1", "P1#2"} => "P0#1, P1#2"
    """
    return ", ".join(sorted(history))

class MessageSES:
    def __init__(self, sender, content, causal_history):
        self.sender = sender            # Process ID of the sender
        self.content = content          # Message content
        # Attach a deep copy of the sender's causal history (set of event IDs)
        self.causal_history = copy.deepcopy(causal_history)
    
    def __str__(self):
        return f"Message from P{self.sender}: '{self.content}', History: [{format_history(self.causal_history)}]"

class ProcessSES:
    def __init__(self, pid, total_processes):
        self.pid = pid
        self.total_processes = total_processes
        # Causal history: set of event IDs that this process has seen
        self.history = set()
        # Local counter to generate unique event IDs
        self.local_counter = 0
        # Queue for messages waiting for delivery (due to causal constraints)
        self.message_queue = []
        # Log of delivered messages
        self.delivered_messages = []
    
    def generate_event_id(self):
        """Generate a unique event ID for a local event, e.g., 'P0#1'."""
        self.local_counter += 1
        event_id = f"P{self.pid}#{self.local_counter}"
        self.history.add(event_id)
        return event_id
    
    def local_event(self):
        event_id = self.generate_event_id()
        print(f"\n[Process P{self.pid}] -- Local Event --")
        print(f"   Generated Event: {event_id}")
        print(f"   Updated Causal History: [{format_history(self.history)}]")
    
    def send_message(self, content, recipient):
        # Perform a local event before sending (to record sending time)
        event_id = self.generate_event_id()
        msg = MessageSES(self.pid, content, self.history)
        print(f"\n[Process P{self.pid}] -- Sending Message --")
        print(f"   Generated Event: {event_id}")
        print(f"   Message: '{content}'")
        print(f"   To: Process P{recipient.pid}")
        print(f"   Attached Causal History: [{format_history(msg.causal_history)}]")
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
            # Check a copy of the queue to attempt delivery
            for msg in self.message_queue[:]:
                if self.can_deliver(msg):
                    self.message_queue.remove(msg)
                    self.deliver_message(msg)
                    delivered_any = True
    
    def can_deliver(self, message):
        """
        Delivery condition for SES-based causal ordering:
        A message is deliverable if all events in its attached causal history
        are already in the receiver's causal history.
        """
        return message.causal_history.issubset(self.history)
    
    def deliver_message(self, message):
        # Upon delivery, merge the message's causal history into the process's history.
        self.history.update(message.causal_history)
        self.delivered_messages.append(message)
        print(f"\n[Process P{self.pid}] -- Delivered Message --")
        print(f"   {message}")
        print(f"   Updated Causal History: [{format_history(self.history)}]")

def simulation():
    print("=" * 60)
    print("Welcome to the SES-based Causal Ordering Simulation!")
    print("=" * 60)
    
    total = int(input("Enter number of processes: "))
    processes = [ProcessSES(pid, total) for pid in range(total)]
    
    print("\nCommands:")
    print("  local <pid>                      - Process <pid> performs a local event.")
    print("  send <sender> <recipient> <msg>  - Process <sender> sends <msg> to Process <recipient>.")
    print("  print                            - Print current causal histories and delivered messages for all processes.")
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
                    print(f"   Causal History: [{format_history(proc.history)}]")
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
