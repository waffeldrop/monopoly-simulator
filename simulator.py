import random as rd
from bisect import bisect_left

# TODO fix the secret and community cards, changing them to a more sensible system.
# TODO add more options to Simulation.visualize()
# TODO minor optimizations to play() function in class Game

"""
This program simulates Monopoly games, returning the most visited spots.
"""


def check_type_error(expected_type, *args):
    """Raises error if any of the arguments in args isn't of expected_type

    :param expected_type: Type to be checked against every var in args
    :param args: arguments to be checked agaisnt expected_type
    
    :type expected_type: Varies
    :type args: list of varying types
    
    :returns: None
    
    :raises TypeError: if var isn't of expected_type
    """
    for var in args:
        if not isinstance(var, expected_type):
            raise TypeError(f"{var} must be {expected_type}")


class Simulation:
    idx = 0
    gooj = False
    jailed = False

    def __init__(self, num_of_simulations, turns_per_simulation):
        """Values we are going to need to simulate Monopoly games
        
        :param num_of_simulations: Defines how many simulations we are going to run
        :param turns_per_simulation: Defines how many turns (dice rolls) a simulation goes through
        
        :type num_of_simulations: int
        :type turns_per_simulation: int
        
        :returns: None
        """
        check_type_error(int, num_of_simulations, turns_per_simulation)
        self.sims = num_of_simulations
        self.turns = turns_per_simulation
        self.simulated_games = None
    
    def print_dict(self):
        self.run()
        visualize_dict = self.visualize()
        
        for i in visualize_dict:
            print(f"spot={i} "
                  f"visits={visualize_dict[i]}")

    def run(self):
        """
        Runs n amounts of custom games with o turns where n = self.sims (num_of_simulations) and o = self.turns
        Also takes in self variables for initial_idx, gooj, jailed
        
        :returns: list of lists detailing every spot visited in every game
        """
        game1 = Game(self.turns, self.idx, self.gooj, self.jailed)
        self.simulated_games = [game1.play() for _ in range(self.sims)]
        return self.simulated_games
        
    def visualize(self, sort=True, reverse=True):
        """
        Visualizes the result of self.simulated_games
        
        :param sort: Defaults to True, defines wheter to return a sorted or unsorted dict
        :param reverse: Defaults to True, defines whether to return a dict with counting or reverse counting order vals
        
        :type sort: bool
        :type reverse: bool
        
        :return: varies
        """
        lst = [spot for lst_of_spots in self.simulated_games for spot in lst_of_spots]
        tmp = list(set(lst))
        visits = {item: lst.count(item) for item in tmp}
        
        if sort:
            return {key: visits[key] for key in sorted(visits, key=visits.get, reverse=reverse)}
        
        else:
            return lst


class Game:
    comm_chest = [0, 10,
                  True]
    
    secret_chest = [0, 5, 10, 11, 24, 39,
                    [12, 28], [5, 15, 25, 35],
                    True,
                    "-3"]
    
    comm_chest.extend(None for x in range(14))
    secret_chest.extend(None for x in range(6))
    
    def __init__(self, turns, initial_idx, initial_gooj_card, initial_jailed):
        """
        Values used to play a game of monopoly
        
        :param turns: Defines how many turns we play
        :param initial_idx: Defines where in the board we start (for reference, 0=GO!, 10=JAIL, 20=PARK, 30=GO TO JAIL)
        :param initial_gooj_card: Defines if we have the "get out of jail free" card at the start
        :param initial_jailed: Defines if we are jailed at the start, if so our initial_idx is 10 (JAIL)
        
        :type turns: int
        :type initial_idx: int
        :type initial_gooj_card: bool
        :type initial_jailed: bool
        
        :returns: None
        """
        check_type_error(int, turns, initial_idx)
        check_type_error(bool, initial_gooj_card, initial_jailed)
        if not initial_jailed:
            self.idx = initial_idx

        else:
            self.idx = 10

        self.turns = turns
        self.gooj = initial_gooj_card
        self.jailed = initial_jailed

    def card_test(self, card):
        """
        Function that changes variables in the class in accordance to what cards we draw in the chests in-game
        
        :param card: The card we drew
        
        :type card: varies
        
        :returns: None
        """
        
        if card:
            # If card is True we get a "get out of jail free" card
            self.gooj = True
    
        elif isinstance(card, int):
            # If card is type int we move to that position
            self.idx = card
    
        elif isinstance(card, str):
            # If card is type str, we convert it to int and add it to our current position
            self.idx += int(card)
    
        elif isinstance(card, list):
            # If card is type list, we go to the spot closest to our current position in list (see: def closest())
            self.idx = self.closest(card, self.idx)
    
    def play(self):
        """
        Plays a game of monopoly, returning a list of all spots visited in the game
        
        :returns: list of int where int is every spot visited in the game.
        """
        visited = []
        
        for turn in range(self.turns):
            if not self.jailed:
                self.idx += self.dice_roll()
                
                if self.idx >= 40:
                    self.idx -= 40
                    
                if self.idx == 30:
                    self.idx = 10
                    self.jailed = True
                
                if self.idx in [2, 17, 33]:
                    self.card_test(rd.choice(self.comm_chest))

                elif self.idx in [7, 22, 36]:
                    self.card_test(rd.choice(self.secret_chest))

            else:
                if self.gooj:
                    self.jailed = False

                else:
                    tmp = self.dice_roll()
                    if tmp == self.dice_roll():
                        self.jailed = False
                        self.idx += tmp
            visited.append(self.idx)
        return visited

    @staticmethod
    def dice_roll():
        """
        Returns a random number from 1 to 6, simulating a dice roll.

        :returns: random int from 1 to 6
        """
        return rd.randint(1, 6)

    @staticmethod
    def closest(lst, num):
        """
        Returns the integer closest to num in lst

        :param lst: List to be checked to find closest to num
        :param num: Number to be checked to find closest to in lst

        :type lst: list of int
        :type num: int

        :returns: int from lst closest to num
        """
        pos = bisect_left(lst, num)
        if pos == 0:
            return lst[0]
        if pos == len(lst):
            return lst[-1]
        before = lst[pos - 1]
        after = lst[pos]
        if after - num < num - before:
            return after
        else:
            return before
