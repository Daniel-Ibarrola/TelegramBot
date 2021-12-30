### Program to send messages to telegram using a bot

# Standard library
import datetime
import logging
import os
import queue
import re
import signal
import socket
import sys
import time
import threading
import tkinter as tk
import tkinter.scrolledtext as tkscrolled
# telegramBot
from bot.bot import telegramBot
from ftp.ftpserver import upload_file_to_ftp
import utils.utils as utils

## Uncomment this lines when creating the executable file.
if sys.frozen == "windows_exe":
    sys.stderr._error = "inhibit log creation"


# Connection status
counter = 2
connected = False
# FTP access info
user, password = utils.get_ftp_login_data()
# Other options
display_data = False
# Logging
logger = logging.getLogger(__name__)
# Data queue
data_queue = queue.Queue()

class QueueHandler(logging.Handler):
    """Class to send logging records to a queue.

    It can be used from different threads. The ConsoleUi class polls 
    this queue to display records in a ScrolledText widget.
    """

    def __init__(self, log_queue):
        super().__init__()
        self.log_queue = log_queue

    def emit(self, record):
        self.log_queue.put(record)

class ConsoleUi:
    """Poll messages from a logging queue and display them in a scrolled text widget"""

    def __init__(self, frame):
        self.frame = frame
        # Create a ScrolledText wdiget
        self.scrolled_text = tkscrolled.ScrolledText(master=frame, fg="#FFFCFC", bg="#1F1919")
        self.scrolled_text.grid(row=0, column=0, sticky="nsew")
        # Create a logging handler using a queue
        self.log_queue = queue.Queue()
        self.queue_handler = QueueHandler(self.log_queue)
        logger.addHandler(self.queue_handler)
        # Start polling messages from the queue
        self.frame.after(100, self.poll_log_queue)

    def display(self, record):
        msg = self.queue_handler.format(record)
        self.scrolled_text.configure(state='normal')
        self.scrolled_text.insert(tk.END, msg + '\n', record.levelname)
        self.scrolled_text.configure(state='disabled')
        # Autoscroll to the bottom
        self.scrolled_text.yview(tk.END)

    def poll_log_queue(self):
        """Checks every 100ms if there is a new message in the queue to display"""
        while True:
            try:
                record = self.log_queue.get(block=False)
            except queue.Empty:
                break
            else:
                self.display(record)
        self.frame.after(100, self.poll_log_queue)

class OptionsUi:
    """ Class that handles the checkbox button, and the status light."""

    def __init__(self, frame):
        self.frame = frame
        # Connection Status
        self.fr_connect = tk.Frame(master=self.frame,  bg="#4B7398")
        # Create a string variable to change label text
        self.status = tk.StringVar()
        self.status.set('Desconectado')
        self.lbl_connect = tk.Label(master=self.fr_connect, textvariable=self.status, bg="#4B7398")
        self.lbl_connect.config(font=("helvetica", 14, "bold"))
        self.canvas_connect = tk.Canvas(master=self.fr_connect, bg="#C91717", width=20, height=20, bd=0, highlightthickness=0)
        self.fr_connect.grid(row=0, column=0, pady=30)
        self.canvas_connect.pack(side=tk.LEFT, padx=5)
        self.lbl_connect.pack(side=tk.LEFT)
        # Checkbox button
        self.check_var = tk.IntVar(value=1)
        self.btn_text = tk.Checkbutton(master=self.frame, text="Ocultar Texto", variable=self.check_var,  bg="#4B7398", command=set_display)
        self.btn_text.grid(row=1, column=0, sticky="w")
        self.btn_text.config(font=("helvetica", 12))
        self.frame.grid(row=0, column=1, sticky="ns", pady=10)


    def recolor(self):
        """Change status and color depending if it is connected or not"""
        # green: #27BA0F
        # red: #C91717
        if self.status.get() == 'Conectado':
            self.status.set('Desconectado')
            self.canvas_connect.config(background='#C91717')
        elif self.status.get() == 'Desconectado':
            self.status.set('Conectado')
            self.canvas_connect.config(background='#27BA0F')

    def change_status(self):
        """Change status to connected after succesfully establishing a connection through the ip and port entrys"""
        self.status.set('Conectado')
        self.canvas_connect.config(background='#27BA0F')

    def blink(self):
        """Change the color of the box to simulate a blinking light"""
        self.canvas_connect.config(background='#4FFF32')
        time.sleep(1)
        self.canvas_connect.config(background='#27BA0F')


