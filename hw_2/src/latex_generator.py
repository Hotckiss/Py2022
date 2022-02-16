import os
import functools
from hotckissast import build_ast


def make_head() -> str:
    return (
        "\\documentclass{article}\n"
        "\\usepackage[utf8]{inputenc}\n"
        "\\usepackage{graphicx}\n"
        "\\title{{Latex table}}\n"
        "\\begin{document}\n"
        "\\maketitle\n\n"
    )


def make_tail() -> str:
    return "\\end{document}"


def validate_input(table):
    return len(table) > 0 and len(table[0]) > 0 and all(map(lambda x: len(x) == len(table[0]), table))


def make_table(table) -> str:
    return f'\\begin{{tabular}}' \
           f'{{{"| c " * len(table[0]) + "|"}}}' \
           f'\n\\hline\n' + \
           functools.reduce(
               lambda current_table, row: f"{current_table} \\\\\n\\hline\n{row}",
               map(functools.partial(functools.reduce, lambda l, r: f"{l} & {r}"), table)
           ) + \
           f'\\\\\n\\hline\n' \
           f'\\end{{tabular}}\n'


def make_image(image_path: str) -> str:
    return f"\\newline\\newline\\\\\n\\includegraphics[scale=0.3]{{{image_path}}}\\\\\n"


def create_latex(table):
    if not validate_input(table):
        raise ValueError("Incorrect table provided!")

    with open('../artifacts/table.tex', 'w') as f:
        f.write(make_head())
        f.write(make_table(table))
        f.write(make_image('ast.png'))
        f.write(make_tail())


if __name__ == "__main__":
    test_table = [
        ['1', '2', '3', '4'],
        ['5', '6', '7', '8'],
        ['9', '10', '11', '12'],
        ['13', '14', '15', '16']
    ]

    if not os.path.exists("../artifacts"):
        os.mkdir("../artifacts")

    build_ast('fib.py', '../artifacts/ast.png')
    create_latex(test_table)

    with open("../artifacts/link.txt", "w") as f:
        f.write("https://pypi.org/project/hotckissast/1.0.1/")
