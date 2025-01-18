import pandas as pd
import string as str
import time
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from dsci524_group13_quizit.utils import (
    select_questions, print_question, prompt_input, input_check, 
    mcq_score, score_log, question_log, QuizResult
)
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
        pass

    def take_multiple_choice(self, n, save_questions=False, save_score=False, file_path=""):
        """
        Conducts a multiple-choice quiz and provides optional result tracking.

        This method randomly selects `n` questions from the question bank and 
        prompts the user to answer one question at a time. At the end of the quiz, 
        the function will display the total score and the time taken.

        Optional logging and score saving:
        - If `save_score` is True, the final score and time spent are saved to a file.
        - If `save_questions` is set to "all", "incorrect", or "correct", it saves the 
        corresponding questions (with their options, user answers, correct answers, and explanations) 
        to a log file.

        Parameters:
        -----------
        n : int
            The number of questions to randomly select from the question bank.
            If `n` exceeds the total number of questions in the bank, all available questions are used.
            
        save_questions : str or bool, optional (default=False)
            Specifies which questions to save to a log file.
            - "all": Saves all answered questions.
            - "incorrect": Saves only the incorrect questions.
            - "correct": Saves only the correct questions.
            - False: No questions are saved.

        save_score : bool, optional (default=False)
            If True, save the final quiz score and the time taken to a file.

        Returns:
        --------
        results : str
            A summary of the quiz, including the final score and the time used to complete the quiz.

        Example:
        --------
        quiz.take_multiple_choice(10, save_questions="incorrect", save_score=True)
        """
        # Handle Exceptions
        if self.mcq is None:
            raise ValueError("No multiple-choice questions loaded.")

        if save_questions not in ["all", "correct", "incorrect", False]:
            raise TypeError("Invalid value for 'save_questions'. \nExpected one of: 'all', 'correct', 'incorrect', or False.")

        if save_score not in [True, False]:
            raise TypeError("Invalid value for 'save_score'. \nExpected boolean: True or False.")

        if not isinstance(n, int):
            raise TypeError("Invalid value for 'n'. Expected positive integer.")
        
        mcq = self.mcq
        mcq = mcq.dropna()
        mcq = mcq[
        (mcq['answers'].map(len) > 0) &
        (mcq['options'].map(len) > 0) &
        (mcq['options'].map(len) >= mcq['answers'].map(len))
        ]

        if mcq is None:
            raise ValueError("No multiple-choice questions loaded.")

        # Initialise Quiz
        n, quiz = select_questions(self.mcq, max(n, 1))
        final_score = []
        
        print(f"This quiz contains {n} questions.\
            \nTo answer, type the corresponding letter of your choice (e.g. A). \
            \nIf there are multiple answers, separate your choices with commas (e.g. A, B).")

        # Quiz
        start_time = time.time()
        for i in range(n):
            n_options, options_dict = print_question(quiz.iloc[i], i)
            
            # Validate user input
            valid = False
            count = 0
            while not valid:
                count += 1
                user_input = prompt_input()
                user_input, valid, message = input_check(user_input, n_options, count)
                print(message)
            
            quiz.loc[i, "response"] = user_input
            score = mcq_score(options_dict, quiz.iloc[i], user_input)
            final_score.append(score)
            quiz.loc[i, "score"] = score

        # Saving and Displaying Quiz Results
        time_used = round((time.time() - start_time), 2)
        pct_score = round(sum(final_score)/n, 2)
        score_log(round(pct_score, 2), time_used, save_score, file_path)
        quiz = question_log(save_questions, quiz, file_path)
        result = QuizResult(time_used=time_used, score=pct_score, question_summary=quiz)
        
        print("="*30, "\nQuiz Results")
        print(f"Score: {sum(final_score)}/{n} ({pct_score*100}%)" )
        print("Time used:", round(time_used, 2), "seconds")     

        return result

