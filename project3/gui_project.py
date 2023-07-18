"""

Name:      Minh Vu
Email:     minh.vu@tuni.fi

This GUI program simulates the rock-paper-scissor game
between 2 players. However, this program only represents the
randomness of the game, not the strategic side of the game
(if it has ^_^). By default, the "special rule" checkbox is
unchecked, and the game will be played in a normal sense as
following: Each time the user click the button "GO!", the program
randomly generate an option (rock/paper/scissor) for each player.
As usual, rock beats scissor, paper beats rock and scissor beats paper.
For each round a player win, that player will gain 1 point, and whoever
achieves 10 points first will win the game.

If the "special rule" checkbox is checked, the game will be performed
in a different way of calculating point, which means that the only difference is
how much points a player gains from the winning round. If a player wins by using
rock, 3 points are gained. 2 points are gained for a winning round using scissor,
and if the player wins by using paper, only 1 point is gained. Moreover, if a player's
total point will exceed 10 after winning round, the current point will be deducted
by 2, which means that a player can only win the game with exact 10 points.

Also, the program have a "Quit" button that close the whole game and a
"Reset" button that will reset the whole game, which means that each
player's total point will be 0 and the "special rule" checkbox in unchecked.


"""

from tkinter import *
import random


# Constants
STRIKE_IMAGE_FILES = ["rock.gif", "paper.gif", "scissor.gif"]
LOAD_IMAGE_FILES = ["1.gif", "2.gif"]
Points_to_win = 10
ROCK_POINTS = 3
SCISSOR_POINTS = 2
PAPER_POINTS = 1


