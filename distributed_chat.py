import copy

def format_matrix(matrix):
    """Return a string representation of a matrix clock in a readable format."""
    rows = []
    for i, row in enumerate(matrix):
        row_str = ", ".join(f"P{j}={val}" for j, val in enumerate(row))
        rows.append(f"Row P{i}: [{row_str}]")
    return "\n           ".join(rows)

class ChatMessage:
    def __init__(self, sender, content, matrix_clock):
        self.sender = sender      # Sender's process ID
        self.content = content    # Chat message content
        # Attach a deep copy of the sender's matrix clock at send time
        self.matrix_clock = copy.deepcopy(matrix_clock)
    
    def __str__(self):
        return f"ChatMessage from P{self.sender}: '{self.content}', Matrix Clock:\n           {format_matrix(self.matrix_clock)}"

class ChatParticipant:
    def __init__(self, pid, total_participants):
        self.pid = pid
        self.total = total_participants
        # Initialize the matrix clock: an n x n matrix with all entries 0.
        self.matrix_clock = [[0 for _ in range(total_participants)] for _ in range(total_participants)]
        # Queue for messages waiting for delivery (due to causal constraints)
        self.message_queue = []
        # Log of delivered messages (chat history for the participant)
        self.delivered_messages = []
    
    def local_event(self):
        # Simulate a local event (e.g., user typing or internal state update)
        self.matrix_clock[self.pid][self.pid] += 1
        print(f"\n[ChatParticipant P{self.pid}] -- Local Event Occurred --")
        print(f"   Updated Matrix Clock:\n           {format_matrix(self.matrix_clock)}")
    
    def send_chat_message(self, content, recipient):
        # Before sending, record a local event to capture the send event.
        self.local_event()
        msg = ChatMessage(self.pid, content, self.matrix_clock)
        print(f"\n[ChatParticipant P{self.pid}] -- Sending Chat Message --")
        print(f"   Message: '{content}'")
        print(f"   To: ChatParticipant P{recipient.pid}")
        print(f"   Attached Matrix Clock:\n           {format_matrix(msg.matrix_clock)}")
        recipient.receive_chat_message(msg)
    
    def receive_chat_message(self, message):
        print(f"\n[ChatParticipant P{self.pid}] -- Chat Message Received --")
        print(f"   {message}")
        self.message_queue.append(message)
        self.try_deliver_messages()
    
    def try_deliver_messages(self):
        delivered_any = True
        while delivered_any:
            delivered_any = False
            # Iterate over a copy of the queue to attempt delivery.
            for msg in self.message_queue[:]:
                if self.can_deliver(msg):
                    self.message_queue.remove(msg)
                    self.deliver_message(msg)
                    delivered_any = True
    
    def can_deliver(self, message):
        """
        Delivery condition based on the sender's row in the matrix clock:
        For a message sent by process i (sender):
           - The sender's own counter in the message's matrix (matrix[i][i]) 
             must equal self.matrix_clock[i][i] + 1.
           - For every other process k (k != i), the message's matrix[i][k] 
             must be <= self.matrix_clock[i][k].
        This ensures that all causally preceding events from sender i have been delivered.
        """
        sender = message.sender
        if message.matrix_clock[sender][sender] != self.matrix_clock[sender][sender] + 1:
            return False
        for k in range(self.total):
            if k != sender and message.matrix_clock[sender][k] > self.matrix_clock[sender][k]:
                return False
        return True
    
    def deliver_message(self, message):
        # Update the local matrix clock: perform element-wise maximum.
        for i in range(self.total):
            for j in range(self.total):
                self.matrix_clock[i][j] = max(self.matrix_clock[i][j], message.matrix_clock[i][j])
        self.delivered_messages.append(message)
        print(f"\n[ChatParticipant P{self.pid}] -- Delivered Chat Message --")
        print(f"   {message}")
        print(f"   Updated Matrix Clock:\n           {format_matrix(self.matrix_clock)}")

def simulation():
    print("=" * 60)
    print("Welcome to the Distributed Chat Simulation (Matrix Clock-based Causal Ordering)!")
    print("=" * 60)
    
    total = int(input("Enter number of chat participants: "))
    participants = [ChatParticipant(pid, total) for pid in range(total)]
    
    print("\nCommands:")
    print("  local <pid>                      - Participant <pid> performs a local event.")
    print("  send <sender> <recipient> <msg>  - Participant <sender> sends a chat message <msg> to Participant <recipient>.")
    print("  print                            - Print current matrix clocks and delivered chat messages for all participants.")
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
                    print("Invalid participant id.")
                    continue
                print("-" * 60)
                participants[pid].local_event()
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
                participants[sender].send_chat_message(msg, participants[recipient])
                print("-" * 60)
            
            elif command == "print":
                print("-" * 60)
                for part in participants:
                    print(f"Participant P{part.pid}:")
                    print(f"   Matrix Clock:\n           {format_matrix(part.matrix_clock)}")
                    print("   Delivered Chat Messages:")
                    if part.delivered_messages:
                        for m in part.delivered_messages:
                            print(f"      {m}")
                    else:
                        print("      None")
                    if part.message_queue:
                        print("   Pending Message Queue:")
                        for m in part.message_queue:
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
