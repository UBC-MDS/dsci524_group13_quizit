
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

def score_log(final_score, time_used, save_score=True, file_path=""):
    """Saves the quiz score and time taken to finish the quiz to a text file."""
    if save_score == False:
        return

    score_rec = f"{time.asctime()}  | {round(final_score*100)}%      | {time_used}"
    
    file = os.path.join(file_path, "score.txt")
    if not os.path.exists(file):
        mode = "x"
    else: 
        mode = "a"

    with open(file, mode) as f:
        if mode == "x":
            f.write("Date                      | Score    |Time Used (s)\n")
        f.write(f"{score_rec}\n")
    return 

def question_log(type, quiz, file_path=""):
    """Logs questions along with user's input based on the specified type (all, correct, or incorrect)."""
    if type == "all":
        pass
    elif type == "incorrect":
        quiz = quiz.loc[quiz["score"]!=1]
    elif type == "correct":
        quiz = quiz.loc[quiz["score"]==1]
    else:
        return quiz

    file = os.path.join(file_path, type + ".txt")
    with open(file, "a") as f:
        for i in range(quiz.shape[0]):
            f.write(f"Question \n")
            f.write(print_question(quiz.iloc[i], i, print_q=False))
            f.write(f"Your Answer: {quiz.iloc[i]['response']}\n")
            f.write(f"Correct Answer: {quiz.iloc[i]['answers']}\n")
            f.write(f"Explanations: {quiz.iloc[i]['explanations']}\n")
            f.write("====================================\n")
    return quiz

class QuizResult:
    """Represents the results of a quiz, including time taken, score, and question details."""
    def __init__(self, time_used, score, question_summary):
        self.time_used = time_used
        self.score = score
        self.question_summary = question_summary
        pass
        