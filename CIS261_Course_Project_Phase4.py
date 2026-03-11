#Stephanie Brainard
#CIS261 Course Project
#Phase 4
#Week 9

# -------------------------------
# IMPORTS
# -------------------------------

from datetime import datetime, timedelta
import bcrypt

# ------------------------------
# HELPER FUNCTIONS
#-------------------------------

#Displays the name of the program
def start_heading():
    print("\nEMPLOYEE PAYROLL AUTOMATION POC")

#Function that returns to menu
def back_to_menu():
    input("\nPress Enter to return to the menu...")

#Function to create new user
def load_users():
    users_list = []

    try:
        with open("users.txt", "r") as file:
            for line in file:
                parts = line.strip().split("|")
                if len(parts) >= 1:
                    users_list.append(parts[0].lower())
    except FileNotFoundError:
        pass
    
    return users_list

#Shows current user and authorization code
def show_logged_user(user, role):
    print(f"\nLOGGED IN AS: {user} ({role})")

def menu_choice(prompt, options):
    while True:
        choice = input(prompt).strip()
        if choice in options:
            return choice
        
        print(f"\nInvalid selection. Please choose {', '.join(options)}.")

#Checks to see that the file that stores and reads the list info exists
def data_check(filename):
    try:
        with open(filename, "r") as file:
            return bool(file.readline().strip())
    except FileNotFoundError:
        return False

# ------------------------------
# TABLE DISPLAY FUNCTIONS
# ------------------------------

#Creates a header for a table display for search_report() output
def display_report_header(user, role):
    
    show_logged_user(user, role)

    headers = [
        f"{'Start':12}",
        f"{'End':12}", 
        f"{'Employee':20}",
        f"{'Hours':8}",
        f"{'Pay Rate':10}",
        f"{'Tax Rate':10}",
        f"{'Gross':10}",
        f"{'Total Tax':13}",
        f"{'Net':10}"
    ]

    headerLine = " ".join(headers)

    print("\nEMPLOYEE PAYROLL REPORT:\n")
    print(headerLine)
    print("-" * len(headerLine))
    
    return len(headerLine)

#Creates rows to display info for search_report() table
def employee_row_format(parts):
    row = [
        f"{parts[0]:<12}",
        f"{parts[1]:<12}",
        f"{parts[2]:<20}",
        f"{float(parts[3]):>8.2f}",
        f"{float(parts[4]):>10.2f}",
        f"{float(parts[5]):>10.2f}",
        f"{float(parts[6]):>10.2f}",
        f"{float(parts[7]):>13.2f}",
        f"{float(parts[8]):>10.2f}"
    ]

    return " ".join(row)

#Creates a row to display totals within the search_report() display table
def display_report_totals_row(total_hours, total_gross, total_taxes, total_net, width):
    
    totals_row = [
        f"{'Totals':<12}",
        f"{'':<12}",
        f"{'':<20}",
        f"{total_hours:>8.2f}",
        f"{'':>10}",
        f"{'':>10}",
        f"{total_gross:>10.2f}",
        f"{total_taxes:>13.2f}",
        f"{total_net:>10.2f}"
    ]

    rowLine = " ".join(totals_row)

    print("-" * width)

    return rowLine

#Creates a header for the table for display_users()
def all_users_header(user, role):
    
    show_logged_user(user, role)

    users_header = [
        f"{'Username':<20}",
        f"{'Authorization Code':<20}"
    ]
    
    headerLine = " ".join(users_header)
    
    print("\nALL USERS:\n")
    print(headerLine)
    print("-" * len(headerLine))
    

#Creates the rows that display user info for display_users() 
def all_users_row(username, userRole):
    
    users_row = [
        f"{username:<20}",
        f"{userRole:<20}"
    ]
    return " ".join(users_row)

#Creates a table to display running totals and final totals add_employee_payroll()
def totals_table(user, role, total_counts, title):

    print(f"{title}\n")

    header = [
        f"{'Employees':<12}",
        f"{'Hours':>10}",
        f"{'Gross':>12}",
        f"{'Taxes':>12}",
        f"{'Net':>12}"
    ]

    headerLine = " ".join(header)
    print(headerLine)
    print("-" * len(headerLine))


    row = [
        f"{total_counts['empCount']:<12}",
        f"{total_counts['hours']:>10.2f}",
        f"{total_counts['gross']:>12.2f}",
        f"{total_counts['taxes']:>12.2f}",
        f"{total_counts['net']:>12.2f}"
    ]

    print(" ".join(row))


