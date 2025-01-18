import pandas as pd
from enum import Enum

class QuestionType(Enum):
    MULTIPLE_CHOICE = "multiple choice"
    SHORT_ANSWER = "short answer"

def load_questions_from_file(input_file: str, question_type: QuestionType, has_header: bool = True) -> pd.DataFrame:
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
    pass
    


def load_questions_from_dataframe(questions: pd.DataFrame, question_type: QuestionType, has_header: bool = True) -> pd.DataFrame:
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
        Indicates if the CSV file contains a header. Default is True.
    
    Returns
    -------
    pd.DataFrame
        A pandas DataFrame containing the questions.
    
    Raises
    ------
    TypeError
        If the `questions` is not a pandas DataFrame.
    ValueError
        If the DataFrame is empty.
    """
    pass
    


def load_questions(questions: pd.DataFrame = None, input_file: str = None, question_type: QuestionType = None, has_header: bool = True) -> pd.DataFrame:
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

    pass

