# Importando os módulos
import datetime
import sys
import os
import time
import json
import locale
import pyttsx3
import speech_recognition as sr
from PyQt5.QtCore import QThread, QCoreApplication, Qt 
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QScrollArea, QLabel, QPushButton,
    QFileDialog
)
from PyQt5.QtGui import QIcon, QFont, QMovie
import requests
import pyautogui
import webbrowser
from STOP import main2 
from Tictactoe2 import main
from patterns_and_responses import propt, times1, reminder_phrases, weather_queries, speech_off
import random
import pywhatkit
import subprocess

from groq import Groq

# Passe a chave da API diretamente
client = Groq(
    api_key="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",
)

recognizer = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('rate', 175)
voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
engine.setProperty('voice', voice_id)

now = datetime.datetime.now()
if now.hour < 12:
    greeting = 'Good morning'
elif now.hour < 18:
    greeting = 'Good afternoon'
else:
    greeting = 'Good night'

user_home = 'United States of America'
siblings = 'Cálita and Guilherme'
best_friend = 'Weveton'
favorite_color = 'blue'

current_date = datetime.datetime.now()
day = current_date.day
month = current_date.month
year = current_date.year
locale.setlocale(locale.LC_ALL, 'en_US.utf8')
current_date = datetime.datetime.now()
day_of_week = current_date.strftime("%A")
birthday = datetime.datetime(2008, 7, 6).date()
next_birthday = datetime.date(current_date.year, birthday.month, birthday.day)
birth_date = datetime.datetime(2008, 7, 6)
age = current_date.year - birth_date.year

if (current_date.month, current_date.day) < (birth_date.month, birth_date.day):
    age -= 1


def get_current_season():
    now = datetime.datetime.now()
    month1 = now.month
    if 3 <= month1 <= 5:
        return 'spring'
    elif 6 <= month1 <= 8:
        return 'summer'
    elif 9 <= month1 <= 11:
        return 'autumn'
    else:
        return 'winter'
    
conversation_history = []

def get_previous_conversation():
    return conversation_history

user_data_file = 'user_data.json'

if os.path.exists(user_data_file):
    with open(user_data_file, 'r') as file:
        user_data = json.load(file)
        user_name = user_data.get('user_name', '')
else:
    user_name = "User"


