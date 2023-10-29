import keyboard
import os
import time
from colorama import init, Fore, Back, Style
import requests
from bs4 import BeautifulSoup

init(convert=True)

english = {}

current_dir = os.getcwd()
file_name = "English.txt"
file_path = os.path.join(current_dir, file_name)

try:
    with open(file_path, 'r', encoding="utf-8") as file:
        readalllines = file.readlines()
        for eachline in readalllines:
            spacefixed = eachline.replace(' : ', ': ')
            key, value = spacefixed.strip().split(':')
            english[key.capitalize()] = value[1:].capitalize()
except FileNotFoundError as e:
    print('File not found')
    time.sleep(1)
    exit()

# Copy dictionary
englishcop = english.copy()

# Function to scrape word meaning from dictionary.com
def scrape_word_meaning(wordtoask):
    url = f"https://www.dictionary.com/browse/{wordtoask}"
    response = requests.get(url)
    if response == 200:
        print('Connection to the website was successful.' + '')
    content = response.text
    soup = BeautifulSoup(content, 'html.parser')
    element = soup.find('div', class_="ESah86zaufmd2_YPdZtq")
    if element:
        word_meaning = element.find('p').text.strip()
        return word_meaning
    else:
        return "Word meaning not found."

# Call the function to add word and meaning to dictionary
def add_word_meaning_to_dictionary():
    while True:
        wordtoask = input('Please enter the word you would like to find its meaning => ')
        while wordtoask.capitalize() in englishcop.keys():
                print('The key already exists')
                wordtoask = input('Please enter the word you would like to find its meaning => ')
        word_meaning = scrape_word_meaning(wordtoask)
        if word_meaning != "Word meaning not found.":
                
            if ":" not in word_meaning:
                value = word_meaning
                key = wordtoask
                englishcop[key.capitalize()] = value.capitalize()
            elif ":" in word_meaning:
                value = word_meaning
                key = ''
                value, key = word_meaning.split(":")
                englishcop[wordtoask.capitalize()] = value.capitalize()
            
            print( f'({Fore.RED}{wordtoask.capitalize()}{Fore.RESET}) and its definition ({Fore.RED}{value.capitalize()}{Fore.RESET}) has been added to your dictionary.' + '\n' +'-------------------------(Pressing Right Shift will save and close the file)-------------------------')
        else:
            print("Word meaning not found.")

# Save dictionary to file
def save_dictionary():
    sorted_dict = dict(sorted(englishcop.items(), key=lambda x: x[0]))
    with open(file_path, 'w', encoding="utf-8") as file:
        for key, value in sorted_dict.items():
            file.write(key + ' : ' + value + '\n')
        print()
        print('File has been successfully saved.')
    print

# Register the hotkey to save the dictionary
keyboard.add_hotkey('right shift', save_dictionary)

# Call the function
add_word_meaning_to_dictionary()