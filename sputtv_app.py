import sqlite3
import tkinter as tk
from tkinter import messagebox
from flask import Flask, request, jsonify
import threading

# --- Создаем Flask-сервер ---
app = Flask(__name__)

# База данных SQLite
conn = sqlite3.connect('sputtv.db', check_same_thread=False)
cursor = conn.cursor()

# Таблица для хранения заявок
cursor.execute('''
CREATE TABLE IF NOT EXISTS requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message TEXT NOT NULL,
    contact_number TEXT NOT NULL,
    address TEXT NOT NULL
)
''')
conn.commit()

# API для получения заявок
@app.route('/api/requests', methods=['GET'])
def get_requests():
    cursor.execute('SELECT id, message, contact_number, address FROM requests')
    data = cursor.fetchall()
    return jsonify(data)

# API для добавления заявки
@app.route('/api/requests', methods=['POST'])
def add_request_api():
    data = request.json
    message = data.get('message')
    contact_number = data.get('contact_number')
    address = data.get('address')

    if not message or not contact_number or not address:
        return jsonify({"error": "Все поля обязательны"}), 400

    cursor.execute('INSERT INTO requests (message, contact_number, address) VALUES (?, ?, ?)',
                   (message, contact_number, address))
    conn.commit()
    return jsonify({"success": True, "message": "Заявка добавлена"}), 201

# Функция для запуска Flask-сервера в отдельном потоке
def start_server():
    app.run(port=5000)

# --- GUI Приложение ---
def add_request_gui():
    message = message_entry.get()
    contact_number = contact_entry.get()
    address = address_entry.get()

    if not message or not contact_number or not address:
        messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
        return

    cursor.execute('INSERT INTO requests (message, contact_number, address) VALUES (?, ?, ?)',
                   (message, contact_number, address))
    conn.commit()
    messagebox.showinfo("Успех", "Заявка добавлена!")
    clear_entries()
    load_requests()

def delete_request():
    selected_item = request_listbox.curselection()
    if not selected_item:
        messagebox.showerror("Ошибка", "Выберите заявку для удаления!")
        return
    
    request_id = request_ids[selected_item[0]]
    cursor.execute('DELETE FROM requests WHERE id = ?', (request_id,))
    conn.commit()
    messagebox.showinfo("Успех", "Заявка удалена!")
    load_requests()

def load_requests():
    request_listbox.delete(0, tk.END)
    global request_ids
    request_ids = []

    cursor.execute('SELECT id, message, contact_number, address FROM requests')
    for row in cursor.fetchall():
        request_ids.append(row[0])
        request_listbox.insert(tk.END, f"{row[1]} | {row[2]} | {row[3]}")

def clear_entries():
    message_entry.delete(0, tk.END)
    contact_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)

# Интерфейс приложения
root = tk.Tk()
root.title("SputTV - Управление заявками")

tk.Label(root, text="Сообщение").grid(row=0, column=0, padx=10, pady=5, sticky="w")
message_entry = tk.Entry(root, width=50)
message_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Контактный номер").grid(row=1, column=0, padx=10, pady=5, sticky="w")
contact_entry = tk.Entry(root, width=50)
contact_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Адрес").grid(row=2, column=0, padx=10, pady=5, sticky="w")
address_entry = tk.Entry(root, width=50)
address_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Button(root, text="Добавить заявку", command=add_request_gui).grid(row=3, column=0, columnspan=2, pady=10)
tk.Button(root, text="Удалить заявку", command=delete_request).grid(row=4, column=0, columnspan=2, pady=10)

tk.Label(root, text="Список заявок").grid(row=5, column=0, padx=10, pady=5, sticky="w")
request_listbox = tk.Listbox(root, width=80, height=15)
request_listbox.grid(row=6, column=0, columnspan=2, padx=10, pady=5)

load_requests()

# Запуск Flask-сервера в отдельном потоке
server_thread = threading.Thread(target=start_server, daemon=True)
server_thread.start()

root.mainloop()
conn.close()
