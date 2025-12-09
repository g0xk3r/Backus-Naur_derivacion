import random

class GramaticaBackusNaur:
    def __init__(self):
        self.cadena_final = ""

    def derivar(self, n_objetivo):
        cadena = "S"
        ifs_actuales = 0
        step_counter = 0
        with open("derivaciones_random.txt", "w", encoding="utf-8") as f:
            f.write("DERIVACIÓN ALEATORIA PASO A PASO\n")
            f.write(f"Paso {step_counter}: {cadena}\n")

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
                        reemplazo = "" # S muere
                elif simbolo == 'A':
                    if ifs_actuales < n_objetivo:
                        if random.choice([True, False]):
                            reemplazo = ";e(S)"
                        else:
                            reemplazo = "epsilon"
                    else:
                        reemplazo = "epsilon"

                cadena = cadena[:idx] + reemplazo + cadena[idx+1:]
                step_counter += 1
                f.write(f"Paso {step_counter}: {cadena}\n")

        self.cadena_final = cadena.replace("epsilon", "")
        print("Archivo 'derivaciones_random.txt' completado.")
        print("Se realizaron ", step_counter, "pasos de derivación.")
        self.guardar_pseudocodigo()

    def guardar_pseudocodigo(self):
        with open("pseudocodigo.txt", "w", encoding="utf-8") as f:
            nivel = 0
            indent_str = "  "
            i = 0
            txt = self.cadena_final
            n = len(txt)

            while i < n:
                if txt[i:].startswith("iCt"):
                    linea = (indent_str * nivel) + "if (condicion):"
                    f.write(linea + "\n")
                    i += 3
                    continue

                if txt[i:].startswith(";e"):
                    linea = (indent_str * nivel) + "else:"
                    f.write(linea + "\n")
                    i += 2
                    continue

                char = txt[i]
                if char == "(":
                    nivel += 1
                    if i + 1 < n and txt[i+1] == ")":
                        f.write((indent_str * nivel) + "pass\n")
                elif char == ")":
                    nivel -= 1
                elif char == "[" or char == "]":
                    pass
                i += 1

        print("Archivo 'pseudocodigo.txt' completado.")

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