# ADConverter

Classe base para leitura analógica (ADC) em MicroPython.  
Detecta automaticamente a plataforma e configura o hardware.

## Plataformas suportadas

| Plataforma                 | Chip             | Resolução          |                         |
|----------------------------|------------------|--------------------|-------------------------|
| ESP8266 (NodeMCU/D1 Mini)  | ESP8266          | 10 bits (0–1023)   | 3.3V (divisor na placa) |
| ESP8266 (ESP-01)           | ESP8266          | 10 bits (0–1023)   | 1.0V (sem divisor)      |
| ESP32 / S3 / C3            | ESP32            | 12 bits (0–4095)   |                         |
| Raspberry Pi Pico          | RP2040           | 16 bits (0–65535)  |                         |
| STM32 Blackpill / Nucleo   | STM32            | 12 bits (0–4095)   |                         |

## Instalação

Copie o arquivo `adc.py` para a raiz do seu dispositivo ou  
para uma pasta chamada `ADConverter/`.

## Uso básico

```python
from ADConverter.adc import ADConverter
import time

adc = ADConverter(pino=34)     # ESP32
# adc = ADConverter()          # ESP8266 (pino ignorado)
# adc = ADConverter(v_ref=3.3) # ESP8266 NodeMCU/D1 Mini — com divisor de tensão na placa
# adc = ADConverter(v_ref=1.0) # ESP8266 ESP-01 — sem divisor de tensão
# adc = ADConverter(pino=26) # Pico

while True:
    print(adc.ler())             # valor bruto
    print(adc.ler_normalizado()) # 0.0 a 1.0
    print(adc.ler_tensao())      # em Volts
    time.sleep(0.5)
```

## Métodos

| Método              | Retorno | Descrição                     |
|---------------------|---------|-------------------------------|
| `ler()`             | `int`   | Valor bruto do ADC            |
| `ler_normalizado()` | `float` | Valor entre 0.0 e 1.0         |
| `ler_tensao(v_ref)` | `float` | Tensão em Volts (padrão 3.3V) |
| `plataforma`        | `str`   | Nome da plataforma detectada  |
| `resolucao`         | `int`   | Valor máximo do ADC           |

## Exemplos

- [`examples/basic/basic.py`](examples/basic/basic.py) — leitura simples
- [`examples/com_tensao/com_tensao.py`](examples/com_tensao/com_tensao.py) — leitura com barra visual

## Herança

Esta classe foi projetada para ser extendida:

```python
from ADConverter.adc import ADConverter

class Potenciometro(ADConverter):
    def percentual(self):
        return round(self.ler_normalizado() * 100, 1)
```

## Licença
MIT — Flavio Guimarães — [Inovando com Ideias](https://youtube.com/@inovandocomideias)