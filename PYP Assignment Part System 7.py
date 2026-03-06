import os
import datetime

# File name
SPACES_FILE = "spaces.txt"
TYPES_FILE = "permit_types.txt"
VEHICLES_FILE = "vehicles.txt"
PERMITS_FILE = "permits.txt"
REQUESTS_FILE = "requests.txt"
LOGS_FILE = "parking_logs.txt"
PASSES_FILE = "temporary_passes.txt"
FILE_REQUESTS = "requests.txt"

# use file with try-except


def read_file(filename):
    try:
        if not os.path.exists(filename):
            return []
        lines = []
        with open(filename, "r") as file:
            for data in file:
                data = data.strip()
                if data:
                    lines.append(data)
        return lines
    except Exception as e:
        print(f"Error reading file '{filename}': {e}")
        return []

def write_file(filename, lines):
    try:
        with open(filename, "w") as file:
            for line in lines:
                file.write(line + "\n")
    except Exception as e:
        print(f"Error writing to file '{filename}': {e}")

def add_line(filename, add):
    try:
        with open(filename, "a") as file:
            file.write(add + "\n")
    except Exception as e:
        print(f"Error appending to file '{filename}': {e}")


# System Administrator part


def add_parking_space():
    print("Add Parking Space")
    space_id = input("Enter New Space ID [EXP (S001)]: ").strip().upper()

    lines = read_file(SPACES_FILE)
    for add in lines:
        if add.startswith(space_id + ","):
            print("Space ID Already Exists！")
            return

    space_type = input("Enter Type (Regular / Reserved / Electric): ").strip().capitalize()
    if space_type not in ["Regular", "Reserved", "Electric"]:
        print("Invalid Type, Please select in [(Regular),(Reserved),(Electric)]")
        return

    new_line = f"{space_id},{space_type},Available"
    add_line(SPACES_FILE, new_line)
    print(f"Renew Successfully！ {space_id} - {space_type} - Available")

def remove_parking_space():
    print("Delete Space ID")
    space_id = input("ID need to delete: ").strip().upper()

    lines = read_file(SPACES_FILE)
    new_lines = []
    found = False

    for remove in lines:
        if remove.startswith(space_id + ","):
            found = True
            print(f"Find & Delete: {remove}")
        else:
            new_lines.append(remove)

    if found:
        write_file(SPACES_FILE, new_lines)
        print("Delete Successfully")
    else:
        print("Undefined")

def update_parking_space():
    print("Update Space ID")
    space_id = input("ID need to update: ").strip().upper()

    lines = read_file(SPACES_FILE)
    new_lines = []
    found = False

    for update in lines:
        if update.startswith(space_id + ","):
            found = True
            parts = update.split(",")
            print(f"Now: {parts[1]} Type, {parts[2]} Status")

            new_type = input("New Type (Press Enter To Maintain): ").strip().capitalize()
            if new_type:
                parts[1] = new_type

            new_status = input("New status (available/occupied)(Press Enter To Maintain): ").strip().lower()
            if new_status:
                parts[2] = new_status

            new_line = ",".join(parts)
            new_lines.append(new_line)
        else:
            new_lines.append(update)

    if found:
        write_file(SPACES_FILE, new_lines)
        print("Update Successfully")
    else:
        print("Undefined")


def add_permit_type():
    print("Add New Permit Type")
    type_name = input("Name of new type (Daily / Monthly / Annual): ").strip().capitalize()

    if type_name not in ["Daily", "Monthly", "Annual"]:
        print("Invalid Type")
        return

    types = read_file(TYPES_FILE)
    for existing in types:
        parts = existing.split(',')
        if len(parts) > 0 and parts[0].strip() == type_name:
            print(f"Type '{type_name}' already exists! Cannot add duplicate.")
            return

    try:
        price = float(input("Price (RM): "))
        if price <= 0:
            print("Price must be positive!")
            return
    except:
        print("Please enter a valid number")
        return

    new_line = f"{type_name},{price:.2f},available"
    add_line(TYPES_FILE, new_line)
    print(f"New type '{type_name}' added successfully with price RM {price:.2f}")

