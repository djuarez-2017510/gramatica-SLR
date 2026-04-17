GRAMMARS = {
    "1": (
        "Gramática 1):  S → SS+ | SS* | a",
        """
S -> S S + | S S * | a
""",
    ),
    "2": (
        "Gramática 2):  S → (S) | ε",
        """
S -> ( S ) | ε
""",
    ),
    "3": (
        "Gramática 3):  S → L,  L → aL | a",
        """
S -> L
L -> a L | a
""",
    ),
    "4": (
        "Gramática vista en clase:  E → E+T | T,  T → T*F | F,  F → (E) | id",
        """
E -> E + T | T
T -> T * F | F
F -> ( E ) | id
""",
    ),
}
