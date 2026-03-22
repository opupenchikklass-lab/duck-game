import sqlite3
from datetime import datetime

# Твоя сетка уровней
UPGRADE_COSTS = {1: 1000, 2: 2000, 3: 5000, 4: 8000, 5: 20000, 6: 40000, 7: 80000}
RARITIES = ['common', 'rare', 'epic', 'legendary']

def init_db():
    conn = sqlite3.connect('duck_game.db')
    cursor = conn.cursor()
    
    # Таблица игроков
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        food INTEGER DEFAULT 1000,
        batcoins REAL DEFAULT 0.0,
        last_tap_reset TEXT,
        taps_in_session INTEGER DEFAULT 0,
        referrer_id INTEGER
    )''')
    
    # Таблица уток (10 слотов)
    cursor.execute('''CREATE TABLE IF NOT EXISTS ducks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        slot_id INTEGER,
        level INTEGER DEFAULT 1,
        rarity TEXT DEFAULT 'common'
    )''')
    conn.commit()
    return conn

# Функция для выдачи первой утки
def give_starter_duck(user_id):
    conn = sqlite3.connect('duck_game.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ducks (user_id, slot_id, level, rarity) VALUES (?, ?, ?, ?)", 
                   (user_id, 1, 1, 'common'))
    conn.commit()