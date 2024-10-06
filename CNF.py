import re
import copy
from itertools import combinations

# Definir una clase para representar la gramática
# Para este proyecto estaré tomando a ε como 'e', ya que ε no es reconocido por mi programa
class Grammar:
    def __init__(self):
        self.productions = {}  # Diccionario: No terminal -> Lista de producciones

    def add_production(self, lhs, rhs_list):
        if lhs not in self.productions:
            self.productions[lhs] = []
        self.productions[lhs].extend(rhs_list)

    def remove_epsilon_productions(self):
        print("\n--- Eliminación de Producciones-ε ---")
        nullable = self.find_nullable_symbols()
        print(f"Símbolos anulables: {nullable}")

        new_productions = copy.deepcopy(self.productions)

        for lhs, productions in self.productions.items():
            updated_productions = set()
            for production in productions:
                symbols = list(production)
                indices_nullable = [i for i, symbol in enumerate(symbols) if symbol in nullable]
                subsets = []
                # Generar todas las combinaciones posibles de símbolos anulables
                for i in range(1, len(indices_nullable)+1):
                    subsets.extend(combinations(indices_nullable, i))
                # Generar nuevas producciones eliminando símbolos anulables
                for subset in subsets:
                    new_symbols = [symbols[i] for i in range(len(symbols)) if i not in subset]
                    if new_symbols:
                        updated_productions.add(''.join(new_symbols))
                    else:
                        updated_productions.add('e')
                # Mantener la producción original
                updated_productions.add(production)
            new_productions[lhs] = list(updated_productions)

        # Eliminar las producciones-e originales, aqui yo consideraba que esto era excepto si S → ε está permitido, pero creo que no ¿o sí?
        for lhs in new_productions:
            new_productions[lhs] = [prod for prod in new_productions[lhs] if prod != 'e'] #or lhs == 'S']

        print("\nProducciones después de eliminar e-producciones:")
        for lhs, rhs in new_productions.items():
            print(f"{lhs} → {' | '.join(rhs)}")

        self.productions = new_productions

    def find_nullable_symbols(self):
        nullable = set()
        # Inicialmente, cualquier producción que produce ε directamente
        for lhs, productions in self.productions.items():
            for prod in productions:
                if prod == 'e':
                    nullable.add(lhs)
        # Iterativamente agregar símbolos que pueden producir ε
        changed = True
        while changed:
            changed = False
            for lhs, productions in self.productions.items():
                if lhs not in nullable:
                    for prod in productions:
                        if all(symbol in nullable for symbol in prod):
                            nullable.add(lhs)
                            changed = True
                            break
        return nullable

    def display(self):
        print("\nGramática Actual:")
        for lhs, rhs in self.productions.items():
            print(f"{lhs} → {' | '.join(rhs)}")

# Función para validar y parsear las producciones
def parse_grammar(grammar_text):
    grammar = Grammar()
    # Regex para validar una producción
    production_regex = re.compile(r'^([A-Z])\s*->\s*([0-9A-Za-z]+(\s*\|\s*[0-9A-Za-z]+)*)$')
    
    for line_num, line in enumerate(grammar_text.strip().split('\n'), start=1):
        line = line.strip()
        if not line:
            continue  # Saltar líneas vacías
        match = production_regex.match(line)
        if not match:
            raise ValueError(f"Error de sintaxis en la línea {line_num}: {line}")
        lhs = match.group(1)
        rhs = match.group(2).replace(' ', '')
        rhs_list = rhs.split('|')
        grammar.add_production(lhs, rhs_list)
    return grammar

# Función para leer la gramática desde un archivo de texto
def read_grammar_from_file(file_path):
    with open(file_path, 'r') as file:
        grammar_text = file.read()
    return grammar_text

# Función principal
def main():
    # Leer la gramática desde un archivo porque antes no lo hacía-.
    file_path = "gramatica2.txt"  #Lo que entendi es que se tenian que estar cada gramatica en un txt distinto por lo que solo habria que cambiar por gramatica.txt o gramatica2.txt
    
    try:
        grammar_input = read_grammar_from_file(file_path)
    except FileNotFoundError:
        print(f"Archivo {file_path} no encontrado.")
        return

    print("Parsing la gramática...")
    try:
        grammar = parse_grammar(grammar_input)
    except ValueError as ve:
        print(ve)
        return

    print("\nGramática original:")
    grammar.display()

    # Eliminar producciones-ε
    grammar.remove_epsilon_productions()

    # Mostrar la gramática final
    print("\nGramática sin producciones-e:")
    grammar.display()

if __name__ == "__main__":
    main()