def update_permit_type():
        print("Update Permit Type Price or Availability")

        type_name = input("Enter Type to update (Daily / Monthly / Annual): ").strip().capitalize()

        if type_name not in ["Daily", "Monthly", "Annual"]:
            print("Invalid Type! Must be Daily, Monthly, or Annual.")
            return

        types = read_file(TYPES_FILE)
        new_lines = []
        found = False

        for t in types:
            parts = t.split(',')
            if len(parts) >= 3 and parts[0] == type_name:
                found = True
                current_price = parts[1]
                current_avail = parts[2]

                print(f"\nCurrent Info for '{type_name}':")
                print(f"  Price: RM {current_price}")
                print(f"  Availability: {current_avail}")

                new_price_input = input("Enter new price (RM, press Enter to keep current): ").strip()
                if new_price_input:
                    try:
                        new_price = float(new_price_input)
                        if new_price <= 0:
                            print("Price must be positive! Keeping current.")
                        else:
                            parts[1] = f"{new_price:.2f}"
                            print(f"Price updated to RM {new_price:.2f}")
                    except ValueError:
                        print("Invalid price! Keeping current.")

                new_avail_input = input(
                    "Enter new availability (available/unavailable, press Enter to keep): ").strip().lower()
                if new_avail_input:
                    if new_avail_input in ["available", "unavailable"]:
                        parts[2] = new_avail_input
                        print(f"Availability updated to {new_avail_input}")
                    else:
                        print("Invalid availability! Keeping current.")

                new_line = ",".join(parts)
                new_lines.append(new_line)
            else:
                new_lines.append(t)

        if found:
            write_file(TYPES_FILE, new_lines)
            print(f"\nType '{type_name}' updated successfully!")
        else:
            print(f"\nType '{type_name}' not found!")

def show_simple_report():
    print("\n=== Parking System Report ===")

    # 1. Parking Spaces Status
    spaces = read_file(SPACES_FILE)
    total_spaces = len(spaces)
    available = 0
    occupied = 0
    for space in spaces:
        if ",Available" in space:
            available += 1
        elif ",Occupied" in space:
            occupied += 1
    print(f"Total Parking Spaces: {total_spaces}")
    print(f"Available: {available}")
    print(f"Occupied: {occupied}")
    print(f"Unavailable/Reserved: {total_spaces - available - occupied}")

    # 2. Total Active Permits
    permits = read_file(PERMITS_FILE)
    active_permits = 0
    for permit in permits:
        parts = permit.split(',')
        if len(parts) >= 6 and parts[5].strip() == "Active":
            active_permits += 1
    print(f"\nTotal Active Permits: {active_permits}")

    # 3. Revenue Calculation
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    current_month = datetime.datetime.now().strftime("%Y-%m")
    daily_revenue = 0.0
    monthly_revenue = 0.0

    # Part A: Revenue from Temporary Passes (from passes.txt)
    temp_passes = read_file(PASSES_FILE)
    for tp in temp_passes:
        parts = tp.split(',')
        if len(parts) >= 5:
            issue_time = parts[2].strip()  # issue_time
            try:
                tp_fee = float(parts[4].strip())  # fee 在第5字段
                issue_date = issue_time[:10]  # YYYY-MM-DD
                if issue_date == today:
                    daily_revenue += tp_fee
                if issue_date.startswith(current_month):
                    monthly_revenue += tp_fee
            except ValueError:
                continue

    # Part B: Revenue from Active Permits (type price × count)
    type_prices = {}
    types = read_file(TYPES_FILE)
    for t in types:
        parts = t.split(',')
        if len(parts) >= 3:
            try:
                type_prices[parts[0].strip()] = float(parts[1])
            except ValueError:
                pass

    type_counts = {"Daily": 0, "Monthly": 0, "Annual": 0}
    for permit in permits:
        parts = permit.split(',')
        if len(parts) >= 6 and parts[5].strip() == "Active":
            p_type = parts[3].strip()
            if p_type in type_counts:
                type_counts[p_type] += 1

    permit_revenue = 0.0
    for p_type, count in type_counts.items():
        price = type_prices.get(p_type, 0.0)
        permit_revenue += count * price

    # Total Revenue = Temporary Passes + Active Permits
    total_revenue = monthly_revenue + permit_revenue

    print(f"\nRevenue Summary:")
    print(f"  Daily Revenue (from Temp Passes, today {today}): RM {daily_revenue:.2f}")
    print(f"  Monthly Revenue (from Temp Passes, {current_month}): RM {monthly_revenue:.2f}")
    print(f"  Revenue from Active Permits (fixed): RM {permit_revenue:.2f}")
    print(f"Total Monthly Revenue: RM {total_revenue:.2f}")

