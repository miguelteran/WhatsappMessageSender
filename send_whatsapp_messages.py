from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from urllib.parse import urlencode
import time
import os
import sys



WHATSAPP_URL = 'https://web.whatsapp.com'
WHATSAPP_SEND_URL = WHATSAPP_URL + '/send?{0}'

SEND_MESAGE_BUTTON_XPATH = '//*[@id="main"]/footer/div[1]/div[3]/button'
ATTACHMENT_BUTTON_XPATH = '//*[@id="main"]/footer/div[1]/div[1]/div[2]/div/div/span'
UPLOAD_IMAGE_BUTTON_XPATH = '//*[@id="main"]/footer/div[1]/div[1]/div[2]/div/span/div[1]/div/ul/li[1]/button/input'
SEND_IMAGE_BUTTON_XPATH = '//*[@id="app"]/div[1]/div[1]/div[2]/div[2]/span/div[1]/span/div[1]/div/div[2]/span/div'
INVALID_NUMBER_BUTTON_XPATH = '//*[@id="app"]/div[1]/span[2]/div[1]/span/div[1]/div/div/div/div/div[2]/div'

PHONE_NUMER_PARAM = 'phone'
TEXT_PARAM = 'text'


def print_usage():
    print('')
    print('Usage: python .\send_whatsapp_messages.py <message_file_path> <phone_numbers_file_path> {<image_path>}')
    print('')
    exit(0)
    

if __name__ == '__main__':
    
    args = sys.argv
    if len(args) < 3:
        print_usage()

    message_file_path = args[1].replace('\\', '\\\\')
    phone_numbers_file_path = args[2].replace('\\', '\\\\')
    image_path = ''
    if len(args) > 3:
        image_path = args[3].replace('\\', '\\\\')

    send_image = len(image_path) > 0

    if not os.path.isfile(message_file_path):
        print('Provided message file does not exist')
        exit(1)

    if not os.path.isfile(phone_numbers_file_path):
        print('Provided phone numbers file does not exist')
        exit(1)

    if send_image and not os.path.isfile(image_path):
        print('Provided image does not exist')
        exit(1)

    message = open(message_file_path, "r").readline().strip()
    phone_numbers = open(phone_numbers_file_path, "r")
    
    driver = webdriver.Chrome(executable_path="C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")
    driver.implicitly_wait(0.5)

    print('')
    print('Opening whatsapp in your browser...')
    print('')
    driver.get(WHATSAPP_URL)

    print('Scan QR code in your browser to login to whatsapp. Then return to this window and press Enter.')
    input()

    print('Sending messages...')
    print('')

    for number in phone_numbers:
        
        if len(number) > 0:
            number = number.strip()
            url_params = { PHONE_NUMER_PARAM: number, TEXT_PARAM: message}

            # Open window for sending message
            time.sleep(3)
            driver.get(WHATSAPP_SEND_URL.format(urlencode(url_params)))
            time.sleep(3)

            # Check for invalid phone number error in the UI
            invalid_number_button = driver.find_elements_by_xpath(INVALID_NUMBER_BUTTON_XPATH)
            if len(invalid_number_button) > 0:
                print('Invalid phone number {}. Skipping...'.format(number))
                invalid_number_button[0].click()
                continue
            
            try:
                print('Sending message to {}...'.format(number))
                if send_image:
                    # Need to click on upload image and upload it
                    attachment_button = driver.find_element_by_xpath(ATTACHMENT_BUTTON_XPATH)
                    attachment_button.click()
                    time.sleep(2)
                    upload_image_button = driver.find_element_by_xpath(UPLOAD_IMAGE_BUTTON_XPATH)
                    upload_image_button.send_keys(image_path)
                    time.sleep(2)
                    send_image_button = driver.find_element_by_xpath(SEND_IMAGE_BUTTON_XPATH)
                    send_image_button.click()
                else:
                    send_button = driver.find_element_by_xpath(SEND_MESAGE_BUTTON_XPATH)
                    send_button.click()
            
            except NoSuchElementException:
                print('An error occurred while sending message to number {}'.format(number))


    # TODO: generate report and tell user where it is
    time.sleep(3)
    print('')
    print('Finished sending messages.')
    print('')
    driver.quit()