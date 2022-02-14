#
#
#
from wordle.find_words import FindWords
import random


class Wordle(object):
    def __init__(self, length=5):
        self._find_word = FindWords(length=length)

        self._word = None
        self._remaining = None
        self._remaining_stats = []
        self._length = length

        self.guess_count = 0
        self.min_guesses = 999
        self.max_guesses = -1
        self.total_runs = 0
        self.wins = 0

    def pick_word(self, use_word=None):
        if isinstance(use_word, str):
            if not self._find_word.is_valid_word(use_word.lower()) or len(use_word) != self._length:
                raise ValueError(f'{use_word} is an invalid word')
            self._word = use_word.lower()
        else:
            self._word = self._find_word.get_random_word()
        return self

    def reset_stats(self):
        self._remaining = None
        self._remaining_stats = []
        self.guess_count = 0

    def save_stats(self):
        if self._remaining is not None:
            self._remaining_stats.append(len(self._remaining))

    @property
    def word(self):
        return self._word

    @property
    def remaining_words(self):
        return self._remaining if self._remaining is not None else []

    @property
    def remaining_stats(self):
        return self._remaining_stats

    def print_stats(self):
        values = []
        for idx, amount in enumerate(self._remaining_stats):
            values.append(f'{amount}' if idx != 4 else f'{amount}*')
        return str(values)

    def print(self):
        if self._word is not None:
            print(f'Remaining words for "{self._word}" - {len(self.remaining_words)}')
        else:
            print(f'Remaining words - {len(self.remaining_words)}')
        for i in range(0, len(self.remaining_words), 15):
            print('\t', ', '.join(self.remaining_words[i:i+15]))

    def get_remaining_words(self, guess):
        match = ''
        unmatch = ''
        included = ''
        excluded = ''

        if not self._find_word.is_valid_word(guess.lower()) or len(guess) != self._length:
            raise ValueError(f'{guess} is an invalid word')

        for idx, letter in enumerate(guess.lower()):
            if letter in self._word and letter not in included:
                included += letter

            if letter not in self._word and letter not in excluded:
                excluded += letter

            if letter == self._word[idx]:
                match += letter
                unmatch += '.'
            else:
                match += '.'
                unmatch += letter

        self._remaining = self._find_word.get_possibles(matches=match, unmatches=unmatch, includes=included,
                                                        excludes=excluded, remaining=self._remaining)
        return self._remaining

    def get_included_letters(self, included):
        self._remaining = self._find_word.get_possibles(includes=included, remaining=self._remaining)
        self.save_stats()
        return self._remaining

    def get_excluded_letters(self, excludes):
        self._remaining = self._find_word.get_possibles(excludes=excludes, remaining=self._remaining)
        self.save_stats()
        return self._remaining

    def get_matches_letters(self, matches):
        self._remaining = self._find_word.get_possibles(matches=matches, remaining=self._remaining)
        self.save_stats()
        return self._remaining

    def get_unmatches_letters(self, unmatches):
        self._remaining = self._find_word.get_possibles(unmatches=unmatches, remaining=self._remaining)
        self.save_stats()
        return self._remaining

    def guess_word(self, word_list, is_avoid_double_letters=False):
        guess = word_list[0]
        if len(word_list) > 2:
            for _ in '1' * 10:
                guess = random.choice(word_list)
                if not is_avoid_double_letters or not self._find_word.has_repeating_letter(guess):
                    break
        return guess

    def run(self, first_word, is_double_guess=False, is_avoid_double_letters=False):
        if not isinstance(first_word, list):
            first_word = [first_word]

        self.reset_stats()
        self.guess_count = len(first_word)
        for guess in first_word:
            self._remaining = self.get_remaining_words(guess)
            self.save_stats()

        if is_double_guess:
            alternates = self._find_word.get_possibles(excludes=self._find_word.get_unique_letters(first_word[0]))
            if len(alternates) > 0:
                self.guess_count += 1
                guess = self.guess_word(alternates, is_avoid_double_letters=True)
                self._remaining = self.get_remaining_words(guess)
                self.save_stats()

        while len(self._remaining) > 0:
            self.guess_count += 1
            guess = self.guess_word(self._remaining, is_avoid_double_letters=is_avoid_double_letters)
            if guess == self._word:
                break

            self._remaining = self.get_remaining_words(guess)
            self.save_stats()
            if len(self._remaining) < 16:
                is_avoid_double_letters = False

        self.total_runs += 1
        if self.guess_count <= 6:
            self.wins += 1
        self.min_guesses = min(self.guess_count, self.min_guesses)
        self.max_guesses = max(self.guess_count, self.max_guesses)
        return self
