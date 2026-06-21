#Getting employee information
def employeeInput (min_val=0, max_val=float('inf')): 
    while True:
        try:
            global employeeFName
            global employeeLName
            global employeeName
            employeeFName = str(input("Enter the employee's first name: "))
            employeeLName = str(input("Enter the employee's last name: "))
            employeeName = (employeeFName.capitalize()) + " " + (employeeLName.capitalize())
            if employeeName.isdigit():
               raise ValueError
               break
            elif print(f"You entered: {employeeName}"):
               break 
        except ValueError:
            print("Invalid entry: Please enter an alphabetic character.")
            

    while True:  
        try:
            global payRate
            payRate = float(input(f"Enter {employeeName}'s rate of pay: "))
            payRate = "{: .2f}" .format(payRate)
            print(f"You entered: ${payRate}")
            break
        except ValueError:
            print("Invalid entry: Please enter a numeric value.")
       
    while True:
        try:
            global hoursWorked
            hoursWorked = float(input(f"Enter the hours worked by {employeeName}: "))
            print(f"You entered: {hoursWorked}")
            break
        except ValueError:
            print("Invalid entry: Please enter a numeric value.")
    
    while True:
        try:
            global taxRate
            global percentTaxRate
            taxRate = float(input(f"Enter {employeeName}'s the tax rate: "))
            if isinstance(taxRate, str):
                raise ValueError
                break
            elif taxRate > 100:
                    print("Invalid entry: Value must be between 0 and 100")
                    continue
            elif taxRate > 0.9:
                percentTaxRate = taxRate
                print(f"You entered: {taxRate:g}%")
                break
            elif taxRate <= 0.9:
               percentTaxRate = float(taxRate * 100)
               print(f"You entered: {percentTaxRate:g}%")
               break
        except ValueError:
            print("Invalid entry: Please enter a numeric value.")
        return employeeName, payRate, hoursWorked, taxRate
employeeInput()

#Pay calculator
def calcPay ():
    grossPay = float(hoursWorked) * float(payRate)
    print(f"{employeeName}'s gross pay is ${grossPay}")

    totalTax = float(grossPay) * (float(percentTaxRate) / 100)
    print(f"{employeeName}'s total tax rate is {totalTax}")

    netPay = grossPay - totalTax
    print(f"{employeeName}'s net pay is {netPay}")
    return grossPay, totalTax, netPay
calcPay()

#def displayEmployee():
#displayEmployee()

#def disTotals ()
#disTotals () 

#def main ()
#if__name__ == "__main__":
    #main ()