# ------------------------------
# AUTHENTICATION FUNCTIONS
# ------------------------------

#Hashes password for added security
def hash_password(password):
    passwordBytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(passwordBytes,salt)
    return hashed.decode("utf-8")

#Verifies hash for password entered matches stored value
def verify_password(password, storedHash):
    enteredBytes = password.encode("utf-8")
    storedBytes = storedHash.encode("utf-8")
    return bcrypt.checkpw(enteredBytes, storedBytes)

#Creates new users
def create_user():
    while True:
        users_list = load_users()
        
        while True:
            userNew= input("Enter new username: ").strip().lower()

            if userNew == "":
                print("Username cannot be blank.")
            elif userNew in users_list:
                print("Username already exists. Please choose another.")
            
            else:
                break

        while True:
            userPass = input("Enter password: ").strip()
            
            if userPass == "":
                print("Password cannot be blank.")
                continue

            confirmPass = input("Confirm password: ")

            if userPass != confirmPass:
               print("\nPasswords do not match. Please try again.\n") 
               continue
            break
    
        hashedPass = hash_password(userPass)

        while True:
            validRoles = ("Admin", "User")
            
            if not users_list:
                userRole = "Admin"
                print("First user created as admin.")
            
            else:
                userRole = input("Enter authorization code (Admin or User): ").strip().title()
        
            if userRole in validRoles:
                break
            
            else:
                print("Invalid authorization code. Please enter Admin or User")
    
        with open("users.txt", "a") as file: 
            file.write(f"{userNew}|{hashedPass}|{userRole}\n")
        print("User created successfully")

        addAnother = input("\nAdd another user ('y' or 'n')? ").strip().lower()

        if addAnother == "n":
            print("\nDirecting to menu...")
            break
        elif addAnother != 'y':
            print("\nInvalid entry. Please enter 'Y' or 'N'. ")
            
        
#Allows user to login
def user_login():
    print("\nPlease Login:\n")

    MAX_USER_ATTEMPTS = 3
    MAX_PW_ATTEMPTS = 3

    userAttempts = 0

    while userAttempts < MAX_USER_ATTEMPTS:

    
        userName = input("Enter your username (or 'End' to exit): ").strip().lower()
    
        if userName.lower() == "end":
            print("\nExiting program...")
            print("\nGoodbye!\n")
            return None, None
    
        try:
            with open("users.txt", "r") as file:
                
                userFound = False

                for line in file:
                
                    parts = line.strip().split("|")
                
                    if len(parts) != 3:
                        continue
                
                    storedUser = parts[0].lower()
                    storedHash = parts[1]
                    storedRole = parts[2]
            
            
                    if userName == storedUser:
                        
                        userFound = True
                        pwAttempts = 0

                        while pwAttempts < MAX_PW_ATTEMPTS:

                            password = input("Enter your Password: ").strip()

                            if verify_password(password, storedHash):
                                print("\nLogin Successful.")
                                print(f"\nAuthorization code: {storedRole}")
                                return storedUser, storedRole
                        
                            else:
                                pwAttempts += 1
                                print(f"Invalid password. {MAX_PW_ATTEMPTS - pwAttempts} attempts remaining.")
                             
                        print("Too many password attempts. Exiting program.")
                        return None, None

                if not userFound:
                    userAttempts += 1
                    print(f"Username not found. {MAX_USER_ATTEMPTS - userAttempts} attempts remaining.")

        except FileNotFoundError:
            print("No users exist. Please create an admin account first. ")
            return None, None

    print("\nToo many username attempts. Exiting program.")
    return None, None

# ------------------------------
# DISPLAY ALL USERS FUNCTION
# ------------------------------

#Displays all users and their authorization codes   
def display_users(user, role):
    all_users_header(user, role)

    try:
        with open("users.txt", "r") as file:

            for line in file:
                parts = line.strip().split("|")

                if len(parts) != 3:
                    continue
                
                username = (parts[0])
               #userPassword = (parts[1])
                userRole = (parts[2])

                print(all_users_row(username, userRole))
                
        back_to_menu()
                
    
    except FileNotFoundError:
        print("\nNo user records exist yet.")