class RPSGame:
    def __init__(self):
        self.__main_window = Tk()
        self.__main_window.title("Rock-Paper-Scissor")

        # Define fonts for labels and buttons
        normal_font = ('Arial', 12)
        bold_font = ('Arial', 12, 'bold')

        # attribute used in displaying images
        self.__update_counter = 0

        # load images
        self.__loading_images = []
        for image in LOAD_IMAGE_FILES:
            load_image = PhotoImage(file=image)
            self.__loading_images.append(load_image)

        # strike images
        self.__strikes_images = []
        for image_file in STRIKE_IMAGE_FILES:
            strike_image = PhotoImage(file=image_file)
            self.__strikes_images.append(strike_image)

        self.__empty_image = PhotoImage(width=250, height=250)

        # Checkbox for special rule
        self.__special_rule_var = BooleanVar()
        self.__special_rule_checkbox = Checkbutton(self.__main_window, text="SPECIAL RULE",
                                                   variable=self.__special_rule_var, command=self.check_or_uncheck,
                                                   font=normal_font)

        # Buttons
        self.__start_button = Button(self.__main_window, text="GO!", command=self.start, font=normal_font, relief=RAISED
                                     , background="green", borderwidth=5)
        self.__reset_button = Button(self.__main_window, text="RESET", command=self.new_game, font=normal_font,
                                     relief=RAISED, borderwidth=5, background="yellow")
        self.__quit_button = Button(self.__main_window, text="QUIT", command=self.quit, font=normal_font, relief=RAISED,
                                    background="red", borderwidth=5)

        # Labels
        self.__player1_title_label = Label(self.__main_window, text="PLAYER 1", font=normal_font)
        self.__player2_title_label = Label(self.__main_window, text="PLAYER 2", font=normal_font)
        self.__player1_points_title_label = Label(self.__main_window, text="TOTAL POINTS:", font=bold_font)
        self.__player2_points_title_label = Label(self.__main_window, text="TOTAL POINTS:", font=bold_font)
        self.__player1_points_label = Label(self.__main_window, width=2, font=bold_font)
        self.__player2_points_label = Label(self.__main_window, width=2, font=bold_font)
        self.__player1_points_comment_label = Label(self.__main_window, text="",
                                                    font=bold_font)  # announce points deduction
        self.__player2_points_comment_label = Label(self.__main_window, text="",
                                                    font=bold_font)  # announce points deduction
        self.__winner_label = Label(self.__main_window, text="", font=bold_font)  # announce the winner
        self.__player1_strike_label = Label(self.__main_window, width=260, anchor=E)
        self.__player2_strike_label = Label(self.__main_window, width=260, anchor=W)
        self.__instruction_label = Label(self.__main_window, font=normal_font, height=3,
                                         width=30)  # special rule's gaining point mechanism

        # placing all the components into a grid
        self.__start_button.grid(row=0, column=2, pady=20)
        self.__player1_title_label.grid(row=1, column=0, columnspan=2, sticky=E + W)
        self.__player2_title_label.grid(row=1, column=3, columnspan=2, sticky=E + W)
        self.__player1_strike_label.grid(row=2, column=0, columnspan=2,  pady=20, sticky=E)
        self.__player2_strike_label.grid(row=2, column=3, columnspan=2,  pady=20, sticky=W)
        self.__player1_points_title_label.grid(row=3, column=0, sticky=E)
        self.__player2_points_title_label.grid(row=3, column=3, sticky=E)
        self.__player1_points_label.grid(row=3, column=1, sticky=W)
        self.__player2_points_label.grid(row=3, column=4, sticky=W)
        self.__player1_points_comment_label.grid(row=4, column=0, columnspan=2, sticky=E + W)
        self.__player2_points_comment_label.grid(row=4, column=3, columnspan=2, sticky=E + W)
        self.__winner_label.grid(row=5, column=0, columnspan=5, sticky=E + W)
        self.__reset_button.grid(row=10, column=0, columnspan=2, sticky=S + N + E + W)
        self.__quit_button.grid(row=10, column=3, columnspan=2, sticky=S + N + E + W)
        self.__special_rule_checkbox.grid(row=6, column=2)
        self.__instruction_label.grid(row=7, column=2, rowspan=3, sticky=N)

        # Initialize game state variables
        self.__player1_deduct = False
        self.__player2_deduct = False

        self.new_game()

        self.__main_window.mainloop()

    def check_or_uncheck(self):
        """"
        manipulate program's behavior based on the
        state of the checkbox (checked or unchecked)

        :return: None
        """

        if self.__special_rule_var.get():
            self.new_game()
            self.__special_rule_checkbox.select()
            self.__instruction_label["text"] = "3 points for winning with rock\n2 points for winning with scissor" \
                                               "\n1 point for winning with paper"
        else:
            self.new_game()

    def new_game(self):
        """
        Start a new game when the program runs or
        every time the reset button is clicked

        :return: None
        """

        self.__player1_points = 0
        self.__player2_points = 0
        self.__player1_strike_label["image"] = self.__empty_image
        self.__player2_strike_label["image"] = self.__empty_image
        self.__instruction_label["text"] = ""
        self.updated_ui()

        # Activate the buttons that would be deactivated after game_over
        self.__start_button.configure(state=NORMAL)
        self.__special_rule_checkbox.configure(state=NORMAL)

        # The Checkbox is unchecked by default and when the game is reset
        self.__special_rule_checkbox.deselect()

    def updated_ui(self):
        """
        Update the user interface every time a new game is created
        or when the user click the "GO!" button

        :return: None
        """

        self.__player1_points_label["text"] = self.__player1_points
        self.__player2_points_label["text"] = self.__player2_points
        self.__update_counter = 0
        self.__winner_label["text"] = ""

        if self.__player1_deduct:
            self.__player1_points_comment_label["text"] = "DEDUCT 2 POINTS"
        else:
            self.__player1_points_comment_label["text"] = ""

        if self.__player2_deduct:
            self.__player2_points_comment_label["text"] = "DEDUCT 2 POINTS"
        else:
            self.__player2_points_comment_label["text"] = ""

    def start(self):
        """
        Manipulate the program's behavior when the
        "GO!" button is clicked

        :return: None
        """

        # generate the load images for both players
        if self.__update_counter < 5:
            self.__player1_strike_label.configure(image=self.__loading_images[self.__update_counter % 2])
            self.__player2_strike_label.configure(image=self.__loading_images[self.__update_counter % 2])
            self.__update_counter += 1
            self.__main_window.after(250, self.start)

        # randomly generate the strike images for each player
        else:
            player1_choice_index = random.randint(0, 2)
            player2_choice_index = random.randint(0, 2)
            self.__player1_strike_label["image"] = self.__strikes_images[player1_choice_index]
            self.__player2_strike_label["image"] = self.__strikes_images[player2_choice_index]

            # finding out which player has won the round
            self.winning_round(player1_choice_index, player2_choice_index)
            # update the user interface accordingly
            self.updated_ui()
            # check if any of the players has won the game or not
            self.game_over()

    def winning_round(self, player1_choice, player2_choice):
        """
        Determines the winner of a round based on the choices made by two players.
        Updates the points of the respective players accordingly.

        :param player1_choice: The choice made by player 1 (0 for Rock,
        1 for Paper, 2 for Scissors)
        :param player2_choice: The choice made by player 2 (0 for Rock,
        1 for Paper, 2 for Scissors)
        :return: None
        """

        self.__player1_deduct = False
        self.__player2_deduct = False

        # Define the winning conditions for player 1
        player1_win = {(0, 1): False, (1, 2): False, (2, 0): False, (1, 0): True, (2, 1): True, (0, 2): True}

        if not self.__special_rule_var.get():
            # Normal gameplay mode
            if (player1_choice, player2_choice) in player1_win:
                # Player 1 wins the round
                if player1_win[player1_choice, player2_choice]:
                    self.__player1_points += 1
                # Player 2 wins the round
                else:
                    self.__player2_points += 1
            else:
                # The round is a tie
                pass

        else:
            # Special gameplay mode
            if (player1_choice, player2_choice) in player1_win:
                # Apply special rules for determining the winner
                self.winning_special_rule(player1_choice, player2_choice)
            else:
                # The round is a tie
                pass

    def winning_special_rule(self, player1_choice, player2_choice):
        """
        Applies special rules to determine the winner of a round in a special gameplay mode.

        :param player1_choice: The choice made by player 1 (0 for Rock,
        1 for Paper, 2 for Scissors)
        :param player2_choice: The choice made by player 2 (0 for Rock,
         1 for Paper, 2 for Scissors)
        :return: None
        """

        # if player 1 wins
        if (player1_choice, player2_choice) == (1, 0):
            self.__player1_points += 1
        elif (player1_choice, player2_choice) == (2, 1):
            # Check if adding SCISSOR_POINTS would exceed the points needed to win
            if (self.__player1_points + SCISSOR_POINTS) > Points_to_win:
                self.__player1_points -= 2
                self.__player1_deduct = True
            else:
                self.__player1_points += SCISSOR_POINTS
        elif (player1_choice, player2_choice) == (0, 2):
            # Check if adding ROCK_POINTS would exceed the points needed to win
            if (self.__player1_points + ROCK_POINTS) > Points_to_win:
                self.__player1_points -= 2
                self.__player1_deduct = True
            else:
                self.__player1_points += ROCK_POINTS

        # if player 2 wins
        elif (player1_choice, player2_choice) == (0, 1):
            self.__player2_points += 1
        elif (player1_choice, player2_choice) == (1, 2):
            # Check if adding SCISSOR_POINTS would exceed the points needed to win
            if (self.__player2_points + SCISSOR_POINTS) > Points_to_win:
                self.__player2_points -= 2
                self.__player2_deduct = True
            else:
                self.__player2_points += SCISSOR_POINTS
        else:
            # Check if adding ROCK_POINTS would exceed the points needed to win
            if (self.__player2_points + ROCK_POINTS) > Points_to_win:
                self.__player2_points -= 2
                self.__player2_deduct = True
            else:
                self.__player2_points += ROCK_POINTS

    def game_over(self):
        """
        Checking if any of the players has won a game or not

        :return: None
        """

        if self.__player1_points == Points_to_win or self.__player2_points == Points_to_win:
            if self.__player1_points > self.__player2_points:
                self.__winner_label.configure(text="PLAYER 1 HAS WON!")
            else:
                self.__winner_label.configure(text="PLAYER 2 HAS WON!")

            self.__start_button.configure(state=DISABLED)
            self.__special_rule_checkbox.configure(state=DISABLED)
        else:
            pass

    def quit(self):
        """
        Terminate the program

        :return: None
        """

        self.__main_window.destroy()


def main():
    game = RPSGame()


if __name__ == "__main__":
    main()
