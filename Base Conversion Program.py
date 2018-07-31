
import math
import shelve
import string

# A number system conversion program.
# A Python 3 project.
# Can handle up to base 16.

# Written by Josheb P. Dayrit.
# Finalized on 7/30/18.

# NOTE: Any output with over 1000 decimal places is considered "non-terminating."


def input_error_catcher(any_input):
    """Detects anomalous inputs for number to be converted."""

    error_counter = 0
    decimal_point_counter = 0

    # If blank, error.
    if any_input == '':
        error_counter += 1
        print('\nError: Blank input.')

    # Scans input for non-letter/non-digit elements and excess periods.
    for alpha_or_num in any_input:
        if alpha_or_num.isnumeric() or alpha_or_num.isalpha():
            continue
        elif alpha_or_num == '.':
            decimal_point_counter += 1
            if decimal_point_counter > 1:
                error_counter += 1
        else:
            error_counter += 1
            print('\nError:', alpha_or_num, 'is not an acceptable value.')

    if decimal_point_counter > 1:
        print('\nError: Excess decimal points.')

    if error_counter != 0:
        is_there_error = True
    else:
        is_there_error = False

    return is_there_error


def is_base_appropriate_for_input(hexadecimal_dict_letter, number_to_be_converted, original_base):
    """Checks if base is compatible with the inputted number."""
    
    my_input_as_list = []

    for elements in number_to_be_converted:
        if elements.isalpha() and \
                elements.capitalize() in string.ascii_uppercase:
            my_input_as_list.append(hexadecimal_dict_letter.get(elements.capitalize()))
        elif elements.isnumeric():
            my_input_as_list.append(int(elements))
        else:
            continue

    error_indicator = 0

    # Compares base with each digit in input.
    for elements in my_input_as_list:
        if elements >= original_base:
            error_indicator += 1
        else:
            continue

    if error_indicator != 0:
        is_there_error = True
    else:
        is_there_error = False

    return is_there_error


def enter_original_and_desired_base():
    """Verifies if base inputs are valid."""

    while True:
        try:
            original_base = int(input('\nOriginal base: '))
            desired_base = int(input('\nDesired base: '))
        except ValueError:
            print('\nInvalid. Try again.')
        else:
            break

    base_data = {'OriginalBase': original_base, 'DesiredBase': desired_base}

    if base_data['OriginalBase'] > 16 or \
            base_data['DesiredBase'] > 16 or \
            base_data['OriginalBase'] < 2 or \
            base_data['DesiredBase'] < 2 or \
            base_data['OriginalBase'] == base_data['DesiredBase']:
        while base_data['OriginalBase'] > 16 or \
                base_data['DesiredBase'] > 16 or \
                base_data['OriginalBase'] < 2 or \
                base_data['DesiredBase'] < 2 or \
                base_data['OriginalBase'] == base_data['DesiredBase']:
            print('\nInvalid. Try again.')
            print('\nRemember:')
            print('\t1. Original base and desired base must not be the same.')
            print('\t2. Base(s) must not exceed 16 or go under 2.')
            base_data = enter_original_and_desired_base()  # recursion.

    return base_data


def split_input(number_to_be_converted):
    """Splits input into 2 parts: its integer part and its decimal part."""

    dec_pt_index_indicator = 0
    decimal_point_counter = 0

    # Checks for existence of a decimal point.
    for num in number_to_be_converted:
        if num == '.':
            decimal_point_counter += 1
        else:
            continue

    # Marks the index of decimal point (if any).
    for num in number_to_be_converted:
        if num == '.':
            break
        else:
            dec_pt_index_indicator += 1

    # Separates number-to-be-converted into 2 parts and stores in dictionary.
    if decimal_point_counter == 0:
        user_data = {'IntegerPart': number_to_be_converted[:dec_pt_index_indicator],
                     'DecimalPart': '0'}
    else:
        user_data = {'IntegerPart': number_to_be_converted[:dec_pt_index_indicator],
                     'DecimalPart': number_to_be_converted[dec_pt_index_indicator + 1:]}

    return user_data


