import logging  # For keeping track of what happens
import json     # For handling data
import time     # For time-related functions
from binance import Client  # The main Binance library
from binance.exceptions import BinanceAPIException, BinanceOrderException  # For handling errors


class TradingBot:
    """
    This is our main trading bot class
    Think of it like a robot that can trade for us
    """
    
    def __init__(self, api_key, api_secret, use_testnet=True):
        """
        This function runs when we create our bot
        It's like turning on the robot
        """
        print("Starting up the trading bot...")
        
        # Store our API keys (like our username and password for Binance)
        self.api_key = api_key
        self.api_secret = api_secret
        
        # Create connection to Binance (testnet means fake money for practice)
        self.client = Client(api_key, api_secret, testnet=use_testnet)
        
        # Set up logging (like keeping a diary of what we do)
        self.setup_logging()
        
        # Test if we can connect to Binance
        try:
            self.client.ping()  # Like saying "hello" to Binance
            print(" Successfully connected to Binance!")
            self.logger.info("Bot connected successfully")
        except Exception as error:
            print(f" Failed to connect: {error}")
            self.logger.error(f"Connection failed: {error}")
            raise  # Stop the program if we can't connect
    
    def setup_logging(self):
        """
        This sets up our logging system
        Like setting up a notebook to write down everything that happens
        """
        logging.basicConfig(
            level=logging.INFO,  # What level of detail to log
            format='%(asctime)s - %(levelname)s - %(message)s',  # How to format our logs
            handlers=[
                logging.FileHandler('my_trading_bot.log'),  # Save to file
                logging.StreamHandler()  # Also show on screen
            ]
        )
        self.logger = logging.getLogger('TradingBot')
        print("Logging system ready!")
    
    def check_my_account(self):
        """
        Check how much money we have in our account
        Like checking your wallet
        """
        try:
            print(" Checking account balance...")
            account_info = self.client.futures_account()
            
            # Get the total balance
            balance = account_info.get('totalWalletBalance', '0')
            print(f"Your account balance: {balance} USDT")
            
            self.logger.info(f"Account balance checked: {balance} USDT")
            return account_info
            
        except BinanceAPIException as error:
            print(f"Error checking account: {error}")
            self.logger.error(f"Account check failed: {error}")
            return None
    
    def get_price(self, symbol):
        """
        Get the current price of a cryptocurrency
        Like checking the price tag in a store
        """
        try:
            print(f" Getting price for {symbol}...")
            
            # Get price information
            price_info = self.client.futures_symbol_ticker(symbol=symbol)
            current_price = price_info['price']
            
            print(f"Current price of {symbol}: ${current_price}")
            self.logger.info(f"Price for {symbol}: {current_price}")
            
            return float(current_price)
            
        except BinanceAPIException as error:
            print(f" Error getting price for {symbol}: {error}")
            self.logger.error(f"Price check failed for {symbol}: {error}")
            return None
    
    def buy_crypto(self, symbol, amount):
        """
        Buy cryptocurrency at current market price
        Like buying something at the store at the current price
        """
        try:
            print(f" Trying to BUY {amount} of {symbol}...")
            
            # Place a market buy order (buy at current price immediately)
            order = self.client.futures_create_order(
                symbol=symbol,          # What to buy (like BTCUSDT)
                side='BUY',            # We want to buy
                type='MARKET',         # Buy at current market price
                quantity=amount        # How much to buy
            )
            
            order_id = order['orderId']
            print(f" Buy order successful! Order ID: {order_id}")
            
            # Log the details
            self.log_order_info(order)
            return order
            
        except BinanceOrderException as error:
            print(f" Buy order failed: {error}")
            self.logger.error(f"Buy order failed: {error}")
            return None
        except BinanceAPIException as error:
            print(f"API error during buy: {error}")
            self.logger.error(f"API error during buy: {error}")
            return None
    
    def sell_crypto(self, symbol, amount):
        """
        Sell cryptocurrency at current market price
        Like selling something at the current market price
        """
        try:
            print(f"💸 Trying to SELL {amount} of {symbol}...")
            
            # Place a market sell order (sell at current price immediately)
            order = self.client.futures_create_order(
                symbol=symbol,          # What to sell
                side='SELL',           # We want to sell
                type='MARKET',         # Sell at current market price
                quantity=amount        # How much to sell
            )
            
            order_id = order['orderId']
            print(f"Sell order successful! Order ID: {order_id}")
            
            # Log the details
            self.log_order_info(order)
            return order
            
        except BinanceOrderException as error:
            print(f" Sell order failed: {error}")
            self.logger.error(f"Sell order failed: {error}")
            return None
        except BinanceAPIException as error:
            print(f" API error during sell: {error}")
            self.logger.error(f"API error during sell: {error}")
            return None
    
    def buy_at_specific_price(self, symbol, amount, price):
        """
        Place an order to buy at a specific price (limit order)
        Like putting in a request to buy something only if the price drops to what you want
        """
        try:
            print(f" Placing limit BUY order: {amount} of {symbol} at ${price}")
            
            # Place a limit buy order
            order = self.client.futures_create_order(
                symbol=symbol,
                side='BUY',
                type='LIMIT',                    # Wait for specific price
                timeInForce='GTC',              # Good Till Cancelled
                quantity=amount,
                price=price
            )
            
            order_id = order['orderId']
            print(f"Limit buy order placed! Order ID: {order_id}")
            print(f"The order will execute when {symbol} price reaches ${price}")
            
            self.log_order_info(order)
            return order
            
        except BinanceOrderException as error:
            print(f" Limit buy order failed: {error}")
            self.logger.error(f"Limit buy order failed: {error}")
            return None
        except BinanceAPIException as error:
            print(f" API error during limit buy: {error}")
            self.logger.error(f"API error during limit buy: {error}")
            return None
    
    def sell_at_specific_price(self, symbol, amount, price):
        """
        Place an order to sell at a specific price (limit order)
        Like putting in a request to sell something only if the price goes up to what you want
        """
        try:
            print(f"Placing limit SELL order: {amount} of {symbol} at ${price}")
            
            # Place a limit sell order
            order = self.client.futures_create_order(
                symbol=symbol,
                side='SELL',
                type='LIMIT',
                timeInForce='GTC',
                quantity=amount,
                price=price
            )
            
            order_id = order['orderId']
            print(f" Limit sell order placed! Order ID: {order_id}")
            print(f"The order will execute when {symbol} price reaches ${price}")
            
            self.log_order_info(order)
            return order
            
        except BinanceOrderException as error:
            print(f" Limit sell order failed: {error}")
            self.logger.error(f"Limit sell order failed: {error}")
            return None
        except BinanceAPIException as error:
            print(f" API error during limit sell: {error}")
            self.logger.error(f"API error during limit sell: {error}")
            return None
    
    def check_order_status(self, symbol, order_id):
        """
        Check if our order has been completed
        Like checking if your online order has been delivered
        """
        try:
            print(f" Checking status of order {order_id}...")
            
            order = self.client.futures_get_order(symbol=symbol, orderId=order_id)
            
            status = order['status']
            filled_amount = order['executedQty']
            total_amount = order['origQty']
            
            print(f"Order Status: {status}")
            print(f"Filled: {filled_amount} out of {total_amount}")
            
            if status == 'FILLED':
                print(" Order completed successfully!")
            elif status == 'PARTIALLY_FILLED':
                print(" Order partially completed")
            elif status == 'NEW':
                print("Order is waiting to be filled")
            elif status == 'CANCELED':
                print(" Order was cancelled")
            
            self.logger.info(f"Order {order_id} status: {status}")
            return order
            
        except BinanceAPIException as error:
            print(f" Error checking order status: {error}")
            self.logger.error(f"Order status check failed: {error}")
            return None
    
    def cancel_order(self, symbol, order_id):
        """
        Cancel an order that hasn't been completed yet
        Like cancelling an online order before it ships
        """
        try:
            print(f" Cancelling order {order_id}...")
            
            result = self.client.futures_cancel_order(symbol=symbol, orderId=order_id)
            
            print(f"Order {order_id} cancelled successfully!")
            self.logger.info(f"Order {order_id} cancelled")
            return result
            
        except BinanceAPIException as error:
            print(f" Error cancelling order: {error}")
            self.logger.error(f"Order cancellation failed: {error}")
            return None
    
    def see_my_open_orders(self, symbol=None):
        """
        See all orders that are still waiting to be completed
        Like checking all your pending online orders
        """
        try:
            print("Checking your open orders...")
            
            orders = self.client.futures_get_open_orders(symbol=symbol)
            
            if not orders:
                print("No open orders found")
                return []
            
            print(f"You have {len(orders)} open orders:")
            print("-" * 50)
            
            for order in orders:
                print(f"Order ID: {order['orderId']}")
                print(f"Symbol: {order['symbol']}")
                print(f"Side: {order['side']} (Buy/Sell)")
                print(f"Amount: {order['origQty']}")
                print(f"Price: {order['price']}")
                print(f"Status: {order['status']}")
                print("-" * 50)
            
            self.logger.info(f"Retrieved {len(orders)} open orders")
            return orders
            
        except BinanceAPIException as error:
            print(f" Error getting open orders: {error}")
            self.logger.error(f"Open orders check failed: {error}")
            return []
    
    def log_order_info(self, order):
        """
        Save order information to our log file
        Like keeping a receipt of what we did
        """
        order_details = {
            'Order ID': order.get('orderId'),
            'Symbol': order.get('symbol'),
            'Side': order.get('side'),
            'Type': order.get('type'),
            'Status': order.get('status'),
            'Amount': order.get('origQty'),
            'Price': order.get('price'),
            'Filled': order.get('executedQty')
        }
        
        self.logger.info(f"Order details: {json.dumps(order_details, indent=2)}")
    
    def is_valid_input(self, symbol, side, amount, price=None):
        """
        Check if the user input is correct
        Like double-checking before placing an order
        """
        # Check if symbol is valid
        if not symbol or not isinstance(symbol, str):
            print(" Invalid symbol! Please enter a valid trading pair like BTCUSDT")
            return False
        
        # Check if side is valid
        if side not in ['BUY', 'SELL']:
            print(" Invalid side! Please enter 'BUY' or 'SELL'")
            return False
        
        # Check if amount is valid
        if amount <= 0:
            print(" Invalid amount! Amount must be greater than 0")
            return False
        
        # Check if price is valid (if provided)
        if price is not None and price <= 0:
            print(" Invalid price! Price must be greater than 0")
            return False
        
        return True


