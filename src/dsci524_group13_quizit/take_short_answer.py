def take_short_answer(questions: list) -> dict:
    """
    Allows the user to take a short-answer quiz and evaluates their score.
    
    This feature displays a series of short-answer questions to the user. The user must provide their own replies for each inquiry. 
    The function compares the user's response with the proper answer to each question. The system calculates the user's score based on 
    the correctness of their replies and provides a summary with the list of properly answered and poorly answered questions.

    Parameters:
        questions (list): A list of short-answer question dictionaries or objects. Each question should have the following fields:
            - question_text (str): The question prompt.
            - correct_answer (str): The correct answer for the short-answer question.
            - question_type (str): Should be 'short_answer'.

    Returns:
        dict: A dictionary containing the user's performance:
            - score (float): The percentage of correct answers.
            - correct_answers (list): A list of questions that were answered correctly.
            - incorrect_answers (list): A list of questions that were answered incorrectly.

    Raises:
        ValueError: If the `questions` list is empty, the function will raise an error as there are no questions to quiz.
        TypeError: If the items in the `questions` list are not in the expected format (e.g., missing necessary fields).

    Example:
        take_short_answer(questions)
        # Returns a dictionary like:
        # {
        #     'score': 100.0,
        #     'correct_answers': ['xxx'],
        #     'incorrect_answers': []
        # }
    """
    pass
