from dsci524_group13_quizit.load_questions import QuestionType, load_questions
import os
import pandas as pd
import pytest

def test_load_questions_empty_csv():
    """Test loading from an empty CSV file."""
    empty_csv_path = "tests/empty.csv"
    with open(empty_csv_path, "w") as f:
        pass  

    with pytest.raises(ValueError, match="The CSV file is empty."):
        load_questions(input_file=empty_csv_path)
    
    os.remove(empty_csv_path)  # Clean up

def test_load_questions_empty_dataframe():
    """Test loading from an empty pandas DataFrame."""
    empty_df = pd.DataFrame()
    with pytest.raises(ValueError, match="The provided DataFrame is empty."):
        load_questions(questions=empty_df)

def test_load_questions_invalid_file_path():
    with pytest.raises(FileNotFoundError):
        load_questions(input_file="invalid_path.csv", question_type=QuestionType.MULTIPLE_CHOICE)

def test_load_questions_invalid_file_type():
    with pytest.raises(ValueError):
        load_questions(input_file="invalid_file.txt", question_type=QuestionType.MULTIPLE_CHOICE)

def test_load_questions_invalid_question_type():
    with pytest.raises(TypeError):
        load_questions(input_file="questions.csv", question_type="essay")

def test_load_questions_invalid_dataframe_type():
    with pytest.raises(TypeError):
        load_questions(questions=["invalid", "data"], question_type=QuestionType.SHORT_ANSWER)

def test_load_questions_missing_question_type():
    with pytest.raises(ValueError):
        load_questions(input_file="questions.csv", question_type=None)

def test_load_questions_invalid_dataframe_structure():
    invalid_df = pd.DataFrame({"InvalidColumn": [1, 2, 3]})
    with pytest.raises(ValueError):
        load_questions(questions=invalid_df, question_type=QuestionType.MULTIPLE_CHOICE)