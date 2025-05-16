# Blackjack

Konzolová hra Blackjack ovládaná tlačítky, která přináší klasický herní zážitek přímo na váš Raspberry Pi Pico s displejem ve stylu Game Boye.

---

## Obsah
1. [Cíl](#cíl)
2. [Proces](#proces)
3. [Problémy](#problémy)
4. [Pravidla](#pravidla)
5. [Návod k použití](#návod-k-použití)
6. [Hardware](#hardware)
7. [Ukázka](#ukázka)

---

## Cíl
Cílem bylo vytvořit hratelný Blackjack na Raspberry Pi Pico s displejem, připomínajícím Game Boy.

---

## Proces
- V prvním pololetí jsem vytvořil konzolovou verzi hry s ovládáním pomocí tlačítek.
- Ve druhém pololetí jsem přidal renderování hry na displeji a propojil ho s původním kódem.

---

## Problémy
- Kvůli použití `time.sleep()` není časování hry plynulé, ale při hraní to není příliš znatelné.
- Displej umožňuje zobrazit pouze 4 karty v jedné řadě. To omezuje hru, protože je malá šance, že hráč nebo krupiér dostane víc než 4 karty. Zmenšení karet způsobuje, že jsou téměř nečitelné.
- Kvůli nedostatku paměti RAM na Pico jsem musel odstranit možnost rozdělit dvojici karet na dvě herní ruce (split).

---

## Pravidla

# Cíl hry
Porazit krupiéra tím, že budete mít hodnotu karet **blíže k 21** než krupiér, **aniž byste tuto hodnotu překročili**.

---

# Hodnoty karet
- **2–10**: Nominální hodnota  
- **J, Q, K**: 10 bodů  
- **Eso (A)**: 1 nebo 11 bodů (podle toho, co je výhodnější)

---

# Průběh hry

1. **Prvotní rozdání**:
   - Každý hráč i krupiér dostane **2 karty**
   - Krupiér ukáže **1 kartu lícem nahoru**, druhou ponechá **lícem dolů** („hole card“)

2. **Tah krupiéra**:
   - Krupiér odkryje skrytou kartu
   - Musí **táhnout, dokud nedosáhne alespoň 17 bodů**
   - Při hodnotě **17 a více** musí **zůstat stát**

---

# Výhra a výplaty
- **Blackjack** (eso + karta s hodnotou 10 při prvním rozdání): Výplata **3:2**
- **Vyšší hodnota než krupiér bez překročení 21**: Výplata **1:1**
- **Shoda s krupiérem**: **Remíza** (nikdo nevyhrává ani neprohrává)
- **Krupiér přetáhne, hráč ne**: Hráč **vyhrává**

---

## Návod k použití

### Nastavení sázky a balancu:
- **Joystick nahoru** – zvýší hodnotu (amount)  
- **Joystick dolů** – sníží hodnotu  
- **Joystick doleva** – odečte hodnotu z balancu / přidá k sázce  
- **Joystick doprava** – přidá hodnotu do balancu / odečte ze sázky  
- **Joystick stisk** – potvrdí hodnotu balancu / sázky  

### Průběh hry:
- **Tlačítko H (Hit)** – přidá hráči kartu  
- **Tlačítko P (Pass)** – ukončí tah hráče  
- **Tlačítko D (Double)** – přidá hráči kartu a ukončí jeho tah  

---

## Hardware
- **[Raspberry Pi Pico 2 H](https://rpishop.cz/590612/raspberry-pi-pico-2-h/)**
- **[Waveshare 1.3" LCD displej (240×240, SPI)](https://rpishop.cz/lcd-oled-displeje/4022-waveshare-13-lcd-displej-pro-raspberry-pi-pico-240240-spi.html)**
- **Micro-USB kabel**

---

## Ukázka
![Ukázka hry](https://github.com/user-attachments/assets/97c523bc-52c9-4472-8c38-767d63d46572)
