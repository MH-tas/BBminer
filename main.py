from customtkinter import *
import tkinter as tk
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import ccxt
import time
from binance.client import Client
import threading
from pygame import mixer

# Create Window with tkinter
app = CTk()
app.geometry("1280x760")
app.resizable(False, False) # Unchangeable Window Size
app.configure(fg_color="#1a1a1a")
app.iconbitmap("icon.ico")
set_appearance_mode("dark")


api_key = 'api_key'
api_secret = 'api_secret'

global Target_coin
Target_coin = "BTC"
global amount
amount = "1"
global symbol  # Selected Coin
symbol = Target_coin + '/USDT'
global symbol2  # Selected Coin
symbol2 = Target_coin + 'USDT'
stop_flag = False
global kar
kar = "0.0"
global startedMoney


# Define Your Id
binance = ccxt.binance({
    'apiKey': api_key,
    'secret': api_secret,
})

client = Client(api_key, api_secret)

# Status None
previous_status = None

# Check Order
order_executed = False

# Create Your Bools
bool1 = False
bool2 = False
bool3 = False


def run_bot_thread():
    # Start bot
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()

def toggle_bool1():
    global bool1
    bool1 = not bool1
    printer("Bool 123123987: " + str(bool1) + " olarak değiştirildi")

def toggle_bool2():
    global bool2
    bool2 = not bool2
    printer("Bool 135792468: " + str(bool2) + " olarak değiştirildi")

def toggle_bool3():
    global bool3
    bool3 = not bool3
    printer("Bool 112211441: " + str(bool3) + " olarak değiştirildi")

def printer(text):
    print_text = text
    entry.insert(tk.END, "\n" + print_text)

def get_coin_price(symbol):
    ticker = client.get_symbol_ticker(symbol=symbol)
    return float(ticker['price'])

def start_bot():

    global stop_flag
    global symbol  # Selected coin
    symbol = Target_coin + '/USDT'
    printer("Bot başlatıldı...")
    update_coin()
    update_amount()
    if not stop_flag:
        run_bot_thread()
    else:
        stop_flag = False
        run_bot_thread()

    label_11.configure(text="Balance: " + str(get_account_balance("USDT")) + " USDT")
    label_Status.configure(text="Çalışıyor",text_color="#00d400")

def stop_bot():
    printer("Bot durduruldu...")
    label_11.configure(text="Balance: " + str(get_account_balance("USDT")) + " USDT")
    label_Status.configure(text="Durduruldu",text_color="#d40000")
    global stop_flag
    stop_flag = True
def run_bot():
    global previous_status, order_executed
    printer("Chrome Portu aranıyor...")
    global stop_flag
    while not stop_flag:
        # Select port for chrome
        remote_debugging_port = 9223

        # Edit or Change Your Options
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", f"localhost:{remote_debugging_port}")


        driver = webdriver.Chrome(options=chrome_options)

        # Get Data From Website (Website will be Currently opened)
        html_content = driver.page_source

        # Check the numbers in this data
        if bool1 and not bool2 and not bool3:
            target_numbers = ["123123987"]
        elif bool2 and not bool1 and not bool3:
            target_numbers = ["135792468"]
        elif bool3 and not bool1 and not bool2:
            target_numbers = ["112211441"]
        elif bool1 and bool2 and not bool3:
            target_numbers = ["123123987", "135792468"]  # Örneğin, bool1 ve bool2 etkinse, hedef sayı 123123987 olur
        elif bool1 and bool3 and not bool2:
            target_numbers = ["123123987", "112211441"]  # Örneğin, bool1 ve bool3 etkinse, hedef sayı 123123987 olur
        elif bool2 and bool3 and not bool1:
            target_numbers = ["135792468", "112211441"]  # Örneğin, bool2 ve bool3 etkinse, hedef sayı 135792468 olur
        elif bool1 and bool2 and bool3:
            target_numbers = ["123123987","135792468", "112211441"]  # Örneğin, bool1, bool2 ve bool3 etkinse, hedef sayı 123123987 olur
        else:
            printer("No Selected Bool !")

        current_status = None

        if ("123123987" in html_content):

            # BUY
            if not order_executed:
                order_executed = True
                market_order(symbol, amount, 'buy')
                current_status = "Pump tespit edildi. Alım yapıldı"
        else:
            # SELL
            if order_executed:
                order_executed = False
                max_quantity_coin = get_account_balance(Target_coin)
                market_order(symbol, max_quantity_coin, 'sell')
                current_status = "Bullish tespit edildi. Satış yapıldı"

        # Notfication
        if current_status != previous_status:
            printer(str(current_status))
            previous_status = current_status

        # Quit
        driver.quit()
        time.sleep(0.04)


