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
        'question': ['What is Python?'],
        'answers': ['python']
    })
    return quiz


def test_take_short_answer_not_enough_questions(quizit):
    """
    Test for raising ValueError when there are not enough questions.
    """
    with pytest.raises(ValueError):
        quizit.take_short_answer(n=5)


def test_take_short_answer_no_questions_loaded():
    """
    Test for raising ValueError when no questions are loaded.
    """
    quizit = Quizit()
    quizit.shrtq = None  
    with pytest.raises(ValueError):
        quizit.take_short_answer(n=1)


def test_save_score(quizit):
    """
    Test saving the score to a file and verifying its content.
    """
    file_path = 'test/path'
    score = 85.5
    time_used = 120.5
    score_rec = f"{score}% | {time_used}s\n"
    
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    
    file = os.path.join(file_path, "score.txt")
    
    with open(file, "a") as f:
        f.write(score_rec)

    with open(file, 'r') as f:
        saved_content = f.read()

    assert score_rec in saved_content


def test_save_question_log(quizit):
    """
    Test logging correct and incorrect answers to separate files.
    """
    file_path = 'test/path'
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    
    correct_answers = ['What is Python?']
    incorrect_answers = ['What is 2+2?']

    correct_file = os.path.join(file_path, "correct_answers.txt")
    incorrect_file = os.path.join(file_path, "incorrect_answers.txt")

    with open(correct_file, 'a') as f:
        f.write(f"Question: What is Python?\n")
        f.write(f"Correct Answer: python\n")
        f.write(f"Your Answer: python\n")
        f.write("=" * 30 + "\n")

    with open(incorrect_file, 'a') as f:
        f.write(f"Question: What is 2+2?\n")
        f.write(f"Correct Answer: 4\n")
        f.write(f"Your Answer: 5\n")
        f.write("=" * 30 + "\n")

    with open(correct_file, 'r') as f:
        correct_content = f.read()
    assert "What is Python?" in correct_content
    assert "Your Answer: python" in correct_content

    with open(incorrect_file, 'r') as f:
        incorrect_content = f.read()
    assert "What is 2+2?" in incorrect_content
    assert "Your Answer: 5" in incorrect_content


def test_edge_case_empty_questions():
    """
    Test for raising ValueError when there are no questions available.
    """
    quizit = Quizit()
    quizit.shrtq = pd.DataFrame()  

    with pytest.raises(ValueError):
        quizit.take_short_answer(n=1)


def test_take_short_answer_with_edge_case_empty_question():
    """
    Test for raising ValueError with an empty question set.
    """
    quizit = Quizit()
    quizit.shrtq = pd.DataFrame()  

    with pytest.raises(ValueError):
        quizit.take_short_answer(n=1)

