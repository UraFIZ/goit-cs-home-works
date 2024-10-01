import os
import socket
import json
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
import threading

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class MainHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        logging.info(f"GET запит на шлях: {self.path}")
        if self.path == '/':
            self.send_file('index.html', 'text/html')
        elif self.path == '/message.html':
            self.send_file('message.html', 'text/html')
        elif self.path == '/style.css':
            self.send_file('style.css', 'text/css')
        elif self.path == '/logo.png':
            self.send_file('logo.png', 'image/png')
        else:
            logging.info(f"Файл не знайдено: {self.path}")
            self.send_error(404, 'Not Found')
            self.send_file('error.html', 'text/html')

    def send_file(self, filename, content_type):
        try:
            self.send_response(200)
            self.send_header('Content-type', content_type)
            self.end_headers()
            with open(os.path.join('client', filename), 'rb') as file:
                self.wfile.write(file.read())
            logging.info(f"Файл надіслано: {filename}")
        except FileNotFoundError:
            logging.info(f"Файл не знайдено: {filename}")
            self.send_error(404, 'File Not Found')

    def do_POST(self):
        logging.info("Отримано POST запит")
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        logging.info(f"Отримані POST дані: {post_data}")
        data = parse_qs(post_data)
        logging.info(f"Розпарсені дані: {data}")
        
        message = {
            "username": data.get('username', [''])[0],
            "message": data.get('message', [''])[0]
        }
        logging.info(f"Сформоване повідомлення: {message}")
        
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            logging.info("Відправка повідомлення на Socket сервер")
            sock.sendto(json.dumps(message).encode(), ('socket_server', 5000))
            logging.info("Повідомлення відправлено")
        
        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()
        logging.info("Відправлено редірект на головну сторінку")

def run_http_server(server_class=HTTPServer, handler_class=MainHandler, port=3000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info(f'Запуск HTTP сервера на порту {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    http_thread = threading.Thread(target=run_http_server)
    http_thread.start()
    logging.info("HTTP сервер запущено в окремому потоці")
    http_thread.join()