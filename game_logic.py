import random
from datetime import datetime, timedelta

def process_tap(user_id, conn):
    cursor = conn.cursor()
    cursor.execute("SELECT food, last_tap_reset, taps_in_session FROM users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
    
    food, last_reset_str, taps = user
    now = datetime.now()
    last_reset = datetime.fromisoformat(last_reset_str) if last_reset_str else now
    
    # Сброс цены тапа раз в 10 часов
    if now > last_reset + timedelta(hours=10):
        taps = 0
        last_reset = now
    
    # Цена тапа растет (условно +1 корм за каждые 10 тапов)
    tap_cost = 1 + (taps // 10)
    
    if food >= tap_cost:
        new_food = food - tap_cost
        new_taps = taps + 1
        
        # Шанс выпадения яйца (например 5%)
        egg_dropped = random.random() < 0.05
        
        cursor.execute("UPDATE users SET food=?, taps_in_session=?, last_tap_reset=? WHERE user_id=?",
                       (new_food, new_taps, last_reset.isoformat(), user_id))
        conn.commit()
        return {"status": "ok", "egg": egg_dropped, "cost": tap_cost}
    return {"status": "no_food"}