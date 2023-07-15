import datetime
import os
import sqlite3
import time

import beaupy
from tabulate import tabulate


def ex():
    conn.close()
    exit()

def clear(t=0):
    time.sleep(t)
    os.system("cls || clear")

def ask():
    print("What would you like to do?")
    ans = beaupy.select(['Show all notes', 'Look at note', 'Add note', 'Delete note', 'Leave'])
    clear()
    return ans

def leave():
    print("OK,\nHave a great day!")
    time.sleep(1.456)
    ex()

def addNote():
    cursor.execute("SELECT title FROM notes")
    rows = cursor.fetchall()
    rows = [v[0] for v in rows]
    title = input("Enter title for note (leave empty to cancel): ")
    while (title in rows) or title == 'cancel and return to main menu':
        print("Title already exists or cant be used")
        title = input("Enter a different title for note (leave empty to cancel): ")
    if title != '':
        content = rf'{input("Enter note: ")}'
        t = datetime.datetime.now()
        cursor.execute("INSERT INTO notes (title, content, created_at) VALUES (?, ?, ?)", (title, content, t))
        conn.commit()
        print("Note added")
    else:
        clear()
        print("OK,\nReturning to main menu")
        clear(0.567)

def deleteNote():
    cursor.execute("SELECT title FROM notes")
    rows = cursor.fetchall()
    rows = [v[0] for v in rows]
    rows.append('cancel and return to main menu')
    print("What note would you like to delete?")
    ans = beaupy.select(rows)
    clear()
    if ans != 'cancel and return to main menu':
        cursor.execute("DELETE FROM notes WHERE title = ?", (ans,))
        conn.commit()
        print(f"Note '{ans}' deleted successfully.")
        clear(0.756)
    else:
        print("OK,\nReturning to main menu")
        clear(0.567)

def lookAtNote():
    cursor.execute("SELECT title FROM notes")
    rows = cursor.fetchall()
    rows = [v[0] for v in rows]
    rows.append('cancel and return to main menu')
    print("What note would you like to look at?")
    ans = beaupy.select(rows)
    clear()
    if ans != 'cancel and return to main menu':
        cursor.execute("SELECT content FROM notes WHERE title = ?", (ans,))
        cont = cursor.fetchall()[0][0]
        print(cont)
        print("(press ENTER to exit)")
        input()
        clear(0.234)
        print("OK,\nReturning to main menu")
        clear(0.567)
    else:
        clear(0.234)
        print("OK,\nReturning to main menu")
        clear(0.567)

def showAll():
    cursor.execute("SELECT title, content, created_at FROM notes")
    rows = cursor.fetchall()
    rows = [list(row) for row in rows]
    for i, row in enumerate(rows):
        datetime_obj = datetime.datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S.%f')
        readable_time = datetime_obj.strftime('%d/%m/%Y %H:%M:%S')
        rows[i][2] = readable_time
    headers = ["Title", "Content", "Created at"]
    table = tabulate(rows, headers, tablefmt="grid")
    print(table)
    print("(press ENTER to exit)")
    input()


conn = sqlite3.connect('toDo.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS notes (
        title TEXT,
        content TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')
conn.commit()
clear()
print("Hello")
clear(0.5)
while True:
    ans = ask()
    match(ans):
        case "Leave":
            leave()
        case "Add note":
            addNote()
        case "Delete note":
            deleteNote()
        case "Look at note":
            lookAtNote()
        case 'Show all notes':
            showAll()
    clear(1)