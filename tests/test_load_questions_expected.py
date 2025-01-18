from dsci524_group13_quizit.load_questions import QuestionType, load_questions
from dsci524_group13_quizit.quizit import Quizit
import os
import pytest
import pandas as pd


MCQ_FILE_PATH = "tests/multiple_choice.csv"
SHRTQ_FILE_PATH = "tests/short_answer.csv"
MCQ_COLUMNS = ["question","options","answers","explanations"]
SHRTQ_COLUMNS = ["question","answers","explanations"]

@pytest.fixture
def quizit_object():
    """Fixture for the quiz"""
    return Quizit()

@pytest.fixture
def mc_questions():
    """Fixture for multiple choice questions"""
    df = pd.read_csv(MCQ_FILE_PATH, header=0)
    return df

@pytest.fixture
def shrt_questions():
    """Fixture for short answer questions"""
    df = pd.read_csv(SHRTQ_FILE_PATH, header=0)
    return df

def validate_dataframe(df, expected_columns, description):
    """
    Helper function to validate a DataFrame.
    
    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame to validate.
    expected_columns : list
        List of expected column names.
    description : str
        Description of the DataFrame being tested (used for error messages).
    """
    assert isinstance(df, pd.DataFrame), f"The input {description} is not a DataFrame; found {type(df)}."
    assert not df.empty, f"The {description} DataFrame is empty."
    assert len(expected_columns) == len(df.columns), (
        f"The {description} DataFrame should have {len(expected_columns)} columns "
        f"but has {len(df.columns)} columns."
    )
    for col in expected_columns:
        assert col in df.columns, f"The {description} DataFrame is missing the column '{col}'."


def test_load_questions_from_csv_multiple_choice(mc_questions):
    """Test loading multiple-choice questions from a CSV file."""
    assert os.path.isfile(MCQ_FILE_PATH), f"The file {MCQ_FILE_PATH} does not exist."
    questions = load_questions(input_file=MCQ_FILE_PATH, question_type=QuestionType.MULTIPLE_CHOICE)
    validate_dataframe(mc_questions, MCQ_COLUMNS, "multiple-choice questions")
    assert mc_questions.equals(questions), "The loaded questions DataFrame does not match the expected DataFrame."

def test_load_questions_from_csv_short_answer(shrt_questions):
    """Test loading short-answer questions from a CSV file."""
    assert os.path.isfile(SHRTQ_FILE_PATH), f"The file {SHRTQ_FILE_PATH} does not exist."
    questions = load_questions(input_file=SHRTQ_FILE_PATH, question_type=QuestionType.SHORT_ANSWER)
    validate_dataframe(shrt_questions, SHRTQ_COLUMNS, "short-answer questions")
    assert shrt_questions.equals(questions), "The loaded questions DataFrame does not match the expected DataFrame."

def test_load_questions_from_dataframe_multiple_choice(mc_questions):
    """Test loading multiple-choice questions from a pandas DataFrame."""
    validate_dataframe(mc_questions, MCQ_COLUMNS, "multiple-choice questions")
    questions = load_questions(questions=mc_questions, question_type=QuestionType.MULTIPLE_CHOICE)
    assert mc_questions.equals(questions), "The loaded questions DataFrame does not match the expected DataFrame."

def test_load_questions_from_dataframe_short_answer(shrt_questions):
    """Test loading short-answer questions from a pandas DataFrame."""
    validate_dataframe(shrt_questions, SHRTQ_COLUMNS, "short-answer questions")
    questions = load_questions(questions=shrt_questions, question_type=QuestionType.SHORT_ANSWER)
    assert shrt_questions.equals(questions), "The loaded questions DataFrame does not match the expected DataFrame."

def test_load_questions_csv_without_header_multiple_choice():
    """Test loading from a CSV file without a header."""
    # Create a temporary CSV without a header
    no_header_path = "tests/no_header.csv"
    no_header_data = "Question1,Option1,Answer1,Explanation1\nQuestion2,Option2,Answer2,Explanation2"
    with open(no_header_path, "w") as f:
        f.write(no_header_data)
    
    questions = load_questions(input_file=no_header_path, question_type=QuestionType.MULTIPLE_CHOICE, has_header=False)
    assert not questions.empty, "The loaded DataFrame should not be empty."
    assert len(questions.columns) == len(MCQ_COLUMNS), "The DataFrame should have 4 columns when loaded without a header."
    
    os.remove(no_header_path)  # Clean up

def test_load_multiple_choice_with_question_type(mc_questions, quizit_object):
    """Test loading and saving multiple-choice questions to the Quizit object."""
    
    validate_dataframe(mc_questions, MCQ_COLUMNS, "multiple-choice questions")
    questions = load_questions(questions=mc_questions, question_type=QuestionType.MULTIPLE_CHOICE, delimeter=";")
    assert mc_questions.equals(questions), "The loaded questions DataFrame does not match the expected DataFrame."
    
    quizit_object.mcq = questions
    
    assert quizit_object.mcq is not None, "The multiple-choice questions were not set in the Quizit object."
    assert isinstance(quizit_object.mcq, pd.DataFrame), "The multiple-choice questions in Quizit object should be a DataFrame."
    assert all(quizit_object.mcq.columns == MCQ_COLUMNS), "The Quizit object's multiple-choice DataFrame has incorrect columns."
    print(quizit_object.mcq['options'].head())
    assert isinstance(quizit_object.mcq['answers'], pd.Series ), f"The multiple-choice answers in Quizit object should be a pandas Series but recieved {type(quizit_object.mcq['answers'])}."
    assert isinstance(quizit_object.mcq['options'], pd.Series), f"The multiple-choice options in Quizit object should be a pandas Series but recieved {type(quizit_object.mcq['options'])}."
    assert isinstance(quizit_object.mcq['options'][0], list), f"The multiple-choice options in Quizit object should contain a list but recieved {type(quizit_object.mcq['options'][0])}."


def test_load_short_answer_with_question_type(shrt_questions, quizit_object):
    """Test loading and saving short answer questions to the Quizit object."""
    
    validate_dataframe(shrt_questions, SHRTQ_COLUMNS, "short answer questions")
    questions = load_questions(questions=shrt_questions, question_type=QuestionType.SHORT_ANSWER)
    assert shrt_questions.equals(questions), "The loaded questions DataFrame does not match the expected DataFrame."
    
    quizit_object.shrt = questions
    
    assert quizit_object.shrt is not None, "The short answer questions were not set in the Quizit object."
    assert isinstance(quizit_object.shrt, pd.DataFrame), "The short answer questions in Quizit object should be a DataFrame."
    assert all(quizit_object.shrt.columns == SHRTQ_COLUMNS), "The Quizit object's short answer DataFrame has incorrect columns."