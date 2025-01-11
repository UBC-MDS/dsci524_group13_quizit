import pandas as pd
from enum import Enum

class QuestionType(Enum):
    MULTIPLE_CHOICE = "multiple choice"
    SHORT_ANSWER = "short answer"

def load_questions(questions: pd.DataFrame = None, input_file: str = None, question_type: QuestionType = None, has_header: bool = True):
    """
    Loads user's questions from a CSV file or a pandas DataFrame.

    This function reads the user's questions either from a CSV file or a pandas DataFrame.
    The questions are converted into a pandas DataFrame and saved in the internal class variable.

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

    Returns
    -------
    None

    Raises
    -------
    FileNotFoundError
        If the `input_file` path does not exist.
    ValueError
        If the `input_file` is not a CSV file or if the question_type is not recognized.
    TypeError
        If the `questions` is not a pandas DataFrame.

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

    pass

