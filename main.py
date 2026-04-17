from grammar import Grammar
from lr0_item import LR0Item
from closure import closure, print_closure_result
from grammars_predefined import GRAMMARS

def main():
    print("\n" + "═" * 55)
    print("   Calculador de CERRADURA (Closure) — Ítems LR(0)")
    print("═" * 55)

    while True:
        grammar = select_grammar()
        if grammar is None:
            break

        print("\nGramática cargada:")
        print(grammar)

        while True:
            items = select_items(grammar)
            if items is None:
                break  # volver a elegir gramática

            print()
            result = closure(items, grammar, verbose=True)
            print_closure_result(result)

            if not ask_yes_no("¿Calcular otra cerradura con la misma gramática?"):
                break

        if not ask_yes_no("¿Usar otra gramática?"):
            break

    print("\n¡Hasta luego!\n")


def select_grammar() -> Grammar | None:
    print("\n" + "─" * 55)
    print("  Selecciona una gramática:")
    print("─" * 55)
    for key, (desc, _) in GRAMMARS.items():
        print(f"  [{key}]  {desc}")
    print("  5  Ingresar gramática manualmente")
    print("  6  Salir")
    print("─" * 55)

    while True:
        choice = input("Opción: ").strip().lower()

        if choice == "5":
            return None

        if choice == "6":
            return input_grammar_manually()

        if choice in GRAMMARS:
            _, text = GRAMMARS[choice]
            try:
                g = Grammar.from_text(text)
                return g
            except ValueError as e:
                print(f"  Error al parsear gramática: {e}")

        print("  Opción no válida.")


def input_grammar_manually() -> Grammar | None:
    print("\n  Ingresa la gramática (una producción por línea).")
    print("  Usa '->' para separar cabeza y cuerpo, '|' para alternativas.")
    print("  Usa 'ε' o 'eps' para producciones vacías.")
    print("  Escribe una línea vacía para terminar.\n")

    lines = []
    while True:
        line = input("  > ")
        if line.strip() == "":
            break
        lines.append(line)

    if not lines:
        print("  (no se ingresó ninguna producción)")
        return None

    try:
        return Grammar.from_text("\n".join(lines))
    except ValueError as e:
        print(f"  Error: {e}")
        return None

def select_items(grammar: Grammar) -> set[LR0Item] | None:
    print("\n" + "─" * 55)
    print("  ¿Cómo deseas ingresar el conjunto inicial de ítems?")
    print("─" * 55)
    print("  1  Ítem inicial del símbolo de inicio  (S' → · S)")
    print("  2  Todos los ítems iniciales de un no-terminal")
    print("  3  Ingresar ítem(s) manualmente")
    print("  4 Volver a elegir gramática")
    print("─" * 55)

    while True:
        choice = input("Opción: ").strip().lower()

        if choice == "4":
            return None

        if choice == "1":
            start = grammar.start_symbol
            items = grammar.initial_items(start)
            if not items:
                print(f"  No hay producciones para '{start}'.")
                continue
            selected = set(items)
            print(f"\n  Ítems iniciales de  {start}:")
            for it in sorted(selected, key=str):
                print(f"    {it}")
            return selected

        if choice == "2":
            nts = sorted(grammar.non_terminals)
            print(f"\n  No-terminales disponibles: {', '.join(nts)}")
            nt = input("  No-terminal: ").strip()
            if nt not in grammar.non_terminals:
                print(f"  '{nt}' no es un no-terminal de la gramática.")
                continue
            selected = set(grammar.initial_items(nt))
            if not selected:
                print(f"  No hay producciones para '{nt}'.")
                continue
            return selected

        if choice == "3":
            return input_items_manually(grammar)

        print("  Opción no válida.")


def input_items_manually(grammar: Grammar) -> set[LR0Item] | None:
    print("\n  Ingresa los ítems (uno por línea).")
    print("  Formato:   A -> alpha . B beta")
    print("  El punto '.' separa lo visto de lo que falta.")
    print("  Escribe una línea vacía para terminar.\n")

    items = set()
    while True:
        raw = input("  > ").strip()
        if raw == "":
            break
        item = parse_item(raw, grammar)
        if item is None:
            print("  Formato inválido. Ejemplo:  S -> a . B c")
        else:
            items.add(item)
            print(f"  Ítem agregado: {item}")

    if not items:
        print("  (no se ingresaron ítems)")
        return None

    return items


def parse_item(text: str, grammar: Grammar) -> LR0Item | None:
    if "->" not in text and "→" not in text:
        return None

    sep = "->" if "->" in text else "→"
    parts = text.split(sep, 1)
    head = parts[0].strip()
    rhs = parts[1].strip().split()

    if not head:
        return None

    if "." not in rhs:
        return None

    dot_pos = rhs.index(".")
    body = rhs[:dot_pos] + rhs[dot_pos + 1:]  

    if head not in grammar.non_terminals:
        print(f"  Advertencia: '{head}' no es un no-terminal conocido.")

    if body == ["ε"] or body == ["eps"]:
        return LR0Item(head, [], dot_pos)

    return LR0Item(head, body, dot_pos)


def ask_yes_no(prompt: str, default: bool = True) -> bool:
    hint = "[S/n]" if default else "[s/N]"
    answer = input(f"\n  {prompt} {hint}: ").strip().lower()
    if answer == "":
        return default
    return answer in {"s", "si", "sí", "y", "yes"}

if __name__ == "__main__":
    main()