# ----------------------------
# PAYROLL FUNCTIONS
# ----------------------------

#Getting employee name
def get_name():
    employeeFName = input("Enter the employee's first name (or 'End' to quit): ").strip().title()

    if employeeFName.lower() == "end":
        return None

    employeeLName = input("Enter the employee's last name: ").strip().title()

    employeeName = f"{employeeFName} {employeeLName}"

    return employeeName

#getting dates and times
def get_hours(): 
    while True:
        dateWrkdInput = input("Enter the date (MM/DD/YYYY) employee worked: ")
        
        try:
            dateWorked = datetime.strptime(dateWrkdInput, "%m/%d/%Y").date()
            break
        except ValueError:
                print("\nYou entered an invalid format. Please use MM/DD/YYYY format.")
            
    while True:
        startTimeInput = input("Enter the start time (HH:MM 24hr): ")
        
        try:
            startTime = datetime.strptime(f"{startTimeInput}", "%H:%M")
            break
        except ValueError:
            print("\nYou entered an invalid format. Please enter HH:MM using 24hr clock format.")

    while True:        
        endTimeInput = input("Enter the end time (HH:MM 24hr): ")
        
        try:
            endTime = datetime.strptime(f"{endTimeInput}", "%H:%M")
            break               
        except ValueError:                   
            print("\nInvalid format.")
       
    if endTime < startTime:
        endTime += timedelta(days=1)
        
    hoursWorked =  (endTime - startTime).total_seconds() / 3600
    
    
    
    return dateWorked, hoursWorked

#getting date ranges
def getDateRngs(dates_list):
    if not dates_list:
        return 
    return min(dates_list), max(dates_list)
    
#Get hourly wage        
def get_rate ():
    while True:
        try:
            payRate = float(input("Enter the employee hourly wage: "))
            if payRate >= 0:
                return payRate
            else:
                print("\nHourly wage cannot be negative. Please try again.")
        except ValueError:
            print("\nPlease enter a valid positive number. ")

#Get income tax rate
def get_tax ():
    while True:
        try:
            taxRate = float(input("Enter income tax rate: "))
            if 0 <= taxRate < 1:
                return taxRate   
            else:
                print("\nIncome tax rate cannot be an integer. Please enter in decimal form (e.g. .10 for 10%). ")
        except ValueError:
            print("\nPlease enter a decimal. ")          
        
#Calculator
def calc_pay (payRate, hoursWorked, taxRate): 
    grossPay = payRate * hoursWorked
    totalTax = grossPay * taxRate
    netPay = grossPay - totalTax
    return grossPay, totalTax, netPay
 
def display_info(employee_record, user, role):
    show_logged_user(user, role)
    
    
    
    sDate, eDate = employee_record['dates']
    start = sDate.strftime("%b %d, %Y")
    end = eDate.strftime("%b %d, %Y")

    if sDate == eDate:
        dateDis = start
    else:
        dateDis = f"{start} - {end}"

    header = [
        f"{'Employee Name':<20}",
        f"{'Dates Worked':40}",
        f"{'Total Hours':>12}",
        f"{'Pay Rate':>12}",
        f"{'Tax Rate':>12}",
        f"{'Gross':>12}",
        f"{'Taxes Paid':>15}",
        f"{'Net':>12}"
    ]

    headerLine = " ".join(header)

    print("\nEMPLOYEE INFORMATION:\n")
    print(headerLine)
    print("-" *len(headerLine))
    
    row = [
        f"{employee_record['name']:<20}",
        f"{dateDis:<40}",
        f"{employee_record['total hours']:>12.2f}",
        f"{employee_record['wage']:>12.2f}",
        f"{employee_record['tax rate']:>12.2f}",
        f"{employee_record['gross pay']:>12.2f}",
        f"{employee_record['total taxes']:>15.2f}",
        f"{employee_record['net pay']:>12.2f}"
    ]

    print(" ".join(row))
    
