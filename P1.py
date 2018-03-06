import numpy as np
import scr.FigureSupport as figureLibrary
from enum import Enum
import numpy as np
import scr.SamplePathClass as PathCls
import scr.StatisticalClasses as Stat


class Game(object):
    def __init__(self, id, prob_head):
        self._id = id
        self._rnd = np.random
        self._rnd.seed(id)
        self._probHead = prob_head  # probability of flipping a head
        self._countWins = 0  # number of wins, set to 0 to begin

    def simulate(self, n_of_flips):

        count_tails = 0  # number of consecutive tails so far, set to 0 to begin

        # flip the coin 20 times
        for i in range(n_of_flips):

            # in the case of flipping a heads
            if self._rnd.random_sample() < self._probHead:
                if count_tails >= 2:  # if the series is ..., T, T, H
                    self._countWins += 1  # increase the number of wins by 1
                count_tails = 0  # the tails counter needs to be reset to 0 because a heads was flipped

            # in the case of flipping a tails
            else:
                count_tails += 1  # increase tails count by one

    def get_reward(self):
        # calculate the reward from playing a single game
        return 100*self._countWins - 250


class SetOfGames:

    def __init__(self, prob_head, n_games):
        self._gameRewards = [] # create an empty list where rewards will be stored
        self._prob_head=prob_head
        self._n_games=n_games
    def simulation(self,prob_head, n_games):
        # simulate the games
        for n in range(n_games):
            # create a new game
            game = Game(id=n, prob_head=prob_head)
            # simulate the game with 20 flips
            game.simulate(20)
            # store the reward
            self._gameRewards.append(game.get_reward())


        return CohortOutcomes(self)

    def get_ave_reward(self):
        """ returns the average reward from all games"""
        return sum(self._gameRewards) / len(self._gameRewards)

    def get_reward_list(self):
        """ returns all the rewards from all game to later be used for creation of histogram """
        return self._gameRewards


    def get_max(self):
        """ returns maximum reward"""
        return max(self._gameRewards)

    def get_min(self):
        """ returns minimum reward"""
        return min(self._gameRewards)

    def get_probability_loss(self):
        """ returns the probability of a loss """
        count_loss = 0
        for value in self._gameRewards:
            if value < 0:
                count_loss += 1
        return count_loss / len(self._gameRewards)

class CohortOutcomes:
    def __init__(self,simulated_cohort):
        self._simulatedCohort = simulated_cohort
        self._sumStat_rewards = \
            Stat.SummaryStat('The total rewards', self._simulatedCohort.get_ave_reward())
        self._sumStat_loss = \
            Stat.SummaryStat('The probability of loss', self._simulatedCohort.get_probability_loss())

    def get_CI_expected_rewards(self):
        return self._sumStat_rewards.get_t_CI(alpha)

    def get_CI_probability_loss(self):
        return self._sumStat_loss.get_t_CI(alpha)



class Multicohort:
    def __init__(self, ids, n_games, prob_head):
        self._ids = ids
        self._n_games = n_games
        self._prob_head=prob_head

        self._ExpectedRewards = []
        self._Uncertainty = []
        self._sumStat_meanRewards = []

    def simulate(self, n_times):
        for i in range(len(self._ids)):
            cohort = SetOfGames(self._ids[i], self._prob_head[i])
            output=cohort.simulate(n_times)
            self._ExpectedRewards.append(cohort.get_ave_reward())
            self._Uncertainty.append(cohort.get_probability_loss())
            self._sumStat_meanRewards.append(output.get_)



    def get_overall_mean_rewards(self):
        return self._sumStat_meanRewards.get_mean()
    def get_cohort_PI_survival(self,cohort_index,alpha):
        st = Stat.SummaryStat('', self._ExpectedRewards[cohort_index])
        return st.get_PI(alpha)

        # Calculate expected reward of 1000 games
trial = SetOfGames(prob_head=0.5, n_games=1000)
cohortOutcome=trial.simulation(prob_head=0.5, n_games=1000)
print("The average expected reward is:", cohortOutcome.get_ave_reward())

# Problem 1: Confidence Interval
ALPHA=0.05

