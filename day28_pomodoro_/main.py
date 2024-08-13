from tkinter import *
import math

# ---------------------------- CONSTANTS ------------------------------- #
#colors taken from colorhunt.co palette
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None

# ---------------------------- TIMER RESET ------------------------------- #
def reset():
    global reps, timer
    reps = 0
    window.after_cancel(timer)
    ##timer_text = 00:00
    canvas.itemconfig(timer_text, text="00:00")
    ##title_label = Timer
    timer_label.config(text="Timer")
    #reset check marks
    check_marks.config(text="")



# ---------------------------- TIMER MECHANISM ------------------------------- # 
def start_timer():
    global reps
    reps += 1
    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if reps % 8 == 0:
        timer = long_break_sec
        timer_label.config(text="Long Break", fg=RED)
    elif reps % 2 == 0:
        timer = short_break_sec
        timer_label.config(text="Short Break", fg=PINK)
    else:
        timer_label.config(text="Work", fg=GREEN)
        timer = work_sec
    count_down(timer)

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #

def count_down(count):

    # 1:25 format would be  245 /60 = 4.### and 245%60 = 0.08###
    count_min = math.floor(count / 60) #returns largest whole number less than or equal
    count_sec = count % 60 #returns the decimal
    if count_sec < 10:
        count_sec = f"0{count_sec}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        start_timer()
        marks = ""
        work_sessions = math.floor(reps/2)
        for _ in range(work_sessions):
            marks += "✔"
        check_marks.config(text=marks)
        check_marks.config(text="✔")
# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

#TimerTitle
timer_label = Label(text="Timer",font=(FONT_NAME,50), fg=GREEN, bg=YELLOW, highlightthickness=0)
timer_label.grid(column=2,row=1)

#start button
start_btn = Button(text="Start", font=(FONT_NAME,8), bg=YELLOW, command=start_timer)
start_btn.grid(column=1, row=3)

#checkmark label #label color fg=GREEN#copy checkmark symbol from wikipedia if needed
check_marks = Label(fg=GREEN, bg=YELLOW)
check_marks.grid(column=2,row=4)

#reset button .grid(column=3, row=3)
reset_btn = Button(text="Reset", font=(FONT_NAME,8), bg=YELLOW, command=reset, highlightthickness=0)
reset_btn.grid(column=3, row=3)

#canvas widget for the tomato background image
canvas = Canvas(width=200,height=224, bg=YELLOW, highlightthickness=0) #dimensions taken from tomato.png
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100,112, image=tomato_img)  #shifted to the right(102) because the tomato img appeared cut
timer_text = canvas.create_text(100,130,text="00:00", fill="white",font=(FONT_NAME,35,"bold")) #shifted down with the 130 code to center it
canvas.grid(column=2, row=2)


window.mainloop()