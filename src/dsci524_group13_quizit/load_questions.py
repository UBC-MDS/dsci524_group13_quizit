import pandas as pd
from enum import Enum

class QuestionType(Enum):
    MULTIPLE_CHOICE = "multiple choice"
    SHORT_ANSWER = "short answer"

MCQ_COLUMNS = ["question","options","answers","explanations"]
SHRTQ_COLUMNS = ["question","answers","explanations"]

QUESTION_COLUMN_MAPPING = {
    QuestionType.MULTIPLE_CHOICE: MCQ_COLUMNS,
    QuestionType.SHORT_ANSWER: SHRTQ_COLUMNS
}

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
        
        return _validate_question_format(self, question_type=question_type, has_header=has_header, questions=questions_df, delimeter=delimeter)

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
    
    return _validate_question_format(self, question_type=question_type, has_header=has_header, questions=questions, delimeter=delimeter)


def load_questions(questions: pd.DataFrame = None, input_file: str = None, question_type: QuestionType = None, has_header: bool = True, delimeter: str = None) -> pd.DataFrame:
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
        return load_questions_from_dataframe(questions=questions, question_type=question_type, has_header=has_header, delimeter=delimeter)
    
    if input_file is not None:
        return load_questions_from_file(input_file=input_file, question_type=question_type, has_header=has_header, delimeter=delimeter)
    
    raise ValueError("Please provide either a questions DataFrame or an input file.")

