# basic.py — Exemplo básico de uso da classe ADConverter
# Autor: Flavio Guimarães — Inovando com Ideias
# GitHub: github.com/inovando-com-ideias

from ADConverter.adc import ADConverter
import time

# Cria o objeto ADC no pino 34 (ESP32)
# Para ESP8266 o pino é ignorado automaticamente
adc = ADConverter(pino=34)

print(f"Plataforma: {adc.plataforma}")
print(f"Resolução:  {adc.resolucao} bits")
print("---")

while True:
    valor     = adc.ler()
    normaliz  = adc.ler_normalizado()
    tensao    = adc.ler_tensao()

    print(f"Bruto: {valor:5d} | Norm: {normaliz:.3f} | Tensão: {tensao:.2f}V")
    time.sleep(0.5)