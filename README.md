# Blackjack

Konzolová hra Blackjack ovládaná tlačítky, která přináší klasický herní zážitek přímo na váš Raspberry Pi Pico.

---

## Obsah
1. [Cíl](#Cíl)
2. [Proces](#Proces)
3. [Problémi](#Problémi)
4. [Návod k použití](#Návodkpoužití)
5. [Hardware](#hardware)
6. [Ukázka](#ukázka)

---

## Cíl  
  Mým cílem bylo udělat blackjack na raspberry pi s displejem na podobu gameboyje.  
  
## Proces  
  V prvním pololetí jsem zhotovil kod pro blackjack s hraním přes tlačítko a vypisované do konzole.  
  V druhém pololetí jsem napsal kod na renderovaný hry na displeji a spároval jsem ho s kodem.  
  
## Problémi  
  - kvůli používání příkazu time.sleep() není časování hry prosné, tento problém je na první pohled nepatrný.  
  - kvůli velikosti displeje se na plochu vejdou jen 4 karty v řadě což je problém protože je malá šance že si hráč nebo krupiér 
    může vytáhnout více než čtyři karty tento problém nemůžu moc spravit protože po zmenšení karet jsou skoro nečitelné.  
  - z hry jsem musel odstranit možnost rozdělit jednu herní ruku na dva při schodě karet protože na picu mi došla RAM pro zpracování kodu.  
  
## Návodkpoužití
  - nastavovaní balancu a sázky  
      joystick nahoru     = zvedne hodnotu ammount  
      joystick dolu       = zmensi hodnotu ammount  
      joystick doleve     = odebere hodnotu ammount od balancu/sázky  
      joystick doprava    = přídá hodnotu ammount od balancu/sázky  
      joystick stisk      = uloží hodnotu balanc/sazka  
  
  - prubeh hry  
      tlacitko h (hit)    = přidá hráčovy jednu kartu a rozhodne viz:    
      tlacitko p (pass)   = ukončí hráčovo kolo    
      tlacitko d (double) = přidá hráčovy jednu kartu a ukončí jeho kolo  
    
## Hardware
- **Raspberry Pi Pico**
- **[Waveshare 1,3" LCD displej pro Raspberry Pi Pico, 240×240, SPI](https://rpishop.cz/lcd-oled-displeje/4022-waveshare-13-lcd-displej-pro-raspberry-pi-pico-240240-spi.html)**
- **Micro-USB power cable**

---
## Ukázka
![1747412186078](https://github.com/user-attachments/assets/97c523bc-52c9-4472-8c38-767d63d46572)
---
