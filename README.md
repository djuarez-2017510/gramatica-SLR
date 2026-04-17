# gramatica-SLR

Calculador de **CERRADURA (Closure)** para ítems LR(0). Implementación para calcular automáticamente el conjunto completo de ítems tras aplicar las reglas de cerradura de una gramática libre de contexto.

## Video del proyecto

[![Ver video](https://img.youtube.com/vi/nCat5DnkUFc/0.jpg)](https://youtu.be/nCat5DnkUFc)

## Estructura

```
closure.py              Función CERRADURA e impresión de resultados
grammar.py              Clase Grammar - parseo y gestión de gramáticas
lr0_item.py             Clase LR0Item - representación de ítems A → α · β
main.py                 Menú interactivo principal
grammars_predefined.py  Gramáticas precargadas para pruebas rápidas
README.md               Este archivo
```

## Uso

```bash
python main.py
```

El menú permite:
- Seleccionar una gramática (precargadas o manual)
- Ingresar ítems iniciales de tres formas
- Calcular y visualizar la cerradura paso a paso

## Gramáticas Precargadas

| Opción | Descripción |
|--------|------------|
| `1` | `S → SS+ \| SS* \| a` |
| `2` | `S → (S) \| ε` |
| `3` | `S → L;  L → aL \| a` |
| `4` | `E → E+T \| T;  T → T*F \| F;  F → (E) \| id` (clase) |
| `m` | Ingresar manualmente |

## Ejemplo

```
Selecciona gramática: 4
Ítems iniciales de E
Ítems de entrada:
    E → · E + T
    E → · T
    T → · T * F
    T → · F
    ...
```
