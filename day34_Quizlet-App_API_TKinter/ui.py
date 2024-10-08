import tkinter
from tkinter import *
from quiz_brain import QuizBrain

THEME_COLOR = "#375362"
FONT = ("Arial",20,"italic")

#creating the UI within a class
class QuizInterface:
    def __init__(self,quiz_brain: QuizBrain):
        self.quiz = quiz_brain

        self.window = Tk()
        self.window.title("Quizzler")
        self.window.config(padx=20,pady=20,bg=THEME_COLOR)

        self.score_label = Label(text="Score: ",fg="white", bg=THEME_COLOR)
        self.score_label.grid(row=0,column=1)

        self.canvas = Canvas(bg="white",highlightthickness=0, width=300,height=250)
        self.question_text = self.canvas.create_text(
            150,
            125,
            width=280,
            text="some question text",
            fill=THEME_COLOR,
            font=FONT)
        self.canvas.grid(row=1,column=0,columnspan=2,pady=50)

        self.true_btn_img = PhotoImage(file="images/true.png")
        self.false_btn_img = PhotoImage(file="images/false.png")
        self.true_button = Button(image=self.true_btn_img, highlightthickness=0, command=self.true_pressed)
        self.true_button.grid(row=2,column=0)
        self.false_button = Button(image=self.false_btn_img, highlightthickness=0, command=self.false_pressed)
        self.false_button.grid(row=2, column=1)

        self.get_next_question()
        self.window.mainloop()

    #calls the next question from quiz_brain.py
    def get_next_question(self):
        self.canvas.config(bg="white")
        if self.quiz.still_has_questions():
            q_text = self.quiz.next_question()
            self.canvas.itemconfig(self.question_text,text=q_text)
        else:
            self.canvas.itemconfig(self.question_text, text="You've reached the end of the quiz.")
            self.true_button.config(state="disabled")
            self.false_button.config(state="disabled")

    def true_pressed(self):
        self.give_feedback(self.quiz.check_answer("True"))
    def false_pressed(self):
        self.give_feedback(self.quiz.check_answer("False"))

    def give_feedback(self, is_right):
        if is_right:
            self.canvas.config(bg="green")
            self.score_label.config(text=f"Score: {self.quiz.score}")
        else:
            self.canvas.config(bg="red")
        self.window.after(1000, self.get_next_question)

