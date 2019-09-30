
# AUTHOR  : MD RUMAN HOSSAIN
# Date: 2019-09-30 11:18AM
# File Name: ATM project
import sys
import os
import time
import re
from datetime import datetime
from decimal import Decimal

# Function to change the user file. Complete
def replaceAccountFile(account, file):
   os.remove(account + '.txt')
   userFile = open(account + '.txt', 'w')
   # Rewrite here
   for line in range(len(file)):
       userFile.write(str(file[line]) + '\n')
   userFile.close()
   return file

# Function to change the user file. Complete
def replaceFile(type,account, file):
   os.remove(type+account + '.txt')
   userFile = open(type+account + '.txt', 'w')
   # Rewrite here
   for line in range(len(file)):
       userFile.write(str(file[line]) + '\n')
   userFile.close()
   return file


# Recursion to make sure the pin numbers are the same
def equal(p):
   # If there is only one number left, we know all were equal
   if len(p) == 1:
       return True
   else:
       if p[0] == p[1]:
           # If they are equal, we have to check the next ones
           return equal(p[1:])
       else:
           return False

# Handles special cases such as 20 & 8 transactions
def is_special(type,account, file):
   myFile = open(type+account + 'history.txt')
   allTransactions = myFile.readlines()
   if len(allTransactions) % 8 == 0:
       now = datetime.now()
       current_time = "%s:%s %s / %s / %s" % (
       now.hour, now.minute, now.month, now.day, now.year)
       history_file = open(type+account + 'history.txt', 'a')
       history_file.write(current_time + '\n')
       history_file.write(str(-4.00) + '\n')
       if Decimal(file[4]) >= 4:
           balance = file[4]
           file.pop(4)
           file.insert(4, str(Decimal(balance) - Decimal(4)))  # at place 4 I insert the money - 4
       elif 0 < Decimal(file[4]) < 4:
           difference = 4 - Decimal(file[4])
           file.pop(4)
           file.pop(4)
           file.insert(4, str(0))
           file.insert(5, str(Decimal(file[5]) -difference))
           file = overdraftfunction(difference, file[2], current_time, file)
       else:
           to_be_used = file[5]
           file.pop(5)
           file.insert(5, Decimal(to_be_used) - 4)
   elif len(allTransactions) % 40 == 0:
       history_file = open(type+account + 'history.txt', 'r')
       myhistory = history_file.readlines()
       total = 0
       print("You Have Reached 20 Transactions. Here they are:")
       for a in range(len(myhistory)):
           if not a % 2 == 0:
               total += Decimal(myhistory[a].split('\n')[0])
           sys.stdout.write(myhistory[a])
       if total > 0:
           print("\nYour Net Income is: %s" % total)
       else:
           print("\nYour Net Lose is: %s" % total)

   pass

# Account details.
def view(type,file):
   os.system('cls')
   print(file)
   print("Account Details:")
   print("_______________________")
   print("Card Number: %s" % file[0])
   print("Account Type: %s"%type.upper())
   print("Balance: %s" % file[4])
   print("Overdraft: %s" % file[5])
   time.sleep(5)


# Printing transaction history
def print_transaction(type,account):
   os.system('cls')
   transactions = open(type+account + 'history.txt', 'r')
   allTransactions = transactions.readlines()
   transactions.close()
   if len(allTransactions) == 0:
       print("No transactions yet")
   else:
       print("Transactions:")
       for tran in range(len(allTransactions)):
           sys.stdout.write(allTransactions[tran])


# Replacing the pin
def pin(current, account, file):
   while True:
       pin = input("Enter The New Pin(Must Be 4 Digits): ")
       if not re.search(r'^\d{4}$', pin):
           continue
       if equal(pin):
           continue
       if pin == current:
           continue
       if pins_check(pin):
           break
       else:
           print("This Pin Already Exists. Try Another !!!")
   file.pop(1)
   file.insert(1, str(pin))
   sys.stdout.write("Changing pin")
   name = "....\n"
   for char in name:
       sys.stdout.write(char)
       sys.stdout.flush()
       time.sleep(.5)
   return replaceAccountFile(account, file)