class App:
    """ Main class fot the GUI."""
    def __init__(self, root):
        self.root = root
        root.title("Envío Telegram 2.2.1")
        root.configure(background="#4B7398")
        root.rowconfigure(0, minsize=100, weight=1)
        root.columnconfigure(0, minsize=100, weight=1)
        root.columnconfigure(1, minsize=30, weight=1)
        # Frames
        fr_options = tk.Frame(master=root, bg="#4B7398")
        # Initialize all frames
        self.console = ConsoleUi(root)
        self.options = OptionsUi(fr_options)
        self.root.protocol('WM_DELETE_WINDOW', self.quit)
        self.root.bind('<Control-q>', self.quit)
        signal.signal(signal.SIGINT, self.quit)

    def change_color(self):
        self.options.recolor()

    def update_status(self):
        self.options.change_status()

    def blink(self):
        self.options.blink()

    def quit(self, *args):
        self.root.destroy()

def set_display():
    """Function to show/hide text to the console."""
    global display_data
    display_data = not display_data

def reconnect(ip, port):
    """Reconnect after changing IP and/or Port"""
    global client_socket
    global app
    global connected
    global counter
    global IP
    global PORT

    IP = ip
    PORT = port

    try:
        client_socket.shutdown(socket.SHUT_RDWR)
        client_socket.close()
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except:
        pass
    try:
        client_socket.connect((IP, PORT))
        logger.log(logging.INFO, f'Conectado a IP:{IP}\nPuerto:{PORT}')
        app.update_status()
        connected = True
        counter = 0
    except socket.error:
        logger.log(logging.INFO, f'No se pudo establecer la conexión\n')
        connected = False
        counter = 3

def send_message():
    """Sends  a message every 30 seconds"""
    message = 'Hola' + '\r\n'
    message = message.encode('utf-8')
    global connected
    global client_socket
    while True:
        try:
            client_socket.send(message)
            time.sleep(30)
        except:
            connected = False
            time.sleep(2)

def rcv_message():
    """ Receives data from the server and puts it in a queue."""
    global client_socket
    
    while True:
        try:
            data = client_socket.recv(512)

            if (len(data) < 1):
                time.sleep(2)
                continue
            
            data_queue.put(data)
          
        except:
            time.sleep(2)

def process_data():
    """ Process incoming data from the server. Sends messages and/or images according to
        the code recieved from the server. Also uploads a file to the ftp server if the 
        code to do so is received.

        The codes are the following:

        23,0 : indicates that a text message must be sent.
        23,1 : code to send an image (mapa racdmx).
        23,2 : code to send an image (mapa mex).
        23,3 : confirms the connection with the server
        23,4 : indicates that a .dat file is going to be written using incoming data
        23,5 : code to upload the .dat file to the ftp server. 
    """
    global client_socket
    global sending_image
    global counter
    global app
    global user
    global password
    global PORT
    
    writing_to_file = False
    message = '23,4,Recibido' + '\r\n'
    message = message.encode('utf-8')
    # Regular expression to find image paths
    while True:
        
        data = data_queue.get().decode()

        if display_data:
            logger.log(logging.INFO, data)

        if 'Hola' in data:
            counter = 0

        if '23,0,' in data:
            # Send Message
            msg = data.split('23,0,')[1]
            bot.send_message(msg, group_id)
            logger.log(logging.INFO, 'Mensaje enviado: ' + msg)

        if '23,1,' in data or '23,2,' in data:
            # Send an image
            path = utils.extract_path(data)
            try:
                bot.send_photo(path, group_id)
                if '23,1' in data:
                    logger.log(logging.INFO, 'Mapa RACDMX enviado por Telegram\n')
                else:
                    logger.log(logging.INFO, 'Mapa de sismo enviado por Telegram\n')
                counter = 0
            except Exception as e:
                if '23,1' in data:
                    logger.log(logging.WARNING, 'Falló envio de mapa RACDMX\n')
                else:
                    logger.log(logging.WARNING, 'Falló envio mapa de sismo enviado por Telegram')
                logger.log(logging.WARNING, e)


        if '23,3,' in data:
            # Confirm connection
            app.blink()

        if PORT == 13384:

            if '23,4,' in data and not writing_to_file:
                logger.log(logging.INFO, "Escribiendo Archivo...")
                writing_to_file = True
                line = data.split('23,4,')[1]
                line = line.rstrip()
                line += '\n'
                filename = datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + '.txt'
                file = open(filename, "w")
                file.write(line)
                client_socket.send(message)
                continue

            if '23,4,' in data and writing_to_file:
                line = data.split('23,4,')[1]
                line = line.rstrip()
                line += '\n'
                file.write(line)
                client_socket.send(message)

            if '23,5,' in data:
                logger.log(logging.INFO, data)
                new_filename = data.split('23,5,')[1]
                new_filename = new_filename.rstrip()
                file.close()
                os.rename(filename, new_filename)
                logger.log(logging.INFO, "Archivo completado\n")
                writing_to_file = False
                try:
                    upload_file_to_ftp(user, password, new_filename)
                    logger.log(logging.INFO, "Archivo subido con éxito")
                except Exception as e:
                    logger.log(logging.WARNING, e)
                    logger.log(logging.WARNING, "No se pudo subir el archivo")
      

