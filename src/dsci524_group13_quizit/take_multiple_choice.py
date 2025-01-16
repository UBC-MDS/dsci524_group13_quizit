import numpy as np
import pandas as pd
import string as str
import time
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
            If True, save the final quiz score and the time taken to a file.

        Returns:
        --------
        results : str
            A summary of the quiz, including the final score and the time used to complete the quiz.

        Example:
        --------
        quiz.take_multiple_choice(10, save_questions="incorrect", save_score=True)
        """
        if self.mcq == None:
            raise ValueError("No multiple choice questions loaded.")
        try:
            quiz = np.random.choice(self.mcq, n, replace=False)
        except:
            quiz = self.mcq
        

        question = quiz["questions"]
        options = quiz["options"]
        answers = quiz["answers"]
        explanations = quiz["explanations"]
        quiz["response"] = ""
        score = []

        start = time.time()
        for i in range(questions.shape[0]):
            options_dict = {}
            print(questions[i])
            n_options = list(str.ascii_uppercase[0:len(options[i])])
            for j in range(len(n_options)):
                print(n_options[j], ":", options[i][j])
                options_dict[n_options[j]] = options[i][j]     
            count = 0
            user_input = input("Enter Answer:\n")
            user_input = user_input.upper().replace(" ", "").split(",")
            right = [key for key, val in options_dict.items() if val in answers[i]]
            wrong = [key for key, val in options_dict.items() if val not in answers[i]]
            while count <= 2:
                if all(ele in n_options for ele in user_input):
                    print("Your Answer:", user_input)
                    break
                elif count < 2:
                    print("Your Answer:", user_input)
                    print("Invalid answer, choose from the options")
                    count += 1
                    user_input = input()
                    user_input = user_input.upper().replace(" ", "").split(",")
                elif count == 2:
                    print("Your Answer:", user_input)
                    print("Invalid answer, Maximum attempts reached, Proceed to next question.")
                    user_input = [""] 
                    break
            quiz.loc[[i],["response"]] = user_input
            if user_input != [""]:
                q_score = round((sum([rt in user_input for rt in right]) + sum([wrg not in user_input for wrg in wrong]))/len(n_options),2)
            else:
                q_score = 0
            score.append(q_score)
            if q_score != 1:
                wrong_q = pd.concat([wrong_q, quiz.iloc[[i],:]])
            else:
                correct_q = pd.concat([right_q, quiz.iloc[[i],:]])
        time_used = time.time() - start
        score_rec = {"date": time.asctime(), "pct_score": round(sum(score)/questions.shape[0],2), "time_used": round(time_used, 2)}
        print("===============================")
        print("Quiz Results")
        print(f"Score: {sum(score)}/{questions.shape[0]} ({round(sum(score)/questions.shape[0]*100,2)}%)" )
        print("time used:", round(time_used, 2), "seconds")
        print(score_rec)
        pass
