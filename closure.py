from grammar import Grammar
from lr0_item import LR0Item


def closure(
    items: set[LR0Item] | list[LR0Item],
    grammar: Grammar,
    verbose: bool = True,
) -> set[LR0Item]:
    result: set[LR0Item] = set(items)

    if verbose:
        _print_section("Ítems de entrada")
        for item in sorted(result, key=str):
            print(f"    {item}")
        print()
        _print_section("Proceso de cierre")

    changed = True
    step = 1

    while changed:
        changed = False
        # Iteramos sobre una copia
        for item in list(result):
            sym = item.symbol_after_dot()
            if sym is None or not grammar.is_non_terminal(sym):
                continue
            # Agregamos todos los ítems iniciales de ese no-terminal
            for new_item in grammar.initial_items(sym):
                if new_item not in result:
                    result.add(new_item)
                    changed = True
                    if verbose:
                        print(
                            f"  Paso {step:>2}: {item}  →  agrega  {new_item}"
                        )
                        step += 1

    if verbose:
        if step == 1:
            print("  (no se agregaron nuevos ítems)\n")
        else:
            print()

    return result

# Utilidades de impresión

def print_closure_result(result: set[LR0Item], title: str = "Cerradura completa"):
    _print_section(title)
    reduction_items = []
    normal_items = []
    for item in sorted(result, key=str):
        if item.is_complete():
            reduction_items.append(item)
        else:
            normal_items.append(item)

    for item in normal_items:
        print(f"    {item}")
    for item in reduction_items:
        print(f"    {item}   ← [REDUCCIÓN]")
    print()


def _print_section(title: str):
    print(f"{'─' * 50}")
    print(f"  {title}")
    print(f"{'─' * 50}")
