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

    def take_multiple_choice(self, n, save_questions=False, save_score=False, file_path=None):
        """
        Conducts a multiple-choice quiz and provides optional result tracking.

        This method randomly selects `n` questions from the question bank and 
        prompts the user to answer one question at a time. At the end of the quiz, 
        the function will display the total score and the time taken.

        Optional logging and score saving:
        - If `save_score` is True, the final score and time spent are saved to a txt file.
        - If `save_questions` is set to "all", "incorrect", or "correct", 
        corresponding questions, along with multiple choice options, user answers, 
        correct answers, and explanations are saved to a txt file. 
        
        Notes:
        
        If `file_path` is not specified, all files will be saved to `"results"` folder 
        in your current working directory.

        Parameters:
        ----------
        n : int    
        The number of questions to randomly select from the question bank. 
        If `n` exceeds the total number of questions in the bank, all available questions are used.
                
        save_questions : str or bool, optional (default=False)
        Specifies which questions to save to a log file.
            - "all": Saves correct and incorrect questions in separate files.
            - "incorrect": Saves only the incorrect questions.
            - "correct": Saves only the correct questions.
            - False: No questions are saved.

        save_score : bool, optional (default=False)
        If True, save the final quiz score and the time taken to a file.
            
        file_path : str, optional (default=None)
        Allow users to specify the location where the quiz score and question log are stored.

        Returns
        -------
        QuizResult
        An instance of QuizResult class, which contains:
        - `time_used`: The time (in seconds) taken to complete the quiz.
        - `score`: The final quiz percentage score.
        - `question_summary`: A DataFrame with details about all answered questions, including user responses, correct answers, and scores.
        - `question_type`: A string specifying the type of questions ("mcq" or "shrtq")
        
        Raises
        -------
        ValueError
        - If no multiple-choice questions are loaded in the `Quizit` class instance (`self.mcq` == `None`).
        - If there are no valid multiple-choice questions available.
        
        TypeError
        - If the `save_questions` parameter is not one of: 'all', 'correct', 'incorrect', or False.
        - If the `save_score` parameter is not a boolean (True or False).
        - If the `n` parameter is not an integer.

        Example:
        --------
        quiz.take_multiple_choice(10, save_questions="incorrect", save_score=True, file_path=None)
        """
        # Exception Handling - Invalid Argument Input
        if self.mcq is None:
            raise ValueError("No multiple-choice questions loaded.")

        if save_questions not in ["all", "correct", "incorrect", False]:
            raise TypeError("Invalid value for 'save_questions'. \nExpected one of: 'all', 'correct', 'incorrect', or False.")

        if save_score not in [True, False]:
            raise TypeError("Invalid value for 'save_score'. \nExpected boolean: True or False.")

        if not isinstance(n, int):
            raise TypeError("Invalid value for 'n'. Expected positive integer.")
        
        # Exception Handling - Invalid Question Dataset
        mcq = self.mcq
        mcq = mcq.dropna()
        mcq = mcq[
        (mcq['answers'].map(len) > 0) &
        (mcq['options'].map(len) > 0) &
        (mcq['options'].map(len) >= mcq['answers'].map(len))
        ]
        if mcq.shape[0] == 0:
            raise ValueError(
        "No valid multiple-choice questions are available. Ensure that the data has no missing values, "
        "'answers' and 'options' columns contains non-empty list, and that the number of options is greater than "
        "or equal to the number of answers."
        )

        # Initialise Quiz
        n, quiz = select_questions(self.mcq, max(n, 1))
        quiz["response"] = ""
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
            
            quiz.at[i, "response"] = user_input
            score = mcq_score(options_dict, quiz.iloc[i], user_input)
            quiz.loc[i, "score"] = score
            final_score.append(score)

        # Saving and Displaying Quiz Results
        time_used = round((time.time() - start_time), 2)
        final_score = sum(final_score)
        pct_score = round(final_score/n*100, 2)
        score_log(pct_score, time_used, "mcq", save_score, file_path)
        question_log(save_questions, quiz, "mcq", file_path)
    
        result = QuizResult(time_used=time_used, score=pct_score, question_summary=quiz, question_type="mcq")
        
        print("="*30, "\nQuiz Results")
        print(f"Score: {round(final_score, 2)}/{n} ({pct_score}%)" )
        print("Time used:", round(time_used, 2), "seconds")     

        return result