def watch_dog():
    """ If conection is lost it reconnects. Also veryfies if threads are still alive. 
    
        Keeps track of the counter variable. If it passes a certain treshold, it raises an alert
    """
    global app
    global client_socket
    global connected
    global connection_failed
    global counter
    
    if not connection_failed:
        app.change_color()

    logger.log(logging.INFO, f'Puerto: {PORT}')
    logger.log(logging.INFO, f'Grupo: {group_name}\n')

    while True:
        # If it doesn't connect at start, try to connect again
        if connection_failed:
             while not connected:
                try:
                    client_socket.connect((IP, PORT))
                    logger.log(logging.INFO, 'Conexión exitosa')
                    connected = True
                    app.change_color()
                    break

                except socket.error:
                    time.sleep(2)

        if counter > 2 and not connected:
            app.change_color()
            now = datetime.datetime.now()
            alert_message = 'Se perdio la conexión!\nTiempo: {}'.format(now.strftime("%H:%M:%S"))
            logger.log(logging.WARNING, alert_message)
            counter = 0
            logger.log(logging.WARNING, '\nConexion perdida... reconectando')
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            while not connected:
                try:
                    client_socket.connect((IP, PORT))
                    logger.log(logging.INFO, 'Reconección exitosa')
                    connected = True
                    app.change_color()
                    break

                except socket.error:
                    time.sleep(2)

        time.sleep(30)
        counter += 1

        # Check if threads are alive
        if not t1.is_alive():
            logger.log(logging.WARNING, "Send message thread is dead")
        if not t2.is_alive():
            logger.log(logging.WARNING, "Rcv message thread is dead")
        if not t3.is_alive():
            logger.log(logging.WARNING, "Process data thread is dead")
        

def main():
    """ Main function. Starts the threads and the gui. 

        At the beginning it retrieves the port and group from argvs and instansiates
        the bot and the socket.

    """
    global app
    global bot
    global client_socket
    global connected
    global connection_failed
    global IP
    global PORT
    global group_id
    global group_name
    global t1, t2, t3
    
    # Socket variables
    IP = '127.0.0.1'
    group_name, group_id, bot_name, PORT = utils.get_group_port_and_bot(sys.argv)
    _, token = telegramBot.read_token(bot_name)

    bot = telegramBot(bot_name, token)
        
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((IP, PORT))
        connected = True
        connection_failed = False # Variable to know if the socket connected at the start of the program
    except:
        logger.log(logging.INFO, 'Error al conectarse')
        connection_failed = True
    
    logging.basicConfig(level=logging.INFO)
    root = tk.Tk()
    app = App(root)

    t1 = threading.Thread(target=send_message, daemon=True)
    t2 = threading.Thread(target=rcv_message, daemon=True)
    t3 = threading.Thread(target=process_data, daemon=True)
    t4 = threading.Thread(target=watch_dog, daemon=True)

    t1.start()
    t2.start()
    t3.start()
    t4.start()

    app.root.mainloop()
    sys.exit()


if __name__ == '__main__':
    main()
