import pandas as pd
from enum import Enum
import string as str
import time
import sys
import os
from dsci524_group13_quizit.utils import (
    select_questions, print_question, prompt_input, input_check, 
    mcq_score, score_log, question_log, QuizResult
)

class QuestionType(Enum):
    MULTIPLE_CHOICE = "multiple choice"
    SHORT_ANSWER = "short answer"

MCQ_COLUMNS = ["question","options","answers","explanations"]
SHRTQ_COLUMNS = ["question","answers","explanations"]

QUESTION_COLUMN_MAPPING = {
    QuestionType.MULTIPLE_CHOICE: MCQ_COLUMNS,
    QuestionType.SHORT_ANSWER: SHRTQ_COLUMNS
}
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


    def _validate_question_format(self, question_type: QuestionType, has_header: bool, questions: pd.DataFrame, delimeter: str):
        """
        Validates the format of the questions DataFrame based on the specified question type.
        
        Parameters
        ----------
        question_type : QuestionType
            The type of the questions (e.g., multiple choice, short answer).
        has_header : bool
            Indicates whether the DataFrame has a header row.
        questions : pd.DataFrame
            The DataFrame containing the questions to be validated.
        delimeter : bool, optional
            The delimeter of the `answers` and `options` for the 'multiple choice' questions.
        
        Returns
        -------
        pd.DataFrame
            The validated questions DataFrame with processed columns based on the question type.
        
        Raises
        ------
        ValueError
            If the question type is not specified, unsupported, or if the DataFrame does not follow the expected format.
        TypeError
            If the question type is not of type `QuestionType`.
        """
        if not question_type:
            raise ValueError("The question type must be specified")
        
        if not isinstance(question_type, QuestionType):
            raise TypeError(f"The question type must be of type `QuestionType`, received {type(question_type)}")

        expected_columns = QUESTION_COLUMN_MAPPING.get(question_type)
        if expected_columns is None:
            raise ValueError(f"Unsupported question type: {question_type}")
        
        if len(questions.columns) != len(expected_columns):
            raise ValueError(f"The question must follow a specific format. Expected {len(expected_columns)} columns.")
        
        if has_header and any(questions.columns != expected_columns):
            raise ValueError(f"The question must follow a specific format. Expected columns: {expected_columns}, received: {questions.columns}")
        
        
        if delimeter:
            if question_type == QuestionType.MULTIPLE_CHOICE:
                questions['options'] = questions['options'].apply(lambda x: x.split(delimeter))
                questions['answers'] = questions['answers'].apply(lambda x: x.split(delimeter))
                self.mcq = questions.copy()
                return self.mcq
            
            else:
                questions['answers'] = questions['answers'].apply(lambda x: x.split(delimeter))
                self.shrtq = questions.copy()
                return self.shrtq
        else:
            if question_type == QuestionType.MULTIPLE_CHOICE:
                self.mcq = questions.copy()
                return self.mcq
            else:
                self.shrtq = questions.copy()
                return self.shrtq
        
        
    def load_questions_from_file(self, input_file: str, question_type: QuestionType, has_header: bool = True, delimeter: str = None) -> pd.DataFrame:
        """

        This function reads the user's questions from a CSV file.
        The questions are converted into a pandas DataFrame and saved in the internal class variable.
        
        Parameters
        ----------
        input_file : str
            The path to the CSV file containing the questions.
        question_type : QuestionType
            The type of questions, either 'multiple choice' or 'short answer'. 
        has_header : bool, optional
            Indicates if the CSV file contains a header. Default is True.
        delimeter : bool, optional
            The delimeter of the `answers` and `options` for the 'multiple choice' questions. Default is None.
        
        Returns
        -------
        pd.DataFrame
            A pandas DataFrame containing the questions.
        
        Raises
        ------
        FileNotFoundError
            If the `input_file` path does not exist.
        ValueError
            If the file is empty or cannot be read.
        """
        if not input_file:
            raise ValueError("Input file path must be provided.")
        
        try:
            header = 0 if has_header else None
            try:
                questions_df = pd.read_csv(input_file, header=header)
            except ValueError:
                raise ValueError("The input file is empty.")
            
            return self._validate_question_format(question_type=question_type, has_header=has_header, questions=questions_df, delimeter=delimeter)

        except FileNotFoundError:
            raise FileNotFoundError(f"The file at {input_file} was not found.")
        except Exception as e:
            raise ValueError(f"An error occurred while reading the file: {e}")


    def load_questions_from_dataframe(self, questions: pd.DataFrame, question_type: QuestionType, has_header: bool = True, delimeter: str = None) -> pd.DataFrame:
        """
        
        This function reads the user's questions from a pandas DataFrame.
        The questions are converted into a pandas DataFrame and saved in the internal class variable.
        
        Parameters
        ----------
        questions : pd.DataFrame
            The user questions as a pandas DataFrame.
        question_type : QuestionType
            The type of questions, either 'multiple choice' or 'short answer'. 
        has_header : bool, optional
            Indicates if the DataFrame contains a header. Default is True.
        delimeter : bool, optional
            The delimeter of the `answers` and `options` for the 'multiple choice' questions. Default is None.
        
        Returns
        -------
        pd.DataFrame
            A pandas DataFrame containing the questions.
        
        Raises
        ------
        TypeError
            If the `questions` is not a pandas DataFrame.
        ValueError
            If the DataFrame is empty or if the question type is not specified.
        """
        if not isinstance(questions, pd.DataFrame):
            raise TypeError(f"The `questions` parameter must be a pandas DataFrame, received {type(questions)}")
        
        if questions.empty:
            raise ValueError("The input DataFrame cannot be empty.")
        
        return self._validate_question_format(question_type=question_type, has_header=has_header, questions=questions, delimeter=delimeter)

    def load_questions(self, questions: pd.DataFrame = None, input_file: str = None, question_type: QuestionType = None, has_header: bool = True, delimeter: str = None) -> pd.DataFrame:
        """
        
        Wrapper function to load questions from a DataFrame or a file (CSV).
        
        Parameters
        ----------
        questions : pd.DataFrame, optional
            The user questions as a pandas DataFrame. Default is None.
        input_file : str, optional
            The path to the CSV file containing the questions. Default is None.
        question_type : QuestionType, optional
            The type of questions, either 'multiple choice' or 'short answer'. Default is None.
        has_header : bool, optional
            Indicates if the CSV file or DataFrame contains a header. Default is True.
        delimeter : bool, optional
            The delimeter of the `answers` and `options` for the 'multiple choice' questions. Default is None.
        
        Returns
        -------
        pd.DataFrame
            A pandas DataFrame containing the questions.
        
        Raises
        ------
        ValueError
            If both `questions` and `input_file` are provided or neither is provided.
        
        Examples
        --------
        >>> load_questions(input_file="questions.csv", question_type=QuestionType.MULTIPLE_CHOICE)
        >>> load_questions(questions=pd.DataFrame(data), question_type=QuestionType.SHORT_ANSWER)
        
        Notes
        -----
        The input file needs to be formatted as follows:

        For multiple choice questions:
        Question | Answers       | Correct Answers | Explanation
        -------- | ------------- | --------------- | -----------
        mcq      | [A, B, C]     | [B, C]          | explanation

        For short answer questions:
        Question                                    | Answer
        --------------------------------------------| ------
        What continent has the largest population?  | Asia
        """

        if questions is not None and input_file is not None:
            raise ValueError("Please provide either a questions DataFrame or an input file, not both.")
        
        if questions is not None:
            return self.load_questions_from_dataframe(questions=questions, question_type=question_type, has_header=has_header, delimeter=delimeter)
        
        if input_file is not None:
            return self.load_questions_from_file(input_file=input_file, question_type=question_type, has_header=has_header, delimeter=delimeter)
        
        raise ValueError("Please provide either a questions DataFrame or an input file.")


    def take_multiple_choice(self, n, save_questions=False, save_score=False, file_path=None):
        """
        Conducts a multiple-choice quiz and provides optional result tracking.

        This method randomly selects `n` questions from the question bank and 
        prompts the user to answer one question at a time. At the end of the quiz, 
        the function will display the total score and the time taken.

        Optional logging and score saving:
        - If `save_score` is True, the final score and time spent are saved to a file.
        - If `save_questions` is set to "all", "incorrect", or "correct", it saves the 
        corresponding questions (with their options, user answers, correct answers, and explanations) 
        to a log file. If `file_path` is not specified, log files will be saved to your current working directory.

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
        
        file_path : str, optional (default=None)
            Allow users to specify the location where the quiz score and question log are stored.

        Returns:
        --------
        results : QuizResult
            An instance of the `QuizResult` class, which contains:
            - `time_used`: The time (in seconds) taken to complete the quiz.
            - `score`: The final quiz percentage score.
            - `question_summary`: A DataFrame with details about all answered questions, including user responses, correct answers, and scores.

        Raises:
        -------
        ValueError
            If no multiple-choice questions are loaded in the `Quizit` class instance (`self.mcq` == `None`).
            If there are no valid multiple-choice questions available.
        
        TypeError
            If the `save_questions` parameter is not one of: 'all', 'correct', 'incorrect', or False.
            If the `save_score` parameter is not a boolean (True or False).
            If the `n` parameter is not an integer.

        Example:
        --------
        quiz.take_multiple_choice(10, save_questions="incorrect", save_score=True)
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
            
            quiz.loc[i, "response"] = user_input
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

    def take_short_answer(self, n, save_questions=False, save_score=False, file_path=None):
        """
        Allows the user to take a short-answer quiz and evaluates their score.
        
        This feature displays a series of short-answer questions to the user. The user must provide their own replies for each inquiry. 
        This function displays a series of short-answer questions to the user. The user must provide their own replies for each inquiry. 
        The function compares the user's response with the proper answer to each question. The system calculates the user's score based on 
        the correctness of their replies and provides a summary with the list of properly answered and poorly answered questions.
        Additionally, it writes out the correct answers to one file and the incorrect answers to a different file.
        
        Parameters:
            questions (list): A list of short-answer question dictionaries or objects. Each question should have the following fields:
                - question_text (str): The question prompt.
                - correct_answer (str): The correct answer for the short-answer question.
                - question_type (str): Should be 'short_answer'.
            n (int): The number of questions to present in the quiz.
            save_questions (bool): If True, saves the questions answered correctly or incorrectly to two different files.
            save_score (bool): If True, saves the score to a file.
        
        Returns:
            dict: A dictionary containing the user's performance:
                - score (float): The final score percentage.
                - correct_answers (list): A list of questions that were answered correctly.
                - incorrect_answers (list): A list of questions that were answered incorrectly.
        
        Raises:
            ValueError: If the `questions` list is empty, the function will raise an error as there are no questions to quiz.
            TypeError: If the items in the `questions` list are not in the expected format (e.g., missing necessary fields).
            ValueError: If the questions list is empty or None, the function will raise an error as there are no questions to quiz.
            TypeError: If the items in the questions list are not in the expected format (e.g., missing necessary fields).
        
        Example:
            take_short_answer(questions)
            # Returns a dictionary like:
            # {
            #     'score': 100.0,
            #     'correct_answers': ['xxx'],
            #     'incorrect_answers': []
            # }
        
        take_short_answer(3, save_questions=True, save_score=True)
        """
        if self.shrtq is None:
            raise ValueError("No short-answer questions loaded.")
        
        if n > len(self.shrtq):
            raise ValueError(f"Not enough questions available. Only {len(self.shrtq)} questions loaded.")
        
        quiz = self.shrtq.sample(n, ignore_index=True)
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
                quiz.loc[[i], "score"] = 1
            else:
                score.append(0)
                quiz.loc[[i], "response"] = user_input
                quiz.loc[[i], "score"] = 0

        time_used = round((time.time() - start_time), 2)
        score_percent = round(sum(score) / n * 100, 2)

        result = QuizResult(time_used=time_used, score=score_percent, question_summary=quiz, question_type="shrtq")

        score_log(score_percent, time_used, "shrtq", save_score, file_path)
        question_log(save_questions, quiz, "shrtq", file_path)
        return result
    