# adc.py — ADConverter v0.2
# Suporte: ESP8266, ESP32 (S3/C3), Raspberry Pi Pico (RP2040), STM32
# Autor: Flavio Guimarães — Inovando com Ideias
# GitHub: github.com/inovando-com-ideias

from machine import Pin, ADC
import os

class ADConverter:
    """
    Classe base para leitura ADC.
    Detecta automaticamente a plataforma e configura o hardware.
    """

    # Constantes de plataforma
    PLAT_ESP8266 = 'esp8266'
    PLAT_ESP32   = 'esp32'
    PLAT_RP2040  = 'rp2040'
    PLAT_STM32   = 'pyboard'

    def __init__(self, pino=0):
        self._plataforma = os.uname()[0].lower()
        self._pino = pino
        self._adc = None
        self._ADC_MAX = 4096
        self._ADC_MIN = 0
        self._configurar()

    def _configurar(self):
        """Configura o ADC de acordo com a plataforma detectada."""
        if self._plataforma == self.PLAT_ESP8266:
            self._adc = ADC(0)
            self._ADC_MAX = 1024

        elif self._plataforma == self.PLAT_ESP32:
            self._adc = ADC(Pin(self._pino))
            self._adc.atten(ADC.ATTN_11DB)
            self._ADC_MAX = 4096

        elif self._plataforma == self.PLAT_RP2040:
            self._adc = ADC(self._pino)
            self._ADC_MAX = 65535

        elif self._plataforma == self.PLAT_STM32:
            self._adc = ADC(Pin(self._pino))
            self._ADC_MAX = 4096

        else:
            raise NotImplementedError(
                f"Plataforma '{self._plataforma}' não suportada ainda."
            )

    def ler(self):
        """Retorna o valor bruto do ADC."""
        return self._adc.read()

    def ler_normalizado(self):
        """Retorna valor entre 0.0 e 1.0, independente da plataforma."""
        return self.ler() / self._ADC_MAX

    def ler_tensao(self, v_ref=3.3):
        """Retorna a tensão estimada em Volts."""
        return self.ler_normalizado() * v_ref

    @property
    def plataforma(self):
        return self._plataforma

    @property
    def resolucao(self):
        return self._ADC_MAX

    def __repr__(self):
        return (f"ADConverter(pino={self._pino}, "
                f"plataforma={self._plataforma}, "
                f"resolucao={self._ADC_MAX})")