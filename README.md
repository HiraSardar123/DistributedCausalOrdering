# Distributed Systems Causal Ordering Simulations

This repository contains four Python simulation implementations that demonstrate how to achieve causal ordering in distributed systems using different approaches. Each implementation is in a separate file:

- **BSS.py**: Implements BSS-based causal ordering using vector clocks.
- **SES.py**: Implements the Schwarz & Mattern (SES) approach using causal histories.
- **Matrix_clock.py**: Implements causal ordering using matrix clocks.
- **distributed_chat.py**: Simulates a real-world distributed chat application that uses matrix clocks to ensure that chat messages are delivered in a causally consistent manner.

---

## Contents

### 1. BSS.py
This simulation uses the **Birman-Schiper-Stephenson (BSS)** approach with vector clocks to track and enforce causal message ordering. Each process maintains a vector clock and attaches it to messages. A message is delivered only if its attached vector clock meets the causal delivery conditions at the receiver.

### 2. SES.py
This simulation implements the **Schwarz & Mattern (SES)** approach, which tracks dependencies using causal histories. Each process maintains a set of event identifiers as its causal history. When a message is sent, the current causal history is attached, and the receiver delivers the message only when all events in the sender’s history are known.

### 3. Matrix_clock.py
This simulation uses **Matrix Clocks** to provide a detailed tracking of causal dependencies. Each process maintains an n×n matrix clock that records every process's knowledge about each other's logical time. The message delivery condition is based on comparing the sender's row in the attached matrix clock with the receiver's local matrix clock.

### 4. distributed_chat.py
This is a practical simulation of a distributed chat application where each participant is a process using matrix clocks. It ensures that chat messages are delivered in the correct causal order. The application is interactive and supports local events, message sending, and state printing commands.

---

## Setup Instructions

### Requirements
- Python 3.x
- A terminal or command prompt

### Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/DistributedCausalOrdering.git
   cd DistributedCausalOrdering
   ```
2. **Verify Python Installation:**

   ```bash
   python3 --version
   ```

### Running the Simulations

Each simulation is implemented in a separate Python file. Run them using the following commands:

- **BSS-based Causal Ordering Simulation:**
  ```bash
  python3 BSS.py
  ```

- **SES-based Causal Ordering Simulation:**
  ```bash
  python3 SES.py
  ```

- **Matrix Clock-based Causal Ordering Simulation:**
  ```bash
  python3 Matrix_clock.py
  ```

- **Distributed Chat Application (Matrix Clock-based):**
  ```bash
  python3 distributed_chat.py
  ```

---

## Sample Inputs and Outputs

### BSS Simulation (BSS.py)

**Input Example:**
```
Enter number of processes: 3
Enter command: local 0
Enter command: send 0 1 Hello from P0
Enter command: print
Enter command: quit
```

**Sample Output:**
```
============================================================
Welcome to the BSS-based Causal Ordering Simulation!
============================================================
Enter number of processes: 3

Commands:
  local <pid>                      - Process <pid> performs a local event.
  send <sender> <recipient> <msg>  - Process <sender> sends <msg> to Process <recipient>.
  print                            - Print current vector clocks and delivered messages for all processes.
  quit                             - Exit simulation.
============================================================

Enter command: local 0
------------------------------------------------------------
[Process P0] -- Local Event --
   Updated Vector Clock: [P0=1, P1=0, P2=0]
------------------------------------------------------------

Enter command: send 0 1 Hello from P0
------------------------------------------------------------
[Process P0] -- Sending Message --
   Message: 'Hello from P0'
   To: Process P1
   Current Vector Clock: [P0=2, P1=0, P2=0]
[Process P1] -- Message Received --
   Message from P0: 'Hello from P0', VC: [P0=2, P1=0, P2=0]
------------------------------------------------------------

Enter command: print
------------------------------------------------------------
Process P0:
   Vector Clock: [P0=2, P1=0, P2=0]
   Delivered Messages:
      None
   Pending Message Queue: None
----------------------------------------
Process P1:
   Vector Clock: [P0=0, P1=0, P2=0]
   Delivered Messages:
      None
   Pending Message Queue:
      Message from P0: 'Hello from P0', VC: [P0=2, P1=0, P2=0]
----------------------------------------
Process P2:
   Vector Clock: [P0=0, P1=0, P2=0]
   Delivered Messages:
      None
   Pending Message Queue: None
----------------------------------------
------------------------------------------------------------
Enter command: quit
Exiting simulation. Goodbye!
```

### SES Simulation (SES.py)

**Input Example:**
```
Enter number of processes: 3
Enter command: local 1
Enter command: send 1 2 Hey, this is P1!
Enter command: print
Enter command: quit
```

**Sample Output:**
```
============================================================
Welcome to the SES-based Causal Ordering Simulation!
============================================================
Enter number of processes: 3