def main():
    """
    This is the main function that runs our program
    It's like the control center of our bot
    """
    print("=" * 50)
    print(" WELCOME TO BINANCE TRADING BOT FOR BEGINNERS!")
    print("=" * 50)
    print("  IMPORTANT: This bot uses TESTNET (fake money for practice)")
    print("  No real money will be used!")
    print("=" * 50)
    
    # Get API credentials from user
    print("\n First, we need your Binance API credentials:")
    print("(You can get these from Binance Testnet website)")
    
    api_key = input("Enter your API Key: ").strip()
    api_secret = input("Enter your API Secret: ").strip()
    
    # Check if credentials were provided
    if not api_key or not api_secret:
        print(" Error: You must provide both API key and secret!")
        print("Please get them from https://testnet.binancefuture.com")
        return
    
    try:
        # Create our trading bot
        print("\n Creating your trading bot...")
        bot = TradingBot(api_key, api_secret, use_testnet=True)
        
        # Check account balance
        print("\n Checking your account...")
        bot.check_my_account()
        
        # Main menu loop
        while True:
            print("\n" + "=" * 50)
            print(" WHAT WOULD YOU LIKE TO DO?")
            print("=" * 50)
            print("1.  Check Account Balance")
            print("2.  Get Current Price")
            print("3.  Buy Crypto (Market Order)")
            print("4.  Sell Crypto (Market Order)")
            print("5.  Buy at Specific Price (Limit Order)")
            print("6.  Sell at Specific Price (Limit Order)")
            print("7.  Check Order Status")
            print("8.  See My Open Orders")
            print("9.  Cancel an Order")
            print("10.  Exit")
            print("=" * 50)
            
            choice = input("Enter your choice (1-10): ").strip()
            
            if choice == '1':
                # Check account balance
                print("\n" + "-" * 30)
                bot.check_my_account()
                
            elif choice == '2':
                # Get current price
                print("\n" + "-" * 30)
                symbol = input("Enter symbol (e.g., BTCUSDT): ").strip().upper()
                if symbol:
                    bot.get_price(symbol)
                else:
                    print(" Please enter a valid symbol!")
                    
            elif choice == '3':
                # Buy crypto (market order)
                print("\n" + "-" * 30)
                symbol = input("Enter symbol (e.g., BTCUSDT): ").strip().upper()
                try:
                    amount = float(input("Enter amount to buy: "))
                    if bot.is_valid_input(symbol, 'BUY', amount):
                        bot.buy_crypto(symbol, amount)
                except ValueError:
                    print(" Please enter a valid number for amount!")
                    
            elif choice == '4':
                # Sell crypto (market order)
                print("\n" + "-" * 30)
                symbol = input("Enter symbol (e.g., BTCUSDT): ").strip().upper()
                try:
                    amount = float(input("Enter amount to sell: "))
                    if bot.is_valid_input(symbol, 'SELL', amount):
                        bot.sell_crypto(symbol, amount)
                except ValueError:
                    print(" Please enter a valid number for amount!")
                    
            elif choice == '5':
                # Buy at specific price (limit order)
                print("\n" + "-" * 30)
                symbol = input("Enter symbol (e.g., BTCUSDT): ").strip().upper()
                try:
                    amount = float(input("Enter amount to buy: "))
                    price = float(input("Enter price you want to buy at: "))
                    if bot.is_valid_input(symbol, 'BUY', amount, price):
                        bot.buy_at_specific_price(symbol, amount, price)
                except ValueError:
                    print(" Please enter valid numbers!")
                    
            elif choice == '6':
                # Sell at specific price (limit order)
                print("\n" + "-" * 30)
                symbol = input("Enter symbol (e.g., BTCUSDT): ").strip().upper()
                try:
                    amount = float(input("Enter amount to sell: "))
                    price = float(input("Enter price you want to sell at: "))
                    if bot.is_valid_input(symbol, 'SELL', amount, price):
                        bot.sell_at_specific_price(symbol, amount, price)
                except ValueError:
                    print(" Please enter valid numbers!")
                    
            elif choice == '7':
                # Check order status
                print("\n" + "-" * 30)
                symbol = input("Enter symbol: ").strip().upper()
                try:
                    order_id = int(input("Enter order ID: "))
                    bot.check_order_status(symbol, order_id)
                except ValueError:
                    print(" Please enter a valid order ID (number)!")
                    
            elif choice == '8':
                # See open orders
                print("\n" + "-" * 30)
                symbol = input("Enter symbol (or press Enter for all): ").strip().upper()
                symbol = symbol if symbol else None
                bot.see_my_open_orders(symbol)
                
            elif choice == '9':
                # Cancel order
                print("\n" + "-" * 30)
                symbol = input("Enter symbol: ").strip().upper()
                try:
                    order_id = int(input("Enter order ID to cancel: "))
                    bot.cancel_order(symbol, order_id)
                except ValueError:
                    print(" Please enter a valid order ID (number)!")
                    
            elif choice == '10':
                # Exit
                print("\n Thanks for using the trading bot!")
                print("Happy trading! ")
                break
                
            else:
                print(" Invalid choice! Please enter a number between 1-10")
            
            # Wait a moment before showing menu again
            input("\nPress Enter to continue...")
    
    except Exception as error:
        print(f"\n Something went wrong: {error}")
        print("Please check:")
        print("1. Your internet connection")
        print("2. Your API credentials are correct")
        print("3. Your API has futures trading enabled")


# This is where our program starts
if __name__ == "__main__":
    main()