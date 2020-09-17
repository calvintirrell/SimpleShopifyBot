# imported packages to create this bot
import time
import json
import requests
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from selenium import webdriver


# this function actually opens a Chrome browser, fills in information and purchases the item
# time.sleep(#) pauses the program between steps so websites don't detect the 'bot' due to 'typing' speed
def buy_stuff(item_url):
    # open Chrome browser to the specified item's url and choose the shoe size (13)
    driver = webdriver.Chrome(executable_path='/Users/calvintirrell/Downloads/chromedriver')
    driver.get(item_url)
    time.sleep(0.2)
    driver.find_element_by_xpath('//div[@data-value="11"]').click()
    time.sleep(1)

    # add the selected size shoe to the shopping cart and then proceed to checkout
    driver.find_element_by_xpath('//button[@class="primary-btn add-to-cart"]').click()
    time.sleep(1)
    driver.find_element_by_xpath('//a[@class="btn btn-solid"]').click()
    time.sleep(1)

    # inputs shipping information and go to next page; country and state are completed by the website
    driver.find_element_by_xpath('//input[@placeholder="Email"]').send_keys('BubbaGump@gmail.com')
    time.sleep(0.2)
    driver.find_element_by_xpath('//input[@placeholder="First name"]').send_keys('Bubba')
    driver.find_element_by_xpath('//input[@placeholder="Last name"]').send_keys('Gump')
    time.sleep(0.2)
    driver.find_element_by_xpath('//input[@placeholder="Address"]').send_keys('8795 580th CT NE')
    driver.find_element_by_xpath('//input[@placeholder="Apartment, suite, etc. (optional)"]').send_keys('Unit 100')
    time.sleep(0.2)
    driver.find_element_by_xpath('//input[@placeholder="City"]').send_keys('Nomde')
    driver.find_element_by_xpath('//input[@placeholder="ZIP code"]').send_keys('98059')
    time.sleep(0.2)
    driver.find_element_by_xpath('//input[@placeholder="Phone (We\'ll only contact you regarding your order)"]') \
        .send_keys('12345678901')
    driver.find_element_by_xpath('//button[@type="submit"]').click()
    time.sleep(2)

    # go to next page if NOT choosing faster shipping OR adding a discount code/gift card
    driver.find_element_by_xpath('//button[@type="submit"]').click()
    time.sleep(4)

    # inputs payment information
    driver.find_element_by_xpath('//iframe[@title="Field container for: Card number"]').send_keys('4242')
    driver.find_element_by_xpath('//iframe[@title="Field container for: Card number"]').send_keys('4242')
    driver.find_element_by_xpath('//iframe[@title="Field container for: Card number"]').send_keys('4242')
    driver.find_element_by_xpath('//iframe[@title="Field container for: Card number"]').send_keys('4242')
    time.sleep(0.2)

    driver.find_element_by_xpath('//iframe[@title="Field container for: Name on card"]').send_keys('Bubba Gump')
    time.sleep(0.2)

    driver.find_element_by_xpath('//iframe[@title="Field container for: Expiration date (MM / YY)"]').send_keys(
        '09')
    driver.find_element_by_xpath('//iframe[@title="Field container for: Expiration date (MM / YY)"]').send_keys(
        '23')
    time.sleep(0.25)

    driver.find_element_by_xpath('//iframe[@title="Field container for: Security code"]').send_keys('321')
    time.sleep(0.25)

    # final order submit but in this case the order fails to complete due to fake information being provided
    driver.find_element_by_xpath('//button[@id="continue_button"]').click()
    time.sleep(10)

    driver.quit()

    # once everything is done a pop up box displays the message below
    messagebox.showinfo("Good News!", "Purchase complete, feel free to exit.")


# this function checks if an item is available through the specific Shopify-based e-commerce store (or not)
def check_availability():
    r = requests.get('https://www.featuresneakerboutique.com/products.json')

    items = json.loads(r.text)['products']

    for item in items:
        item_name = item['title']

        if item_name == 'Air Jordan 1 Mid SE - White/Cyber/Active Fuchsia/Black':
            item_url = 'https://www.featuresneakerboutique.com/products/' + item['handle']
            item_name_label.set("Item name: %s" % item_name)
            item_found_label.set("Item url: %s" % item_url)
            buy_stuff(item_url)

    return False


# close the program function
def client_exit():
    exit()


# setting up the visual interface
root = Tk()
root.title("Shopify Bot v0.1")
root.geometry("900x225")
root.configure(bg="gray")

# button (and it's attributes) to check if item is available / in stock
check_item_available = Button(text="1) Run Shopify Bot", fg="blue", command=check_availability)
check_item_available.place(x=25, y=25)

# initial labels to eventually display information about item / availability
item_name_label = tk.StringVar()
item_found_label = tk.StringVar()
item_name_label.set(" ")
item_found_label.set(" ")

# label displaying the item name
check_item_result_label = Label(textvariable=item_name_label, fg="green")
check_item_result_label.pack()
check_item_result_label.place(x=25, y=75)

# label displaying the item url
display_item_url = Label(textvariable=item_found_label, fg="green")
display_item_url.pack()
display_item_url.place(x=25, y=125)

# the Quit button and it's attributes
quit_button = Button(text="Quit Program", fg="red", command=client_exit)
quit_button.place(x=25, y=175)

root.mainloop()