Commands:
  local <pid>                      - Process <pid> performs a local event.
  send <sender> <recipient> <msg>  - Process <sender> sends <msg> to Process <recipient>.
  print                            - Print current causal histories and delivered messages for all processes.
  quit                             - Exit simulation.
============================================================

Enter command: local 1
------------------------------------------------------------
[Process P1] -- Local Event --
   Generated Event: P1#1
   Updated Causal History: [P1#1]
------------------------------------------------------------

Enter command: send 1 2 Hey, this is P1!
------------------------------------------------------------
[Process P1] -- Sending Message --
   Generated Event: P1#2
   Message: 'Hey, this is P1!'
   To: Process P2
   Attached Causal History: [P1#1, P1#2]
[Process P2] -- Message Received --
   Message from P1: 'Hey, this is P1!', History: [P1#1, P1#2]
------------------------------------------------------------

Enter command: print
------------------------------------------------------------
Process P0:
   Causal History: []
   Delivered Messages:
      None
   Pending Message Queue: None
----------------------------------------
Process P1:
   Causal History: [P1#1, P1#2]
   Delivered Messages:
      None
   Pending Message Queue: None
----------------------------------------
Process P2:
   Causal History: []
   Delivered Messages:
      None
   Pending Message Queue:
      Message from P1: 'Hey, this is P1!', History: [P1#1, P1#2]
----------------------------------------
------------------------------------------------------------
Enter command: quit
Exiting simulation. Goodbye!
```

### Matrix Clock Simulation (Matrix_clock.py)

**Input Example:**
```
Enter number of processes: 3
Enter command: local 0
Enter command: send 0 2 Greetings from P0!
Enter command: print
Enter command: quit
```

**Sample Output:**
```
============================================================
Welcome to the Matrix Clock-based Causal Ordering Simulation!
============================================================
Enter number of processes: 3

Commands:
  local <pid>                      - Process <pid> performs a local event.
  send <sender> <recipient> <msg>  - Process <sender> sends <msg> to Process <recipient>.
  print                            - Print current matrix clocks and delivered messages for all processes.
  quit                             - Exit simulation.
============================================================

Enter command: local 0
------------------------------------------------------------
[Process P0] -- Local Event --
   Updated Matrix Clock:
           Row P0: [P0=1, P1=0, P2=0]
           Row P1: [P0=0, P1=0, P2=0]
           Row P2: [P0=0, P1=0, P2=0]
------------------------------------------------------------

Enter command: send 0 2 Greetings from P0!
------------------------------------------------------------
[Process P0] -- Local Event --
   Updated Matrix Clock:
           Row P0: [P0=2, P1=0, P2=0]
           Row P1: [P0=0, P1=0, P2=0]
           Row P2: [P0=0, P1=0, P2=0]
[Process P0] -- Sending Message --
   Message: 'Greetings from P0!'
   To: Process P2
   Attached Matrix Clock:
           Row P0: [P0=2, P1=0, P2=0]
           Row P1: [P0=0, P1=0, P2=0]
           Row P2: [P0=0, P1=0, P2=0]
[Process P2] -- Message Received --
   Message from P0: 'Greetings from P0!', Matrix Clock:
           Row P0: [P0=2, P1=0, P2=0]
           Row P1: [P0=0, P1=0, P2=0]
           Row P2: [P0=0, P1=0, P2=0]
------------------------------------------------------------

Enter command: print
------------------------------------------------------------
Process P0:
   Matrix Clock:
           Row P0: [P0=2, P1=0, P2=0]
           Row P1: [P0=0, P1=0, P2=0]
           Row P2: [P0=0, P1=0, P2=0]
   Delivered Messages: None
   Pending Message Queue: None
----------------------------------------
Process P1:
   Matrix Clock:
           Row P0: [P0=0, P1=0, P2=0]
           Row P1: [P0=0, P1=0, P2=0]
           Row P2: [P0=0, P1=0, P2=0]
   Delivered Messages: None
   Pending Message Queue: None
----------------------------------------
Process P2:
   Matrix Clock:
           Row P0: [P0=0, P1=0, P2=0]
           Row P1: [P0=0, P1=0, P2=0]
           Row P2: [P0=0, P1=0, P2=0]
   Delivered Messages:
      Message from P0: 'Greetings from P0!', Matrix Clock:
           Row P0: [P0=2, P1=0, P2=0]
           Row P1: [P0=0, P1=0, P2=0]
           Row P2: [P0=0, P1=0, P2=0]
   Pending Message Queue: None
----------------------------------------
------------------------------------------------------------
Enter command: quit
Exiting simulation. Goodbye!
```

### Distributed Chat Application (distributed_chat.py)
Here is the practical implementation to simulate a real-world distributed chat application where time synchronization or causal ordering is essential. 


**Input Example:**
```
Enter number of chat participants: 3
Enter command: send 0 1 Hi, I'm P0!
Enter command: send 1 2 Hello from P1!
Enter command: local 2
Enter command: print
Enter command: quit
```

**Sample Output:**
```
============================================================
Welcome to the Distributed Chat Simulation (Matrix Clock-based Causal Ordering)!
============================================================
Enter number of chat participants: 3

Commands:
  local <pid>                      - Participant <pid> performs a local event.
  send <sender> <recipient> <msg>  - Participant <sender> sends a chat message <msg> to Participant <recipient>.
  print                            - Print current matrix clocks and delivered chat messages for all participants.
  quit                             - Exit simulation.
============================================================

Enter command: send 0 1 Hi, I'm P0!
------------------------------------------------------------
[ChatParticipant P0] -- Local Event Occurred --
   Updated Matrix Clock:
           Row P0: [P0=1, P1=0, P2=0]
           Row P1: [P0=0, P1=0, P2=0]
           Row P2: [P0=0, P1=0, P2=0]
[ChatParticipant P0] -- Sending Chat Message --
   Message: 'Hi, I'm P0!'
   To: ChatParticipant P1
   Attached Matrix Clock:
           Row P0: [P0=1, P1=0, P2=0]
           Row P1: [P0=0, P1=0, P2=0]
           Row P2: [P0=0, P1=0, P2=0]
[ChatParticipant P1] -- Chat Message Received --
   ChatMessage from P0: 'Hi, I'm P0!', Matrix Clock:
           Row P0: [P0=1, P1=0, P2=0]
           Row P1: [P0=0, P1=0, P2=0]
           Row P2: [P0=0, P1=0, P2=0]
------------------------------------------------------------
Enter command: send 1 2 Hello from P1!
------------------------------------------------------------
[ChatParticipant P1] -- Local Event Occurred --
   Updated Matrix Clock:
           Row P0: [P0=0, P1=0, P2=0]
           Row P1: [P0=0, P1=1, P2=0]
           Row P2: [P0=0, P1=0, P2=0]
[ChatParticipant P1] -- Sending Chat Message --
   Message: 'Hello from P1!'
   To: ChatParticipant P2
   Attached Matrix Clock:
           Row P0: [P0=0, P1=0, P2=0]
           Row P1: [P0=0, P1=1, P2=0]
           Row P2: [P0=0, P1=0, P2=0]
[ChatParticipant P2] -- Chat Message Received --
   ChatMessage from P1: 'Hello from P1!', Matrix Clock:
           Row P0: [P0=0, P1=0, P2=0]
           Row P1: [P0=0, P1=1, P2=0]
           Row P2: [P0=0, P1=0, P2=0]
------------------------------------------------------------
Enter command: local 2
------------------------------------------------------------
[ChatParticipant P2] -- Local Event Occurred --
   Updated Matrix Clock:
           Row P0: [P0=0, P1=0, P2=0]
           Row P1: [P0=0, P1=0, P2=0]
           Row P2: [P0=0, P1=0, P2=1]
------------------------------------------------------------
Enter command: print
------------------------------------------------------------
Participant P0:
   Matrix Clock:
           Row P0: [P0=1, P1=0, P2=0]
           Row P1: [P0=0, P1=0, P2=0]
           Row P2: [P0=0, P1=0, P2=0]
   Delivered Chat Messages:
      ChatMessage from P0: 'Hi, I'm P0!', Matrix Clock:
           Row P0: [P0=1, P1=0, P2=0]
           Row P1: [P0=0, P1=0, P2=0]
           Row P2: [P0=0, P1=0, P2=0]
   Pending Message Queue: None
----------------------------------------
Participant P1:
   Matrix Clock:
           Row P0: [P0=0, P1=0, P2=0]
           Row P1: [P0=0, P1=1, P2=0]
           Row P2: [P0=0, P1=0, P2=0]
   Delivered Chat Messages:
      ChatMessage from P0: 'Hi, I'm P0!', Matrix Clock:
           Row P0: [P0=1, P1=0, P2=0]
           Row P1: [P0=0, P1=0, P2=0]
           Row P2: [P0=0, P1=0, P2=0]
      ChatMessage from P1: 'Hello from P1!', Matrix Clock:
           Row P0: [P0=0, P1=0, P2=0]
           Row P1: [P0=0, P1=1, P2=0]
           Row P2: [P0=0, P1=0, P2=0]
   Pending Message Queue: None
----------------------------------------
Participant P2:
   Matrix Clock:
           Row P0: [P0=0, P1=0, P2=0]
           Row P1: [P0=0, P1=0, P2=0]
           Row P2: [P0=0, P1=0, P2=1]
   Delivered Chat Messages:
      ChatMessage from P1: 'Hello from P1!', Matrix Clock:
           Row P0: [P0=0, P1=0, P2=0]
           Row P1: [P0=0, P1=1, P2=0]
           Row P2: [P0=0, P1=0, P2=0]
   Pending Message Queue: None
----------------------------------------
------------------------------------------------------------
Enter command: quit
Exiting simulation. Goodbye!
```

## Contributing

Contributions, bug reports, and suggestions are welcome. Feel free to open an issue or submit a pull request.
