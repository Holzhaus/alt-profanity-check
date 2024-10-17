"""For Command Line Interface"""

import sys
import argparse
import pathlib

from .profanity_check import predict
from .profanity_check import predict_prob


def main(argv=None) -> None:
    """Main command line entry point

    First implementation is experimental hence suboptimal, will improve
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--threshold", action="store", type=float, default=0.5, help="threshold for profanity")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-f", "--files", action="store", nargs="+", type=pathlib.Path, help="file to check")
    group.add_argument("-s", "--strings", action="store", nargs="+", help="text string to check")
    args = parser.parse_args(argv)

    if args.strings:
        return check_strings(args.strings, args.threshold)
    else:
        return check_files(args.files, args.threshold)


def check_files(paths, threshold) -> int:
    profanity_found = False
    for path in paths:
        with path.open(mode="r", encoding="utf-8", errors="ignore") as fp:
            for lineno, probability in enumerate(predict_prob(iter(fp)), start=1):
                if probability >= threshold:
                    print(f"{path}:{lineno}: Profanity detected (probability: {probability})")
                    profanity_found = True

    if profanity_found:
        return 1

    return 0


def check_strings(texts_vector, threshold) -> int:
    print("Binary Predictions:")
    print()
    for item, prediction in zip(texts_vector, predict(texts_vector)):
        print(f"{item}: {prediction}")
    print()

    print("Probabilistic Predictions:")
    print()
    max_probability = 0.0
    for (item, probability) in zip(texts_vector, predict_prob(texts_vector)):
        print(f"{item}: {probability}")
        max_probability = max(max_probability, probability)
    print()

    print(f"Maximum Probability: {max_probability}")
    if max_probability >= threshold:
        return 1

    return 0