#some predefined commands
class CommandProcessorThread(QThread):
    def __init__(self, message_label):
        self.conversation_history = []
        super().__init__()
        self.message_label = message_label   
        self.context = {'last_question': '', 'last_command': ''}

    def run(self):
        global app
        while True:
            self.update_label_text('Listening...')

            command = self.listen_for_command()

            if command:
                conversation_history.append(f"You: {command}")

            if any(keyword in command for keyword in times1):
                current_time = datetime.datetime.now().time()
                new_time = current_time.strftime("%I:%M %p")
                self.speak_response('The current time is ' + new_time)
                time.sleep(2)    

            if 'close the program' in command or 'end the program' in command or 'stop the program' in command or 'shutdown the program' in command or 'quit the program' in command or 'sleep' in command or 'shut down' in command:
                response = 'Closing the program...'
                self.speak(response)
                self.update_label_text(response)
                app.quit()
            
            elif any(keyword in command for keyword in weather_queries):
                    api_key = '2817980ed8b96c10646184775f6a6ff7'
                    base_url = 'http://api.openweathermap.org/data/2.5/weather?'
                    city_name = 'Boston,Massachusetts,USA'
                    complete_url = base_url + 'appid=' + api_key + '&q=' + city_name
                    response = requests.get(complete_url)
                    data = response.json()
                    current_temperature = round(data['main']['temp'] - 273.15, 1 )
                    weather_description = data['weather'][0]['description']
                    weather_message = f"The approximate temperature is  {current_temperature} degrees and the weather is {weather_description}"
                    print(weather_message)
                    engine.say(weather_message)
                    engine.runAndWait()
                    self.message_label.setText(weather_message)
                    time.sleep(5)

            elif 'movies for free' in command or 'movies website' in command:
               url = "https://onionplay.se/"
               webbrowser.open(url)
               engine.say(f"Opeinig the the website for free movie, please look at the screen.{url}")
               engine.runAndWait()
               time.sleep(2)   

            elif 'news' in command:
               articles = get_news()
               news_text = "Here are the latest news headlines:\n\n"
               for article in articles:
                   title = article['title']
                   description = article['description']
                   news_text += f"{title}: {description}\n\n"
               engine.say(news_text)
               self.update_label_text(news_text)
               engine.runAndWait()

            elif 'date' in command:
               if 'what is today date' in command:
                   texto = command.replace('what is today date', '').strip()
               elif 'what is today date' in command:
                   texto = command.replace('what is today date', '').strip()
               else:
                   texto = ''
                   engine.say(f"Today's date {day}, month {month} and year {year}")
                   print(f"Today's date {day}, month {month} and year {year}")
                   texto = f"Today's date {day}, month {month} and year {year}"
                   self.update_label_text(texto)
                   engine.runAndWait()
                   time.sleep(2)

            elif 'season' in command or 'seasons' in command:
               estacao_atual = get_current_season()
               mensagem = f"We are  {estacao_atual}."
               engine.say(mensagem)
               self.update_label_text(mensagem)
               engine.runAndWait()
               time.sleep( 5 )

            elif 'day is' in command:
               if 'what day is today' in command:
                   texto = command.replace('what day is today', '').strip()
               elif 'what day is today' in command:
                   texto = command.replace('what day is today', '').strip()
               else:
                   texto = ''
                   engine.say(f"Today is {day_of_week}")
                   print(f"Today is {day_of_week}")
                   texto = f"today is {day_of_week}"
                   self.update_label_text(texto)
                   engine.runAndWait()
                   time.sleep( 5 )

            elif 'birthday' in command:
               text = ''
               if 'my' in command:
                   birthday_date = datetime.datetime(current_date.year, 7, 6)
                   if birthday_date < current_date:
                      birthday_date = datetime.datetime(current_date.year + 1, 7, 6)
                   days_left = (birthday_date - current_date).days
                   text = f"Your birthday will be on {birthday_date.strftime('%B')} {birthday_date.day}, {birthday_date.year}. There are {days_left} days left."
               elif 'your' in command:
                   text = "Sorry, I can't reveal my birthdate."
               else:
                   text = "Sorry, I didn't understand the birthday question."
               engine.say(text)
               print(text)
               engine.runAndWait()
               self.update_label_text(text)
               time.sleep(5)

            elif 'my birth' in command:
               if 'tell me date of my birth when i born' in command:
                   texto = command.replace('tell me date of my birth when i born', '').strip()
               elif 'tell me date of my birth when i born' in command:
                   texto = command.replace('tell me date of my birth when i born', '').strip()
               else:
                   texto = ''
                   engine.say(f"You born on day {birthday.day} of {birthday.strftime('%B')} of {birthday.year}")
                   print(f"You born on day{birthday.day} of {birthday.strftime('%B')} of {birthday.year}")
                   texto = f"You born on day {birthday.day} of {birthday.strftime('%B')} of {birthday.year}"
                   self.update_label_text(texto)
                   engine.runAndWait()
                   time.sleep(5)    

            elif "let's do search" in command:
                self.speak("Okay, do you want to search on Google or on Wikipedia?")
                self.update_label_text("Okay, do you want to search on Google or on Wikipedia?")
                user_response = self.listen_for_command()

                if 'google' in user_response:
                    search_term = command
                    google_search_url = f"https://www.google.com/search?q={search_term}"
                    webbrowser.open(google_search_url)
                    self.speak(f"Please look at the screen for what I found on Google about '{search_term}'.")
                    self.update_label_text(f"Please look at the screen for what I found on Google about '{search_term}'.")
                    time.sleep(2)
                elif 'wikipedia' in user_response or 'search on wikipedia' in user_response:
                    self.ask_wikipedia_search(command)
                else:
                    self.speak("I didn't understand your choice. Please specify Google or Wikipedia.")
                    self.update_label_text("I didn't understand your choice. Please specify Google or Wikipedia.")
                    time.sleep(3)    

            elif any(x in command for x in ['play a video', 'open a video', 'play a song', 'open a song']):
               if 'play a video' in command or 'open a video' in command or 'play a song' in command or 'open a song' in command:
                   song = command.replace('play a video', '').replace('open a video', '').strip().replace('play a song', '').strip().replace('open a song', '').strip()
               elif 'open' in command:
                   song = command.replace('open', '')
               pywhatkit.playonyt(song)
               engine.say(f"Opening {song}")
               engine.runAndWait()

               text = f"Opening {song}"
               self.update_label_text(text)
               time.sleep(2)

            elif 'google chrome' in command:
               chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
               subprocess.Popen( [chrome_path] )
               mensagems = "Abrindo o Google Chrome..."
               self.label_mensagem.setText( mensagems )
               time.sleep( 5 )    

            elif 'microsoft store' in command:
               subprocess.Popen( ['explorer', 'shell:AppsFolder\Microsoft.WindowsStore_8wekyb3d8bbwe!App'] )
               mensagems = "Opening microsoft store.."
               self.update_label_text( mensagems )
               time.sleep( 5 )

            elif 'fie explorer' in command:
               subprocess.Popen( ['explorer'] )
               mensagems = "Opening file explorer"
               self.update_label_text( mensagems )
               time.sleep( 5 )

            elif 'pc settings' in command:
               subprocess.Popen( ['explorer', 'shell:::{BB06C0E4-D293-4f75-8A90-CB05B6477EEE}'] )
               mensagems = "Opening the pc settings..."
               self.update_label_text( mensagems )
               time.sleep( 2 )

            elif 'settings' in command:
               os.startfile( 'ms-settings:' )
               mensagems = "Opening settings.."
               self.update_label_text( mensagems )

            elif 'whatsapp' in command:
               pywhatkit.search( "WhatsApp desktop" )
               mensagems = "Opening the WhatsApp..."
               self.update_label_text( mensagems )
               time.sleep( 2 )    

            elif "restart the computer" in command or 'reboot the computer' in command or 'restart the PC' in command:
               print("Restarting the computer...")
               engine.say("Restarting the computer...")
               engine.runAndWait()
               self.update_label_text("Restarting the computer...")
               subprocess.call(["shutdown", "-r"])    
               
            elif 'turn off the computer' in command or 'turn off my computer' in command:
               print('turning off...' )
               engine.say( 'turning off...' )
               engine.runAndWait()
               self.update_label_text( 'turning off...' )
               subprocess.call( ['shutdown', '-s'] )

            elif 'shut off' in command:
                engine.say("Do you want me to turn off the computer or the program?")   
                print("Do you want me to turn off the computer or the program?")
                self.update_label_text("Do you want me to turn off the computer or the program?")
                engine.runAndWait()

                r = sr.Recognizer()
                with sr.Microphone() as source:
                       audio = r.listen(source)

                try:
                    answer = r.recognize_google( audio, language='en-US' )
                    if 'computer' in answer:
                        print('turning off...' )
                        engine.say( 'turning off...' )
                        engine.runAndWait()
                        self.update_label_text( 'turning off...' )
                        subprocess.call( ['shutdown', '-s'] )
                    elif 'program' in answer:
                        response = 'Closing the program...'
                        self.speak(response)
                        self.update_label_text(response)
                        app.quit()
                    else:
                        engine.say("I didn't understand you. Please say in the correct way")    
                        self.speak("I didn't understand you. Please say in the correct way")
                        self.update_label_text("I didn't understand you. Please say in the correct way")
                        time.sleep(3)
                        engine.runAndWait()

                except sr.UnknownValueError:
                       print( "I couldn't understand you" )
                       texto = "I couldn't understand you"
                       self.update_label_text( texto )   
                       time.sleep(3)     

            elif any(keyword in command for keyword in reminder_phrases):
               engine.say("you can add you reminder using this app. Can you please look at the screen!")
               print("You can add you reminder using this app. Can you please look at the screen!")
               self.update_label_text("You can add you reminder using this app. Can you please look at the screen!")
               import Reminder  
               Reminder.main()
               time.sleep(3)
               engine.runAndWait()  

            elif any(keyword in command for keyword in speech_off):
                self.speak_response("I will enter in the silence mode")
                if __name__ == "__main__":
                   main2()


            elif 'play game' in command or 'hash' in command or 'play a game' in command or 'tictactoe' in command or 'game' in command:
                print("Let's play tic-tac-toe")
                engine.say("Let's play tic-tac-toe")
                self.update_label_text("Let's play tic-tac-toe")
                engine.runAndWait()
                time.sleep(1)
                if __name__ == "__main__":
                   main()    

            else:
                self.generate_response(command)

