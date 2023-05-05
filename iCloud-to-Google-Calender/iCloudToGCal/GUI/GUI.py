from iCloudToGCal.selenuimFunctions.iCloud import openiCloud
from iCloudToGCal.chromedriver.installDriver import install_driver
from time import sleep
def check_if_ID_pass_is_correct(username, password, app, finishLabel, button1):

    finishLabel.configure(text="Verifying...")
    button1.configure(state="disabled")
    driver = openiCloud(username=username,password=password)
    if driver.current_url == "https://gu.icloudems.com/corecampus/index.php":
        driver.quit()
        finishLabel.configure(text="Incorrect Username or Password")
        button1.configure(state="normal")
    else:
        driver.quit()
        finishLabel.configure(text="Saved")
        app.after(1000)
        app.quit()





def GUI(s="", a=False):
    install_driver()
    import time
    import tkinter

    import customtkinter

    app = customtkinter.CTk()
    customtkinter.set_appearance_mode("System-")
    customtkinter.set_default_color_theme("green")

    app.geometry("720x480")
    app.title("GUI for Timetable")

    # def about(): about_text_outer.configure(text="In this, we will be collecting the raw data from iCloud using
    # Selenium then we convert that data into a CSV file and upload that data into Google sheets. In sheets,
    # an app script will be run to showcase the timetable on Google calendar. The sheet will be updated every hour
    # and an email will be sent to the user if there are any updates in the timetable.  Students can also check their
    # attendance and if there is any problem with their attendance they can contact the teacher which will save them
    # from getting debarred")

    def submit():
        if a:
            if len(entry1.get()) != 0 and len(entry2.get()) != 0 and len(entry2.get()) != 0:
                finishLabel.configure(text=s)

        if len(entry1.get()) > 1 and len(entry2.get()) > 1:
            import threading
            thread = threading.Thread(target=check_if_ID_pass_is_correct,
                                      args=(entry1.get(), entry2.get(), app, finishLabel, button1))
            thread.start()
        elif len(entry3.get()) > 1 and len(entry1.get()) > 1:
            finishLabel.configure(text="Enter password")
        elif len(entry3.get()) > 1 and len(entry2.get()) > 1:
            finishLabel.configure(text="Enter Username")
        elif len(entry3.get()) > 1:
            finishLabel.configure(text="Saved")
            app.after(1000)
            app.quit()
        else:
            finishLabel.configure(text="Either enter form link or Username and password!")

            # about_text_outer.configure(text="")
            # about_text_outer.configure(text="How is it working?", font=('comicsansms', 16))
            #
            # # About button
            # button2 = customtkinter.CTkButton(master=frame, text="About", command=about)
            # button2.pack(pady=10)

    frame = customtkinter.CTkFrame(master=app)
    frame.pack(pady=20, padx=60, fill="both", expand=True)

    label = customtkinter.CTkLabel(master=frame, text="GU Icloud to Google Calendar Automation",
                                   font=('comicsansms', 26, "bold"))
    label.pack(pady=32, padx=10)

    entry1 = customtkinter.CTkEntry(master=frame, placeholder_text="Username")
    entry1.pack(pady=12, padx=10)

    entry2 = customtkinter.CTkEntry(master=frame, placeholder_text="Password", show="*")
    entry2.pack(pady=12, padx=10)

    entry3 = customtkinter.CTkEntry(master=frame, placeholder_text="Form Link")
    entry3.pack(pady=12, padx=10)

    button1 = customtkinter.CTkButton(master=frame, text="Submit", command=submit)
    button1.pack(pady=12, padx=10)
    from .GUI.create import create_desktop_icon
    button2 = customtkinter.CTkButton(master=frame, text="Add Icon", command=create_desktop_icon)
    button2.pack(pady=12, padx=10)

    finishLabel = customtkinter.CTkLabel(frame, text=s)
    finishLabel.pack(pady=20)

    # about_text_outer = customtkinter.CTkLabel(master=frame, text="")
    # about_text_outer.pack(pady=(20,5))

    # Array

    app.mainloop()
    return [entry1.get(), entry2.get(), entry3.get()]


def check_for_data():
    with open(r"C:\icloud_resources\cerdential.txt", "r+") as f:
        d = f.read()
        if d == "" or "" in d.split("\n") or len(d.split("\n")) < 3:
            data = GUI(s="Please fill all data fields.", a=True)
            f.seek(0)
            f.write("\n".join(data))
            f.truncate()
