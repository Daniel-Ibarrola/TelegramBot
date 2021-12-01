import tkinter as tk
import tkinter.scrolledtext as tkscrolled
import os
import threading
import queue
import time
import datetime
import logging
import socket
import signal
import sys
import re
from utils import get_ftp_login_data
from ftpserver import upload_file_to_ftp
from bot import telegramBot

# Socket variables
IP = '127.0.0.1'
try:
    PORT = int(sys.argv[1])
except:
    PORT = 13384

if PORT == 13385:
    bot = telegramBot.cires_bot()
else:
    bot = telegramBot.test_bot()

# Groups
groups = {
    '13384': ['RACM', -1001139087723],
    '13385': ['SASMEX', -467285177], 
    }
group_id = groups[str(PORT)][1]

# Connection status
counter = 2
connected = False
# FTP access info
user, pasword = get_ftp_login_data()
# Other options
display_data = False
# Logging
logger = logging.getLogger(__name__)

# if sys.frozen == "windows_exe":
#     sys.stderr._error = "inhibit log creation"

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
        # Check every 100ms if there is a new message in the queue to display
        while True:
            try:
                record = self.log_queue.get(block=False)
            except queue.Empty:
                break
            else:
                self.display(record)
        self.frame.after(100, self.poll_log_queue)

class OptionsUi:
    """ Class that handles the checkbox button, and thte status light."""

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

def set_group_id(port):
    """ Change the group id"""
    global group_id
    group_id = groups[str(port)][1]
    logger.log(logging.INFO, f'Grupo: {groups[str(port)][0]}')

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
    """Receives data from the server. If it recieves  15,5 alert, it downloads a file form ftp server,
        writes the data to a text file and sends a photo trough telegram"""
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
    while True:
        try:
            data = client_socket.recv(512)

            if (len(data) < 1):
                time.sleep(2)
                continue

            if display_data:
                logger.log(logging.INFO, data.decode())

            if 'Hola' in data.decode():
                counter = 0

            if '23,0,' in data.decode():
                # Send Message
                logger.log(logging.INFO, data.decode())
                msg = data.decode().split('23,0,')[1]
                # bot.send_message(msg, group_id)
                bot.send_message(msg, -373994761)
                logger.log(logging.INFO, 'Mensaje enviado: ' + msg)

            if '23,1,' in data.decode():
                # Send image 1
                logger.log(logging.INFO, data.decode())
                path = data.decode().split('23,1,')[1]
                path = re.search(pattern, path)
                logger.log(logging.INFO, path)
                try:
                    bot.send_photo(path, -373994761)
                    logger.log(logging.INFO, 'Imagen 1 enviada por Telegram\n')
                    counter = 0
                except Exception as e:
                    logger.log(logging.INFO, "No se pudo enviar la primer imagen\n")
                    logger.log(logging.INFO, e)

            if '23,2,' in data.decode():
                # Send image 2
                print(data.decode())
                path = data.decode().split('23,2,')[1]
                path = re.search(pattern, path)
                logger.log(logging.INFO, path)
                try:
                    bot.send_photo(path, -373994761)
                    logger.log(logging.INFO, 'Imagen 2 enviada por Telegram\n')
                    counter = 0
                except:
                    logger.log(logging.INFO, "No se pudo enviar la segunda imagen\n")

            if '23,3,' in data.decode():
                # Confirm connection
                app.blink()

            if PORT == 13384:

                if '23,4,' in data.decode() and not writing_to_file:
                    logger.log(logging.INFO, "Escribiendo Archivo...")
                    writing_to_file = True
                    line = data.decode().split('23,4,')[1]
                    line = line.rstrip()
                    line += '\n'
                    filename = datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + '.txt'
                    file = open(filename, "w")
                    file.write(line)
                    client_socket.send(message)
                    continue

                if '23,4,' in data.decode() and writing_to_file:
                    line = data.decode().split('23,4,')[1]
                    line = line.rstrip()
                    line += '\n'
                    file.write(line)
                    client_socket.send(message)

                if '23,5,' in data.decode():
                    logger.log(logging.INFO, data.decode())
                    new_filename = data.decode().split('23,5,')[1]
                    new_filename = new_filename.rstrip()
                    file.close()
                    os.rename(filename, new_filename)
                    logger.log(logging.INFO, "Archivo completado\n")
                    writing_to_file = False
                    try:
                        # upload_file_to_ftp(user, password, new_filename)
                        logger.log(logging.INFO, "Archivo subido con éxito")
                    except Exception as e:
                        logger.log(logging.INFO, e)
                        logger.log(logging.INFO, "No se pudo subir el archivo")
        except:
            time.sleep(2)

def watch_dog():
    """Keeps track of the counter variable. If it passes a certain treshold, it raises an alert"""
    global counter
    global connected
    global app
    global connection_failed
    global client_socket

    if not connection_failed:
        app.change_color()

    # logger.log(logging.INFO, f'IP: {IP}')
    logger.log(logging.INFO, f'Id: {PORT}\n')
    logger.log(logging.INFO, f'Grupo: {groups[str(PORT)][0]}\n')

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
            # print('Contador mayor a 2')
            app.change_color()
            now = datetime.datetime.now()
            alert_message = 'Se perdio la conexión!\nTiempo: {}'.format(now.strftime("%H:%M:%S"))
            logger.log(logging.INFO, alert_message)
            counter = 0
            logger.log(logging.INFO, '\nConexion perdida... reconectando')
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
        print(counter)

def main():
    global app
    global connected
    global connection_failed
    
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

    t1 = threading.Thread(target=send_message)
    t2 = threading.Thread(target=rcv_message)
    t3 = threading.Thread(target=watch_dog)

    t1.daemon = True
    t2.daemon = True
    t3.daemon = True

    t1.start()
    t2.start()
    t3.start()

    app.root.mainloop()
    sys.exit()


if __name__ == '__main__':
    main()
