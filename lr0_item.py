class LR0Item:
    def __init__(self, head: str, body: list[str], dot_pos: int = 0):
        self.head = head
        self.body = body         
        self.dot_pos = dot_pos

    # Consultas útiles
    def is_complete(self) -> bool:
        return self.dot_pos >= len(self.body)

    def symbol_after_dot(self):
        if self.is_complete():
            return None
        return self.body[self.dot_pos]

    def advance(self) -> "LR0Item":
        if self.is_complete():
            raise ValueError("No se puede avanzar: el ítem ya está completo.")
        return LR0Item(self.head, self.body, self.dot_pos + 1)

    def __str__(self) -> str:
        body_with_dot = list(self.body)
        body_with_dot.insert(self.dot_pos, "·")
        rhs = " ".join(body_with_dot) if body_with_dot else "·"
        return f"{self.head} → {rhs}"

    def __repr__(self) -> str:
        return f"LR0Item({self!s})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, LR0Item):
            return False
        return (
            self.head == other.head
            and self.body == other.body
            and self.dot_pos == other.dot_pos
        )

    def __hash__(self) -> int:
        return hash((self.head, tuple(self.body), self.dot_pos))
