from wordle.wordle import Wordle


if __name__ == '__main__':
    w = Wordle()
    w.pick_word(use_word='humor')
    w.get_remaining_words('irate')
    w.get_remaining_words('cloud')
    w.get_remaining_words('rough')
    w.print()

    w = Wordle()
    w.get_included_letters('aeu')
    w.get_excluded_letters('irtclod')
    w.get_matches_letters('....e')
    w.get_unmatches_letters('irat.')
    w.get_unmatches_letters('cloud')
    w.print()

    w = Wordle()
    w.pick_word(use_word='pause')
    w.get_remaining_words('irate')
    w.get_remaining_words('cloud')
    w.print()

    w = Wordle()
    w.get_included_letters('rue')
    w.get_excluded_letters('aistoghnd')
    w.get_unmatches_letters('arise')
    w.get_unmatches_letters('tough')
    w.get_unmatches_letters('.nd..')
    w.get_matches_letters('u..er')
    w.print()

    w = Wordle()
    w.pick_word(use_word='might')
    w.get_remaining_words('irate')
    w.get_remaining_words('cloud')
    w.print()

    w = Wordle()
    w.pick_word(use_word='ultra')
    w.get_remaining_words('raise')
    w.get_remaining_words('tough')
    w.print()

    w = Wordle()
    w.pick_word(use_word='spank')
    w.get_remaining_words('irate')
    w.get_remaining_words('cloud')
    w.get_remaining_words('swank')
    w.print()

    w = Wordle(length=6)
    w.pick_word(use_word='sparks')
    w.get_remaining_words('pirate')
    w.get_remaining_words('clouds')
    w.get_remaining_words('graphs')
    w.print()
