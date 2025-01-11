class Quizit():
    def __init__(self):
        self.mcq = None
        self.shrtq = None
        pass
    def load_questions(self):
        pass
    def take_multiple_choice(self, n, save_questions=False, save_score=False):
        """
        Conducts a multiple-choice quiz and provides optional result tracking.

        This method randomly selects `n` questions from the question bank and 
        prompts the user to answer one question at a time. At the end of the quiz, 
        the function will display the total score and the time taken.

        Optional logging and score saving:
        - If `save_score` is True, the final score and time spent are saved to a file.
        - If `save_questions` is set to "all", "incorrect", or "correct", it saves the 
        corresponding questions (with their options, user answers, correct answers, and explanations) 
        to a log file.

        Parameters:
        -----------
        n : int
            The number of questions to randomly select from the question bank.
            If `n` exceeds the total number of questions in the bank, all available questions are used.
            
        save_questions : str or bool, optional (default=False)
            Specifies which questions to save to a log file.
            - "all": Saves all answered questions.
            - "incorrect": Saves only the incorrect questions.
            - "correct": Saves only the correct questions.
            - False: No questions are saved.

        save_score : bool, optional (default=False)
            If True, saves the final quiz score and the time taken to a file.

        Returns:
        --------
        results : str
            A summary of the quiz, including the final score and the time used to complete the quiz.

        Example:
        --------
        question = pd.DataFrame({
            "Question": ["What is 1 + 1?"],
            "A": [1], "B": [2], "C": [3], "D": [4], "Answer": [2], "Explanation": ["1 + 1 = 2"]
        })
        mc_quiz = Quizit(question, type="mcq")
        mc_quiz.take_multiple_choice(1, save_questions="incorrect", save_score=True)
        """
        pass

    def take_short_answer(self):
        pass