#Creating file if needed and writing database entries to it
def write_to_file(employee_record):
    sDate, eDate = employee_record['dates']
    startDate = sDate.strftime("%m/%d/%Y")
    endDate = eDate.strftime("%m/%d/%Y")
    fDisplay = f"{startDate}"
    tDisplay = f"{endDate}"

    with open("employees.txt", "a") as file: 
        file.write(
        f"{fDisplay}|{tDisplay}|{employee_record['name']}|{employee_record['total hours']:.2f}|"
        f"{ employee_record['wage']:.2f}|{employee_record['tax rate']:.2f}|{employee_record['gross pay']:.2f}|"
            f"{employee_record['total taxes']:.2f}|{employee_record['net pay']:.2f}\n"
        )

#Updating new totals
def update_totals(total_counts, totalHours, grossPay, totalTax, netPay):
    total_counts["empCount"] += 1
    total_counts["hours"] += totalHours
    total_counts["gross"] += grossPay
    total_counts["taxes"] += totalTax
    total_counts["net"] += netPay
    
#Adding totals that already exist in the file
def update_existing_totals(total_counts):
    try:
        with open("employees.txt", "r") as file:
            for line in file:
                parts = line.strip().split("|")
                if len(parts) != 9:
                    continue
            
                empCount = (parts[2]) 
                hours = float(parts[4])
                gross = float(parts[6])
                taxes = float(parts[7])
                net = float(parts[8])

                total_counts["empCount"] += 1
                total_counts["hours"] += hours
                total_counts["gross"] += gross
                total_counts["taxes"] += taxes
                total_counts["net"] += net
    
    except FileNotFoundError:
        pass


# ---------------------------
# REPORT FUNCTION
# ---------------------------

#Allows for searching by date or all and prints report
def search_report(user, role):
    if not data_check("employees.txt"):
        print("\nNo payroll records exist yet.")
        back_to_menu()
        return
    
    while True:
        total_hours = 0
        total_gross = 0
        total_taxes = 0
        total_net = 0

        while True:
            filterDate = input(
                "\nEnter a start date (MM/DD/YYYY) for the report or type 'All': "
            ).strip()

            if filterDate.lower() == "all":
                filterDate = "all"
                break
        
            try:
                filterDate = datetime.strptime(filterDate, "%m/%d/%Y").date()
                break

            except ValueError:
                print("\nInvalid format. Please use MM/DD/YYYY (e.g. 03/09/2036, 3/9/2026.")               
    
    
        found = False

        try:
            with open("employees.txt", "r") as file:

                width = display_report_header(user, role)      
                
                for line in file:
                    parts = line.strip().split("|")

                    if len(parts) != 9:
                        continue

                    emSDate = datetime.strptime(parts[0], "%m/%d/%Y").date()
                
                    if filterDate != "all" and emSDate != filterDate:
                        continue 

                    print(employee_row_format(parts))

                    hours = float(parts[3])
                    wage = float(parts[4])
                    taxRate = float(parts[5]) 
                    gross = float(parts[6])
                    taxes = float(parts[7])
                    net = float(parts[8])

                   

                    total_hours += hours
                    total_gross += gross
                    total_taxes += taxes
                    total_net += net
            
                    found = True
                
                   
        except FileNotFoundError:
            print("\nNo payroll records exist yet.")
            return

        if found:
            print(display_report_totals_row(
                total_hours, 
                total_gross, 
                total_taxes, 
                total_net,
                width
            ))

        else:
            print("\nNo records found.")

        while True:
            again = input(
                "\nWould you like to run another report? (Enter 'Y' or 'N'): "
            ).strip().lower()
        
            if again == 'y':
                break
            elif again == 'n':
                back_to_menu()
                return
            else: 
                print("\nInvalid entry. Please enter 'Y' or 'N'. ")
                

# ------------------------------
# MENU FUNCTIONS
# ------------------------------

#Adds admin menu for admin privileges
def admin_menu(user, role, total_counts):
    while True:

        print()
        print("-" * 26)
        print("ADMIN MENU:")
        print("-" * 26)
        print("1. Add Employee Payroll")
        print("2. Search Payroll Report")
        print("3. Create User")
        print("4. Display Users")
        print("5. Display Employee Totals")
        print("6. Logout")
        print("7. Exit")

        adminSelection = menu_choice("\nSelect an option by number: ", 
                                     ("1", "2", "3", "4", "5", "6", "7"))

        if adminSelection == '1':
            add_employee_payroll(user, role, total_counts)
    
        elif adminSelection == '2':
            search_report(user, role)
    
        elif adminSelection == '3':
            create_user()
    
        elif adminSelection == '4': 
            display_users(user, role)
    
        elif adminSelection == '5':
            totals_table(user, role, total_counts, "\nEMPLOYEE TOTALS:")
            back_to_menu()

        elif adminSelection == '6':
            print("\nLogging out...")
            return "logout"

        elif adminSelection == '7':
            print("\nGoodbye!\n")
            return "exit"
            
        else:
            print("\nInvalid selection. Please enter a number from 1-7. ")

