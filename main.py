import customtkinter as ctk
import pandas as pd
from datetime import datetime
from PIL import Image
import pygame
import time

pygame.mixer.init()
AZAN_SOUND = "abd_albaset.mp3"
def play_azan():
        pygame.mixer.music.load(AZAN_SOUND)
        pygame.mixer.music.play()


def prayer_time():
    db = pd.read_excel("all_prayer_time.xlsx")
    date = datetime.now().strftime("%Y-%m-%d")
    times=db[db["date.gregorian.date"]==date]
    return times

class PrayerApp:
    def __init__(self, root):
        self.root = root
        ctk.set_appearance_mode("dark")  # Light mode for better readability
        ctk.set_default_color_theme("green")

        self.root.title("🕌مواقيت الصلاة")
        self.root.geometry("650x800")
        self.root.resizable(False, False)

        # Background Image
        self.bg_image = ctk.CTkImage(light_image=Image.open("al-aqsa.jpg"), size=(700, 800))
        self.bg_frame = ctk.CTkLabel(self.root, image=self.bg_image)
        self.bg_frame.place(relwidth=1, relheight=1)  # Cover entire window

        times= prayer_time()
        self.fram2=ctk.CTkFrame(self.root,fg_color="#d6eaf8",corner_radius=0,border_width=3,border_color="white")
        self.fram2.pack(padx=25,pady=10)

        self.fram1=ctk.CTkFrame(self.root,fg_color="#ebedef",corner_radius=0,border_width=3,border_color="white")
        self.fram1.pack(padx=25,pady=15,fill="x")

        self.fram3=ctk.CTkFrame(self.root,fg_color="#d6eaf8",corner_radius=0,border_width=4,border_color="white")
        self.fram3.pack(padx=25,pady=10)

        self.title = ctk.CTkLabel(
            self.fram2,fg_color="transparent",
            text="🕌مواقيت الصلاة",
            font=("Arial", 42, "bold"),
            text_color="#184D47")
        self.title.pack(pady=10,padx=10)
        self.timer_label=ctk.CTkButton(self.fram3,text="  00:00⏳  ",font=("Arial", 28, "bold"),corner_radius=0,text_color="black"
                                       ,text_color_disabled="black",fg_color="transparent",command=self.stop_azan)
        self.timer_label.pack()
        

        # Day of the week and date
        self.day = ctk.CTkLabel(self.fram1,text=f"{times.iloc[0,15]}\n{times.iloc[0,13].strftime("%d-%m-%Y")}📅",font=("Arial", 28, "bold")
                                , text_color="#184D47",fg_color="transparent")
        self.day.pack(side="left", padx=25, pady=15)
        self.a_day =  ctk.CTkLabel(self.fram1,text=f"{times.iloc[0,56]}\n🕋{times.iloc[0,22]}",font=("Arial", 28, "bold")
                                   , text_color="#184D47",fg_color="transparent")
        self.a_day.pack(side="right", padx=25, pady=15)

        # Prayer times dictionary
        self.prayer_times = {
            "الفجر 🌑": times.iloc[0, 0].strftime("%I:%M %p"),
            "الشروق 🌅": times.iloc[0, 1].strftime("%I:%M %p"),
            "الظهر 🔆": times.iloc[0, 2].strftime("%I:%M %p"),
            "العصر 🌇": times.iloc[0, 3].strftime("%I:%M %p"),
            "المغرب 🌆": times.iloc[0, 5].strftime("%I:%M %p"),
            "العشاء 🌙": times.iloc[0, 6].strftime("%I:%M %p")
        }

        # Create prayer time cards
        for prayer, time in self.prayer_times.items():
            date = datetime.now().strftime("%I:%M %p")
            d=date.replace(":",".")
            t=time.replace(":",".")
            d = float(d[:-3])
            t = float(t[:-3])
            if date.endswith("PM") and int(d)!=12 :
                d=d+12
            if time.endswith("PM") and int(t)!=12:
                t=t+12
            print(d,t)
            print(type(d))
            print(type(t))
            if d < t:
                self.create_prayer_card_intime(prayer, time)
            else:
                self.create_prayer_card(prayer, time)
        self.update_countdown()
    def stop_azan(self):
        pygame.mixer.music.stop()
        self.update_countdown()

    def create_prayer_card(self, prayer_name, prayer_time):
        """Creates a modern glassmorphism-style card for each prayer."""
        frame = ctk.CTkFrame(
            self.root, fg_color="#eafaf1",bg_color="transparent",
            corner_radius=0,border_width=3,border_color="#566573")
        frame.pack(pady=10, padx=10, fill="x")

        # Prayer Name Label (Right-aligned for Arabic layout)
        prayer_label = ctk.CTkLabel(frame, text=prayer_name, font=("Arial", 30, "bold"), text_color="#154360")
        prayer_label.pack(side="right", padx=25, pady=15)

        # Time Label (Left-aligned)
        time_label = ctk.CTkLabel(
            frame, text=prayer_time, font=("Arial", 28, "bold"), text_color="#154360")
        time_label.pack(side="left", padx=25, pady=15)

    def create_prayer_card_intime(self, prayer_name, prayer_time):
        frame = ctk.CTkFrame(
            self.root, fg_color="green",bg_color="green",
            corner_radius=0,border_width=3,border_color="#566573")
        frame.pack(pady=10, padx=10, fill="x")

        # Prayer Name Label (Right-aligned for Arabic layout)
        prayer_label = ctk.CTkLabel(frame, text=prayer_name, font=("Arial", 30, "bold"), text_color="#154360")
        prayer_label.pack(side="right", padx=25, pady=15)

        # Time Label (Left-aligned)
        time_label = ctk.CTkLabel(
            frame, text=prayer_time, font=("Arial", 28, "bold"), text_color="#154360")
        time_label.pack(side="left", padx=25, pady=15)


    def update_countdown(self):
        """Updates the countdown timer to the next prayer time."""
        now = datetime.now()
        prayer_times_list = list(self.prayer_times.values())
        for time_str in prayer_times_list:
            prayer_time = datetime.strptime(time_str, "%I:%M %p")
            prayer_time = now.replace(hour=prayer_time.hour, minute=prayer_time.minute, second=0)

            if prayer_time > now:  # Find the next prayer time
                remaining_time = prayer_time - now
                hours, remainder = divmod(remaining_time.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                self.timer_label.configure(text=f"{hours:02}:{minutes:02}:{seconds:02}⏳",fg_color="transparent")
                if seconds == 1 and minutes==0 and hours == 0:
                    self.timer_label.configure(text="أذان الصلاة",fg_color="red")
                    play_azan()
                else:
                    self.root.after(1000, self.update_countdown)  # Update every second
                return
        else:
            self.timer_label.configure(text="أنتهت صلاوات اليوم")


# Run the application
if __name__ == "__main__":
    root = ctk.CTk()
    app = PrayerApp(root)
    root.mainloop()
