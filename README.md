# 🎰 Blackjack

Retro stylový **Blackjack pro Raspberry Pi Pico**, který kombinuje kouzlo Game Boye s programováním a vlastnoručně ovládanou hratelností. Konzolová verze klasické karetní hry, kterou ovládáte tlačítky — přímo na vlastním mikrokontroléru.

---

## 📄 Obsah
1. [🎯 Cíl](#-cíl)
2. [⚙️ Proces](#️-proces)
3. [🐞 Problémy](#-problémy)
4. [📜 Pravidla](#-pravidla)
5. [🕹️ Návod k použití](#️-návod-k-použití)
6. [🔌 Hardware](#-hardware)
7. [📸 Ukázka](#-ukázka)

---

## 🎯 Cíl
Cílem bylo vytvořit jednoduchou, ale funkční hru Blackjack, běžící na Raspberry Pi Pico s displejem připomínajícím Game Boy. Celý projekt byl navržen s ohledem na minimální prostředky a maximální nostalgii.

---

## ⚙️ Proces
- 🔧 **1. pololetí**: Vytvoření herní logiky s textovým výstupem v konzoli a ovládáním pomocí tlačítek.
- 🎨 **2. pololetí**: Integrace grafického rozhraní na displej a propojení s herní logikou pro plně vizuální zážitek.

---

## 🐞 Problémy
- ⏱️ **Zpoždění** – Použití `time.sleep()` ovlivňuje plynulost hry. Není to zásadní, ale časování není ideální.
- 🃏 **Zobrazování karet** – Displej umožňuje pouze 4 karty v řadě. Při vícero kartách je nutné volit kompromis mezi velikostí a čitelností.
- 🧠 **Paměť** – Rozdělení ruky (split) bylo odstraněno kvůli limitům RAM u Raspberry Pi Pico.
- 📹 **Video** -Video se mi nepodařilo natočit kvůli odleskům a světlu z displeje, proto jsem přiložil obrázek, který ukazuje, jak hra vypadá v akci.


---

## 📜 Pravidla

### 🎯 Cíl hry
Porazit krupiéra tím, že vaše kombinace bude **blíže 21** než jeho – ale **nepřesáhne ji**.

---

### 🃏 Hodnoty karet
- **2–10**: Odpovídá číselné hodnotě  
- **J, Q, K**: 10 bodů  
- **Eso (A)**: 1 nebo 11 bodů (co je výhodnější)

---

### 🔄 Průběh hry

1. **Začátek**:
   - Hráč i krupiér obdrží **2 karty**
   - Krupiér odkryje **1 kartu**, druhou nechá skrytou

2. **Tah krupiéra**:
   - Odkryje svou druhou kartu
   - Táhne, dokud nedosáhne **alespoň 17 bodů**
   - Na **17 a více** už netáhne

---

### 💰 Výhry
- **Blackjack (A + 10)**: 3:2  
- **Vyšší kombinace než krupiér** bez překročení: 1:1  
- **Remíza**: Nikdo nevyhrává  
- **Krupiér přetáhne, hráč ne**: Výhra pro hráče  

---

## 🕹️ Návod k použití

### 🎛️ Nastavení sázky a balancu:
- **Joystick nahoru** – zvýší hodnotu (amount)  
- **Joystick dolů** – sníží hodnotu  
- **Joystick doleva** – odečte hodnotu z balancu / přidá ke sázce  
- **Joystick doprava** – přidá hodnotu do balancu / odečte ze sázky  
- **Joystick stisk** – uloží nastavení

### ▶️ Herní tlačítka:
- **H (Hit)** – přidá kartu hráči  
- **P (Pass)** – ukončí tah hráče  
- **D (Double)** – přidá kartu a ihned končí tah  

---

## 🔌 Hardware
- **[Raspberry Pi Pico 2 H](https://rpishop.cz/590612/raspberry-pi-pico-2-h/)**  
- **[Waveshare 1.3" LCD displej (240×240, SPI)](https://rpishop.cz/lcd-oled-displeje/4022-waveshare-13-lcd-displej-pro-raspberry-pi-pico-240240-spi.html)**  
- **Micro-USB kabel**

---

## 📸 Ukázka
![Ukázka hry](https://github.com/user-attachments/assets/97c523bc-52c9-4472-8c38-767d63d46572)
