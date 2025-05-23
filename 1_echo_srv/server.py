import socket
import datetime

def get_port(default_port):
    while True:
        port_str = input(f"Введите номер порта для сервера (по умолчанию {default_port}): ").strip()
        if not port_str:
            return default_port
        try:
            port = int(port_str)
            if 0 <= port <= 65535:
                return port
            else:
                print(f"Ошибка: Порт должен быть от 0 до 65535. Используется порт по умолчанию {default_port}.")
                return default_port
        except ValueError:
            print("Ошибка: Введите корректное число для порта.")

def log(message, log_file):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] СЕРВЕР: {message}\n"
    try:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(log_entry)
    except Exception as e:
        print(f"Ошибка записи в лог-файл: {e}")

log_file = "server.log"
default_port = 9090
port = get_port(default_port)
current_port = port

sock = socket.socket()

# Автоматический поиск свободного порта
while current_port <= 65535:
    try:
        sock.bind(('', current_port))
        print(f"СЕРВЕР: Используется порт {current_port}")  # Консольный вывод
        log(f"Сокет привязан к порту {current_port}.", log_file)
        break
    except OSError:
        log(f"Порт {current_port} занят, пробуем следующий...", log_file)
        current_port += 1
else:
    log("Нет свободных портов в диапазоне 9090-65535", log_file)
    print("СЕРВЕР: Нет свободных портов в диапазоне 9090-65535")
    exit()

sock.listen(0)
log("Начало прослушивания входящих подключений.", log_file)

shutdown_requested = False
while not shutdown_requested:
    conn, addr = sock.accept()
    log(f"Подключился клиент с адресом {addr}.", log_file)
    msg = ''
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                log("Клиент прекратил отправку данных или отключился.", log_file)
                break
            decoded_data = data.decode().strip().lower()
            log(f"Получена порция данных: {decoded_data}", log_file)
            if decoded_data == "shutdown":
                conn.send(b"Server shutting down...")
                shutdown_requested = True
                break
            msg += " " + decoded_data
            conn.send(data)
        log(f"Полное сообщение от клиента: {msg}", log_file)
    except ConnectionResetError:
        log(f"Клиент {addr} отключился неожиданно.", log_file)
    finally:
        conn.close()
        log(f"Соединение с {addr} закрыто.", log_file)

sock.close()
log("Остановка сервера. Работа завершена.", log_file)