def market_order(symbol, quantity, side):
    global kar
    try:
        # Check Your Balance
        if side == 'buy':
            order = binance.create_market_order(symbol=symbol, side='buy', amount=quantity)
            printer(f"Buy order placed: {str(order)}")
            label_11.configure(text="Balance: " + str(get_account_balance("USDT")) + " USDT")
            mixer.init()
            mixer.music.load('buy.mp3')
            mixer.music.play()
        elif side == 'sell':
            order = binance.create_market_order(symbol=symbol, side='sell', amount=quantity)
            printer(f"Sell order placed: {str(order)}")
            label_11.configure(text="Balance: " + str(get_account_balance("USDT")) + " USDT")
            kar = float(get_account_balance("USDT")-startedMoney)
            label_12.configure(text="KAR :                  $"+str(round(kar, 5)))
            mixer.init()
            mixer.music.load('sell.mp3')
            mixer.music.play()

    except Exception as e:
        printer(f"Error placing {side} order: {e}"+Target_coin)

def get_account_balance(asset):
    try:
        balance = binance.fetch_balance()
        return balance['total'][asset] if asset in balance['total'] else 0
    except Exception as e:
        printer(f"Error fetching account balance: {e}")
        return 0

# Update Your Coin

def update_coin():
    coin_name = coin_entry.get()
    coin_label.configure(text=coin_name+" / USDT")
    global Target_coin
    Target_coin = coin_name
    global symbol2
    symbol2 = Target_coin + 'USDT'
    printer("Coin " + str(Target_coin) + " olarak değiştirildi.")
    label_13.configure(text="Mks alım :      "+str(round(get_account_balance("USDT")/get_coin_price(symbol2),4))+" "+Target_coin)
# Update The Count Of Coin
def update_amount():
    coin_amount = amount_entry.get()
    global amount
    amount = coin_amount
    printer(str(amount) +" "+ str(Target_coin) + " alımı planlanıyor")

def start_chrome():
    import subprocess
    subprocess.Popen('cmd /K cd /d "C:\\Program Files\\Google\\Chrome\\Application" && start chrome.exe --remote-debugging-port=9223')
    printer("Chrome 9223 portu üzerinden Başlatıldı")









# Name Of Window
app.title("BB Miner")

# Set of UI
frame = CTkFrame(app,fg_color="#1a1a1a")
frame.pack(padx=20, pady=20)

frame_middle = CTkFrame(app,fg_color="#1a1a1a")
frame_middle.pack(padx=40, pady=20)

frame_bottom = CTkFrame(app,fg_color="#1c1c1c")
frame_bottom.pack(fill='both', side='left', expand='True')

frame_bottom_left = CTkFrame(frame_bottom,fg_color="#2b2b2a")
frame_bottom_left.pack(side='left',fill='both',padx=10, pady=10)

frame_bottom_right = CTkFrame(frame_bottom,fg_color="#2b2b2a")
frame_bottom_right.pack(side='right',fill='both',padx=10, pady=10)

frame_bottom_middle = CTkFrame(frame_bottom,fg_color="#2b2b2a")
frame_bottom_middle.pack(side='top',fill='both',padx=10, pady=10)

frame_bottom_middle_2 = CTkFrame(frame_bottom,fg_color="#2b2b2a")
frame_bottom_middle_2.pack(side='bottom',expand='True',fill='both',padx=10, pady=10)



entry = CTkTextbox(frame_bottom_middle_2, width=120,border_color="#F3BA2F",border_width=2)
entry.pack(side=BOTTOM,expand='True', padx=10,fill='both', pady=10)

label_Status = CTkLabel(frame_bottom_middle_2, text="Durduruldu", font=("Century Gothic", 25), text_color="#d40000")
label_Status.pack(side=TOP,padx=10, pady=10)



toggle_button_1 = CTkSwitch(frame_bottom_middle, text="123123987",font=("Century Gothic", 15),progress_color="#F3BA2F",command=toggle_bool1)
toggle_button_1.pack(side=TOP,anchor=NW,padx=30, pady=10)


toggle_button_2 = CTkSwitch(frame_bottom_middle, text="135792468",font=("Century Gothic", 15),progress_color="#F3BA2F",command=toggle_bool2)
toggle_button_2.pack(side=TOP,anchor=W,padx=30, pady=10)

