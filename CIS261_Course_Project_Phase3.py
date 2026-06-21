from datetime import datetime, timedelta


#Displays the name of the program
def start_heading():
    print("\nEMPLOYEE PAYROLL AUTOMATION POC")
    print()


#Getting employee name
def get_name():
    employeeFName = input("\nEnter the employee's first name (or 'End' to quit): ").capitalize().strip()
    
    
    if employeeFName .lower() == "end":
        return None
    
    employeeFName = employeeFName.capitalize()
    employeeLName = input("\nEnter the employee's last name: ").capitalize().strip()
    
    employeeName = f"{employeeFName} {employeeLName}" 
    
    return f"{employeeFName.capitalize()} {employeeLName.capitalize()}"

#getting dates and times
def get_hours(dates_list): 
    while True:
        dateWrkdInput = input("\nEnter the date (MM/DD/YYYY) employee worked: ")
        try:
            dateWorked = datetime.strptime(dateWrkdInput, "%m/%d/%Y").date()
            break
        except ValueError:
                print("\nYou entered an invalid format. Please use MM/DD/YYYY format.")
            
    while True:
        startTimeInput = input("\nEnter the start time (HH:MM 24hr): ")
        try:
            startTime = datetime.strptime(f"{startTimeInput}", "%H:%M")
            break
        except ValueError:
            print("\nYou entered an invalid format. Please enter HH:MM using 24hr clock format.")

    while True:        
        endTimeInput = input("\nEnter the end time (HH:MM 24hr): ")
        try:
            endTime = datetime.strptime(f"{endTimeInput}", "%H:%M")
            break               
        except ValueError:                   
            print("\nYou entered an invalid format. Please enter HH:MM using 24hr clock format.")
       
    if endTime < startTime:
        endTime += timedelta(days=1)
        
    hoursWorked =  (endTime - startTime).total_seconds() / 3600
    stayQuit = input("\nWould you like to add another date? (Enter 'Y' or 'N') ")
    return dateWorked, hoursWorked, stayQuit

#getting date ranges
def getDateRngs(dates_list):
    if not dates_list:
        return 
    return min(dates_list), max(dates_list)
    
#Get hourly wage        
def get_rate ():
    while True:
        try:
            payRate = float(input("\nEnter the employee hourly wage: "))
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
            taxRate = float(input("\nEnter income tax rate: "))
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
 
def display_info(employee_record):
    print()
    print("\n------EMPLOYEE INFORMATION------")
    
    sDate, eDate = employee_record['dates']
    start = sDate.strftime("%b %d,%Y")
    end = eDate.strftime("%b %d,%Y")

    if sDate == eDate:
        dateDis = start
    else:
        dateDis = f"{start} - {end}"
    print(f"Employee Name:          {employee_record['name']}")
    print(f"Dates worked:           {dateDis}")
    print(f"Total hours worked:     {employee_record['total hours']:.2f} ")
    print(f"Hourly rate:            ${employee_record['wage']:.2f} ")
    print(f"Income tax rate:        {employee_record['tax rate']:.2f} ")
    print(f"Gross pay:              ${employee_record['gross pay']:.2f} ") 
    print(f"Income taxes deducted:  ${employee_record['total taxes']:.2f} ")
    print(f"Net pay:                ${employee_record['net pay']:.2f} ")
    
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

#Displaying totals counts for all employees
def print_totals(total_counts):    
    print(f"Total Employee Count:   {total_counts['empCount']}")
    print(f"Total Hours Worked:     {total_counts['hours']:.2f}")
    print(f"Total Gross Pay:        ${total_counts['gross']:.2f}")
    print(f"Total Taxes Paid:       ${total_counts['taxes']:.2f}")
    print(f"Total Net Pay:          ${total_counts['net']:.2f}")               

#Allows for searching by date or all and prints report
def search_report():
    while True:
        filterDate = input(
        "\nEnter a start date (MM/DD/YYYY) for the report (or type 'All' for to display all records): "
        ).strip()

        if filterDate.lower() == "all":
            filterDate = "all"
            break
        
        try:
            filterDate = datetime.strptime(filterDate, "%m/%d/%Y")
            break
        except ValueError:
            print("\nInvalid format. Please use MM/DD/YYYY.")
                
    print("\n------EMPLOYEE REPORT------ ")
    
    found = False

    with open("employees.txt", "r") as file:
        for line in file:
            parts = line.strip().split("|")

            if len(parts) != 9:
                continue

            emSDate = datetime.strptime(parts[0], "%m/%d/%Y")
            emEDate = datetime.strptime(parts[1], "%m/%d/%Y")
            
            if filterDate != "all" and emSDate != filterDate:
                continue 

            hours = float(parts[3])
            wage = float(parts[4])
            taxRate = float(parts[5]) 
            gross = float(parts[6])
            taxes = float(parts[7])
            net = float(parts[8])
            
            found = True

            print(f"Name:       {parts[2]}")
            print(f"Start:      {parts[0]}  End: {parts[1]}")
            print(f"Hours:      {hours:.2f}")  
            print(f"Wage:       ${wage:.2f}")
            print(f"Tax Rate:   {taxRate:.2f}")
            print(f"Gross:      ${gross:.2f}")  
            print(f"Taxes:      ${taxes:.2f}") 
            print(f"Net:        ${net:.2f}")
            print()

    if not found:
        print("\nNo records found.")

#Executes main loop, calls all functions, and adds keys:values to the dictionary
def main():
    all_employees = []
    dates_list = []

    start_heading()

    total_counts = {
        "empCount": 0,
        "hours": 0.0,
        "gross": 0.0,
        "taxes": 0.0,
        "net": 0.0
    }

    update_existing_totals(total_counts)

    while True:
        result = get_name()
        
        if result is None:
            print("\n------EMPLOYEE TOTALS------")
            print_totals(total_counts)
            print("\nGoodbye!")
            break
        

        totalHours = 0.0
        dates_list = []

        while True:
            dateWorked, hoursWorked, stayQuit = get_hours(dates_list)
            totalHours += hoursWorked
            dates_list.append(dateWorked)

            if stayQuit.lower().strip() != 'y':
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

        display_info(employee_record)
        
        
        update_totals(total_counts, totalHours, grossPay, totalTax, netPay)
        
        write_to_file(employee_record)
        
        print("\n------RUNNING TOTALS------")
        print_totals(total_counts)

        while True:
            addResponse = input("\nWould you to enter another employee? (Enter 'Y' or 'N') ").strip().lower()  
            if addResponse in ('y', 'n'):
                break
            else:
                print("\nInvalid entry. Please enter 'Y' or 'N'. ")
        
        if addResponse == 'n':
            break
   
    print("\n------FINAL TOTALS------")
    print_totals(total_counts)

    while True:

        search_report()

        while True:
            again = (input("\nWould you like to run another report? (Enter 'Y' or 'N') ")).strip().lower()
        
            if again in ('y', 'n'):
                break
            else:
                print("\nInvalid entry. Please enter 'Y' or 'N'. ")

        if again == 'n':    
            print("\nGoodbye!")
            break

            
                    
if __name__ == "__main__":
    main ()

       
                             

