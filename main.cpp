#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <cstdio>
#include <random>

using namespace std;

class GramaticaBackusNaur {
public:
    string cadena_final;

    GramaticaBackusNaur() {
        cadena_final = "";
    }

    void derivar(int n_objetivo) {
        string cadena = "S";
        int ifs_actuales = 0;
        long long step_counter = 0;
        ofstream f("derivaciones_random.txt");
        if (!f.is_open()) {
            cerr << "Error al abrir el archivo derivaciones_random.txt" << endl;
            return;
        }

        f << "DERIVACION ALEATORIA PASO A PASO\n";
        f << "Paso " << step_counter << ": " << cadena << "\n";

        // Mientras existan 'S' o 'A' en la cadena
        while (cadena.find('S') != string::npos || cadena.find('A') != string::npos) {
            vector<size_t> todos;
            for (size_t i = 0; i < cadena.length(); ++i) {
                if (cadena[i] == 'S' || cadena[i] == 'A') {
                    todos.push_back(i);
                }
            }
            size_t idx_random = rand() % todos.size();
            size_t idx = todos[idx_random];
            char simbolo = cadena[idx];
            string reemplazo = "";
            if (simbolo == 'S') {
                if (ifs_actuales < n_objetivo) {
                    reemplazo = "iCt(S)[A]";
                    ifs_actuales++;
                } else {
                    reemplazo = ""; // S muere
                }
            }
            else if (simbolo == 'A') {
                if (ifs_actuales < n_objetivo) {
                    if (rand() % 2 == 0) {
                        reemplazo = ";e(S)";
                    } else {
                        reemplazo = "epsilon";
                    }
                } else {
                    reemplazo = "epsilon";
                }
            }

            cadena.replace(idx, 1, reemplazo);
            step_counter++;
            f << "Paso " << step_counter << ": " << cadena << "\n";
        }
        f.close();

        size_t pos = 0;
        while ((pos = cadena.find("epsilon", pos)) != string::npos) {
            cadena.replace(pos, 7, "");
        }

        this->cadena_final = cadena;
        cout << "Archivo 'derivaciones_random.txt' completado." << endl;
        cout << "Se realizaron " << step_counter << " pasos de derivacion." << endl;
        guardar_pseudocodigo();
    }

    void guardar_pseudocodigo() {
        ofstream f("pseudocodigo.txt");
        if (!f.is_open()) {
            cerr << "Error al abrir pseudocodigo.txt" << endl;
            return;
        }

        int nivel = 0;
        string indent_str = "  ";
        size_t i = 0;
        string txt = this->cadena_final;
        size_t n = txt.length();

        while (i < n) {
            if (i + 3 <= n && txt.substr(i, 3) == "iCt") {
                for(int k=0; k<nivel; k++) f << indent_str;
                f << "if (condicion):" << "\n";
                i += 3;
                continue;
            }

            if (i + 2 <= n && txt.substr(i, 2) == ";e") {
                for(int k=0; k<nivel; k++) f << indent_str;
                f << "else:" << "\n";
                i += 2;
                continue;
            }

            char c = txt[i];
            if (c == '(') {
                nivel++;
                if (i + 1 < n && txt[i+1] == ')') {
                    for(int k=0; k<nivel; k++) f << indent_str;
                    f << "pass\n";
                }
            }
            else if (c == ')') {
                nivel--;
            }
            else if (c == '[' || c == ']') {
                // pass
            }
            i++;
        }

        f.close();
        cout << "Archivo 'pseudocodigo.txt' completado." << endl;
    }
};

int main() {
    srand(time(0));
    GramaticaBackusNaur gbn;
    int n, opc = 0;
    printf("1. Correr automaticamente\n");
    printf("2. Correr manualmente\n");
    printf("Seleccione una opcion: ");
    scanf("%d", &opc);
    if (opc == 1) {
        const int min_val = 2;
        const int max_val = 100000;
        std::random_device rd;
        std::mt19937 generador(rd());
        std::uniform_int_distribution<int> distribucion(min_val, max_val);
        printf("Corriendo automaticamente...\n");
        n = distribucion(generador);
        cout << "Numero de IFs deseados: " << n << endl;
    } else {
        printf("Corriendo manualmente...\n");
        cout << "Numero de IFs deseados: ";
        if (!(cin >> n)) {
        cout << "No se ingreso un numero valido, se usara 5 por defecto." << endl;
        n = 5;
        }
    }
    cout << "Generando " << n << " IFs..." << endl;
    gbn.derivar(n);
    cout << "Proceso finalizado" << endl;

    return 0;
}