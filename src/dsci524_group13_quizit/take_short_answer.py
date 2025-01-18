import time
import os
import pandas as pd

class Quizit():
    def __init__(self):
        self.mcq = None
        self.shrtq = None

    def take_short_answer(self, n, save_questions=False, save_score=False, file_path=""):
        """
        Allows the user to take a short-answer quiz and evaluates their score.
        """
        if self.shrtq is None:
            raise ValueError("No short-answer questions loaded.")
        
        if n > len(self.shrtq):
            raise ValueError(f"Not enough questions available. Only {len(self.shrtq)} questions loaded.")
        
        quiz = self.shrtq.sample(n)
        question = quiz["question"]
        answers = quiz["answers"]
        quiz["response"] = ""

        score = []
        correct_answers = []
        incorrect_answers = []

        start_time = time.time()
        for i in range(len(question)):
            print(f"Question {i+1}: {question.iloc[i]}")
            
            correct_answer = answers.iloc[i].lower()
            words = correct_answer.split()
            if len(words) == 1:
                print("Hint: Your answer must be one word.")
            elif len(words) == 2:
                print("Hint: Your answer must be two words.")
            
            user_input = input("Enter Answer: ").strip().lower()
            
            while len(user_input.split()) not in [1, 2]:
                print("Invalid answer. The answer must be either one word or two words.")
                user_input = input("Enter Answer: ").strip().lower()

            if user_input == correct_answer:
                score.append(1)
                quiz.loc[[i], "response"] = user_input
                correct_answers.append(question.iloc[i])
            else:
                score.append(0)
                quiz.loc[[i], "response"] = user_input
                incorrect_answers.append(question.iloc[i])

        time_used = round((time.time() - start_time), 2)
        score_percent = round(sum(score) / n * 100, 2)

        result = QuizResult(time_used=time_used, score=score_percent, question_summary=quiz)

        if save_score:
            self.save_score(score_percent, time_used, file_path)
        if save_questions:
            self.save_question_log(quiz, correct_answers, incorrect_answers, file_path)
        return result

    def save_score(self, score_percent, time_used, file_path):
        """
        Save the score to a file.
        """
        if not os.path.exists(file_path):
            os.makedirs(file_path)

        score_rec = f"{time.asctime()} | {score_percent}% | {time_used}s\n"
        file = os.path.join(file_path, "score.txt")
        mode = "a" if os.path.exists(file) else "x" 

        with open(file, mode) as f:
            if mode == "x":
                f.write("Date                      | Score    | Time Used (s)\n")
            f.write(score_rec)

    def save_question_log(self, quiz, correct_answers, incorrect_answers, file_path):
        """
        Save the questions and answers to a log file.
        """
        if not os.path.exists(file_path):
            os.makedirs(file_path)

        correct_file = os.path.join(file_path, "correct_answers.txt")
        incorrect_file = os.path.join(file_path, "incorrect_answers.txt")

        with open(correct_file, "a") as f:
            for i in correct_answers:
                f.write(f"Question: {i}\n")
                f.write(f"Correct Answer: {quiz.loc[quiz['question'] == i, 'answers'].iloc[0]}\n")
                f.write(f"Your Answer: {quiz.loc[quiz['question'] == i, 'response'].iloc[0]}\n")
                f.write("=" * 30 + "\n")

        with open(incorrect_file, "a") as f:
            for i in incorrect_answers:
                f.write(f"Question: {i}\n")
                f.write(f"Correct Answer: {quiz.loc[quiz['question'] == i, 'answers'].iloc[0]}\n")
                f.write(f"Your Answer: {quiz.loc[quiz['question'] == i, 'response'].iloc[0]}\n")
                f.write("=" * 30 + "\n")


class QuizResult:
    def __init__(self, time_used, score, question_summary):
        self.time_used = time_used
        self.score = score
        self.question_summary = question_summary

    def __repr__(self):
        result_str = f"Quiz Results: \n"
        for idx, row in self.question_summary.iterrows():
            question = row['question']
            user_answer = row['response']
            correct_answer = row['answers']
            score = row['score']
            result_str += f"Question {idx+1}: {question}\n"
            result_str += f"Your Answer: {user_answer}\n"
            result_str += f"Correct Answer: {correct_answer}\n"
            result_str += f"Score: {score}\n"
            result_str += "=" * 30 + "\n"
        
        result_str += f"Total Score: {self.score}%\n"
        result_str += f"Time Used: {self.time_used} seconds"
        
        return result_str