def view_all():
    print("\nShow all Record")

    print("\nParking Space:")
    for record in read_file(SPACES_FILE):
        print(record)

    print("\nPermit Type:")
    for record in read_file(TYPES_FILE):
        print(record)


def admin_menu():
    print("Welcome for using System Administrator")

    while True:
        print("\nPlease select an option:")
        print("1 - Add parking space")
        print("2 - Delete parking space")
        print("3 - Update parking space")
        print("4 - Add permit type")
        print("5 - Update permit type price/availability")
        print("6 - Show Report")
        print("7 - View all Record")
        print("0 - Back")

        choice = input("Please enter an option number: ").strip()

        if choice == "1":
            add_parking_space()
        elif choice == "2":
            remove_parking_space()
        elif choice == "3":
            update_parking_space()
        elif choice == "4":
            add_permit_type()
        elif choice == "5":
            update_permit_type()
        elif choice == "6":
            show_simple_report()
        elif choice == "7":
            view_all()
        elif choice == "0":
            main()
        else:
            print("Invalid Number Option！")



# Parking Staff Part

def check_availability():
    print("AVAILABLE PARKING SPACES")

    try:
        lines = read_file(SPACES_FILE)
        for line in lines:
            line = line.strip()
            if line != "":
                parts = line.split(',')
                if len(parts) >= 3 and parts[2] == "Available":
                    print(f"{parts[0]} - {parts[1]}")
    except:
        print("Error: File not found!")


def record_entry():
    print("RECORD VEHICLE ENTRY")

    plate = input("Enter plate number: ").upper()
    if plate == "":
        print("Error: Plate cannot be empty!")
        return

    print("1. Regular  2. Electric  3. Reserved")
    choice = input("Choose type: ")

    if choice == "1":
        space_type = "Regular"
    elif choice == "2":
        space_type = "Electric"
    elif choice == "3":
        space_type = "Reserved"
    else:
        print("Invalid choice!")
        return

    lines = read_file(SPACES_FILE)
    space_id = None
    new_lines = []
    for line in lines:
        parts = line.strip().split(',')
        if len(parts) >= 3 and parts[1] == space_type and parts[2] == "Available":
            space_id = parts[0]
            new_lines.append(f"{parts[0]},{parts[1]},Occupied")
        else:
            new_lines.append(line)

    if space_id == None:
        print(f"No {space_type} spaces available!")
        return

    write_file(SPACES_FILE, new_lines)

    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    add_line(VEHICLES_FILE, f"{plate},{time_now},{space_id}")
    add_line(LOGS_FILE, f"{plate},{time_now},Parked,{space_id},0")

    print(f"\nSuccess! Assigned to {space_id}")
    print(f"Entry time: {time_now}")


def record_exit():
    print("\n=== RECORD VEHICLE EXIT ===")
    plate = input("Enter plate number: ").upper().strip()
    if not plate: return

   
    logs = read_file(LOGS_FILE)
    new_logs, found, entry_time, space_id = [], False, "", ""

    for line in logs:
        parts = line.strip().split(',')
       
        if not found and parts[0] == plate and parts[2] == "Parked":
            found = True
            entry_time = parts[1]
            space_id = parts[3]
            exit_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            new_logs.append(f"{plate},{entry_time},{exit_time},{space_id},5.0")
        else:
            new_logs.append(line)

    if not found:
        print("Error: No active parking record found for this plate.")
        return

   
    spaces = read_file(SPACES_FILE)
    new_spaces = []
    for line in spaces:
        if line.startswith(space_id + ","):
            parts = line.split(',')
            new_spaces.append(f"{parts[0]},{parts[1]},Available")
        else:
            new_spaces.append(line)

    
    write_file(SPACES_FILE, new_spaces)
    write_file(LOGS_FILE, new_logs)

    print(f"\nSuccess! {plate} exited from {space_id}.")
    print(f"Exit time: {exit_time} | Fee: RM 5.00")

