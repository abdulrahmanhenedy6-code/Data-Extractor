import re
import time 
import os


MONTH_DAYS= {
    1: 31,
    2: 28,
    3: 31,
    4: 30,
    5: 31,
    6: 30,
    7: 31,
    8: 31,
    9: 30,
    10: 31,
    11: 30,
    12: 31
}

patterns_and_kinds = [(r"[\w.\+-]+@[A-Za-z0-9-]+\.[a-z]{2,}", "email"),(r"[A-Za-z0-9]+\.[a-z]{2,}", "domain" ),
(r"01[0125]\d{8}", "phone number"),
(r"(?:\d+\.){3}\d+", "ip"),
( r"http[s]?://\S+\.[a-z]{2,}","website"),
( r"(?:\d+[/-]){2}\d+" ,"date"),
(r"\d{13,19}|(?:\d{4}[ -]){3}\d{4}", "credit_card" ),
(r"[A-Za-z ]+", "name"),
(r"[\w ]+",  "error" ),
(r"[\w ]+" ,  "product" )
]
patterns_of_extractor= [
(r"Email: ([\w\+]+(?:[-.][\w\+]+)*@[A-Za-z0-9]+(?:[.-][A-Za-z0-9]+)*\.[a-z]{2,})"  , "email"),
(r"@([A-Za-z0-9]+(?:[-.][A-Za-z0-9]+)*)\.[a-z]{2,}" ,"domain"),
(r"01[0125]\d{8}"  ,"phone"),
(r"(?:\d+\.){3}\d+" ,"ip"),
(r"https?://\S+\.[a-z]{2,}" ,"website"),
(r"(?:\d+-){2}\d+|(?:\d+/){2}\d+" , "date"),
(r"\d{13,19}|(?:\d{4}[ -]){3}\d{4}" , "credit card"),
(r"Name: ([A-Za-z ]+)" , "name"),
(r"Error: .+$" , 'error') ,
(r"Product: [\w ]+\n\w+:[\w \$£€.]+$" , "product")       
  ]



def clear():
    '''This function clears the screen
    '''
    os.system("cls" if os.name == "nt" else "clear")

def show_menu(action):
    '''This function shows choices for a specific action.
    '''
    result = input(
    f"====={action} Data===== \n"
    f"1.{action} Emails \n"
    f"2.{action} Domains \n"
    f"3.{action} Phone Numbers \n"
    f"4.{action} IP Addresses \n"
    f"5.{action} Websites \n"
    f"6.{action} Dates \n"
    f"7.{action} Credit Cards \n"
    f"8.{action} Employee name\n"
    f"9.{action} Error Logs \n"
    f"10.{action} Products And Prices \n"
    f"11.Return To Main Menu \n"
    "Enter Your Choice (number): \n"
).lower()
    clear()
    return result


def main_menu():
    result = input("===========Data Management========= \n 1.Show Data \n 2.Add Data \n 3.Search Data \n 4.Edit Data \n 5.Exit \n Enter Your Choice (number):\n").lower()
    clear()
    return result

def check_ip(text):
    '''This function  verifies that ip is correct'''
   
    for  i in text:
        on_ip = True
        ip = i.split(".")
        ip = [int(i) for i in ip]
        for n in ip:
            if n > 255:
                on_ip = False
        if on_ip:
            print("_" * 6)
            print(i)


def print_valid_date(i , date):
    '''this F Checks whether a date is valid then prints it'''
    date = [int(i) for i in date]
    if 0 < date[1] < 13:
        month_days = MONTH_DAYS[date[1]]
        if date[1]  == 2 and( (date[2] % 4 == 0 and date[2]% 100 != 0) or date[2] % 400 == 0 ):
            month_days = 29
        if date[0] <= month_days and 1<= date[2] :
            print("_" * 10)
            print(i)
    
def check_date(text):
    '''Validate all extracted dates'''
    for  i in text:
        if "-" in i:
            date = i.split("-")
            print_valid_date(i , date)
        if "/" in i:
            date = i.split("/")
            print_valid_date(i , date)

