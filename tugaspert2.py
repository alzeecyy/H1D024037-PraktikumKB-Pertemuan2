import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from skfuzzy import control as ctrl

# --- 1. Variabel Input & Output ---
suhu = ctrl.Antecedent(np.arange(0, 41, 1), 'suhu')           # 0-40 °C
kelembapan = ctrl.Antecedent(np.arange(0, 101, 1), 'kelembapan')  # 0-100 %
kecepatan = ctrl.Consequent(np.arange(0, 101, 1), 'kecepatan_kipas')  # 0-100

# --- 2. Himpunan Fuzzy ---
# Suhu
suhu['dingin'] = fuzz.trimf(suhu.universe, [0, 0, 20])
suhu['normal'] = fuzz.trimf(suhu.universe, [10, 20, 30])
suhu['panas']  = fuzz.trimf(suhu.universe, [20, 40, 40])

# Kelembapan
kelembapan['kering'] = fuzz.trimf(kelembapan.universe, [0, 0, 50])
kelembapan['sedang'] = fuzz.trimf(kelembapan.universe, [25, 50, 75])
kelembapan['lembap'] = fuzz.trimf(kelembapan.universe, [50, 100, 100])

# Kecepatan Kipas
kecepatan['lambat'] = fuzz.trimf(kecepatan.universe, [0, 0, 50])
kecepatan['sedang'] = fuzz.trimf(kecepatan.universe, [25, 50, 75])
kecepatan['cepat']  = fuzz.trimf(kecepatan.universe, [50, 100, 100])

# --- 3. Aturan Fuzzy ---
rule1 = ctrl.Rule(suhu['dingin'] | kelembapan['lembap'], kecepatan['lambat'])
rule2 = ctrl.Rule(suhu['normal'] & kelembapan['sedang'], kecepatan['sedang'])
rule3 = ctrl.Rule(suhu['panas']  | kelembapan['kering'], kecepatan['cepat'])

# --- 4. Control System ---
kecepatan_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
kipas = ctrl.ControlSystemSimulation(kecepatan_ctrl)

# --- 5. Pengujian ---
if __name__ == '__main__':
    print("=== PENGUJIAN SISTEM KONTROL KIPAS ANGIN ===")
    try:
        input_suhu = float(input("Masukkan nilai Suhu (0-40 °C): "))
        input_kelembapan = float(input("Masukkan nilai Kelembapan (0-100 %): "))

        input_suhu = max(0, min(40, input_suhu))
        input_kelembapan = max(0, min(100, input_kelembapan))

        kipas.input['suhu'] = input_suhu
        kipas.input['kelembapan'] = input_kelembapan
        kipas.compute()

        hasil_kecepatan = kipas.output['kecepatan_kipas']
        print(f"\n=> Suhu: {input_suhu} °C | Kelembapan: {input_kelembapan} %")
        print(f"=> Output Kecepatan Kipas: {hasil_kecepatan:.2f}")

    except ValueError:
        print("Error: Harap masukkan angka yang valid.")

    # Visualisasi
    suhu.view()
    kelembapan.view()
    kecepatan.view(sim=kipas)
    plt.show()