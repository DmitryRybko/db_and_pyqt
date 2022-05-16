import subprocess

client_qty = int(input("Введите количество клиентов:"))
subprocess.call("start python server.py", shell=True)

for item in range(client_qty+1):
    subprocess.call("start python client.py", shell=True)

