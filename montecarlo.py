from wordle.wordle import Wordle
import signal
import traceback

EXIT_PROCESS = False


def sig_handler(signum, frame):
    global EXIT_PROCESS
    print(f'Caught signal {signum} with frame {frame}')
    EXIT_PROCESS = True


def main():
    global EXIT_PROCESS

    signal.signal(signal.SIGINT, sig_handler)

    failures = dict(stare=[], audio=[], train=[], cloud=[],
                    louie=[], adeui=[], great=[], irate=[], shore=[],
                    irate_cloud=[], raise_tough=[])
    ignore_words = []
    for word in failures.keys():
        for w in word.split('_'):
            ignore_words.append(w)

    w = Wordle()
    try:
        for i in range(500):
            if EXIT_PROCESS:
                break

            w.pick_word()
            while w.word in ignore_words:
                w.pick_word()

            for start in failures.keys():
                w.run(start.split('_'))
                if w.guess_count > 6:
                    failures[start].append(w.word + f'-{w.remaining_stats[4]}')
                    print(start, f':{w.print_stats()}:', w.word)

                w.run(start.split('_'), is_avoid_double_letters=True)
                if w.guess_count > 6:
                    failures[start].append(w.word + f'-{w.remaining_stats[4]}')
                    print(start, f':{w.print_stats()}:',  w.word)

                w.run(start.split('_'), is_double_guess=True)
                if w.guess_count > 6:
                    failures[start].append(w.word + f'-{w.remaining_stats[4]}')
                    print(start, f':{w.print_stats()}:',  w.word)
    except Exception as e:
        print(f"Exception {e}", traceback.format_exc())

    print(w.total_runs, w.wins)
    print(w.min_guesses, w.max_guesses)
    for start, words in failures.items():
        print(start, len(words), words)


if __name__ == '__main__':
    main()
