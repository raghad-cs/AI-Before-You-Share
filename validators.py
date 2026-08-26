import re


def clean_text(value):
    """
    Remove spaces and dashes before validation.
    """
    return value.replace(" ", "").replace("-", "").strip()


# -----------------------------
# Saudi Phone Number
# -----------------------------
def validate_saudi_phone(value):
    value = clean_text(value)

    patterns = [
        r"^05\d{8}$",        # 05xxxxxxxx
        r"^\+9665\d{8}$",    # +9665xxxxxxxx
        r"^9665\d{8}$"       # 9665xxxxxxxx
    ]

    return any(re.fullmatch(pattern, value) for pattern in patterns)


# -----------------------------
# Saudi IBAN
# -----------------------------
def validate_saudi_iban(value):
    iban = clean_text(value).upper()

    # Saudi IBAN must start with SA and contain 24 characters
    if not re.fullmatch(r"SA\d{22}", iban):
        return False

    # IBAN MOD-97 validation
    rearranged = iban[4:] + iban[:4]

    numeric = ""

    for char in rearranged:
        if char.isdigit():
            numeric += char
        else:
            numeric += str(ord(char) - 55)

    return int(numeric) % 97 == 1


# -----------------------------
# Credit Card
# -----------------------------
def validate_credit_card(value):
    number = clean_text(value)

    if not number.isdigit():
        return False

    if not 13 <= len(number) <= 19:
        return False

    # Luhn Algorithm
    total = 0
    reverse_digits = number[::-1]

    for index, digit in enumerate(reverse_digits):
        digit = int(digit)

        if index % 2 == 1:
            digit *= 2

            if digit > 9:
                digit -= 9

        total += digit

    return total % 10 == 0


# -----------------------------
# Saudi National ID
# -----------------------------
def validate_saudi_national_id(value):
    number = clean_text(value)

    return (
        number.isdigit()
        and len(number) == 10
        and number.startswith("1")
    )


# -----------------------------
# Saudi Iqama
# -----------------------------
def validate_saudi_iqama(value):
    number = clean_text(value)

    return (
        number.isdigit()
        and len(number) == 10
        and number.startswith("2")
    )


# -----------------------------
# Test
# -----------------------------
if __name__ == "__main__":

    print("Phone:", validate_saudi_phone("0551234567"))

    print(
        "IBAN:",
        validate_saudi_iban("SA0380000000608010167519")
    )

    print(
        "Credit Card:",
        validate_credit_card("4111111111111111")
    )

    print(
        "National ID:",
        validate_saudi_national_id("1023456789")
    )

    print(
        "Iqama:",
        validate_saudi_iqama("2123456789")
    )