def withdraw(type,money, overdraft, file, account, gone_overdraft):
   os.system('cls')
   if overdraft == 'True':
       gone_overdraft = Decimal(gone_overdraft)
   allOptions = {'1': 20, '2': 40, '3': 60, '4': 80, '5': 100, '6': 120, '7': 'other'}
   while True:
       print("Your Current %s Account Balance : %s\n"%(type,file[4]))
       option = input("Pick a withdraw option: 1) $20 2) $40 3) $60 4) $80 5) $100 6) $120 7) Other: ")
       if option not in allOptions.keys():
           os.system('cls')
           print("Wrong Choice. TRY AGAIN\n")
           continue
           
       break
   withdrawen = allOptions[option]
   if withdrawen == 'other':
       while True:
           withdrawen = input("Enter An Amount: ")
           try:
               if Decimal(withdrawen) > 0:
                   break
           except Exception:
               continue
   withdrawen = Decimal(withdrawen)
   if money > withdrawen or overdraft == 'True' and money + gone_overdraft > withdrawen:
       sys.stdout.write("Dispensing Money")
       name = ".....\n"
       for char in name:
           sys.stdout.write(char)
           sys.stdout.flush()
           time.sleep(2)
       if money > withdrawen:
           file.pop(4)
           file.insert(4, str(money - withdrawen))
       else:
           difference = withdrawen - money
           gone_overdraft -= difference
           now = datetime.now()
           current_time = "%s:%s %s / %s / %s" % (
           now.hour, now.minute, now.month, now.day, now.year)
           file =  overdraftfunction(gone_overdraft, file[2], current_time, file)
           money = 0
           file.pop(4)
           file.pop(4)
           file.insert(4, money)
           file.insert(5, gone_overdraft)

       # Rewrite file point
       now = datetime.now()
       current_time = "%s:%s %s / %s / %s" % (now.hour, now.minute, now.month, now.day, now.year)
       history_file = open(account + 'history.txt', 'a')
       history_file.write(current_time + '\n')
       history_file.write(str(-withdrawen) + '\n')
       history_file.close()
       is_special(type,account, file)
       return replaceAccountFile(account, file)
   else:
       print("Not Enough Money")
       return file


def deposit(type,file, userMoney, account):
   os.system('cls')
   allDeposits = []
   while True:
       while True:
           money = input("Enter Amount To Deposit(Q To Go Back): ".lower())
           try:
               if Decimal(money) < 0:
                   continue
               break
           except Exception:
               # Value error means a string was entered
               if money == "q":
                   break
               else:
                   continue

       if money != 'q':
           allDeposits.append(money)
           time.sleep(2)
           print("Deposit accepted")
       else:
           break
   #import pdb; pdb.set_trace()
   total = 0
   for i in range(len(allDeposits)):
       total += Decimal(allDeposits[i])
   if file[3] == 'True' and Decimal(file[5]) < 500:
       if total + Decimal(file[5]) <= 500:
           newOverDraft = Decimal(file[5]) + total
       else:
           subtract = total - Decimal(file[5])
           newOverDraft = 500
           another_varaible_to_store_total = total - subtract
           userMoney += another_varaible_to_store_total
   else:
       userMoney += total
       if file[3] == 'True':
           newOverDraft = 500
       else:
           newOverDraft = "Not In Action"
   file.pop(4)
   file.insert(4, str(userMoney))
   file.pop(5)
   file.insert(5, str(newOverDraft))
   now = datetime.now()
   current_time = "%s:%s %s / %s / %s\n" % (now.hour, now.minute, now.month, now.day, now.year)
   history_file = open(type+account + 'history.txt', 'a')
   history_file.write(current_time)
   history_file.write(str(total) + '\n')
   history_file.close()
   is_special(type,account, file)
   return replaceAccountFile(account, file)


