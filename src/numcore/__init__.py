import argparse
from itertools import combinations, permutations
from typing import Iterable


def calc_core_candidate(numbers: list[int], operands: Iterable[str]) -> int:
    """Calculate the core of a mathematical expression.

    Args:
        numbers (list[int]): The numbers in the expression.
        operands (Iterable[str]): The operators in the expression.

    Raises:
        ValueError: Invalid result.
        ValueError: Unknown operand.

    Returns:
        int: The result of the expression.
    """
    result = numbers[0]
    for number, op in zip(numbers[1:], operands):
        if op == "s":
            result = result - number
        elif op == "d":
            result = result / number
        elif op == "m":
            result = result * number
        else:
            raise ValueError(f"Unknown operand: {op}")
    if result <= 0 or round(result) != result:
        raise ValueError(f"Invalid result: {result}")
    return int(result)


def calc_numeric_core(num: int) -> int:
    """Calculate the numeric core of an integer.

    Args:
        num (int): The integer to calculate the numeric core for.

    Returns:
        int: The numeric core of the integer.
    """
    digits = str(num)
    n_digits = len(digits)
    n_gaps = n_digits - 1
    n_partitions = 3
    """
    ex. 86455
    given        : 8   6   4   5   5
    gaps         :   0   1   2   3
    partitioning :   0   1       3
    gap_flags    :[  1,  1,  0,  1  ]
    numbers      :[8 , 6 , 4   5 , 5 ]
    """
    partitioning_patterns = combinations(range(n_gaps), n_partitions)
    operand_orders = list(permutations("sdm", n_partitions))
    results: list[int] = []
    for partitioning in partitioning_patterns:
        # Create a list of gaps based on the current partition
        gap_flags = [1 if i in partitioning else 0 for i in range(n_gaps)]
        # Create a list of numbers based on the gaps
        numbers: list[int] = []
        last_gap = 0
        for curr_gap, gap_flag in enumerate(gap_flags):
            if gap_flag == 1:
                numbers.append(int(digits[last_gap : curr_gap + 1]))
                last_gap = curr_gap + 1
        numbers.append(int(digits[last_gap:]))
        for operand_pattern in operand_orders:
            try:
                result = calc_core_candidate(numbers, operand_pattern)
            except (ZeroDivisionError, ValueError):
                continue
            results.append(result)
    answer = min(results)
    if len(str(answer)) > 3:
        answer = calc_numeric_core(answer)
    return answer


def numeric_core_4letters(letters: str) -> int:
    """Calculate the numeric core of a 4-letter word.

    Args:
        letters (str): A 4-letter word.

    Returns:
        int: The numeric core of the word.
    """
    results: list[int] = []
    operand_patterns = list(permutations("sdm", 3))
    numbers = [ord(letter.lower()) - ord("a") + 1 for letter in letters]
    for operand_pattern in operand_patterns:
        try:
            result = calc_core_candidate(numbers, operand_pattern)
        except (ZeroDivisionError, ValueError):
            continue
        results.append(result)
    answer = min(results)
    if len(str(answer)) > 3:
        answer = calc_numeric_core(answer)
    return answer


def word_to_number(word: str) -> int:
    """
    Convert a word to a number by assigning each letter a unique digit.
    """
    numerics = [str(ord(letter.lower()) - ord("a") + 1) for letter in word]
    number = "".join(numerics)
    if not number.isdigit():
        ValueError(f"Invalid letter: {word} to {number}")
    return int(number)


def main() -> int:
    parser = argparse.ArgumentParser(description="Calculate numeric core.")
    parser.add_argument(
        "-n", "--number", type=int, help="A number to calculate the numeric core for."
    )
    parser.add_argument(
        "-w",
        "--word",
        type=str,
        help="A 4 letter word to calculate the numeric core for.",
    )
    args = parser.parse_args()
    if args.number:
        if args.number < 0:
            raise ValueError("Number must be positive.")
        numeric_core = calc_numeric_core(args.number)
        print(f"Numeric core of {args.number} is {numeric_core}")
    if args.word:
        if len(args.word) != 4:
            raise ValueError("Word must be 4 letters long.")
        numeric_core = numeric_core_4letters(args.word)
        char = chr(ord("a") + numeric_core - 1)
        print(f"Numeric core of {args.word} is {numeric_core} -> {char}")
    return 0