def issue_pass():
    print("ISSUE TEMPORARY PASS")

    plate = input("Enter plate number: ").upper().strip()
    if not plate:
        print("Error: Plate number cannot be empty!")
        return

    full_fee_input = input("Enter fee (RM): ").strip()
    validity_days_input = input("Enter validity days (e.g., 1): ").strip()

    try:
        validity_days = int(validity_days_input)
        if validity_days <= 0:
            print("Validity days must be positive! Using default 1 day.")
            validity_days = 1
    except ValueError:
        print("Invalid days! Using default 1 day.")
        validity_days = 1

    try:
        full_fee = float(full_fee_input)
        if full_fee <= 0:
            print("Full fee must be positive! Using default RM 5.00.")
            full_fee = 5.00
    except ValueError:
        print("Invalid fee! Using default RM 5.00.")
        full_fee = 5.00

    today = datetime.date.today()
    expiry_date = today + datetime.timedelta(days=validity_days)
    expiry_str = expiry_date.strftime("%Y-%m-%d")

    count = len(read_file(PASSES_FILE))
    pass_id = f"TEMP{count + 1:04d}"
    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    new_line = f"{pass_id},{plate},{time_now},{validity_days},{full_fee:.2f},{expiry_str}"
    add_line(PASSES_FILE, new_line)

    print(f"\nTemporary Pass Issued Successfully!")
    print(f"Pass ID: {pass_id}")
    print(f"Plate: {plate}")
    print(f"Issued on: {time_now}")
    print(f"Valid until: {expiry_str} ({validity_days} days)")
    print(f"Full fee set: RM {full_fee:.2f}")

def view_logs():
    print("TODAY'S LOGS")

    today = datetime.datetime.now().strftime("%Y-%m-%d")

    try:
        lines = read_file(LOGS_FILE)
        for line in lines:
            if today in line:
                parts = line.strip().split(',')
                print(f"{parts[0]} - {parts[1]} - Space {parts[3]}")
    except:
        print("No logs found!")


def staff_menu():
    while True:
        print("      PARKING STAFF MENU")
        print("1. Check Availability")
        print("2. Record Vehicle Entry")
        print("3. Record Vehicle Exit")
        print("4. Issue Temporary Pass")
        print("5. View Daily Logs")
        print("0. Back")

        choice = input("\nEnter choice: ").strip()

        if choice == '1':
            check_availability()
        elif choice == '2':
            record_entry()
        elif choice == '3':
            record_exit()
        elif choice == '4':
            issue_pass()
        elif choice == '5':
            view_logs()
        elif choice == '0':
            main()
        else:
            print("Invalid choice!")

        input("\nPress Enter to continue...")


# Permit Officer Part


# --- Global Variables ---

def read_permit_file():
    """Reads the permit file and returns a list of lines."""
    try:
        with open(PERMITS_FILE, "r") as file:
            lines = [line.strip() for line in file if line.strip()]
        return lines
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"Error Reading File: {e}")
        return []

def write_permit_file(lines):
    """Writes a list of lines back to the permit file."""
    try:
        with open(PERMITS_FILE, "w") as file:
            file.write("\n".join(lines) + "\n")
        return True
    except Exception as e:
        print(f"Error Writing File: {e}")
        return False

# FEATURE FUNCTIONS ---
def check_expiry_notifications(lines):
    updated_lines = []
    has_changes = False
    today = datetime.datetime.now().date()
    notification_count = 0
    for line in lines:
        parts = [p.strip() for p in line.split(',')]
        if len(parts) == 7:
            permit_id, name, plate, permit_type, issue_date, expiry_str, status = parts
            try:
                expiry_date = datetime.datetime.strptime(expiry_str, "%Y-%m-%d").date()
                # Only flag if it's currently Active and past its expiry date. 
                # Ignore Cancelled or already Expired permits
                if expiry_date < today and status.lower() == "active":
                    print(f"ALERT: Permit {permit_id} ({plate}) EXPIRED on {expiry_str}! Auto-updating status.")
                    status = "Expired"
                    has_changes = True
                    notification_count += 1
                updated_lines.append(f"{permit_id},{name},{plate},{permit_type},{issue_date},{expiry_str},{status}")
            except ValueError:
                # If date format is somehow corrupted, keep line as is to prevent crashing
                updated_lines.append(line)
        else:
            updated_lines.append(line)
    # Save updates to the text file in the background if statuses changed
    if has_changes:
        write_permit_file(updated_lines)
        return updated_lines
    return lines