#الدالة دي بعملها بعد ما اخلص كل مهمة اشوفه عايز يوقف البرنامج ولا يكمل
def exit_or_menu():
    '''This function asks you want continue or not on program'''
    global running
    on = True
    while on:
        
          exit_question = input(
          "______________\n"
          "1.Main Menu \n"
          "2.Exit \n"
          "Enter Your Choice :\n ").lower()
          if exit_question == "1" or "main" in exit_question :
              clear()
              on = False
          elif exit_question == "2" or "exit" in exit_question:
              on = False
              running = False
              clear()
          else:
              print("Invalid choice. Please try again.😒")



def extractor(pattern , kind):
    '''This function extract a pattern from data.txt then prints it'''
    with open("data.txt" , "r") as my_file :
        text = my_file.read()
        text = re.findall(pattern , text , re.MULTILINE)           
        if kind == "ip":
            check_ip(text)
        elif kind == "date":
            check_date(text)
        else:
            for i in text:
                print("_" * 10)
                print(i)
    exit_or_menu()



def open_file(message, kind  ):
    '''Open data.txt in append mode and write data ''' 
    with open("data.txt" , "a") as text:
        text.write(message)
        print(f"{kind} Was Added successfully")




def adder(pattern , kind):
    '''This function adds data to data.txt''' 
    on = True
    while on:
        new_text = input(f"Enter The New {kind} correctly:\n ")
        if re.fullmatch(pattern , new_text):
            on = False
            if kind == "email" or kind == "error" or kind == "product" or kind == "name" :
                open_file(f"\n{kind.capitalize()}: {new_text}" , kind)
            else:
                open_file(f"\n{new_text}" , kind)
            exit_or_menu()
        else:
            clear()
            print("Invalid Entry , Try Again")
            time.sleep(3)
            clear()
            
def editor(pattern , kind):
    '''This function edit data at data.txt '''
    on = True
    while on :
        with open("data.txt" , "r") as text:
            text = text.read()
        avalible_text = input(f"Enetr the {kind} you want edit it :\n")
        
        if avalible_text in text:
            new_text = input(f"Enter the new {kind} : \n")
            if re.fullmatch(pattern , new_text , re.MULTILINE):
                with open("data.txt" , "w") as my_file:
                    my_file.write(text.replace(avalible_text , new_text))
                print("The text was successfuly edited")
                on = False
                exit_or_menu() 
            else:
                print(f"({new_text}) is invalid")
                time.sleep(2)
                clear()
        else:
            print(f"({avalible_text}) is not found")
            time.sleep(2)
            clear()
               






def invalid_choice():
    '''This function tells user when he write a wrong thing'''
    print("Invalid choice.We Will Return You T Man Menu!😒")
    time.sleep(3)
    clear()


def handle_sub_choice(sub_choice , func):
    '''This F reviews the if conditions cases of sub_choice'''
    try :
        num = int(sub_choice)
        if 1 <= num<= 10:
            func(*patterns_and_kinds[num- 1])
    
        elif num == 11:
            clear()
        else:
            invalid_choice()
    except ValueError:
        invalid_choice()
        


running = True 
while running:
    #هنا بأعرض الاختيارات الاساسية
    choice = main_menu()
    #هنا بداية الاختيارات  التخصصية للعملية
    if choice == "1" or choice.startswith("show"):
        sub_choice = show_menu("Show")
        try:
            choice_num = int(sub_choice)
            if 1 <= choice_num <= 10:
                extractor(*patterns_of_extractor[choice_num -1])
            else:
                invalid_choice()
        except ValueError:
            invalid_choice()    
    elif choice == "2" or choice.startswith("add"):
        sub_choice =show_menu("Add")
        handle_sub_choice(sub_choice , adder)
    elif choice == "3" or choice.startswith("search"):
        turn_on = True
        while turn_on:
            search_text = input("Enter the text You Want To Search for: \n")
            with open("data.txt" ,"r") as text:
                text = text.read()
                if search_text in text:
                    print(f" ({search_text}) is found!")
                else:
                    print(f"({search_text}) is not found!")
                again = input("1.Again \n2.I finished :\n")
                if again == "1":
                    clear()
                else:
                    turn_on = False
                    clear()
                    exit_or_menu()
    
    elif choice == "4" or choice.startswith("edit"):
        sub_choice = show_menu("Edit")
        handle_sub_choice(sub_choice , editor)
    
    
    elif choice == "5" or choice.startswith("exit"):
        running = False
    
    
    else:
        print("Invalid choice. Please try again.😒")
        time.sleep(3)
        clear()
    #هنا نهاية الاختيارات  التخصصية للعملية















