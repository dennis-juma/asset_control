import re


def generate_code(name: str, length: int = 3) -> str:
    """
    Generate a readable code.

    Examples:
        Laptop              -> LAP
        SIM Card            -> SIM
        Software License    -> SOF
        HP                  -> HPX
    """

    if not name:
        return ""

    words = re.findall(r"[A-Za-z0-9]+", name.strip())

    if not words:
        return ""

    first = words[0].upper()

    code = first[:length]

    while len(code) < length:
        code += "X"

    return code