def issue_permit():
    print("\n--- Pending Permit Requests ---")
    # Fetch pending requests submitted by Vehicle Owners
    requests = read_file(REQUESTS_FILE)
    if not requests:
        print("No pending requests found from Vehicle Owners.")
        return
    # Filter out empty or corrupted lines
    valid_requests = []
    for req in requests:
        parts = [p.strip() for p in req.split(',')]
        if len(parts) >= 3:
            valid_requests.append(req)
    if not valid_requests:
        print("No valid pending requests.")
        return
    # Display the requests for the Officer to choose from
    for i, req in enumerate(valid_requests, 1):
        parts = req.split(',')
        print(f"{i}. Plate: {parts[0]:<10} | Type: {parts[1]:<10} | Date Requested: {parts[2]}")
    # Officer selects a request to approve
    while True:
        choice = input("\nSelect a request to approve (or 0 to cancel): ").strip()
        if choice == '0':
            return
        try:
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(valid_requests):
                break  # Valid input, break out of the loop
            else:
                print("Error: Invalid selection. Please pick a number from the list.")
        except ValueError:
            print("Error: Please enter a valid number.")
    # Extract the data from the chosen request
    selected_req = valid_requests[choice_idx]
    parts = selected_req.split(',')
    req_plate = parts[0]
    req_type = parts[1]
    print(f"\n--- Approving Permit for Plate: {req_plate} ---")
   # Officer inputs the remaining manual details
    current_permits = read_permit_file()
    while True:
        permit_id = input("Enter New Permit ID (e.g., P001): ").strip().upper() 
        if not permit_id:
            print("Error: Permit ID cannot be empty.")
            continue
        is_duplicate = False
        for line in current_permits:
            p_parts = [p.strip() for p in line.split(',')]
            if len(p_parts) > 0 and p_parts[0] == permit_id:
                is_duplicate = True
                break
        if is_duplicate:
            print(f"Error: Permit ID '{permit_id}' Already Exists. Please try another.")
        else:
            break  # Unique ID found, break out of the loop
    name = input("Enter Owner Name: ").strip()
    while not name:
        print("Error: Name cannot be empty.")
        name = input("Enter Owner Name: ").strip()
    # Automatically Calculate Dates
    issue_date_obj = datetime.datetime.now()
    issue_date = issue_date_obj.strftime("%Y-%m-%d")
    # Auto-add days based on the requested permit type
    if req_type.lower() == "daily":
        expiry_obj = issue_date_obj + datetime.timedelta(days=1)
    elif req_type.lower() == "monthly":
        expiry_obj = issue_date_obj + datetime.timedelta(days=30)
    elif req_type.lower() == "annual":
        expiry_obj = issue_date_obj + datetime.timedelta(days=365)
    else:
        expiry_obj = issue_date_obj + datetime.timedelta(days=1)
    expiry = expiry_obj.strftime("%Y-%m-%d")
    status = "Active"
    # Save the new permit to permits.txt
    new_record = f"{permit_id},{name},{req_plate},{req_type},{issue_date},{expiry},{status}"
    try:
        with open(PERMITS_FILE, "a") as file:
            file.write(new_record + "\n")
        print(f"Permit '{permit_id}' Issued Successfully!")
        print(f"Issue Date: {issue_date} | Expiry Date: {expiry}")
        # 7. Remove the approved request from requests.txt so it doesn't show up again
        updated_requests = [req for req in requests if req != selected_req]
        write_file(REQUESTS_FILE, updated_requests)
    except Exception as e:
        print(f"An Error Occurred: {e}")
        