#speak function
    @staticmethod
    def speak(text):
        engine.say(text)
        engine.runAndWait()
#listen function
    @staticmethod
    def listen_for_command():
        try:
            with sr.Microphone() as source:
                audio = recognizer.listen(source)
                command = recognizer.recognize_google(audio, language='en-US').lower()
                print(f"User said: {command}")
                return command
        except sr.UnknownValueError:
            print('Unable to recognize speech')
            return CommandProcessorThread.listen_for_command()
        except sr.RequestError as e:
            print(f'Unable to connect to speech recognition service: {e}')
            return "I'm sorry, I couldn't connect to the speech recognition service."

    def update_label_text(self, text):
        self.typewrite_animation(text)
        self.message_label.setText(text)

    def typewrite_animation(self, text):
        delay_between_chars = 10
        current_text = ""
        for char in text:
            current_text += char
            self.message_label.setText(current_text)
            QCoreApplication.processEvents() 
            time.sleep(delay_between_chars / 1000.0)


    def generate_response(self, command):
        self.conversation_history.append(command)
        context = "\n".join(self.conversation_history)
        prompt = f"{propt} {user_name}:\n{context}"
        response_text = get_groq_response(prompt)
        print(response_text)
        self.conversation_history.append(response_text)
        self.save_conversation(command, response_text)
        self.save_conversation_to_json()
        self.speak_response(response_text)


    def save_conversation(self, question, answer):
        if not hasattr(self, 'conversation_history'):
            self.conversation_history = []

        if any(f'You: {question}' in item for item in self.conversation_history) and any(f'AI: {answer}' in item for item in self.conversation_history):
            return

        self.conversation_history.append(f'You: {question}')
        self.conversation_history.append(f'AI: {answer}')

    def save_conversation_to_json(self):
        conversation_list = []
        try:
            with open('conversation_history.json', 'r') as file:
                conversation_list = json.load(file)
        except FileNotFoundError:
            pass

        for i in range(0, len(self.conversation_history), 2):
            question = self.conversation_history[i].replace('You: ', '').strip()
            answer = self.conversation_history[i + 1].replace('AI: ', '').strip()
            conversation_list.append({"question": question, "answer": answer})

        with open('conversation_history.json', 'w') as file:
            json.dump(conversation_list, file, indent=2)

    def speak_response(self, response_text):
        engine.say(response_text)
        print(f"AI: {response_text}")
        self.update_label_text(response_text)
        engine.runAndWait()
        time.sleep(2)


