"""
Cormac O'Neill
B00758943
COM101 Programming Task
Term 1
"""

#   This program will allow the user to:
#   1. Read total amount of records in table
#   2. Read entirety of file
#   3. Report total salary bill
#   4. Report average salary of employees
#   5. Add record to table
#   6. Report on number of employees grouped by role
#   7. Report on number of employees above a given salary
#   8. Delete a record from the text file
#   9. Exit program

#   FUNCTIONS

#   We'll define these functions in the order that they appear in the requirements above


def mainMenu():  # Main menu where user can select from all available options
    useroption = 0
    valid = False
    while not valid:
        try:
            useroption = int(input("---MAIN MENU---\n" +
                                   "1. Total records in table\n" +
                                   "2. Display contents of table\n" +
                                   "3. Total salary bill\n" +
                                   "4. Average salary\n" +
                                   "5. Add employee\n" +
                                   "6. Employees by role\n" +
                                   "7. Employees above given salary\n" +
                                   "8. Delete employee\n" +
                                   "9. Exit\n" +
                                   ">>> "))
            valid = True
        except ValueError or TypeError:
            print("Invalid option, please try again")
            valid = False
    if useroption == 1:
        print("Total records in table: " + str(totalRecords()))
    elif useroption == 2:
        print(readFile())
    elif useroption == 3:
        print("Total salary of all employees: £" + str(totalSalary()))
    elif useroption == 4:
        print("Average salary of all employees: £" + str(round(averageSalary(), 2)))
    elif useroption == 5:
        with open("EMP.txt", "a+") as emp:
            emp.write(addEmployee())
            emp.close()
    elif useroption == 6:
        for role, quant in (empByRole()).items():
            print(role, ":", quant)
    elif useroption == 7:
        print(aboveSalary())
    elif useroption == 8:
        emp_no = deleteRow()
        with open("EMP.txt", "r") as oldfile:  # save contents of text file
            olddata = oldfile.readlines()
            oldfile.close()
        with open("EMP.txt", "w") as newfile:  # compare old data and user input, leave behind similar data
            for line in olddata:
                if line[0:3] != emp_no:
                    newfile.write(line)
            newfile.close()  # block from line 62 to here will leave whitespace in file

        # block below clears file of any whitespace (although seems to leave a trailing newline, just pretend it's for POSIX compliance ;))
        with open("EMP.txt", "r") as oldfile:
            oldlines = oldfile.readlines()
            oldfile.close()
        with open("EMP.txt", "w") as newfile:
            for line in oldlines:
                if not isLineEmpty(line):
                    newfile.write(line)
            newfile.close()
    else:
        quit()
    return None


def totalRecords():  # Returns total number of lines minus one (to account for the first line being inaccessible)
    with open("EMP.txt", "r") as emp:
        for lines, l in enumerate(emp):
            pass
        return lines


def readFile():  # Returns contents of table
    with open("EMP.txt") as emp:
        return emp.read()


def totalSalary():  # Returns total salary of all employees
    total = 0
    with open("EMP.txt") as emp:
        for line in emp.readlines()[1:]:
            linearray = line.split(", ")
            salary = linearray[4]
            total = total + int(salary)
        emp.close()
    return total


def averageSalary():  # Returns average salary of all employees
    average = (totalSalary() / totalRecords())
    return average


def addEmployee():  # Returns correctly formatted record to add to table
    emp_no = "000"
    emp_name = "None"
    age = 0
    pos = "None"
    salary = 0
    yrs_emp = 0

    #   Retrieve and validate (very inefficiently) EMP_NO
    #   Could automate this, but I'm letting the user enter this in case they need to add an employee with a specific
    #   number. The following validation techniques could be optimised greatly.
    valid = False
    exists = True
    ids = []
    while not valid:
        while exists:
            try:
                emp_no = int(input("Employee number: "))
                if len(str(emp_no)) < 3:  # Make sure input is formatted correctly
                    emp_no = ("0" * (3 - len(str(emp_no)))) + str(emp_no)
                if emp_no.isdecimal():  # Make sure input is numerical
                    with open("EMP.txt") as emp:
                        for line in emp.readlines()[1:]:
                            ids.append(line.split(", ")[0])  # Create a list of all emp_no's to make enumerating easier
                else:
                    print("Invalid employee number")
                if emp_no in ids:
                    print("Employee number already exists")
                else:
                    exists = False
            except:
                print("Invalid employee number")
            else:
                valid = True

    #   Retrieve and validate EMP_NAME
    valid = False
    while not valid:
        try:
            emp_name = str(input("Employee name: "))
            valid = True
        except:
            print("Invalid employee name")
    #   Retrieve and validate AGE
    valid = False
    while not valid:
        try:
            age = int(input("Age: "))
            if 0 <= age <= 125:  # This number may seem high, but the longest living person ever lived to 122
                valid = True
        except:
            print("Invalid age")
    #   Retrieve and validate POSITION
    valid = False
    while not valid:
        try:
            pos = str(input("Position: "))
            if pos in ["Analyst", "Developer", "DevOps", "Tester"]:
                valid = True
            else:
                print("Invalid position")
        except:
            print("Invalid position")
    #   Retrieve and validate SALARY
    valid = False
    while not valid:
        try:
            salary = int(input("Salary: "))
            valid = True
        except:
            print("Invalid salary")
    #   Retrieve and validate YRS_EMP
    valid = False
    while not valid:
        try:
            yrs_emp = int(input("Years employed: "))
            valid = True
        except:
            print("Invalid salary")
    #   Construct correctly formatted record to append to table
    newline = str("\n" +
                  emp_no + ", " +
                  emp_name + ", " +
                  str(age) + ", " +
                  pos + ", " +
                  str(salary) + ", " +
                  str(yrs_emp))
    return newline


def empByRole():  # Returns number of employees in each position
    #   Initialise some counters for use later
    analysts = 0
    developers = 0
    devops = 0
    testers = 0

    #   Calculate number of employees in each role
    with open("EMP.txt") as emp:
        for line in emp.readlines():
            linearray = line.split(", ")
            position = linearray[3]
            if position == "Analyst":
                analysts += 1
            elif position == "Developer":
                developers += 1
            elif position == "DevOps":
                devops += 1
            else:
                testers += 1

    #   Compile values found above into a dictionary
    role_quantities = {"Analysts": analysts,
                       "Developers": developers,
                       "DevOps": devops,
                       "Testers": testers}
    return role_quantities


def aboveSalary():  # Returns list of employees that earn above a given salary
    valid = False
    highearners = []
    threshold = 0
    while not valid:
        try:
            threshold = int(input("Enter salary threshold: "))
            valid = True
        except:
            print("Invalid threshold, please try again")
            valid = False
    with open("EMP.txt") as emp:
        for line in emp.readlines()[1:]:
            linearray = line.split(", ")
            salary = linearray[4]
            if int(salary) > int(threshold):
                highearners.append(linearray[0])
    return highearners


def deleteRow():  # Returns a validated emp_no to be deleted from table
    valid = False
    emp_no = ""
    while not valid:
        try:
            emp_no = str(input("Enter employee number to remove (3 DIGITS): "))
            if len(emp_no) < 3:
                emp_no = ("0" * (3 - len(emp_no))) + emp_no
            if emp_no.isdecimal():
                valid = True
        except ValueError or TypeError:
            print("Invalid employee number")
    return emp_no


def isLineEmpty(line):  # Returns True if given line is functionally blank
    return len(line.strip()) < 1


if __name__ == "__main__":
    while True:
        mainMenu()
