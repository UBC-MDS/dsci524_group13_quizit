import pytest
import os
import pandas as pd
from io import StringIO
from dsci524_group13_quizit.take_short_answer import Quizit, QuizResult

@pytest.fixture
def quizit():
    """
    Fixture to initialize a Quizit object with a sample question.
    """
    quiz = Quizit()
    quiz.shrtq = pd.DataFrame({
        'question': ['What is Python?', 'What is 2+2?'],
        'answers': ['python', '4']
    })
    return quiz

def test_take_short_answer_negative_questions(quizit):
    """
    Test taking a quiz with a negative number of questions.
    """
    with pytest.raises(ValueError):
        quizit.take_short_answer(n=-1)

def test_take_short_answer_empty_questions():
    """
    Test taking a quiz with no questions loaded.
    """
    quizit = Quizit()
    quizit.shrtq = pd.DataFrame()
    with pytest.raises(ValueError):
        quizit.take_short_answer(n=1)

def test_take_short_answer_n_greater_than_available(quizit):
    """
    Test taking a quiz with more questions than available.
    """
    with pytest.raises(ValueError):
        quizit.take_short_answer(n=10)

def test_quiz_result_initialization():
    """
    Test the initialization of the QuizResult class.
    """
    quiz_summary = pd.DataFrame({
        'question': ['What is Python?'],
        'answers': ['python'],
        'response': ['python']
    })
    result = QuizResult(time_used=10.5, score=100.0, question_summary=quiz_summary, question_type="shrtq")
    
    assert result.time_used == 10.5
    assert result.score == 100.0
    assert result.question_summary.equals(quiz_summary)
    assert result.question_type == "shrtq"


def test_take_short_answer_no_save(quizit, monkeypatch, tmpdir):
    """
    Test that no files are saved when save_score and save_questions are False.
    """
    # Mock user input
    monkeypatch.setattr('builtins.input', lambda _: "python")
    file_path = tmpdir.mkdir("test_no_save")
    result = quizit.take_short_answer(n=1, save_score=False, save_questions=False, file_path=str(file_path))

    assert not file_path.join("score.txt").exists()
    assert not file_path.join("correct_answers.txt").exists()
    assert not file_path.join("incorrect_answers.txt").exists()