toggle_button_3 = CTkSwitch(frame_bottom_middle, text="112211441",font=("Century Gothic", 15),progress_color="#F3BA2F",command=toggle_bool3)
toggle_button_3.pack(side=TOP,anchor=SW,padx=30, pady=10)



frame_1 = CTkFrame(frame_bottom_left,fg_color="#1a1a1a")
frame_1.pack(side='top',fill='both',padx=10, pady=10)

label_1 = CTkLabel(frame_1, text="YAPILANDIR", font=("Century Gothic", 20), text_color="#ffffff")
label_1.pack(padx=40, pady=10)

frame_2 = CTkFrame(frame_bottom_left,fg_color="#454545")
frame_2.pack(side='top',fill='both',padx=10, pady=10)

coin_label = CTkLabel(frame_2, text="BTC / USDT", font=("Century Gothic", 15), text_color="#ffffff")
coin_label.pack(side=LEFT,padx=10, pady=10)

button_2 = CTkButton(frame_2, text="Güncelle",fg_color="#F3BA2F",text_color="#1a1a1a",hover_color="#343434", command=update_coin)
button_2.pack(side=RIGHT, padx=10)

coin_entry = CTkEntry(frame_2, width=100)
coin_entry.pack(side=RIGHT, padx=10)
coin_entry.insert(tk.END,"BTC")




frame_2 = CTkFrame(frame_bottom_left,fg_color="#454545")
frame_2.pack(side='top',fill='both',padx=10, pady=10)

label_2 = CTkLabel(frame_2, text="MİKTAR :", font=("Century Gothic", 15), text_color="#ffffff")
label_2.pack(side=LEFT,padx=10, pady=10)

button_2 = CTkButton(frame_2, text="Güncelle",fg_color="#F3BA2F",text_color="#1a1a1a",hover_color="#343434", command=update_amount)
button_2.pack(side=RIGHT, padx=10)

amount_entry = CTkEntry(frame_2, width=100)
amount_entry.pack(side=RIGHT, padx=10)
amount_entry.insert(tk.END,"1")

frame_3 = CTkFrame(frame_bottom_right,fg_color="#1a1a1a")
frame_3.pack(side='top',fill='both',padx=10, pady=10)





label_5 = CTkLabel(frame_3, text="BINANCE INFO", font=("Century Gothic", 20), text_color="#ffffff")
label_5.pack(padx=40, pady=10)

label_11 = CTkLabel(frame_bottom_right, text="Cüzdan :         $"+str(round(get_account_balance("USDT"), 3)), font=("Century Gothic", 15), text_color="#ffffff")
label_11.pack(side=TOP, anchor=NW,padx=10, pady=10)

label_12 = CTkLabel(frame_bottom_right, text="Kar :                  $"+kar, font=("Century Gothic", 15), text_color="#ffffff")
label_12.pack(side=TOP, anchor=NW,padx=10, pady=10)

label_13 = CTkLabel(frame_bottom_right, text="Mks alım :      "+str(round(get_account_balance("USDT")/get_coin_price(symbol2),4))+" "+Target_coin, font=("Century Gothic", 15), text_color="#ffffff")
label_13.pack(side=TOP, anchor=NW,padx=10, pady=10)

# Color Of Background






app.configure(background="#1a1a1a")

# Font And Size
label = CTkLabel(frame, text="BB Miner", font=("Century Gothic", 40), text_color="#F3BA2F")
label.pack()

button_baslat = CTkButton(frame_middle, text="Başlat",fg_color="#F3BA2F",text_color="#1a1a1a",hover_color="#00d400", command=start_bot)
button_baslat.pack(side=LEFT, padx=10)

# Stop button
button_durdur = CTkButton(frame_middle, text="Durdur",fg_color="#F3BA2F",text_color="#1a1a1a",hover_color="#d40000", command=stop_bot)
button_durdur.pack(side=LEFT, padx=10)

# Start Chrome Button
button_chrome = CTkButton(frame_middle, text="Run Chrome",fg_color="#F3BA2F",text_color="#1a1a1a",hover_color="#b52bff", command=start_chrome)

button_chrome.pack(side=LEFT, padx=10)

printer("Hoşgeldiniz Hamza bey, V1.0.0.2 BB Miner")
startedMoney = float(get_account_balance("USDT"))

mixer.init()
mixer.music.load('start.mp3')
mixer.music.play()
# Main loop
app.mainloop()

