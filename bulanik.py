import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Girdi değişkenleri
oda_Sicakligi = ctrl.Antecedent(np.arange(0, 51, 1), 'oda_Sicakligi') #oda sıcaklık değerlerine 0-50 arasında değerler alacağını belirttim
cpu_sicaklik = ctrl.Antecedent(np.arange(0, 101, 1), 'cpu_sicaklik') # cpu_sicaklik degerine 0-100 arasında değerler alacağını belirtiyorum
calisan_Uygulama_Sayisi = ctrl.Antecedent(np.arange(0, 31, 1), 'calisan_Uygulama_Sayisi') # aynı şekilde

# Çıktı değişkeni
fan_Hizi = ctrl.Consequent(np.arange(0, 101, 1), 'fan_Hizi') # çıkış olarak 0-100 arasında fan hızı olacak.

# Üyelik fonksiyonları tanımlama
oda_Sicakligi['low'] = fuzz.trimf(oda_Sicakligi.universe, [0, 0, 50]) #oda sıcaklığı aralığının [0, 0, 50] aralığında üçgen bir şekle sahiptir. Bu fonksiyon, oda sıcaklığı düşükken fan hızının da düşük olmasını önerir.
oda_Sicakligi['medium'] = fuzz.trimf(oda_Sicakligi.universe, [0, 25, 50]) #oda sıcaklığı aralığının [0, 25, 50] aralığında üçgen bir şekle sahiptir. Bu fonksiyon, oda sıcaklığı orta seviyedeyken fan hızının da orta seviye olmasını önerir.
oda_Sicakligi['high'] = fuzz.trimf(oda_Sicakligi.universe, [25, 50, 50])#oda sıcaklığı aralığının [25, 50, 50] aralığında üçgen bir şekle sahiptir. Bu fonksiyon, oda sıcaklığı yüksekken fan hızının da yüksek olmasını önerir.

cpu_sicaklik['low'] = fuzz.trimf(cpu_sicaklik.universe, [0, 0, 50]) # yukardakilerle benzer şekilde
cpu_sicaklik['medium'] = fuzz.trimf(cpu_sicaklik.universe, [0, 50, 100])
cpu_sicaklik['high'] = fuzz.trimf(cpu_sicaklik.universe, [50, 100, 100])

calisan_Uygulama_Sayisi['low'] = fuzz.trimf(calisan_Uygulama_Sayisi.universe, [0, 0, 15]) # yukardakilerle benzer şekilde
calisan_Uygulama_Sayisi['medium'] = fuzz.trimf(calisan_Uygulama_Sayisi.universe, [0, 15, 30])
calisan_Uygulama_Sayisi['high'] = fuzz.trimf(calisan_Uygulama_Sayisi.universe, [15, 30, 30])

fan_Hizi['low'] = fuzz.trimf(fan_Hizi.universe, [0, 0, 50])  # bu durum fan hızının 0-50 arasında olduğunu belirtir.
fan_Hizi['medium'] = fuzz.trimf(fan_Hizi.universe, [0, 50, 100]) # bu durum fan hızının 50-100  arasında 50 ye yakın olduğunu belirtir.
fan_Hizi['high'] = fuzz.trimf(fan_Hizi.universe, [50, 100, 100]) # bu durum fan hızının 50-100 arasında 100 e yakın olduğunu belirtir.

# Kurallar oluşturma

# fan hizi  calisan uygulama sayisi ve oda sıcaklığı düşükse fan hizini düşük yap.
rule1 = ctrl.Rule(cpu_sicaklik['low'] & calisan_Uygulama_Sayisi['low'] & oda_Sicakligi['low'], fan_Hizi['low'])

#cpu,oda sıcaklığı düşük ve calisan uygulama sayisi orta ise fan hizini düşük yap.
rule2 = ctrl.Rule(cpu_sicaklik['low'] & calisan_Uygulama_Sayisi['medium']  & oda_Sicakligi['low'] ,fan_Hizi['low'])

#benzer şekillerde
rule3 = ctrl.Rule(cpu_sicaklik['medium'] & calisan_Uygulama_Sayisi['high'] & oda_Sicakligi['low'], fan_Hizi['medium'])
rule4 = ctrl.Rule(cpu_sicaklik['medium'] & calisan_Uygulama_Sayisi['low'] & oda_Sicakligi['medium'], fan_Hizi['medium'])
rule5 = ctrl.Rule(cpu_sicaklik['medium'] & calisan_Uygulama_Sayisi['medium'] & oda_Sicakligi['high'], fan_Hizi['high'])
rule6 = ctrl.Rule(cpu_sicaklik['medium'] & calisan_Uygulama_Sayisi['high'] & oda_Sicakligi['high'], fan_Hizi['high'])
rule7 = ctrl.Rule(cpu_sicaklik['low'] & calisan_Uygulama_Sayisi['high']  & oda_Sicakligi['high'], fan_Hizi['high'])
rule8 = ctrl.Rule(cpu_sicaklik['high'] & calisan_Uygulama_Sayisi['medium']  & oda_Sicakligi['low'] ,fan_Hizi['high'])
rule9 = ctrl.Rule(cpu_sicaklik['high'] & calisan_Uygulama_Sayisi['high']  & oda_Sicakligi['high'], fan_Hizi['high'])
#yine benzer şekillerde 3*3*3 = 27 adet rule yazılabilir ben 9 adet yazdım


# Kontrol sistemi oluşturma
fan_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9]) # burada tüm rule'lar control edilir

# Simülasyon yapma
fan = ctrl.ControlSystemSimulation(fan_ctrl)


# Girdi değerleri tanımlama
fan.input['cpu_sicaklik'] = 50
fan.input['oda_Sicakligi'] = 25
fan.input['calisan_Uygulama_Sayisi'] = 20

# Hesaplama yapma
fan.compute()

# Çıktı değerlerini yazdırma
print("Fan hızı ==> ", fan.output['fan_Hizi'])