#adds menu for user only privileges    
def user_menu(user, role, total_counts):
    while True:

        print()
        print("-" * 26)
        print("USER MENU:")
        print("-" * 26)
        print("1. Search Payroll Report")
        print("2. Display Users")
        print("3. Display Employee Totals")
        print("4. Logout")
        print("5. Exit")


        userSelection = menu_choice("\nSelect an option by number: ", 
                                     ("1", "2", "3", "4", "5"))
        
        if userSelection == '1':
            search_report(user, role)

        elif userSelection == '2':
            display_users(user, role)
        
        elif userSelection == '3':
            totals_table(user, role, total_counts, "\nEMPLOYEE TOTALS:")
            back_to_menu()

        elif userSelection == '4':
            print("\nLogging out...")
            return "logout"
        
        elif userSelection == '5':
            print("\nGoodbye!\n")
            return "exit"
            
        else:
            print("Invalid entry. Please choose a number between 1-5. ")
        
       


# ---------------------------
# PAYROLL PROCESSING FUNCTION
# ---------------------------

#Adds and processes entered employee payroll info
def add_employee_payroll(user, role, total_counts):
    all_employees = []


    while True:
        
        result = get_name()
        
        if result is None:
            break

        dates_list = []
        totalHours = 0.0

        while True:
            dateWorked, hoursWorked = get_hours()
            
            dates_list.append(dateWorked)
            totalHours += hoursWorked
        
            while True:
                stayQuit = input("\nWould you like to add another date? (Enter 'Y' or 'N'): "
                ).strip().lower()

                if stayQuit in ('y', 'n'):
                    break

                print("\nInvalid entry. Please enter 'Y' or 'N'")

            if stayQuit == 'n':
                break
                
                
        dRanges = getDateRngs(dates_list)
        

        employee_record = {
            'name': result,
            'dates': dRanges,
            'total hours': totalHours,
            'wage': get_rate(),
            'tax rate': get_tax()
        }
        
        grossPay, totalTax, netPay = calc_pay(
            employee_record['total hours'], 
            employee_record['wage'],
            employee_record['tax rate']
        ) 

        employee_record['gross pay'] = grossPay 
        employee_record['total taxes'] = totalTax
        employee_record['net pay'] = netPay

        all_employees.append(employee_record)

        

        display_info(employee_record, user, role)
        
        
        update_totals(total_counts, totalHours, grossPay, totalTax, netPay)
        
        write_to_file(employee_record)
        
        print()
        totals_table(user, role, total_counts, "\nRUNNING TOTALS:")

        while True:
            addResponse = input("\nWould you to enter another employee? (Enter 'Y' or 'N'): "
            ).strip().lower()  
            
            if addResponse in ('y', 'n'):
                break
            else:
                print("\nInvalid entry. Please enter 'Y' or 'N'. ")
        
        if addResponse == 'n':
            break
    
    totals_table(user, role, total_counts, "\nFINAL TOTALS:")

    back_to_menu()


# ------------------------------
# MAIN FUNCTION
# ------------------------------

#Executes main program
def main():
    start_heading()

    users_list = load_users()

    if not users_list:
        print("\nNo users exist. Please create first admin account.")
        create_user()
    
    while True:

        user, role = user_login() 
    

        if user is None:
            return

        total_counts = {
            "empCount": 0,
            "hours": 0.0,
            "gross": 0.0,
            "taxes": 0.0,
            "net": 0.0
        }
    
    
    
        update_existing_totals(total_counts)

        if role == "Admin":
            result = admin_menu(user, role, total_counts)
    
        elif role == "User":
            result = user_menu(user, role, total_counts)

        if result == "exit":
            break

if __name__ == "__main__":
    main()

       
                             

