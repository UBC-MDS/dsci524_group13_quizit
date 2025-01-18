from dsci524_group13_quizit.quizit import Quizit
import pytest
import pandas as pd


MCQ_FILE_PATH = "tests/test_data/multiple_choice.csv"
SHRTQ_FILE_PATH = "tests/test_data/short_answer.csv"
INVALID_FILE_PATH = "tests/test_data/invalid_file.txt"
MCQ_COLUMNS = ["question", "options", "answers", "explanations"]
SHRTQ_COLUMNS = ["question", "answers", "explanations"]

@pytest.fixture
def invalid_file_path():
    return INVALID_FILE_PATH

@pytest.fixture
def mcq_file_path():
    return MCQ_FILE_PATH

@pytest.fixture
def shrtq_file_path():
    return SHRTQ_FILE_PATH

@pytest.fixture
def mcq_columns():
    return MCQ_COLUMNS

@pytest.fixture
def shrtq_columns():
    return SHRTQ_COLUMNS

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