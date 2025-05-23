import socket

def get_host(default_host):
    host = input(f"Введите имя хоста (по умолчанию '{default_host}'): ").strip()
    return host or default_host

def get_port(default_port):
    while True:
        port_str = input(f"Введите номер порта (по умолчанию {default_port}): ").strip()
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

sock = socket.socket()
sock.setblocking(1)

default_host = 'localhost'
default_port = 9090

host = get_host(default_host)
port = get_port(default_port)

print(f"КЛИЕНТ: Попытка соединения с сервером на адресе {host}:{port}...")
try:
    sock.connect((host, port))
    print("КЛИЕНТ: Соединение с сервером установлено.")
except Exception as e:
    print(f"КЛИЕНТ: Ошибка подключения: {e}")
    exit()

while True:
    msg = input("Введите строку для отправки серверу: ")
    if msg == "exit":
        sock.close()
        print("КЛИЕНТ: Соединение с сервером закрыто.")
        break
    print("КЛИЕНТ: Отправка данных серверу...")
    sock.send(msg.encode())
    print("КЛИЕНТ: Данные успешно отправлены серверу.")
    print("КЛИЕНТ: Ожидание ответа от сервера...")
    data = sock.recv(1024)
    print("КЛИЕНТ: Данные получены от сервера.")
    print("Ответ от сервера:", data.decode())
    if msg == "shutdown":
        sock.close()
        print("КЛИЕНТ: Соединение с сервером закрыто.")
        break