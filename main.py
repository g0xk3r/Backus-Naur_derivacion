import random

class GramaticaBackusNaur:
    def __init__(self):
        self.derivaciones = []
        self.cadena_final = ""

    def derivar(self, n_objetivo):
        cadena = "S"
        ifs_actuales = 0
        self.derivaciones = [cadena]

        while "S" in cadena or "A" in cadena:
            indices_s = [i for i, char in enumerate(cadena) if char == 'S']
            indices_a = [i for i, char in enumerate(cadena) if char == 'A']
            todos = indices_s + indices_a
            idx = random.choice(todos)
            simbolo = cadena[idx]
            reemplazo = ""

            if simbolo == 'S':
                if ifs_actuales < n_objetivo:
                    reemplazo = "iCt(S)[A]"
                    ifs_actuales += 1
                else:
                    reemplazo = "" # S muere (se vuelve vacío)
            elif simbolo == 'A':
                if ifs_actuales < n_objetivo:
                    if random.choice([True, False]):
                        reemplazo = ";e(S)"
                    else:
                        reemplazo = "epsilon"
                else:
                    reemplazo = "epsilon" # Si ya cumplimos la meta, A muere

            cadena = cadena[:idx] + reemplazo + cadena[idx+1:]
            self.derivaciones.append(cadena)

        self.cadena_final = cadena.replace("epsilon", "")
        self.guardar_derivaciones()
        self.guardar_pseudocodigo()

    def guardar_derivaciones(self):
        with open("derivaciones_random.txt", "w", encoding="utf-8") as f:
            f.write("DERIVACIÓN ALEATORIA PASO A PASO\n")
            for i, paso in enumerate(self.derivaciones):
                f.write(f"Paso {i}: {paso}\n")
        print("Archivo 'derivaciones_random.txt' actualizado.")

    def guardar_pseudocodigo(self):
        pseudo = []
        nivel = 0
        indent_str = "  "
        i = 0
        txt = self.cadena_final
        n = len(txt)

        while i < n:
            if txt[i:].startswith("iCt"):
                linea = (indent_str * nivel) + "if (condicion):"
                pseudo.append(linea)
                i += 3 # Saltamos los caracteres i C t
                continue

            if txt[i:].startswith(";e"):
                linea = (indent_str * nivel) + "else:"
                pseudo.append(linea)
                i += 2 # Saltamos ';' y 'e'
                continue

            char = txt[i]
            if char == "(":
                nivel += 1
                if i + 1 < n and txt[i+1] == ")":
                    pseudo.append((indent_str * nivel) + "pass")
            elif char == ")":
                nivel -= 1
            elif char == "[" or char == "]":
                pass
            i += 1

        with open("pseudocodigo.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(pseudo))
        print("Archivo 'pseudocodigo.txt' actualizado.")

if __name__ == "__main__":
    app = GramaticaBackusNaur()
    try:
        entrada = int(input("Numero de IFs deseados: "))
        n = entrada
    except:
        print("No se ingreso un numero valido, se usara 5 por defecto.")
        n = 5

    print(f"Generando {n} IFs...")
    app.derivar(n)
    print("Proceso finalizado")