def get_groq_response(prompt):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "your name is Delta",
            },
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama-3.2-90b-vision-preview",
    )
    return chat_completion.choices[0].message.content

def get_news():
    api_key = '43b8a7b79970495d92e58b2e8e70829d'
    url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}'
    response = requests.get(url)
    data = response.json()
    articles = data['articles']
    return articles


#Virtual Assistant GUI
class VirtualAssistant(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Delta AI assistant')
        self.setGeometry(100, 100, 400, 700)
        self.setWindowIcon(QIcon(r"C:\MyFiles\DeltaAI1\UI5.jpg"))

        # Tornando a janela um pouco transparente
        self.setWindowOpacity(0.7)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)

        # Ajustando a folha de estilo para uma cor mais transparente
        self.setStyleSheet("background-color: rgba(0, 0, 0, 200);")

        self.message_scroll_area = QScrollArea(self)
        self.message_scroll_area.setGeometry(10, 60, 380, 400)
        self.message_scroll_area.setWidgetResizable(True)

        self.message_label = QLabel(self.message_scroll_area)
        self.message_label.setFont(QFont('Arial', 16))
        self.message_label.setStyleSheet(
            "background-color: rgba(0, 0, 0, 150); color: #FFFFFF; margin-bottom: 20px; padding: 10px; border-radius: 5px;")

        self.gif_label = QLabel(self)
        self.gif_label.setGeometry(10, 10, 100, 100)
        self.load_gif(r"C:\MyFiles\DeltaAI1\gif5.gif")

        self.message_scroll_area.setWidget(self.message_label)

        button_layout = QVBoxLayout()

        self.button_listen_continuous = QPushButton('Listen', self)
        self.button_listen_continuous.setStyleSheet(
            "background-color: rgba(0, 0, 0, 150); color: #FFFFFF; padding: 10px 20px; font-size: 14px; border: none; border-radius: 5px;")

        self.button_lock_screen = QPushButton('Lock Screen', self)
        self.button_lock_screen.setStyleSheet(
            "background-color: rgba(0, 0, 0, 150); color: #FFFFFF; padding: 10px 20px; font-size: 14px; border: none; border-radius: 5px;")

        self.button_screenshot = QPushButton('Screenshot', self)
        self.button_screenshot.setStyleSheet(
            "background-color: rgba(0, 0, 0, 150); color: #FFFFFF; padding: 10px 20px; font-size: 14px; border: none; border-radius: 5px;")

        self.button_close = QPushButton('Close', self)
        self.button_close.setStyleSheet(
            "background-color: rgba(0, 0, 0, 150); color: #FFFFFF; padding: 10px 20px; font-size: 14px; border: none; border-radius: 5px;")

        button_layout.addWidget(self.button_listen_continuous)
        button_layout.addWidget(self.button_lock_screen)
        button_layout.addWidget(self.button_screenshot)
        button_layout.addWidget(self.button_close)

        layout = QVBoxLayout(self)
        layout.addWidget(self.message_scroll_area)
        layout.addWidget(self.gif_label)
        layout.addLayout(button_layout)

        self.button_listen_continuous.clicked.connect(self.toggle_continuous_listening)
        self.button_lock_screen.clicked.connect(self.lock_screen)
        self.button_screenshot.clicked.connect(self.take_screenshot)
        self.button_close.clicked.connect(QApplication.quit)

        self.command_processor = CommandProcessorThread(self.message_label)

        self.is_listening_continuous = False

        self.show() 

        self.initialize()

    def initialize(self):
        self.init_virtual_assistant()

    def toggle_continuous_listening(self):
        self.button_listen_continuous.setText('listening')

    def typewrite_animation(self, text):
        delay_between_chars = 25
        current_text = ""
        for char in text:
            current_text += char
            self.message_label.setText(current_text)
            QCoreApplication.processEvents()
            time.sleep(delay_between_chars / 1000.0)

    def lock_screen(self):
        lock_screen_command = "rundll32.exe user32.dll,LockWorkStation"
        subprocess.run(lock_screen_command, shell=True)
        self.command_processor.speak("Screen locked.")

    def init_virtual_assistant(self):
        greetings = ["How can I assist you today?",
                     "How are you?",
                     "Welcome back, how can I help you?",
                     "How's your day going?",
                     "Good to see you again! How can I be of service?",
                     "Hello there! What can I do for you today?",
                     "Hi, it's great to have you here. How can I assist you?",
                     "Hey, how's everything going? How can I assist you today?",
                     "Welcome! How may I assist you with your needs?"]

        new_greeting = random.choice(greetings)
        self.message_label.setWordWrap(True)

        user_data_file = 'user_data.json'

        if os.path.exists(user_data_file):
            with open(user_data_file, 'r') as file:
                user_data = json.load(file)
                user_name = user_data.get('user_name', '')

            if user_name:
                if day == birth_date.day and month == birth_date.month:
                    birthday_message = "Happy birthday!"
                    messages = f"{greeting} {user_name}, {birthday_message} {new_greeting}"
                    self.command_processor.speak(messages)
                    self.update_message(messages)
                    time.sleep(2)
                else:
                    messages = f"{greeting} {user_name}, {new_greeting}"
                    self.command_processor.speak(messages)
                    self.update_message(messages)
                    time.sleep(2)
                    self.is_listening_continuous = True
                    self.command_processor.start()
            else:
                messages1 = "I was not able to identify your name, can you please tell me your name?"
                self.command_processor.speak(messages1)
                self.update_message(messages1)

                self.listen_for_name()
        else:
            messages1 = "I was not able to identify your name, can you please tell me your name?"
            self.command_processor.speak(messages1)
            self.update_message(messages1)

            self.listen_for_name()

    def listen_for_name(self):
        try:
            with sr.Microphone() as source:
                audio = recognizer.listen(source)
                name_response = recognizer.recognize_google(audio, language='en-US')
            name = name_response.split()[-1]
            messages = f"Hi {name}, nice to meet you! If your name is incorrect, feel free to let me know so I can change it."
            self.update_message(messages)
            self.command_processor.speak(messages)
            time.sleep(1)
            self.is_listening_continuous = True
            self.command_processor.start()

            with open('user_data.json', 'w') as file:
                json.dump({'user_name': name}, file)

        except sr.UnknownValueError:
            self.update_message("Sorry, I was not able to recognizer your name. Can you please say it again?")
            self.command_processor.speak("Sorry, I was not able to recognizer your name. Can you please say it again?")
            time.sleep(1)
            self.listen_for_name()

        except sr.RequestError as e:
            self.update_message(f"Error when making a request to the speech recognition service; {e}")

        self.message_label.setWordWrap(True)

    def update_message(self, messages):
        self.typewrite_animation(messages)
        self.message_label.setText(messages)

    def take_screenshot(self):
        screenshot_path, _ = QFileDialog.getSaveFileName(None, "Save Screenshot", "", "Images (*.png *.jpg *.bmp *.tiff)")
        if screenshot_path:
            pyautogui.screenshot(screenshot_path)
            self.update_message(f"Screenshot saved to: {screenshot_path}")

    def load_gif(self, path):
        movie = QMovie(path)
        self.gif_label.setMovie(movie)
        movie.start()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    assistant = VirtualAssistant()
    sys.exit(app.exec_())
    
