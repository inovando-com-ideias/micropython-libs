# com_tensao.py — Exemplo com barra visual de tensão (atualização in-place)
# Autor : Flavio Guimarães — Inovando com Ideias
# GitHub: github.com/inovando-com-ideias

from ADConverter.adc import ADConverter
import time

adc = ADConverter(pino=26)

print(f"Plataforma : {adc.plataforma}")
print(f"Resolução  : {adc.resolucao} steps")
print(f"V_Ref      : {adc.v_ref}V")
print("=" * 40)
print()  # linha reservada para a barra — não será sobrescrita

while True:
    tensao = adc.ler_tensao()

    barra  = int((tensao / adc.v_ref) * 20)
    visual = "[" + "█" * barra + "░" * (20 - barra) + "]"
    linha  = f"{visual} {tensao:.2f}V   "  # espaços extras apagam resíduo

    print(linha, end='\r')
    time.sleep(0.5)