# OS_PROJECT
# CPU Scheduling Simulator

A complete, interactive desktop application to visualize, compare, and analyze CPU Scheduling Algorithms.
###  📖 Project Description
The CPU Scheduling Simulator is a high-fidelity, graphical desktop application developed in Python with the Tkinter library. It allows users to simulate and compare two major scheduling algorithms using the **same workload** to ensure a fair and valid comparison:

• Preemptive Priority Scheduling: A method where execution is determined strictly by the priority level assigned to each process.

• Shortest Remaining Time First (SRTF)
The system provides a visual representation using Gantt Charts and calculates key performance metrics like Waiting Time, Turnaround Time, and Response Time.

---
###  👥 Team Members
1. Salma Hesham Elsayed Shawkey
2. Salma Mohamed Ramadan Mohamed
3. Razan Mohammed Hussien Abdl-ALeem
4. 
5. 
6. 
7. 
---
### ✨ Key Features & Capabilities

*   **Modern Interactive GUI:** A premium "Black & Pink" dark-mode interface split into two main sections: **Configuration** and **Analysis & Results**.
*   **Robust Input Validation:** The system strictly prevents invalid inputs (e.g., negative arrival times, zero burst times, missing data, or duplicate Process IDs) with descriptive error dialogs.
*   **Pre-built Test Scenarios:** Instantly load complex edge cases to test system behavior:
    *   *Normal:* Standard execution flow.
    *   *Conflict:* Multiple processes arriving simultaneously.
    *   *Starvation:* Testing how low-priority tasks behave when overwhelmed by high-priority tasks.
*   **Dynamic Gantt Chart Rendering:** Accurately visualizes execution timelines, clearly displaying process preemption (when a process is paused and resumed).
*   **Advanced Tie-Breaking Strategy:** In the event of a tie, the system relies on a strict 3-tier hierarchy to prevent crashes:
    1.  *Primary:* Priority Level (for Priority) or Remaining Time (for SRTF).
    2.  *Secondary:* First Come, First Served (Arrival Time).
    3.  *Final:* If both the primary criteria and arrival times are identical, the process with the lower ID number is granted precedence.
*   **Mathematical Metric Calculation:** Automatically calculates the following for every single process:
    *   Waiting Time (WT)
    *   Turnaround Time (TAT)
    *   Response Time (RT)
---

### ⚙️ Requirements
To successfully run this application, your environment must meet the following specifications:

*   **Python Version:** Python 3.6 or higher must be installed.
*   **System Libraries:** 
    *   `tkinter` 
    

---

### 🚀 Build and Run Steps

Follow these exact steps to launch the simulator on your machine:

1.  **Extract the Project:** Unzip the downloaded project folder to your local machine (e.g., your Desktop).
2.  **Open Terminal / Command Prompt:** Open your command-line interface.
3.  **Verify Python Installation:** Ensure Python is active by typing:
    ```bash
    python --version
    ```
    *(Note: If you are on macOS/Linux, you might need to type `python3 --version`)*
4.  **Navigate to the Source Directory:** Use the `cd` command to move into the `src` folder where the main executable is located:
    ```bash
    cd Desktop/OS_PROJECT/OS_PROJECT/src
    ```
    *(Adjust the path based on exactly where you extracted the folder).*
5.  **Run the Application:** Execute the main Python script to launch the GUI:
    ```bash
    python main.py
    ```
    *(Again, use `python3 main.py` if required by your OS).*

---


