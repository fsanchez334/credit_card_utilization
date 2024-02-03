from expense_functions import ExpenseAnalyzer
from credit_analyzer import CreditAnalyzer
from IPython.display import display
import pandas as pd

if __name__ == "__main__":
    
    

    print("="*90)
    print("Expense Analyzer")
    print("=" * 90)
    print("The 50-30-20 rule")
    print("=" * 90)

    print("We will compile your provided expenses and provide a report in return using the 50-30-20 rule")
    print("The idea is to divide your income into three categories, spending 50% on needs, 30% on wants, and 20% on savings")
    print("=" * 90)
    pay = float(input("Please provide your check pay: "))

    main_df = pd.read_csv("sample_expenses.csv")
    credit_boolean = main_df["Credit Card?"] == "Y"
    credit_df = main_df[credit_boolean]

    EA = ExpenseAnalyzer(pay, main_df)
    CA = CreditAnalyzer(credit_df)
    EA.provideUserStatus()

    amount_available_for_expenses = EA.getAmountforNeeds()
    expected_expenses = EA.expense_collection()
    print("Your expected expenses total: {}".format(expected_expenses))
    credit_utilization = EA.credit_card_utilization()
    print("Your credit utilization is {}".format(credit_utilization))
    credit_df = EA.credit_card_breakdown()
    display(credit_df)
    print("Based on your input, these are the credit cards, in order of priority that you should pay")
    EA.credit_heap(credit_df)
    proceed_ = 1
    if expected_expenses > pay:
        print("You will not have enough to cover your expeneses")
    else:

        while proceed_ == 1:
            if amount_available_for_expenses >= expected_expenses:
        
                print("Paying your expenses result in the following:")
                #Assumes the user can cover the expenses
                EA.updateNeeds(-1 * expected_expenses)
                EA.updateTotal(-1 * expected_expenses)
                EA.provideUserStatus()
                proceed_ = 0
            else:
                while amount_available_for_expenses < expected_expenses:
                    #Calculate how much money you would need to at least cover your expenses
                    extra_money_needed = expected_expenses - amount_available_for_expenses
                    print("You don't have enough to pay your expenses from your 50% bucket. You would need at least {} from your other categories".format(extra_money_needed))
                    print("However, you can use an amount from one of your other catageories")
                    EA.provideUserStatus()
                    category = input("From which category would you like to use money from: ")
                    amount = float(input("How much money would you like to use from your category: "))
                    if category == "Savings":
                        EA.updateSavings(-1 * amount)
                        EA.updateNeeds(amount)
                    if category == "Wants":
                        EA.updateWants(-1 * amount)
                        EA.updateNeeds(amount)
                    amount_available_for_expenses += amount
