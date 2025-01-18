class Quizit():
    """
    A class to manage and conduct custom quizzes with multiple-choice and short-answer questions.
    
    This class allows users to load multiple-choice and short-answer question sets, and take multiple-choice or short-answer quizzes. 
    The quiz can save the user's score, and optionally log the answered questions and their correctness.
    """
    def __init__(self):
        """
        Initializes a new instance of the Quizit class.

        Attributes:
        -----------
        mcq : list, optional
            A collection of multiple-choice questions.

        shrtq : list, optional
            A collection of short-answer questions.

        Example:
        --------
        quiz = Quizit()
        """    
        self.mcq = None
        self.shrtq = None

    def take_short_answer(self, n, save_questions=False, save_score=False) -> dict:
        """
        Allows the user to take a short-answer quiz and evaluates their score.

        This function displays a series of short-answer questions to the user. The user must provide their own replies for each inquiry. 
        The function compares the user's response with the proper answer to each question. The system calculates the user's score based on 
        the correctness of their replies and provides a summary with the list of correctly answered and incorrectly answered questions.
        Additionally, it writes out the correct answers to one file and the incorrect answers to a different file.

        Parameters:
            n (int): The number of questions to present in the quiz.
            save_questions (bool): If True, saves the questions answered correctly or incorrectly to two different files.
            save_score (bool): If True, saves the score to a file.

        Returns:
            dict: A dictionary containing the user's performance:
                - score (float): The percentage of correct answers.
                - correct_answers (list): A list of questions that were answered correctly.
                - incorrect_answers (list): A list of questions that were answered incorrectly.

        Raises:
            ValueError: If the questions list is empty or None, the function will raise an error as there are no questions to quiz.
            TypeError: If the items in the questions list are not in the expected format (e.g., missing necessary fields).
        """
        if self.shrtq is None:
            raise ValueError("No short answer questions loaded.")
        
        if n > len(self.shrtq):
            raise ValueError(f"Not enough questions available. Only {len(self.shrtq)} questions loaded.")
        
        quiz = self.shrtq.sample(n)
        question = quiz["question"]
        answers = quiz["answers"]
        quiz["response"] = ""

        score = []
        correct_answers = []
        incorrect_answers = []

        start = time.time()
        for i in range(len(question)):
            print(f"Question {i+1}: {question.iloc[i]}")
            
            correct_answer = answers.iloc[i].lower()
            words = correct_answer.split()
            if len(words) == 1:
                print("Hint: Your answer must be one word.")
            elif len(words) == 2:
                print("Hint: Your answer must be two words.")
            
            user_input = input("Enter Answer: ").strip().lower()
            
            while len(user_input.split()) not in [1, 2]:
                print("Invalid answer. The answer must be either one word or two words.")
                user_input = input("Enter Answer: ").strip().lower()

            if user_input == correct_answer:
                score.append(1)
                quiz.loc[[i], "response"] = user_input
                correct_answers.append(question.iloc[i])
            else:
                score.append(0)
                quiz.loc[[i], "response"] = user_input
                incorrect_answers.append(question.iloc[i])

        time_used = time.time() - start
        score_percent = round(sum(score) / n * 100, 2)
        score_rec = {"date": time.asctime(), "pct_score": score_percent, "time_used": round(time_used, 2)}

        print("===============================")
        print("Quiz Results")
        print(f"Score: {sum(score)}/{n} ({score_percent}%)")
        print(f"Time used: {round(time_used, 2)} seconds")
        print(score_rec)
