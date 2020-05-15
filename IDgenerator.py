import random
import string


def generate_id(number_of_small_letters=2,
                number_of_capital_letters=2,
                number_of_digits=2,
                number_of_special_chars=2,
                allowed_special_chars=r"_+-!"):
    """
    The funcion generates a random string allowing the user to input teh number for how many and what type of characters
    """
    id = []
    special_chars = list(allowed_special_chars)
    random.shuffle(special_chars)
    for i in range(number_of_small_letters):
        id.append(chr(random.randint(97, 122)))

    for i in range(number_of_capital_letters):
        id.append(chr(random.randint(65, 90)))

    for i in range(number_of_digits):
        id.append(chr(random.randint(48, 57)))

    for i in range(number_of_special_chars):
        id.append(special_chars[i])

    random.shuffle(id)
    return "".join(id)



if __name__ == "__main__":
    generate_id()
