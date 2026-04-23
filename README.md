# OS_PROJECT
# CPU Scheduling Simulator

### 1. Project Description
This project is a CPU Scheduling Simulator built with Python and Tkinter. It allows users to simulate and compare two major scheduling algorithms:
• Priority Preemptive Scheduling
• Shortest Remaining Time First (SRTF)
The system provides a visual representation using Gantt Charts and calculates key performance metrics like Waiting Time, Turnaround Time, and Response Time.

### 2. Team Members (7 Stars)
This project was developed by a team of 2nd-year students at Misr University for Science and Technology (MUST):
1. Salma Hesham Elsayed Shawkey
2. Salma Mohamed Ramadan Mohamed
3. Razan Mohammed Hussien Abdl-ALeem
4. 
5. 
6. 
7. 

### 3. Features
• Advanced GUI: Designed with a Black & Pink modern theme.
• Multi-Error Validation: Detects multiple invalid inputs (negative arrival, zero burst, duplicate IDs) simultaneously.
• Detailed Analytics: Provides Average WT, TAT, and RT for both algorithms.
• Pre-defined Test Cases: Includes Normal, Conflict, and Starvation scenarios for quick testing.

### 4. Requirements
To run this simulator, you need:
• Python 3.10 or higher.
• Tkinter library (usually bundled with Python).

### 5. How to Run
1. Clone or Download the project files.
2. Open your terminal or command prompt in the project directory.
3. Run the command: python main.py

### 6. Tie-Breaking Strategy
In case of simultaneous events, the simulator follows these rules:
1. Priority/Remaining Time: Primary rule.
2. Arrival Time (FCFS): If the primary metric is equal.
3. Process ID (PID): The process with the smaller ID wins as a final tie-breaker
