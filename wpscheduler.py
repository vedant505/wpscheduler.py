import tkinter as tk
from tkinter import messagebox
from twilio.rest import Client
from datetime import datetime
import time
import threading

# Twilio credentials (⚠️ use your real SID and token here)
account_sid = 'ACbaba7d6b6055c3452e0928d392cc2'
auth_token = 'd872c1a87fb6d08af7235a8c357d9'
client = Client(account_sid, auth_token)

# Function to send WhatsApp message
def send_wpmsg(recipent_number, message_body):
    try:
        message = client.messages.create(
            from_='whatsapp:+14155238886',  # Twilio sandbox number
            body=message_body,
            to=f'whatsapp:{recipent_number}'
        )
        messagebox.showinfo("Success", f"Message sent! SID: {message.sid}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to schedule message
def schedule_message():
    name = entry_name.get()
    recipent_number = entry_number.get()
    message = entry_message.get("1.0", tk.END).strip()
    date_str = entry_date.get()
    time_str = entry_time.get()

    try:
        schedule_datetime = datetime.strptime(f'{date_str} {time_str}', "%Y-%m-%d %H:%M")
        current_datetime = datetime.now()
        delay_seconds = (schedule_datetime - current_datetime).total_seconds()

        if delay_seconds <= 0:
            messagebox.showwarning("Invalid Time", "The specified time is in the past!")
        else:
            messagebox.showinfo("Scheduled", f"Message scheduled to {name} at {schedule_datetime}")

            # Run waiting in background so GUI doesn’t freeze
            def wait_and_send():
                time.sleep(delay_seconds)
                send_wpmsg(recipent_number, message)

            threading.Thread(target=wait_and_send, daemon=True).start()
    except Exception as e:
        messagebox.showerror("Error", f"Invalid date/time format: {e}")

# Build GUI
root = tk.Tk()
root.title("WhatsApp Message Scheduler")
root.geometry("400x400")

tk.Label(root, text="Recipient Name:").pack()
entry_name = tk.Entry(root, width=40)
entry_name.pack()

tk.Label(root, text="Recipient Number (+countrycode):").pack()
entry_number = tk.Entry(root, width=40)
entry_number.pack()

tk.Label(root, text="Message:").pack()
entry_message = tk.Text(root, width=40, height=5)
entry_message.pack()

tk.Label(root, text="Date (YYYY-MM-DD):").pack()
entry_date = tk.Entry(root, width=20)
entry_date.pack()

tk.Label(root, text="Time (HH:MM, 24hr):").pack()
entry_time = tk.Entry(root, width=20)
entry_time.pack()

tk.Button(root, text="Schedule Message", command=schedule_message, bg="green", fg="white").pack(pady=10)

root.mainloop()