def integer_conversion_to_base10(hexadecimal_dict_letters, integer_part, original_base):
    """Converts integer part to a base 10 number."""

    integer_conversion = 0
    starting_index = len(integer_part) - 1  # recall: string indices start at 0, not 1.

    if integer_part != '0':
        for num in integer_part:
            if num.isalpha() and \
                    num.capitalize() in string.ascii_uppercase:
                integer_conversion += hexadecimal_dict_letters.get(num.capitalize()) * pow(original_base, starting_index)
                starting_index -= 1
            else:
                integer_conversion += int(num) * pow(original_base, starting_index)
                starting_index -= 1

    return integer_conversion


def decimal_conversion_to_base10(hexadecimal_dict_letters, decimal_part, original_base):
    """Converts decimal part to a base 10 number."""

    decimal_conversion = 0
    starting_index = -1

    if decimal_part != '0':
        for num in decimal_part:
            if num.isalpha() and \
                    num.capitalize() in string.ascii_uppercase:
                decimal_conversion += hexadecimal_dict_letters.get(num.capitalize()) * pow(original_base, starting_index)
                starting_index -= 1
            else:
                decimal_conversion += int(num) * pow(original_base, starting_index)
                starting_index -= 1

    return decimal_conversion


def integer_conversion_to_desired_base(hexadecimal_dict_numbers, integer_part, desired_base):
    """Converts integer part to desired base."""

    if integer_part == 0:
        fin_int_conv_as_list = [0]

    # Resolves if integer part is not 0.
    else:
        fin_int_conv_as_list = []
        if integer_part != 0:
            while integer_part != 0:
                fin_int_conv_as_list.append(integer_part % desired_base)
                integer_part /= desired_base
                integer_part = int(integer_part)
                # print(integer_part)

        fin_int_conv_as_list.reverse()

        # Replaces numbers 10 and above with their letter counterparts.
        for index, elements in enumerate(fin_int_conv_as_list):
            if elements >= 10:
                fin_int_conv_as_list.remove(elements)
                fin_int_conv_as_list.insert(index, hexadecimal_dict_numbers.get(elements))
            else:
                continue

    fin_int_conv_as_str = ''.join(str(num_as_letter) for num_as_letter in fin_int_conv_as_list)

    return fin_int_conv_as_str


def decimal_conversion_to_desired_base(hexadecimal_dict_numbers, decimal_part, desired_base):
    """Converts decimal part to desired base."""

    # Resolves if there is no decimal part.
    if decimal_part == 0:
        fin_dec_conv_as_list = ['.', 0]

    # Converts non-zero decimal part to desired base.
    else:
        fin_dec_conv_as_list = ['.']  # '.' denotes the decimal point.

        non_terminating_counter = 0

        truncation_value = None  # will be updated if decimal part is non-terminating.

        if decimal_part - math.floor(decimal_part) != 0:
            while decimal_part - math.floor(decimal_part) != 0:
                decimal_part *= desired_base
                fin_dec_conv_as_list.append(math.floor(decimal_part))
                decimal_part -= math.floor(decimal_part)
                non_terminating_counter += 1
                if non_terminating_counter > 1000:
                    break

        # Resolves if decimal part is non-terminating.
        if non_terminating_counter == 1000:
            truncation_value = set_truncation_value(non_terminating_counter)

        if truncation_value:
            for index, elements in enumerate(fin_dec_conv_as_list):
                if elements == '.':  # skips the decimal point.
                    continue
                    
                if elements >= 10:
                    fin_dec_conv_as_list.remove(elements)
                    fin_dec_conv_as_list.insert(index, hexadecimal_dict_numbers.get(elements))
                    truncation_value -= 1
                else:
                    truncation_value -= 1

                if truncation_value == 0:
                    break

        if not truncation_value:
            for index, elements in enumerate(fin_dec_conv_as_list):
                if elements == '.':
                    continue

                if elements >= 10:
                    fin_dec_conv_as_list.remove(elements)
                    fin_dec_conv_as_list.insert(index, hexadecimal_dict_numbers.get(elements))

    fin_dec_conv_as_str = ''.join(str(num_as_letter) for num_as_letter in fin_dec_conv_as_list)

    return fin_dec_conv_as_str


