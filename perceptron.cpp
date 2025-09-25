#include <bits/stdc++.h>
using namespace std;

class Perceptron
{
private:
    double tasa_aprendizaje;
    int epocas;
    vector<double> pesos;
    double bias;

public:
    Perceptron(int n_entradas, double tasa = 0.1, int ep = 100) : tasa_aprendizaje(tasa), epocas(ep)
    {
        // Inicializar pesos y bias con valores aleatorios
        mt19937 gen(random_device{}());
        uniform_real_distribution<> dis(0.0, 1.0);

        pesos.resize(n_entradas);
        for (int i = 0; i < n_entradas; ++i)
        {
            pesos[i] = dis(gen);
        }
        bias = dis(gen);
    }

    int activacion(const vector<int> &entrada)
    {
        double z = 0.0;
        for (size_t i = 0; i < pesos.size(); ++i)
        {
            z += pesos[i] * entrada[i];
        }
        return (z + bias > 0) ? 1 : 0;
    }

    void entrenamiento(const vector<vector<int>> &entradas,
                       const vector<int> &salidas)
    {
        for (int epoch = 0; epoch < epocas; ++epoch)
        {
            for (size_t j = 0; j < entradas.size(); ++j)
            {
                int z = activacion(entradas[j]);
                int error = salidas[j] - z;
                for (size_t i = 0; i < pesos.size(); ++i)
                {
                    pesos[i] += tasa_aprendizaje * entradas[j][i] * error;
                }
                bias += tasa_aprendizaje * error;
            }
        }
    }

    // Métodos para acceder a pesos y bias
    const vector<double> &getPesos() const { return pesos; }
    double getBias() const { return bias; }
};

int main()
{
    // Inicializar datos de entrenamiento
    vector<vector<int>> entradas_verdes = {
        {0, 255, 0}, {30, 200, 30}, {60, 220, 40}, {50, 180, 50}, {70, 240, 60}, {20, 210, 20}, {40, 190, 40}, {10, 230, 30}, {80, 200, 70}, {90, 250, 80}, {0, 255, 0}, {50, 205, 50}, {34, 139, 34}, {0, 100, 0}, {127, 255, 0}, {46, 139, 87}, {144, 238, 144}, {107, 142, 35}, {0, 128, 0}, {152, 251, 152}};
    vector<int> salidas_verdes(20, 1);

    vector<vector<int>> entradas_rojos_azules = {
        {255, 0, 0}, {200, 30, 20}, {180, 50, 40}, {150, 40, 60}, {220, 60, 50}, {240, 30, 70}, {210, 80, 90}, {190, 40, 30}, {230, 20, 20}, {255, 100, 90}, {255, 0, 0}, {220, 20, 60}, {178, 34, 34}, {139, 0, 0}, {255, 69, 0}, {205, 92, 92}, {240, 128, 128}, {128, 0, 0}, {255, 99, 71}, {196, 30, 58}, {0, 0, 255}, {0, 0, 128}, {100, 149, 237}, {65, 105, 225}, {0, 191, 255}, {70, 130, 180}, {0, 255, 255}, {0, 128, 128}, {173, 216, 230}, {135, 206, 235}, {30, 144, 255}, {25, 25, 112}, {0, 139, 139}, {10, 50, 100}, {0, 70, 150}, {15, 82, 186}, {138, 43, 226}, {176, 224, 230}, {5, 10, 150}, {0, 51, 102}};
    vector<int> salidas_rojos_azules = {
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};

    // Combinar entradas para el primer perceptrón
    vector<vector<int>> entradas_combinadas = entradas_verdes;
    entradas_combinadas.insert(entradas_combinadas.end(),
                               entradas_rojos_azules.begin(),
                               entradas_rojos_azules.end());
    vector<int> salidas_combinadas = salidas_verdes;
    salidas_combinadas.insert(salidas_combinadas.end(),
                              entradas_rojos_azules.size(), 0);

    // Entrenar perceptrones
    double tasa_aprendizaje = 0.01;
    int epocas = 100;

    Perceptron perceptron1(3, tasa_aprendizaje, epocas);
    perceptron1.entrenamiento(entradas_combinadas, salidas_combinadas);

    Perceptron perceptron2(3, tasa_aprendizaje, epocas);
    perceptron2.entrenamiento(entradas_rojos_azules, salidas_rojos_azules);

    // Datos de prueba
    vector<vector<int>> ejemplos_complicado = {
        {255, 10, 10}, {175, 40, 60}, {210, 30, 0}, {255, 165, 0}, {153, 50, 204}, {250, 128, 114}, {200, 0, 0}, {192, 0, 0}, {230, 25, 75}, {188, 143, 143}, {0, 200, 0}, {154, 205, 50}, {60, 179, 113}, {124, 252, 0}, {30, 60, 0}, {0, 250, 154}, {173, 255, 47}, {169, 169, 169}, {0, 150, 50}, {85, 107, 47}, {0, 150, 200}, {24, 66, 126}, {106, 90, 205}, {176, 196, 222}, {123, 104, 238}, {153, 204, 255}, {0, 102, 204}, {47, 79, 79}, {5, 50, 250}, {95, 158, 160}};

    // Clasificar ejemplos
    int rojos = 0, verdes = 0, azules = 0;

    cout << "Perceptron 1\n";
    cout << "Pesos: ";
    for (double w : perceptron1.getPesos())
        cout << w << " ";
    cout << "\nBias: " << perceptron1.getBias() << "\n";

    cout << "Perceptron 2\n";
    cout << "Pesos: ";
    for (double w : perceptron2.getPesos())
        cout << w << " ";
    cout << "\nBias: " << perceptron2.getBias() << "\n";

    for (const auto &entrada : ejemplos_complicado)
    {
        int z = perceptron1.activacion(entrada);
        if (z)
        {
            verdes++;
        }
        else
        {
            int z2 = perceptron2.activacion(entrada);
            if (z2)
            {
                rojos++;
            }
            else
            {
                azules++;
            }
        }
    }

    cout << "Cantidad de verdes: " << verdes << "\n";
    cout << "Cantidad de rojos: " << rojos << "\n";
    cout << "Cantidad de azules: " << azules << "\n";

    return 0;
}