def view_permit_list():
    lines = read_permit_file()
    if not lines:
        print("\nNo Permit Records Found.")
        return
    # Automatically check for and update expired permits before displaying
    lines = check_expiry_notifications(lines)
    print("\n" + "="*95)
    print(f"{'ID':<8} | {'Owner':<15} | {'Plate':<10} | {'Type':<10} | {'Issued':<10} | {'Expiry':<10} | {'Status':<10}")
    print("-" * 95)
    active_count = 0
    expired_count = 0
    cancelled_count = 0
    for line in lines:
        parts = [p.strip() for p in line.split(',')]
        if len(parts) == 7:
            permit_id, name, plate, permit_type, issue_date, expiry, status = parts
            # Truncate long names to prevent the table from breaking format
            display_name = name[:12] + "..." if len(name) > 15 else name
            print(f"{permit_id:<8} | {display_name:<15} | {plate:<10} | {permit_type:<10} | {issue_date:<10} | {expiry:<10} | {status:<10}")
            # Tally up the statuses for the summary
            if status.lower() == "active":
                active_count += 1
            elif status.lower() == "expired":
                expired_count += 1
            elif status.lower() == "cancelled":
                cancelled_count += 1
    print("-" * 95)
    print(f"Total Permits: {len(lines)} (Active: {active_count}, Expired: {expired_count}, Cancelled: {cancelled_count})")
    print("="*95)

def renew_permit():
    print("\n--- Renew Permit ---")
    target_id = input("Enter Permit ID To Renew: ").strip().upper()
    lines = read_permit_file()
    updated_lines = []
    found = False
    for line in lines:
        parts = [p.strip() for p in line.split(',')]
        if len(parts) >= 7 and parts[0] == target_id:
            found = True
            permit_type = parts[3]
            print(f"Current Expiry: {parts[5]} | Type: {permit_type}")
            confirm = input("Do you want to process this renewal? (y/n): ").strip().lower()
            while True:
                confirm = input("Do you want to process this renewal? (y/n): ").strip().lower()
                if confirm in ['y', 'n']:
                    break
                print("Invalid input. Please type 'y' for yes or 'n' for no.")
            if confirm == 'y':
                # Auto-calculate new date from today
                today_obj = datetime.datetime.now()
                if permit_type.lower() == "daily":
                    new_expiry_obj = today_obj + datetime.timedelta(days=1)
                elif permit_type.lower() == "monthly":
                    new_expiry_obj = today_obj + datetime.timedelta(days=30)
                elif permit_type.lower() == "annual":
                    new_expiry_obj = today_obj + datetime.timedelta(days=365)
                else:
                    new_expiry_obj = today_obj + datetime.timedelta(days=1)

                parts[5] = new_expiry_obj.strftime("%Y-%m-%d")
                parts[6] = "Active"  # Reactivate it if it was expired
                print(f"Permit '{target_id}' Auto-Renewed Successfully until {parts[5]}.")
            else:
                print("Renewal cancelled.")
                
            updated_lines.append(",".join(parts))
        else:
            updated_lines.append(line)
    if not found:
        print(f"Permit ID '{target_id}' Not Found.")
    else:
        write_permit_file(updated_lines)

def update_permit_info():
    print("\n--- Update Permit Info ---")
    target_id = input("Enter Permit ID To Update: ").strip().upper()

    lines = read_permit_file()
    updated_lines = []
    found = False

    for line in lines:
        parts = [p.strip() for p in line.split(',')]
        if parts[0] == target_id:
            found = True
            print(f"Current: {parts[1]} | {parts[2]} | {parts[3]}")
            print("1. Update Name")
            print("2. Update Plate")
            print("3. Update Type")
            choice = input("Enter Choice: ").strip()

            if choice == '1':
                parts[1] = input("Enter New Name: ").strip()
                print("Record Updated Successfully.")
            elif choice == '2':
                parts[2] = input("Enter New Plate: ").strip()
                print("Record Updated Successfully.")
            elif choice == '3':
                # Fetch permit types
                types_lines = read_file(TYPES_FILE)
                available_types = []
                for t_line in types_lines:
                    t_parts = t_line.split(',')
                    if len(t_parts) > 0:
                        available_types.append(t_parts[0])
                
                if not available_types:
                    print("No permit types available.")
                else:
                    print("\nSelect New Type:")
                    for i, t in enumerate(available_types, 1):
                        print(f"{i}. {t}")
                        
                    type_choice = input(f"Enter Choice (1-{len(available_types)}): ").strip()
                    try:
                        choice_idx = int(type_choice) - 1
                        if 0 <= choice_idx < len(available_types):
                            new_type = available_types[choice_idx]
                            parts[3] = new_type
                            
                            # --- NEW: Auto-update expiry based on new type ---
                            today_obj = datetime.datetime.now()
                            if new_type.lower() == "daily":
                                new_exp = today_obj + datetime.timedelta(days=1)
                            elif new_type.lower() == "monthly":
                                new_exp = today_obj + datetime.timedelta(days=30)
                            elif new_type.lower() == "annual":
                                new_exp = today_obj + datetime.timedelta(days=365)
                            else:
                                new_exp = today_obj + datetime.timedelta(days=1)
                                
                            parts[5] = new_exp.strftime("%Y-%m-%d")
                            print(f"Type updated to {new_type}. Expiry automatically adjusted to {parts[5]}.")
                        else:
                            print("Invalid Choice. No update will be made.")
                    except ValueError:
                        print("Error: Please enter a valid number.")
            else:
                print("Invalid Choice. No update will be made.")
        updated_lines.append(",".join(parts))
        
    if not found:
        print(f"Permit ID '{target_id}' Not Found.")
    else:
        write_permit_file(updated_lines)

