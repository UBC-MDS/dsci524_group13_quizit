
import numpy as np
import pandas as pd
import string as str
import re as re
import time
import os

def select_questions(mcq, n):
    """Randomly selects a specified number of questions from the question bank."""
    try:
        quiz = mcq.sample(n, replace=False, ignore_index=True)
    except ValueError:
        quiz = mcq.sample(mcq.shape[0], replace=False, ignore_index=True)
    
    return quiz.shape[0], quiz

def prompt_input():
    """Prompts the user to input their answer."""
    return input("Enter Answer: ")

def print_question(question, iter, print_q=True):   
    """Print question and its options to the user or return a string containing the question and its options."""
    # Print MCQ questions the their options
    options_dict = {}
    options = question["options"]
    n_options = list(str.ascii_uppercase[0:len(options)])

    q_str = f"{question['question']}\n"

    for i in range(len(options)):
        q_str += f"{n_options[i]} : {options[i]}\n"
        options_dict[n_options[i]] = options[i]
    
    if print_q:
        print("=" * 30 + f"\nQuestion {iter+1}:\n" + q_str)
        return (n_options, options_dict)
    else:
        return q_str


def input_check(user_input, n_options, count):
    """Validates the user's input and ensures it matches the available options."""
    clean_user_input = user_input.replace(" ", "").upper().strip(",").split(",")
    if all(ans in n_options for ans in clean_user_input):
        message =  f"Your Answer: {clean_user_input}"
        return (clean_user_input, True, message)
    else:
        if count < 3:
            message = f"Your Answer: {user_input}\
                \nInvalid input. Please select a valid option from the given choices."
            return (user_input, False, message)
        else:
            message = f"Your Answer: {user_input}\
                \nInvalid input, Maximum attempts reached, Proceed to next question.\
                \n {'=' * 30}"
            return ("", True, message)

def mcq_score(options_dict, question_df, user_input):
    """Calculates the score for a question based on the user's input."""
    if user_input == [""]:
        return 0.0
    answers = question_df["answers"]
    right = [key for key, val in options_dict.items() if val in answers]
    wrong = [key for key, val in options_dict.items() if val not in answers]
    right_match = [rt in user_input for rt in right]
    wrong_absent = [wrg not in user_input for wrg in wrong]
    score = sum(right_match + wrong_absent) / len(options_dict)
    return round(score, 2)

def score_log(pct_score, time_used, question_type, save_score:bool, dir_name=None):
    """Saves the quiz score and time taken to finish the quiz to a text file."""
    if save_score == False:
        return

    if dir_name is None:
        dir_name = "results"

    score_rec = f"{time.asctime()}  | {pct_score}%      | {time_used}"
    file_name = "score" + "_" + question_type + ".txt"
    path = os.path.join(dir_name, file_name)
    if not os.path.exists(path):
        mode = "x"
        os.makedirs(os.path.dirname(path), exist_ok=True)
    else: 
        mode = "a"

    with open(path, mode) as f:
        if mode == "x":
            f.write("Date                      | Score       |Time Used (s)\n")
        f.write(f"{score_rec}\n")
    print(f"Score Log Saved to {os.path.abspath(dir_name)}")
    return 

def question_log(type, quiz, question_type:str, dir_name=None):
    """Logs questions along with user's input based on the specified type (all, correct, or incorrect)."""

    if type == False:
        return quiz
    elif type == "all": 
        type = ["incorrect", "correct"]
    elif type == "incorrect" or "correct":
        type = [type]
    
    right_wrong = {
        "incorrect": quiz.loc[quiz["score"]!=1], 
        "correct": quiz.loc[quiz["score"]==1]
    }

    if dir_name is None:
        dir_name = "results"
    path = os.path.join(dir_name, "")
    os.makedirs(os.path.dirname(path), exist_ok=True)

    for i in right_wrong.keys():
        if i not in type:
            continue
        file_name = i + "_" + question_type + ".txt"
        path = os.path.join(dir_name, file_name)
        quiz = right_wrong[i]       
        with open(path, "a") as f:
            for j in range(quiz.shape[0]):
                f.write(f"Question \n")
                if question_type == "mcq":
                    f.write(print_question(quiz.iloc[j], j, print_q=False))
                else:
                    f.write(f"{quiz.iloc[j]['question']}\n")
                f.write(f"Your Answer: {quiz.iloc[j]['response']}\n")
                f.write(f"Correct Answer: {quiz.iloc[j]['answers']}\n")
                f.write(f"Explanations: {quiz.iloc[j]['explanations']}\n")
                f.write("=" * 30 + "\n")

    print(f"Question Log Saved to {os.path.abspath(dir_name)}")
    return

class QuizResult:
    def __init__(self, time_used, score, question_summary, question_type):
        self.time_used = time_used
        self.score = score
        self.question_summary = question_summary
        self.question_type = question_type
        pass

    def __repr__(self):
        result_str = f"Quiz Results: \n"
        for idx, row in self.question_summary.iterrows():
            if self.question_type == "mcq":
                result_str += print_question(row, idx, print_q=False)
            elif self.question_type == "shrtq":
                result_str += f"Question:\n"
                result_str += f"{row['question']}\n"
            result_str += f"Your Answer: {row['response']}\n"
            result_str += f"Correct Answer: {row['answers']}\n"
            result_str += f"Explanation: {row['explanations']}\n"
            result_str += "=" * 30 + "\n"
        
        result_str += f"Total Score: {self.score}%\n"
        result_str += f"Time Used: {self.time_used} seconds"
        
        return result_str
