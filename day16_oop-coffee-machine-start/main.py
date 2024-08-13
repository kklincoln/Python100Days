from menu import Menu, MenuItem
from coffee_maker import CoffeeMaker
from money_machine import MoneyMachine

#creating the classes from money_machine and coffee_maker to call the methods
my_money_machine = MoneyMachine()
maker = CoffeeMaker()
menu = Menu()
is_on = True


#check resources are sufficient?
while is_on:
    options = menu.get_items()
    choice = input(f"What would you like to drink? {options}:").lower()

    #  requirement #2: off for maintenance
    if choice == "off":
        is_on = False
    # requirement #3: report;
    elif choice =="report":
        # print report of remaining ingredients and money made
        my_money_machine.report()  # returns profit report
        maker.report()  # returns ingredient remaining report
    else:
        #find drink using the method;
        drink = menu.find_drink(choice)
        #requirement 4: check the resources with coffeeMaker class # requirement 5: my_money_machine.make_payment(drink.cost) with the cost attribute is met, return true
        if maker.is_resource_sufficient(drink) and my_money_machine.make_payment(drink.cost):
                #requirement 6: If resources_sufficient and payment_made, make_coffee
                maker.make_coffee(drink)