def cancel_permit():
    print("\n--- Cancel Permit ---")
    target_id = input("Enter Permit ID To Cancel: ").strip().upper()
    lines = read_permit_file()
    updated_lines = []
    found = False
    for line in lines:
        parts = [p.strip() for p in line.split(',')]
        if len(parts) >= 7 and parts[0] == target_id:
            found = True
            confirm = input(f"Are you sure you want to cancel {target_id}? (y/n): ").lower()
            while True:
                confirm = input(f"Are you sure you want to cancel {target_id}? (y/n): ").strip().lower()
                if confirm in ['y', 'n']:
                    break
                print("Invalid input. Please type 'y' for yes or 'n' for no.")
            if confirm == 'y':
                parts[6] = "Cancelled" # Soft delete instead of removing line
                print(f"Permit '{target_id}' Status changed to Cancelled.")
            else:
                print("Cancellation aborted. Permit retained.")
                
            updated_lines.append(",".join(parts))
        else:
            updated_lines.append(line)

    if not found:
        print(f"Permit ID '{target_id}' Not Found.")
    else:
        write_permit_file(updated_lines)

# MENU SYSTEM

def permit_officer_menu():
    while True:
        print("PERMIT OFFICER MENU")
        print("1. Issue Permit")
        print("2. Renew Permit")
        print("3. Cancel Permit")
        print("4. Update Permit Information")
        print("5. View Permit List (Check for Expiry)")
        print("6. Back to Main Menu")

        choice = input("Enter your choice: ").strip()

        if choice == '1':
            issue_permit()
        elif choice == '2':
            renew_permit()
        elif choice == '3':
            cancel_permit()
        elif choice == '4':
            update_permit_info()
        elif choice == '5':
            view_permit_list()
        elif choice == '6':
            break
        else:
            print("Invalid Choice.")

# Vehicle Owner Part


def vehicle_owner_menu():
    while True:
        print("VEHICLE OWNER MENU")
        print("1. Register vehicle")
        print("2. View permit status")
        print("3. Request permit")
        print("4. View parking history")
        print("5. Back")

        choice = input("Enter option (1-5): ").strip()

        if choice == '1':
            register_vehicle()
        elif choice == '2':
            view_permit_status()
        elif choice == '3':
            request_permit()
        elif choice == '4':
            view_parking_history()
        elif choice == '5':
            break
        else:
            print("Invalid input. Please enter 1-5.")


def register_vehicle():
    print("Register New Vehicle")
    plate = input("Enter Plate Number: ").strip().upper()

    if not plate:
        print("Error: Plate number cannot be empty!")
        return

    if is_plate_registered(plate):
        print(f"Error: Vehicle '{plate}' is already registered!")
        return

    make = input("Enter Car Make (e.g., Toyota): ").strip().capitalize()
    model = input("Enter Car Model (e.g., Vios): ").strip().capitalize()
    color = input("Enter Color (e.g., Red): ").strip().capitalize()

    if not make or not model or not color:
        print("Error: All fields are required.")
        return

    try:
        with open(VEHICLES_FILE, "a") as f:
            f.write(f"{plate},{make},{model},{color}\n")
        print(f"Success: Vehicle {plate} registered.")
    except Exception as e:
        print(f"Error saving file: {e}")