def set_truncation_value(non_terminating_counter):
    """Limits how many decimal places are displayed in the output."""
    
    while True:
        try:
            truncation_value = int(input('\nWarning: The decimal part spans over 1000 decimal places.'
                                         '\nTruncation is recommended.'
                                         '\n\nTo that end, a truncation value will need to be set.'
                                         '\nThis value controls the number of decimal places your output displays.'
                                         '\n\nTruncation value: '))
        except ValueError:
            print('\nError: You must enter an integer.')

        else:
            break

    # Ensures that truncation value is not greater than the counter.
    if truncation_value > non_terminating_counter:
        while truncation_value > non_terminating_counter:
            print('\nError: Truncation value cannot exceed', str(non_terminating_counter) + '.')
            truncation_value = set_truncation_value(non_terminating_counter)

    return truncation_value


def main():
    """The main function."""
    
    user_shelf = shelve.open('user_shelf.dat')  # will store user inputs for future reference.

    hexadecimal_dict_letters = {}  # will be used to convert from letter to number.

    for index_as_numeric, letters in enumerate(string.ascii_uppercase, 10):
        hexadecimal_dict_letters[letters] = index_as_numeric
        if letters == 'F':
            break

    hexadecimal_dict_numbers = {}  # will be used to convert from number to letter.

    for index_as_numeric, letters in enumerate(string.ascii_uppercase, 10):
        hexadecimal_dict_numbers[index_as_numeric] = letters
        if letters == 'F':
            break

    number_converted = None  # will be used to store the converted number.

    number_to_be_converted = input('\nNumber to be converted: ')

    is_there_input_error = input_error_catcher(number_to_be_converted)

    # Makes sure input is valid.
    if is_there_input_error is True:
        while is_there_input_error is True:
            print('\nError: Input is invalid.')
            number_to_be_converted = input('\nNumber to be converted: ')
            is_there_input_error = input_error_catcher(number_to_be_converted)

    base_data = enter_original_and_desired_base()  # the bases are entered here.

    is_there_base_incompatibility = is_base_appropriate_for_input(hexadecimal_dict_letters,
                                                                  number_to_be_converted,
                                                                  base_data['OriginalBase'])

    # Makes sure base is compatible with input. 
    if is_there_base_incompatibility is True:
        while is_there_base_incompatibility is True:
            print('\nError: Original base is not compatible with input.')
            base_data = enter_original_and_desired_base()
            is_there_base_incompatibility = is_base_appropriate_for_input(hexadecimal_dict_letters,
                                                                          number_to_be_converted,
                                                                          base_data['OriginalBase'])

    original_base = base_data['OriginalBase']
    desired_base = base_data['DesiredBase']

    user_data = split_input(number_to_be_converted)

    print('\nSearching for similar input...')  # flavor text.

    # Searches shelf for similar inputs; prints output if similar input is found.
    if user_shelf:
        for keys in user_shelf:
            if number_to_be_converted + str(original_base) + str(desired_base) == keys:
                number_converted = user_shelf[keys]
                print('\nSimilar input found.')  # flavor text.
                print('\n' + number_to_be_converted,
                      'in base',
                      desired_base,
                      'notation is:',
                      number_converted + '.')

    # Resolves if number has not been converted.
    if not number_converted:

        print('\nNo similar input found.'
              '\n\nProceeding with conversion...')  # a little bit of flavor text.

        integer_part = integer_conversion_to_base10(hexadecimal_dict_letters, user_data['IntegerPart'], original_base)
        decimal_part = decimal_conversion_to_base10(hexadecimal_dict_letters, user_data['DecimalPart'], original_base)

        int_conversion = integer_conversion_to_desired_base(hexadecimal_dict_numbers, integer_part, desired_base)
        dec_conversion = decimal_conversion_to_desired_base(hexadecimal_dict_numbers, decimal_part, desired_base)

        number_converted = int_conversion + dec_conversion

        user_shelf[number_to_be_converted + str(original_base) + str(desired_base)] = number_converted

        print('\n' + number_to_be_converted,
              'in base',
              desired_base,
              'notation is:',
              number_converted + '.')

    user_shelf.sync()  # makes sure data is written to shelf.
    user_shelf.close()


# Executes here.
while True:
    main()
    continue_var = input('\nDo you want to continue?'
                         '\nIf so, press enter.'
                         '\nTapping any other key will terminate the program.'
                         '\n\nSelection: ')
    if continue_var != '':
        break
