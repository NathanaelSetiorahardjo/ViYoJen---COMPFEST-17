#!/usr/bin/env python3
# ws_server_az_primary_ml_filter_ui.py

import asyncio
import json
from collections import deque
import threading
from datetime import datetime

import joblib
import numpy as np
import websockets
import tkinter as tk

# ========= Parameters =========
LOWER = 8.0
UPPER = 11.0
WINDOW_CONFIRM = 3
ML_PROB_THRESH = 0.50
HOST = "0.0.0.0"
PORT = 8765

# ========= Load AZ-only ML =========
MODEL_PATH = "microsleep_model.pkl"
SCALER_PATH = "scaler.pkl"
model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

# ========= Internal State =========
state = {"current": "AWAKE", "count": 0, "log": []}
th_on_hits = deque(maxlen=WINDOW_CONFIRM)
th_off_hits = deque(maxlen=WINDOW_CONFIRM)


def threshold_flag(az: float) -> int:
    return int(az < LOWER or az > UPPER)


def ml_confirm(az: float):
    X = np.array([[az]], dtype=np.float32)
    Xs = scaler.transform(X)
    prob = float(model.predict_proba(Xs)[0][1])
    pred = int(prob >= ML_PROB_THRESH)
    return pred, prob


# ========= WebSocket Handler =========
async def handler(websocket):
    global state, th_on_hits, th_off_hits
    print("Client connected")

    try:
        async for message in websocket:
            try:
                data = json.loads(message)
            except json.JSONDecodeError:
                continue

            az = float(data.get("az", 0.0))
            th = threshold_flag(az)

            ml_checked = False
            ml_prob = None
            ml_pred = None
            event = 0

            if state["current"] == "AWAKE":
                th_on_hits.append(th)
                if len(th_on_hits) == WINDOW_CONFIRM and all(v == 1 for v in th_on_hits):
                    ml_checked = True
                    ml_pred, ml_prob = ml_confirm(az)
                    if ml_pred == 1:
                        state["current"] = "MICROSLEEP"
                        state["count"] += 1
                        event = 1
                        ts = datetime.now().strftime("%H:%M:%S")
                        state["log"].append(f"{ts} - Microsleep Detected")
                        th_on_hits.clear()
                        th_off_hits.clear()
                        print(f"➡ State change: MICROSLEEP (az={az:.2f}, ML_p={ml_prob:.2f})")
                    else:
                        th_on_hits.clear()

            else:  # MICROSLEEP
                th_off_hits.append(1 if th == 0 else 0)
                if len(th_off_hits) == WINDOW_CONFIRM and all(v == 1 for v in th_off_hits):
                    state["current"] = "AWAKE"
                    th_off_hits.clear()
                    th_on_hits.clear()
                    ts = datetime.now().strftime("%H:%M:%S")
                    state["log"].append(f"{ts} - Awake Again")
                    print(f"➡ State change: AWAKE (az={az:.2f})")

            result = {
                "az": round(az, 2),
                "threshold": th,
                "state": state["current"],
                "count": state["count"],
                "event": int(event)
            }
            await websocket.send(json.dumps(result))

    except Exception as e:
        print("Handler error:", e)


async def ws_server():
    async with websockets.serve(handler, HOST, PORT):
        print(f"Hybrid AZ-primary server running on ws://{HOST}:{PORT}")
        await asyncio.Future()


# ========= Tkinter Dashboard =========
def update_ui():
    if state["current"] == "MICROSLEEP":
        status_label.config(text="⚠️ Microsleep Detected", bg="#D9534F", fg="white")
    else:
        status_label.config(text="✅ Driver Awake", bg="#5CB85C", fg="white")

    counter_label.config(text=f"Total Microsleep Episodes: {state['count']}")

    log_box.delete(0, tk.END)
    for entry in state["log"][-5:]:
        log_box.insert(tk.END, entry)

    root.after(1000, update_ui)


def start_ui():
    global root, status_label, counter_label, log_box
    root = tk.Tk()
    root.title("🚗 Microsleep Monitoring Dashboard")
    root.geometry("520x340")
    root.configure(bg="#222")

    status_label = tk.Label(root, text="Waiting for data...", font=("Arial", 18, "bold"),
                            width=35, height=2, bg="#555", fg="white")
    status_label.pack(pady=15)

    counter_label = tk.Label(root, text="Total Microsleep Episodes: 0", font=("Arial", 14), bg="#222", fg="white")
    counter_label.pack(pady=10)

    tk.Label(root, text="Event Log:", font=("Arial", 12, "bold"), bg="#222", fg="white").pack()
    log_box = tk.Listbox(root, height=6, width=60, bg="#111", fg="white", font=("Consolas", 10))
    log_box.pack(pady=5)

    update_ui()
    root.mainloop()


# ========= Entrypoint =========
if __name__ == "__main__":
    # Run WebSocket server in a background thread
    threading.Thread(target=lambda: asyncio.run(ws_server()), daemon=True).start()
    # Run UI
    start_ui()
