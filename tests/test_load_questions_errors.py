from dsci524_group13_quizit.question_type import QuestionType
import os
import pandas as pd
import pytest

def test_load_questions_empty_csv(quizit_object):
    """Test loading from an empty CSV file."""
    empty_csv_path = "tests/test_data/empty.csv"
    with open(empty_csv_path, "w") as f:
        pass  

    with pytest.raises(ValueError, match="The input file is empty."):
        quizit_object.load_questions(input_file=empty_csv_path)
    
    os.remove(empty_csv_path)  # Clean up

def test_load_questions_empty_dataframe(quizit_object):
    """Test loading from an empty pandas DataFrame."""
    empty_df = pd.DataFrame()
    with pytest.raises(ValueError, match="The input DataFrame cannot be empty."):
        quizit_object.load_questions(questions=empty_df)

def test_load_questions_invalid_file_path(quizit_object):
    with pytest.raises(FileNotFoundError):
        quizit_object.load_questions(input_file="invalid_path.csv", question_type=QuestionType.MULTIPLE_CHOICE)

def test_load_questions_invalid_file_type(quizit_object, invalid_file_path):
    with pytest.raises(ValueError):
        quizit_object.load_questions(input_file=invalid_file_path, question_type=QuestionType.MULTIPLE_CHOICE)

def test_load_questions_invalid_question_type(quizit_object):
    with pytest.raises(FileNotFoundError):
        quizit_object.load_questions(input_file="questions.csv", question_type="essay")

def test_load_questions_invalid_dataframe_type(quizit_object):
    with pytest.raises(TypeError):
        quizit_object.load_questions(questions=["invalid", "data"], question_type=QuestionType.SHORT_ANSWER)

def test_load_questions_missing_question_type(quizit_object, shrtq_file_path):
    with pytest.raises(ValueError):
        quizit_object.load_questions(input_file=shrtq_file_path, question_type=None)

def test_load_questions_invalid_dataframe_structure(quizit_object):
    invalid_df = pd.DataFrame({"InvalidColumn": [1, 2, 3]})
    with pytest.raises(ValueError):
        quizit_object.load_questions(questions=invalid_df, question_type=QuestionType.MULTIPLE_CHOICE)