def view_permit_status():
    print("View Permit Status")
    plate = input("Enter Plate Number to search: ").strip().upper()

    found = False
    try:
        if not os.path.exists(PERMITS_FILE):
            print("No permit records found.")
            return

        with open(PERMITS_FILE, "r") as f:
            for line in f:
                data = line.strip().split(',')
                # Changed from >= 5 to >= 7 because we now have 7 fields
                if len(data) >= 7 and data[2] == plate:
                    print("\nPermit Found:")
                    print(f"Type: {data[3]}")
                    print(f"Issued: {data[4]}") # Added the new Issue Date field
                    print(f"Expiry: {data[5]}") # Shifted index from 4 to 5
                    status = data[6] if len(data) > 6 else "Active" # Shifted index from 5 to 6
                    print(f"Status: {status}")
                    found = True

        if not found:
            print(f"No active permit found for '{plate}'.")

    except Exception as e:
        print(f"Error reading permits: {e}")

def request_permit():
    """
    Function 3: Request Permit
    Submits a request and saves it to the requests.txt file.
    Format: Plate,Type,RequestDate
    """
    print("Request Permit")
    plate = input("Enter Plate Number: ").strip().upper()

    # Verify if the vehicle is registered; only registered owners can request permits
    if not is_plate_registered(plate):
        print("Error: Please register your vehicle first (Option 1).")
        return

    print("Options: Daily, Monthly, Annual")
    p_type = input("Enter Permit Type: ").strip().capitalize()

    # Validate if the permit type is valid
    if p_type not in ["Daily", "Monthly", "Annual"]:
        print("Error: Invalid type. Choose Daily, Monthly, or Annual.")
        return

    # Get today's date from the system
    request_date = str(datetime.date.today())

    # Write to the request file
    try:
        with open(FILE_REQUESTS, "a") as f:
            f.write(f"{plate},{p_type},{request_date}\n")
        print("Request submitted successfully.")
    except Exception as e:
        print(f"Error: {e}")

def view_parking_history():
    print("\n--- View Parking History ---")
    plate = input("Enter Plate Number: ").strip().upper()
    
    lines = read_file(LOGS_FILE)
    if not lines:
        print("No parking logs found.")
        return

    print(f"\nHistory for [{plate}]:")
    
    print(f"{'Entry Time':<20} | {'Exit Time':<20} | {'Slot':<10} | {'Fee'}")
    print("-" * 75)

    found_any = False
    for line in lines:
        data = line.strip().split(',')
        if len(data) >= 4 and data[0] == plate:
            entry_t = data[1]
            
            exit_t = data[2] if data[2] != "Parked" else "Still Parked"
            slot = data[3]
            
            fee = f"RM{data[4]}" if len(data) > 4 else "RM0.0"
            
            print(f"{entry_t:<20} | {exit_t:<20} | {slot:<10} | {fee}")
            found_any = True

    if not found_any:
        print("No history found for this vehicle.")

def is_plate_registered(plate):
    if not os.path.exists(VEHICLES_FILE):
        return False
    try:
        with open(VEHICLES_FILE, "r") as f:
            for line in f:
                data = line.strip().split(',')
                if data and data[0] == plate:
                    return True
    except:
        return False
    return False


# Main Menu


def main():
    while True:
        print("1 Admin")
        print("2 Staff")
        print("3 Officer")
        print("4 Owner")
        print("0 Exit")
        choice = input("Choice: ").strip()
        if choice == "1":
            pw1 = input("Admin password: ").strip()
            if pw1 == "ad1234":
                admin_menu()
            else:
                print("Wrong password")
                main()
        elif choice == "2":
            pw2 = input("Staff password: ").strip()
            if pw2 == "st1234":
                staff_menu()
            else:
                print("Wrong password")
                main()
        elif choice == "3":
            pw3 = input("Officer password: ").strip()
            if pw3 == "of1234":
                permit_officer_menu()
            else:
                print("Wrong password")
                main()
        elif choice == "4":
            vehicle_owner_menu()
        elif choice == "0":
            confirm = input("Are you sure to log out? (y/n): ").lower()
            if confirm != "y":
                continue
            print("Thanks for using System！")
            break
        else:
            print("Invalid Choice")


if __name__ == "__main__":

    main()











