import pandas as pd
import time
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from dsci524_group13_quizit.utils import (score_log, question_log, QuizResult)

class Quizit():
    """
    A class to manage and conduct custom quizzes with multiple-choice and short-answer questions.
    
    This class allows users to load multiple-choice and short-answer question sets, and take multiple-choice or short-answer quizzes. 
    The quiz can save the user's score, and optionally log the answered questions and their correctness.
    """
    def __init__(self):
        """
        Initializes a new instance of the Quizit class.

        Attributes:
        -----------
        mcq : list, optional
            A collection of multiple-choice questions.

        shrtq : list, optional
            A collection of short-answer questions.

        Example:
        --------
        quiz = Quizit()
        """    
        self.mcq = None
        self.shrtq = None

    def take_short_answer(self, n, save_questions=False, save_score=False, file_path=""):
        """
        Conducts a short-answer quiz and evaluates the user's performance.

        This method displays a series of `n` short-answer questions, prompts the user for their responses, 
        and compares the responses with the correct answers. Based on the correctness of the answers, the function calculates
        the user's score. It also provides an option to save the answers to log files and save the final score.

        Parameters:
        ----------
        n : int
            The number of short-answer questions to present in the quiz. If `n` exceeds the number of available questions,
            it will present all available questions.
            
        save_questions : bool, optional (default=False)
            If True, saves the questions that were answered correctly and incorrectly to separate files. The correct answers 
            are saved to "correct_answers.txt" and the incorrect answers are saved to "incorrect_answers.txt".

        save_score : bool, optional (default=False)
            If True, saves the final quiz score and the time taken to a file ("score.txt").

        file_path : str, optional (default="")
            The directory path where the quiz score and question logs will be saved. If not provided, it defaults to the current 
            directory, and folders will be created as necessary.

        Returns
        -------
        dict
            A dictionary containing:
            - `score` (float): The final score percentage (0-100%).
            - `correct_answers` (list): A list of questions that were answered correctly.
            - `incorrect_answers` (list): A list of questions that were answered incorrectly.
            
        Raises
        ------
        ValueError
            - If there are no short-answer questions loaded in `self.shrtq`.
            - If the number of questions `n` exceeds the number of available questions in the quiz bank.
        
        TypeError
            - If any question format is not as expected (e.g., missing required fields).
            
        Example:
        --------
        result = quiz.take_short_answer(3, save_questions=True, save_score=True, file_path="results/")
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
        pct_score = round(sum(score) / n * 100, 2)

        # Saving and Displaying Quiz Results
        if save_score:
            score_log(pct_score, time_used, "shrtq", save_score, file_path)
        if save_questions:
            question_log(save_questions, quiz, "shrtq", file_path)
    
        result = QuizResult(time_used=time_used, score=pct_score, question_summary=quiz, question_type="shrtq")
        
        print("="*30, "\nQuiz Results")
        print(f"Score: {sum(score)}/{n} ({pct_score}%)" )
        print("Time used:", time_used, "seconds")     

        return result



