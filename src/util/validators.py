def validate_process_input(pid, arrival_str, burst_str, priority_str, all_processes):
    """
    Validates process input. Returns (is_valid, errors_list, parsed_values).
    parsed_values is a tuple: (arrival_time, burst_time, priority)
    """
    errors = []
    
    if not (pid and arrival_str and burst_str and priority_str):
        return False, ["All fields must be filled!"], None
        
    at_val, bt_val, pr_val = 0, 0, 0
    try:
        at_val = int(arrival_str)
        if at_val < 0: errors.append("- Arrival Time cannot be negative.")
    except ValueError:
        errors.append("- Arrival Time must be a valid number.")

    try:
        bt_val = int(burst_str)
        if bt_val <= 0: errors.append("- Burst Time must be greater than zero.")
    except ValueError:
        errors.append("- Burst Time must be a valid number.")

    try:
        pr_val = int(priority_str)
        if pr_val < 0 or pr_val > 10:
            errors.append("- Wrong number for priority. Please enter a number in the range 0 to 10.")
    except ValueError:
        errors.append("- Priority must be a valid whole number (no decimals, text, or symbols).")

    if any(p.pid == pid for p in all_processes):
        errors.append(f"- Process ID '{pid}' already exists.")
        
    if errors:
        return False, errors, None
        
    return True, [], (at_val, bt_val, pr_val)
