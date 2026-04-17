from lr0_item import LR0Item


EPSILON_ALIASES = {"ε", "eps", "epsilon", "EPSILON"}


def _normalize_symbol(sym: str) -> str:
    return "ε" if sym in EPSILON_ALIASES else sym


class Grammar:
    def __init__(self):
        self.start_symbol: str = ""
        self.productions: dict[str, list[list[str]]] = {}

    # Construcción
   
    def add_production(self, head: str, body: list[str]):
        """Agrega una producción  head → body."""
        if head not in self.productions:
            self.productions[head] = []
        # Normaliza ε
        normalized = [_normalize_symbol(s) for s in body]
        self.productions[head].append(normalized)

    # Propiedades derivadas
    @property
    def non_terminals(self) -> set[str]:
        return set(self.productions.keys())

    @property
    def terminals(self) -> set[str]:
        ts = set()
        for bodies in self.productions.values():
            for body in bodies:
                for sym in body:
                    if sym not in self.non_terminals and sym != "ε":
                        ts.add(sym)
        return ts

    def is_non_terminal(self, sym: str) -> bool:
        return sym in self.productions

    # Generación de ítems iniciales para un no-terminal

    def initial_items(self, non_terminal: str) -> list[LR0Item]:
        items = []
        for body in self.productions.get(non_terminal, []):
            if body == ["ε"]:
                # Producción vacía: el ítem ya está completo
                items.append(LR0Item(non_terminal, [], 0))
            else:
                items.append(LR0Item(non_terminal, body, 0))
        return items

    # Parseo desde texto
    
    @classmethod
    def from_text(cls, text: str) -> "Grammar":
        grammar = cls()
        first = True

        for raw_line in text.strip().splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue

            # Acepta '->' o '→'
            if "->" in line:
                head, rhs = line.split("->", 1)
            elif "→" in line:
                head, rhs = line.split("→", 1)
            else:
                raise ValueError(f"Línea inválida (falta '->'): '{raw_line}'")

            head = head.strip()
            if not head:
                raise ValueError(f"No-terminal vacío en línea: '{raw_line}'")

            if first:
                grammar.start_symbol = head
                first = False

            for alt in rhs.split("|"):
                symbols = alt.split()
                if not symbols:
                    symbols = ["ε"]
                grammar.add_production(head, symbols)

        if not grammar.start_symbol:
            raise ValueError("La gramática está vacía.")

        return grammar

    def __str__(self) -> str:
        lines = []
        for head, bodies in self.productions.items():
            rhs = " | ".join(
                " ".join(b) if b != ["ε"] else "ε" for b in bodies
            )
            marker = "  (inicio)" if head == self.start_symbol else ""
            lines.append(f"  {head} → {rhs}{marker}")
        return "\n".join(lines)
