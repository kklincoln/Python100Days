from question_model import Question
from data import question_data
from quiz_brain import QuizBrain

# write a for loop to iterate over the question data.
# create a question object from each entry in question_data
# append each question object to the question_bank
question_bank = []
for question in question_data:
    question_text = question["question"]
    question_answer = question["correct_answer"]
    new_question = Question(q_question=question_text, q_answer=question_answer)
    question_bank.append(new_question)
# print(question_bank)

quiz = QuizBrain(question_bank)
# if quiz still has questions remaining:
while quiz.still_has_questions():
    quiz.next_question()

# once out of questions; print results
print(f"You've completed the quiz with a final score: {quiz.score}/{len(quiz.question_list)}")