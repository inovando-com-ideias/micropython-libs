# com_tensao.py — Exemplo de leitura com conversão de tensão
# Autor: Flavio Guimarães — Inovando com Ideias
# GitHub: github.com/inovando-com-ideias

from ADConverter.adc import ADConverter
import time

# Cria o objeto ADC
# ESP32: use pinos ADC válidos (32-39)
# ESP8266: pino é ignorado automaticamente
# Pico: use pinos 26, 27 ou 28
adc = ADConverter(pino=34)

print(f"Plataforma : {adc.plataforma}")
print(f"Resolução  : {adc.resolucao} steps")
print(f"Referência : 3.3V")
print("=" * 40)

while True:
    tensao = adc.ler_tensao()

    # Barra visual proporcional à tensão
    barra = int((tensao / 3.3) * 20)
    visual = "[" + "█" * barra + "░" * (20 - barra) + "]"

    print(f"{visual} {tensao:.2f}V")
    time.sleep(0.5)