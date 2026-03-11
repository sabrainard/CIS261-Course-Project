#Stephanie Brainard
#CIS261 Course Project
#Phase 2
#Week 5


from datetime import datetime, timedelta


def start_heading():
    print("_" * 40)
    print()
    print("Employee Payroll Automation Program POC")
    print("_" * 40)
    print()

#Getting employee name
def get_name ():
    employee = str(input("Enter the employee's name (or enter 'End' to quit): ")).strip()
    return employee

#getting dates and times
def get_hours(dates_list): 
    while True:
        date_wrkd_input = input("Enter the date (MM/DD/YYYY) employee worked: ")
        try:
            date_worked = datetime.strptime(date_wrkd_input, "%m/%d/%Y").date()
            break
        except ValueError:
                print("You entered an invalid format. Please use MM/DD/YYYY format.")
            
    while True:
        start_time_input = input("Enter the start time (HH:MM 24hr): ")
        try:
            start_time = datetime.strptime(f"{start_time_input}", "%H:%M")
            break
        except ValueError:
            print("You entered an invalid format. Please enter HH:MM using 24hr clock format.")

    while True:        
        end_time_input = input("Enter the end time (HH:MM 24hr): ")
        try:
            end_time = datetime.strptime(f"{end_time_input}", "%H:%M")
            break               
        except ValueError:                   
            print("You entered an invalid format. Please enter HH:MM using 24hr clock format.")
       
    if end_time < start_time:
        end_time += timedelta(days=1)
        
    hours_worked =  (end_time - start_time).total_seconds() / 3600
    stay_quit = input("Would you like to add another date (enter 'Y' or 'N'): ")
    return date_worked, hours_worked, stay_quit

#getting date ranges
def get_date_rngs(dates_list):
    if not dates_list:
        return 
    return min(dates_list), max(dates_list)
    
#Get hourly wage        
def get_rate ():
    while True:
        try:
            pay_rate = float(input("Enter the employee hourly wage: "))
            if pay_rate >= 0:
                return pay_rate
            else:
                print("Hourly wage cannot be negative. Please try again.")
        except ValueError:
            print("Please enter a valid positive number. ")

#Get income tax rate
def get_tax ():
    while True:
        try:
            tax_rate = float(input("Enter income tax rate: "))
            if 0 <= tax_rate < 1:
                return tax_rate   
            else:
                print("Income tax rate cannot be an interger. Please enter in decimal form (e.g. .10 for 10%). ")
        except ValueError:
            print("Please enter a decimal. ")          
        
#Calculator
def calc_pay (pay_rate, hours_worked, tax_rate): 
    gross_pay = pay_rate * hours_worked
    total_tax = gross_pay * tax_rate
    net_pay = gross_pay - total_tax
    return gross_pay, total_tax, net_pay

#Display individual employee info and totals from dictionary/list
def display_info(employee_record):
    print("_" * 40)
    print("Employee Information: ")
    print("_" * 40)

    s_date, e_date = employee_record['dates']
    start = s_date.strftime("%b %d,%Y")
    end = e_date.strftime("%b %d,%Y")

    if s_date == e_date:
        date_dis = start
    else:
        date_dis = f"{start} - {end}"
    print(f"Employee Name:          {employee_record['name']}")
    print(f"Dates worked:           {date_dis}")
    print(f"Total hours worked:     {employee_record['total hours']:.2f} ")
    print(f"Hourly rate:            ${employee_record['wage']:.2f} ")
    print(f"Income tax rate:        {employee_record['tax rate']:.2f} ")
    print(f"Gross pay:              ${employee_record['gross pay']:.2f} ") 
    print(f"Income taxes deducted:  ${employee_record['total taxes']:.2f} ")
    print(f"Net pay:                ${employee_record['net pay']:.2f} ")

#Math for totals and display, add keys and values
def all_totals(all_employees):
    total_employee_count= (len(all_employees))
    total_hours_worked_count = 0.0
    total_gross_count = 0.0
    total_tax_count = 0.0
    total_net_count = 0.0
  
    for totals in all_employees:
        total_hours_worked_count += totals['total hours']
        total_gross_count += totals['gross pay']
        total_tax_count += totals['total taxes']
        total_net_count += totals['net pay']
       
    print("_" * 40)
    print("Totals For All Employees: ")
    print("_" * 40)
    print(f"Employee Count:        {total_employee_count}")
    print(f"Total Hours worked:    {total_hours_worked_count}")
    print(f"Total Gross Pay:       ${total_gross_count:.2f}")
    print(f"Total Taxes:           ${total_tax_count:.2f}")
    print(f"Total Net Pay:         ${total_net_count:.2f}")
    return total_employee_count, total_employee_count, total_hours_worked_count, total_gross_count, total_tax_count, total_net_count                                                                                                              
    
#Executes main loop, calls all functions, and adds keys:values to the dictionary
def main():
    all_employees = []
    
    start_heading()
    
    while True:
        e_name = get_name()

        if e_name.lower().strip() == 'end':
            print("Goodbye!")
            break
        
        dates_list = []
        total_hours = 0.0
        while True:
            date_worked, hours_worked, stay_quit = get_hours(dates_list)
            total_hours += hours_worked
            dates_list.append(date_worked)

            if stay_quit.lower().strip() != 'y':
                break 
            
        d_ranges = get_date_rngs(dates_list)
        
        
        employee_record = {}
        employee_record['name'] = e_name
        employee_record['dates'] = d_ranges
        employee_record['total hours'] = total_hours
        employee_record['wage'] = get_rate()
        employee_record['tax rate'] = get_tax()
       
        
        gross_pay, total_tax, net_pay = calc_pay(
            employee_record['total hours'], 
            employee_record['wage'],
            employee_record['tax rate']
        ) 

        employee_record['gross pay'] = gross_pay 
        employee_record['total taxes'] = total_tax
        employee_record['net pay'] = net_pay
        
    
        all_employees.append(employee_record)

     

        display_info(employee_record)
        all_totals(all_employees)


      



if __name__ == "__main__":
    main ()

       
                             