# Function that will notify the user when they go beyond overdraft
def overdraftfunction(howfar, email, time, file):
   os.system('cls')
   import smtplib
   from email.mime.multipart import MIMEMultipart
   from email.mime.text import MIMEText

   # variables for to and from
   the_overdraft = str(Decimal(file[5]) - Decimal(howfar))
   charge = str(Decimal(the_overdraft) * Decimal(0.25))
   howfar -= Decimal(charge)
   myadd = "ruman.cse.brur@gmail.com"
   youradd = email

   msg = MIMEMultipart()
   msg['From'] = myadd
   msg['To'] = youradd
   msg['Subject'] = "ATM project"

   # body of text
   body = "Dir Sir/Madam, Your recent transaction at (%s) shows that you have gone into your overdraft.  " \
          "You overdraft protection is $%s.  " \
          "You have gone $%s into your overdraft, leaving you with a balance of $%s in your overdraft. " \
          "This is including a small service charge of $%s (25 percent of $%s) has been added to your account. Thank you." % \
          (time, file[5], the_overdraft, howfar, charge, the_overdraft)
   msg.attach(MIMEText(body, "plain"))

   server = smtplib.SMTP("smtp.gmail.com", 587)
   server.starttls()
   server.login(myadd, 'rumancse')
   text = msg.as_string()
   server.sendmail(myadd, youradd, text)
   server.quit()
   to_be_used = file[5]
   file.pop(5)
   file.insert(5, str(Decimal(to_be_used) - Decimal(charge)))
   return replaceFile(file[0], file)


# Function that lets the user pay bills
def bills(type,file, userMoney, account, overdraft, email, overdraftAmount):
   os.system('cls')
   if overdraft == 'True':
       overdraftAmount = Decimal(overdraftAmount)
   billName = input("Enter Bill Name: ")
   while True:
       accountNumber = input("Enter Account Number(Must Be 6 Digits): ")
       if re.search(r'^\d{6}$', accountNumber):
           break
   while True:
       amount = input("Enter An Amount To Be Paid: ")
       try:
           if Decimal(amount) > 0:
               break
           else:
               continue
       except Exception:
           # Exception indicates decimal error.
           continue
   amount = Decimal(amount)
   # The if statements checks where the money should go (overdraft/balance)
   if userMoney > amount or overdraft == 'True' and userMoney + overdraftAmount > amount:
       if userMoney > amount:
           userMoney -= amount
           file.pop(4)
           file.insert(4, userMoney)
       else:
           userMoney = 0
           goneIntoOverdraft = overdraftAmount - (amount - userMoney)
           now = datetime.now()
           current_time = "%s:%s %s / %s / %s" % (
           now.hour, now.minute, now.month, now.day, now.year)
           file = overdraftfunction(goneIntoOverdraft, email, current_time, file)
           file.pop(4)
           file.pop(4)
           file.insert(4, userMoney)
           file.insert(5, goneIntoOverdraft)
       now = datetime.now()
       current_time = "%s:%s %s / %s / %s\n" % (now.hour, now.minute, now.month, now.day, now.year)
       history_file = open(type+account + 'history.txt', 'a')
       history_file.write(current_time + '\n')
       history_file.write(str(-amount) + '\n')
       history_file.close()
       is_special(type,account, file)
       return replaceAccountFile(account, file)
   else:
       print("Not Enough Money")
       return file

def accountType(file):
    os.system('cls')
    while True:
        print("Your Accounts:"
            "\n1. Credit"
            "\n2. Checkings"
            "\n3. Savings"
            "\n4. Quit")
        navigation=input("Pick Option : ")
        if navigation == '1':
            type="Credit"
            menu(type,file)
        elif navigation == '2':
            type="Checkings"
            menu(type,file)
        elif navigation == '3':
            type="Savings"
            menu(type,file)
        elif navigation == '4':
            return


