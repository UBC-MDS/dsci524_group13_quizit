from dsci524_group13_quizit.question_type import QuestionType, QUESTION_COLUMN_MAPPING
import pandas as pd

def _validate_question_format(question_type: QuestionType, has_header: bool, questions: pd.DataFrame):
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
    delimiter : bool, optional
        The delimiter of the `answers` and `options` for the 'multiple choice' questions.
    
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
    
    
def load_questions_from_file(input_file: str, question_type: QuestionType, has_header: bool = True, delimiter: str = None) -> pd.DataFrame:
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
    delimiter : bool, optional
        The delimiter of the `answers` and `options` for the 'multiple choice' questions. Default is None.
    
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
            questions = pd.read_csv(input_file, header=header)
        except ValueError:
            raise ValueError("The input file is empty.")
        
        _validate_question_format(question_type=question_type, has_header=has_header, questions=questions)
        return questions

    except FileNotFoundError:
        raise FileNotFoundError(f"The file at {input_file} was not found.")


def load_questions_from_dataframe(questions: pd.DataFrame, question_type: QuestionType, has_header: bool = True, delimiter: str = None) -> pd.DataFrame:
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
    delimiter : bool, optional
        The delimiter of the `answers` and `options` for the 'multiple choice' questions. Default is None.
    
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
    
    return _validate_question_format(question_type=question_type, has_header=has_header, questions=questions)
