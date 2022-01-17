from datetime import datetime

'''
Parking Garage Project: simulates parking garage business

classes : 
    UI: handles the majority of the user interface
        Attributes:
            parking_garge: class parking_garage
        Methods:
            clear_terminal: erases content from terminal screen
            run_program: executes parking garage program

    ParkingGarage: handles calculations and data storage of the parking garage
        Attributes:
            rates: dictionary of billable rates
            parking_spaces: list of available parking spaces
            outstanding_tickets: dictionary of outstanding tickets
            sales: dictionary of all recorded sales

        Methods:
            show_rates: Displays parking rates on the terminal screen
            take_ticket: Removes space from available parking spaces, then
                creates an outstanding ticket with time stamp
            pay_ticket: Calculates amount owed by user based on lapsed time.
                If uses pays amount, then space is returned to available
                spaces, the outstanding ticket is deleted, and the transaction
                is recorded in sales.
            print_sales: Prints all transactions with summary to terminal
                screen.

Note:

For the purposes of this exercise, every 1 second will equal 1 hour to 
demonstrate the functionality of the rate calculation in a timely fashion.

'''

class UI():
    def __init__(self, parking_garage):
        self.parking_garage = parking_garage

    def clear_terminal(self):
        print("\033[2J\033[;H", end='')

    def run_program(self):
        su = '\033[04m' #start of underline
        eu = '\033[0m' #end of underline

        while True:
            action = input("Would you like to see " + su + "R" + eu + "ates, " \
                + su + "T" + eu + "ake Ticket, " + su + "P" + eu \
                + "ay Ticket or " + su + "Q" + eu + "uit? ")

            if action.lower() == "rates" or action.lower() == "r":
                self.clear_terminal()
                self.parking_garage.show_rates()
            elif action.lower() == "take" or action.lower() == "t":
                self.clear_terminal()
                self.parking_garage.take_ticket()
            elif action.lower() == "pay" or action.lower() == "p":
                self.clear_terminal()
                self.parking_garage.pay_ticket()
            elif action.lower() == "quit" or action.lower() == "q":
                self.clear_terminal()
                print("Thanks for using the parking garage. Have a nice day!")
                break
            elif action.lower() == "sales" or action.lower() == "s":
                # Hidden menu item to show all sales for the parking garage.
                self.clear_terminal()
                self.parking_garage.print_sales()
            else:
                print("You did not enter a valid command. Please try again.")

class ParkingGarage():
    def __init__(self):
        self.rates = {"hour": 5.00, "day": 100.00, "week": 500.00}
        self.parking_spaces = [1,2,3,4,5]
        self.outstanding_tickets = {}
        self.sales = {}

    def show_rates(self):
        print("Parking Rates:")
        for k in self.rates.keys():
            c = "{:.2f}".format(float(self.rates[k]))
            print(f"\t- ${c} per {k}.")  
        print("Note: 1 hour minimum.")

    def take_ticket(self):
        if self.parking_spaces:
            now = datetime.now()
            date_time = now.strftime("%d/%m/%Y %H:%M:%S")
            self.outstanding_tickets.update({self.parking_spaces[0]:now})
            print(f"Your ticket # is: {self.parking_spaces[0]}. Time In: {date_time}\n")
            self.parking_spaces.remove(self.parking_spaces[0])
        else:
            print("Unfortunately the parking garage is full. Please try" \
                " again later.\n")

    def pay_ticket(self):
        if not self.outstanding_tickets:
            print("There aren't any outstanding tickets. Please try again.")
        else:
            try:
                ticket_number = input("Please enter your ticket number: ")
                if int(ticket_number) in self.outstanding_tickets:
                    # calculate laspsed time
                    now = datetime.now()
                    time_out = now.strftime("%d/%m/%Y %H:%M:%S")
                    time_in = self.outstanding_tickets[int(ticket_number)].strftime("%d/%m/%Y %H:%M:%S")
                    time_lapse = now - self.outstanding_tickets[int(ticket_number)]

                    print(f"Time In: {time_in}")
                    print(f"Time Out: {time_out}")

                    # **************************************************************
                    # Speeds up time for testing purposes.
                    # 1 second = 1 hour.
                    # Remove for real-world application.
                    time_lapse *= 3600 
                    # **************************************************************

                    # Calculate amount owed.
                    sum = 0

                    if (((time_lapse.total_seconds() % 604800) % 86400) // 3600) == 0:
                        sum = self.rates["hour"]
                    else:
                        sum += (time_lapse.total_seconds() // 604800) * self.rates["week"] #weeks
                        sum += ((time_lapse.total_seconds() % 604800) // 86400) * self.rates["day"] #days
                        sum += (((time_lapse.total_seconds() % 604800) % 86400) // 3600) * self.rates["hour"] #hours
                    
                    action = input("Your total cost for parking is $" + \
                        "{:.2f}".format(sum) + ". Would you like to pay? (Yes/No) ")

                    if action.lower() == "yes" or action.lower() == "y":
                        print("Payment confirmed.") 
                        print("Please proceed to the nearest exit.\n")

                        # Make parking space available again
                        self.parking_spaces.insert(len(self.parking_spaces), int(ticket_number))
                        self.parking_spaces = sorted(self.parking_spaces)

                        # Remove ticket from outstanding tickets
                        del self.outstanding_tickets[int(ticket_number)]

                        # Add transaction to sales
                        self.sales[time_out] = sum

                else:
                    print("You have entered and invalid ticket number. Please try again.\n")
            except:
                 print("You have entered and invalid ticket number. Please try again.\n")

    def print_sales(self):
        if self.sales:
            sum = 0
            print("Sales:")
            for s in self.sales.keys():
                sum += self.sales[s]
                # time_out = self.outstanding_tickets[s].strftime("%d/%m/%Y %H:%M:%S")
                print(s + " $" + "{:.2f}".format(self.sales[s]))

            print("Total Sales: $" + "{:.2f}".format(sum) + ".")
        else:
            print("You haven't made any sales today. Get back to work!")

my_park = ParkingGarage()
ui = UI(my_park)
ui.run_program()