def menu(type,file):
    os.system('cls')
    while True:
        print("Welcome To The %s Account Menu."
            "\n1. View Account"
            "\n2. Change PIN"
            "\n3. Withdraw Money"
            "\n4. Deposit Money"
            "\n5. Pay Bills"
            "\n6. View History"
            "\n7. Go Back"
            "\n8. Quit"%type)
        navigation = input("Pick Option: ")
        if navigation == '1':
            view(type,file)
        elif navigation == '2':
            file = pin(file[1], file[0], file)
        elif navigation == '3':
            file = withdraw(type,Decimal(file[4]), file[3], file, file[0], file[5])
        elif navigation == '4':
            file = deposit(type,file, Decimal(file[4]), file[0])
        elif navigation == '5':
            file = bills(type,file, Decimal(file[4]), file[0], file[3], file[2], file[5])
        elif navigation == '6':
            print_transaction(type,file[0])
        elif navigation == '7':
            accountType(file)
        elif navigation == '8':
            print_transaction(type,file[0])
            return

def pins_check(pin_input):
   if os.path.exists('pins.txt'):
       pins = open('pins.txt', 'r')
       myFile = pins.readlines()
       pins.close()
       for pin in range(len(myFile)):
           new = myFile[pin].replace('\n', '')
           myFile.pop(pin)
           myFile.insert(pin, new)
       if pin_input in myFile:
           return False
       else:
           myPin = open('pins.txt', 'a')
           myPin.write(pin_input + '\n')
           myPin.close()
           return True

   else:
       pins = open('pins.txt', 'w')
       pins.write(pin_input + '\n')
       pins.close()
       return True

def signup():
   os.system('cls')
   # Card input
   while True:
       card = input("Enter The Card Number (Must Be 4 Digits): ")
       if not re.search(r'^\d{4}$', card):
           continue
       if equal(card):
           continue
       break
   # PIN input
   while True:
       pin = input("Enter The Pin Number (Must Be 4 Digits): ")
       if not re.search(r'^\d{4}$', pin):
           continue
       if equal(pin):
           continue
       if pins_check(pin):
           break
       else:
           print("The Pin Already Exists.")
   # Gmail input
   while True:
       email = input("Enter Email (Only gmail Account Allowed): ")
       if '@gmail.com' in email:
           break
   # Overdraft protection input
   while True:
       print("Would You Like To Sign Up For Overdraft Protection?\n\t1) YES \t 2) NO \t 3) What is Overdraft")
       prompt_overdraft = input("Pick An Option : ")
       if prompt_overdraft == '1' or prompt_overdraft == 'yes':
           overdraft = 'True'
           break
       elif prompt_overdraft == '2' or prompt_overdraft == 'no':
           overdraft = 'False'
           break
       elif prompt_overdraft == '3':
           print("Overdraft allows you to go beyond 0 to maximum of $500\n"
                 "Each time you go beyond the overdraft, you will be charged with 25% of your overdraft\n"
                 "An email will be sent to you each time you go beyond the overdraft. ")
   for i in range(1,4):
       if i==1:
          type="Credit"
       elif i==2:
          type="Checkings"
       elif i==3:
          type="Savings"

       userFile = open(card + '.txt', 'w')
       userFile.write(card + '\n' + pin + '\n' + email + '\n' + overdraft + '\n' + '0' + '\n')
       if overdraft == 'True':
           userFile.write('500')
       else:
           userFile.write('Not in action')
       userFile.close()
       user_history_file = open(type+card + 'history.txt', 'w')
       user_history_file.close()
       sys.stdout.write("Redirecting To Login")
       name = ".....\n"
       for char in name:
           sys.stdout.write(char)
           sys.stdout.flush()
           time.sleep(.6)
   login()


def login():
   os.system('cls')
   while True:
       card_login = input("Enter Your Card Number: ")
       if not os.path.exists(card_login + '.txt'):
           continue
       break
   user_file = open(card_login + '.txt')
   userLines = user_file.readlines()
   # The process of removing the line spacing
   for line in range(len(userLines)):
       new = userLines[line].replace('\n', '')
       userLines.pop(line)
       userLines.insert(line, new)
   user_file.close()

   actual_pin = userLines[1]
   while True:
       pin_login = input("Enter Your Pin: ")
       if not pin_login == actual_pin:
           continue
       break

   accountType(userLines)
   return


while True:
   print("WELCOME TO ATM SYSTEM\n\n\t1) Login \t 2) Sign Up\n")
   enter = input("Pick An Option : ")
   if enter == '1':
       login()
       break
   elif enter == '2':
       signup()
       break


