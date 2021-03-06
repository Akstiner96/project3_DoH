import numpy as np
import pandas as pd
import time
import alpaca_trade_api as tradeapi
import requests
import os 
from dotenv import load_dotenv


load_dotenv()

#load alpaca keys
alpaca_api_key = os.getenv("ALPACA_API_KEY")
alpaca_secret_key = os.getenv("ALPACA_SECRET_KEY")

api = tradeapi.REST(alpaca_api_key, alpaca_secret_key, api_version='v2')


# Set variables to simulate holding a current bank account that can send and receive
# money via ACH transfers to and from Alpaca
# We are assuming we have 100,000 in the bank and we are sending 100,000 to our alpaca algorithm

beginning_deposit = 100000

bank_balance = 100000

send_to_alpaca_amount = 100000

withdraw_from_alpaca_amount = 0


def send_to_alpaca(send_to_alpaca_amount, bank_balance):
    ''' This function sends money to alpaca and calculates a new bank balance.   
        In reality this would be an ACH transfer from our bank to alpaca. '''

    if send_to_alpaca_amount > bank_balance:
        print("Transfer not completed. Insufficient funds.")
    else:
        bank_balance -= send_to_alpaca_amount
        print()
        print(f"Transfer to alpaca successful. Your bank balance is now {bank_balance} dollars")
        print()   
    return bank_balance
    

def transfer_profits_from_alpaca(bank_balance, beginning_deposit):

    '''This function calculates our profits and sends them back to our bank.
        In reality this would be an ACH transfer too. If there are no profits no transfer takes place.''' 
    
    #Set amount to withdraw to zero and check our cash
    withdraw_from_alpaca_amount = int(0)
    account = api.get_account()
    cash = float(account.cash)
    
    #calculate how much profit we have. Withdraw that amount from alpaca to our bank.
    if float(account.portfolio_value) > beginning_deposit:

        withdraw_from_alpaca_amount += (float(account.portfolio_value) - beginning_deposit)
        
        #check to see if we have enough cash to withdraw the profit.
        if float(cash) > float(withdraw_from_alpaca_amount):
            bank_balance += withdraw_from_alpaca_amount
            print(f"Your withdrawal from alpaca was successful. Your new bank balance is ${bank_balance}")
        
        #if we are fully invested with no cash then we need to sell stock equal to the amount of profit
        else:
            qty = int(withdraw_from_alpaca_amount/float(api.get_position('SPY').current_price))
            
            api.submit_order(
                symbol= symbol,
                qty= qty,
                side='sell',
                type='market',
                time_in_force='gtc'
            )
            # Wait a second for our orders to fill...
            print('Waiting...')
            time.sleep(1)
            bank_balance += withdraw_from_alpaca_amount
            print(f"Your transfer of profits from alpaca was successful. Your new bank balance is ${bank_balance}")
    
    else:
        print("There are no profits to withdraw")
        
    return bank_balance
        
#Transfer any amount from alpaca to the bank
# Set withdraw_from_alpaca_amount = any amount

def transfer_from_alpaca(withdraw_from_alpaca_amount, bank_balance, beginning_deposit):

    #print current market value of account
    print('Total market value is ${account.portfolio_value}.')
    
    if withdraw_from_alpaca_amount <= account.portfolio_value:
        bank_balance += withdraw_from_alpaca_amount
        print(f"Your withdrawal was successful. Your new bank balance is ${bank_balance}")
        
    else:
        print("You do not have enough funds to withdraw that amount.")


def positions():  
    """ Get a list of all of our positions."""
    portfolio = api.list_positions()

    # Print the quantity of shares for each position.
    for position in portfolio:
        print("{} shares of {}".format(position.qty, position.symbol))


#This buy function worked with alpaca. Still need to figure out how to get a price.
symbol = "SPY"

def buy(symbol):
    '''Use cash to buy stock '''
    # get our cash and last price from alpaca  
    cash = float(api.get_account().cash) 
    
    #hard coded price, have not figured out how to get price quote
    price = 343.30
    
    qty = int(cash/price)
    
    api.submit_order(
        symbol= symbol,
        qty= qty,
        side='buy',
        type='market',
        time_in_force='gtc'
    )
    print(f"You sent an order to buy {qty} shares of {symbol} to alpaca.")
          
def sell_all(symbol):
    '''Sell all the shares of a given symbol. '''
    
    # get number of shares we hold of a symbol
    qty = api.get_position(symbol).qty
    
    api.submit_order(
        symbol= symbol,
        qty= qty,
        side='sell',
        type='market',
        time_in_force='gtc'
    )
    print(f"You sent an order to sell {qty} shares of {symbol} to alpaca.")
    
 
    '''''
    Useful commands:

    api.get_account().cash
    api.get_asset('SPY')
    api.list_positions()
    account = api.get_account().cash
    account.status
    account.portfolio_value
    api.list_orders()
    api.get_position("SPY")
    api.get_position("SPY").qty
    api.list
    '''''