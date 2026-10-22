from tkinter import filedialog
import customtkinter as ctk
from PIL import Image
import shared
import watcher
import simulator
import threading
import time
import os
import database
from datetime import datetime
sfolder = None
observer=None
watcher_lock = threading.Lock()
demo_running = False
row_widgets = []

def restart_watcher(folder):
    global observer 
    with watcher_lock:
        watcher.stop_watcher(observer)
        observer = watcher.start_watcher(folder)

def stop_current_watcher():
    global observer
    with watcher_lock:
        watcher.stop_watcher(observer)
        observer = None

def selfol():
    global sfolder,observer
    folder=filedialog.askdirectory()
    if folder:
        sfolder=folder
        sfolder = folder
        restart_watcher(folder)
        switch.select()

root=ctk.CTk()
root.geometry("800x500")
root.resizable(False,False)
root.title("Test Window")
root.configure(fg_color="#241B2F")
ctk.set_appearance_mode('dark')
frame=ctk.CTkFrame(root,width=700,height=180,corner_radius=15,fg_color="#342842")
frame.place(x=50,y=290)
btn1=ctk.CTkButton(frame,text="select folder",corner_radius=32,height=30, width=50,fg_color="#6C4BA6",command=selfol)
def run_demo():
    global demo_running
    try:
        target_folder = sfolder if sfolder else simulator.TEST_DIR
        stop_current_watcher()
        simulator.setup(target_folder)
        restart_watcher(target_folder)
        time.sleep(2)
        simulator.attack(target_folder)
        time.sleep(3)
    finally:
        try:
            stop_current_watcher()
            simulator.cleanup(target_folder)
            if sfolder:
                restart_watcher(sfolder)
        except(Exception, SystemExit) as e:
            print("Cleanup Failed:", e)
        demo_running = False
def start_simulation():
    global demo_running
    if demo_running:
        return
    demo_running = True
    threading.Thread(target=run_demo, daemon=True).start()
def open_history():
    win = ctk.CTkToplevel(root)
    win.title("Scan History")
    win.geometry("640x440")
    win.configure(fg_color = "#241B2F")

    available_dates = database.get_dates()
    if not available_dates:
        available_dates = [datetime.now().strftime("%Y-%m-%d")]

    top_frame = ctk.CTkFrame(win, fg_color = "transparent")
    top_frame.pack(fill = "x", padx = 15, pady = (15, 5))

    date_label = ctk.CTkLabel(top_frame, text = "Select Scan Date:", font = ctk.CTkFont(size = 14, weight = "bold"),)
    date_label.pack(side = "left", padx = (0, 10))

    tb = ctk.CTkTextbox(win, width = 610, height = 340, fg_color = "#1A1024", text_color = "#FFFF00", font = ctk.CTkFont(family = "Consolas", size = 12),)
    tb.pack(padx = 15, pady = (5, 15))

    def load_date_records(selected_date):
        tb.delete("1.0", "end")
        records = database.get_events_by_date(selected_date)
        if not records:
            tb.insert("end", f"No scan events found for {selected_date} ({len(records)} events) ---\n",)  
            return  
        lines = []        
        for f, score, status, t in records:
            lines.append(f"[{t}] {status} (Score {score}) -> {f}\n")
        tb.insert("end", "".join(lines))

    date_menu = ctk.CTkOptionMenu(top_frame, values = available_dates, command = load_date_records, fg_color = "#6C4BA6", button_color = "#533785", dropdown_fg_color = "#342842",)
    date_menu.pack(side = "left")
    date_menu.set(available_dates[0])
    load_date_records(available_dates[0])

btn2=ctk.CTkButton(frame,text="simulate test",corner_radius=32,height=30, width=50,fg_color="#6C4BA6",command=start_simulation)
btn1.place(x=60, y=95, anchor='center')
btn2.place(x=60, y=50, anchor='center')
img= Image.open('picon.jpg')
btn3=ctk.CTkButton(root,text="",corner_radius=32,image=ctk.CTkImage(img),height=5, width=5,fg_color='transparent')
btn3.place(x=780, y=20, anchor='center')
lable=ctk.CTkLabel(root,text="Profile",fg_color='transparent')
lable.place(x=779, y=44, anchor='center')

def toggle_scanner():
    if switch.get() == 1:
        if sfolder:
            restart_watcher(sfolder)
        else:
            switch.deselect()
    else:
        stop_current_watcher()

switch=ctk.CTkSwitch(frame,text='scanner')
switch.place(x=350,y=110, anchor='center',)
switch.select()
btn4=ctk.CTkButton(frame,text="Scan History",corner_radius=32,height=30, width=50,fg_color="#6C4BA6")
btn4.place(x=60, y=140, anchor='center')
btn4.configure(command = open_history)
entry=ctk.CTkScrollableFrame(root,height=20,width=420,fg_color="#1A1024")
entry.place(x=50,y=30)
frame2=ctk.CTkFrame(frame,width=150,height=180,fg_color="#1A1024",corner_radius=15)
frame2.place(x=545)
lable3=ctk.CTkLabel(frame2,text="STATUS:")
lable3.place(relx=0.5,y=30,anchor='center')
img2=Image.open('safe.png')
lable4=ctk.CTkLabel(root,text='',image=ctk.CTkImage(img2,size=(200,200)),fg_color='transparent')
lable4.place(x=597,y=130,anchor='center')

def check_queue():
    while not shared.events.empty():
        kind , file, state = shared.events.get()
        message=f"<{time.strftime("%H:%M:%S")}> {kind}, {os.path.basename(file)}"
        val=ctk.CTkLabel(entry,text=message,text_color="#FFFF00")
        val.pack(anchor='w')
        row_widgets.append(val)
        if len(row_widgets) > 100:
            oldest = row_widgets.pop(0)
            oldest.destroy()
        entry.update_idletasks()
        entry._parent_canvas.yview_moveto(1.0)
        lable3.configure(text=f"STATUS: \n{state}")
        if state == "Confirmed Threat":
            score_val = 2
        elif state == "Suspicious":
            score_val = 1
        else:
            score_val = 0
        try:
            database.log_event(file, score_val, state)
            with open("logs.log", "a", encoding="utf-8") as f:
                f.write(f"<{time.strftime("%H:%M:%S")}> ,{kind}, {file}\n")
        except Exception as e:
            print("Logging failed:",e)
    root.after(100, check_queue)
def on_close():
    global observer
    watcher.stop_watcher(observer)
    root.destroy()
root.protocol("WM_DELETE_WINDOW",on_close)
check_queue() 
root.mainloop()
