# adc.py — ADConverter v0.3
# Classe base para leitura ADC multiplataforma em MicroPython
# Suporte: ESP8266, ESP32 (S3/C3), Raspberry Pi Pico (RP2040), STM32
#
# Autor : Flavio Guimarães — Inovando com Ideias
# GitHub: github.com/inovando-com-ideias
# Licença: MIT

from machine import Pin, ADC
import os

class ADConverter:
    """
    Classe base para leitura ADC multiplataforma.
    Detecta automaticamente a plataforma e configura hardware e VREF.

    Parâmetros:
        pino   : número do pino ADC (ignorado no ESP8266)
        v_ref  : tensão de referência em Volts ou 'externo'
                 Padrão: tensão de operação da placa (3.3V para todas em MicroPython)
                 Valores válidos por plataforma:
                   ESP32        → 1.0, 1.34, 2.0, 3.3
                   ESP8266      → 1.0 (ESP-01, sem divisor) ou 3.3 (NodeMCU/D1 Mini)
                   RP2040       → 3.3 (fixo, não configurável)
                   STM32        → 3.3 (fixo, não configurável)

    Exemplo:
        adc = ADConverter(pino=34)           # ESP32, v_ref=3.3 automático
        adc = ADConverter(pino=34, v_ref=1.0) # ESP32, range 0~1V
    """

    # Identificadores de plataforma
    PLAT_ESP8266 = 'esp8266'
    PLAT_ESP32   = 'esp32'
    PLAT_RP2040  = 'rp2040'
    PLAT_STM32   = 'pyboard'

    # Padrão de v_ref por plataforma (tensão de operação)
    _VREF_PADRAO = {
        PLAT_ESP8266 : 3.3,
        PLAT_ESP32   : 3.3,
        PLAT_RP2040  : 3.3,
        PLAT_STM32   : 3.3,
    }

    # Valores válidos de v_ref por plataforma
    _VREF_VALIDOS = {
        PLAT_ESP8266 : [1.0, 3.3],
        PLAT_ESP32   : [1.0, 1.34, 2.0, 3.3],
        PLAT_RP2040  : [3.3],
        PLAT_STM32   : [3.3],
    }

    def __init__(self, pino=0, v_ref=None):
        self._plataforma = os.uname()[0].lower()
        self._pino       = pino
        self._adc        = None
        self._ADC_MAX    = 4096
        self._ADC_MIN    = 0

        # Detecta v_ref padrão da plataforma se não informado
        if v_ref is None:
            self._v_ref = self._VREF_PADRAO.get(self._plataforma, 3.3)
        else:
            self._v_ref = v_ref

        self._validar_vref()
        self._configurar()

    # ------------------------------------------------------------------
    # Validação
    # ------------------------------------------------------------------

    def _validar_vref(self):
        """Valida se v_ref é suportado na plataforma atual."""
        validos = self._VREF_VALIDOS.get(self._plataforma)

        if validos is None:
            raise NotImplementedError(
                f"Plataforma '{self._plataforma}' não suportada ainda."
            )

        if self._v_ref not in validos:
            raise ValueError(
                f"v_ref={self._v_ref} não é suportado em '{self._plataforma}'.\n"
                f"Valores válidos: {validos}"
            )

    # ------------------------------------------------------------------
    # Configuração de hardware
    # ------------------------------------------------------------------

    def _configurar(self):
        """Configura o ADC de acordo com a plataforma e v_ref."""

        if self._plataforma == self.PLAT_ESP8266:
            self._adc     = ADC(0)
            self._ADC_MAX = 1024

        elif self._plataforma == self.PLAT_ESP32:
            self._adc = ADC(Pin(self._pino))
            # Dicionário local — só criado quando rodando em ESP32
            attn = {
                1.0  : ADC.ATTN_0DB,
                1.34 : ADC.ATTN_2_5DB,
                2.0  : ADC.ATTN_6DB,
                3.3  : ADC.ATTN_11DB,
            }
            self._adc.atten(attn[self._v_ref])
            self._ADC_MAX = 4096

        elif self._plataforma == self.PLAT_RP2040:
            self._adc     = ADC(self._pino)
            self._ADC_MAX = 65535

        elif self._plataforma == self.PLAT_STM32:
            self._adc     = ADC(Pin(self._pino))
            self._ADC_MAX = 4096

    # ------------------------------------------------------------------
    # Leituras
    # ------------------------------------------------------------------

    def ler(self):
        """Retorna o valor bruto do ADC."""
        return self._adc.read()

    def ler_normalizado(self):
        """Retorna valor entre 0.0 e 1.0, independente da plataforma."""
        return self.ler() / self._ADC_MAX

    def ler_tensao(self):
        """Retorna a tensão estimada em Volts, baseada no v_ref configurado."""
        return self.ler_normalizado() * self._v_ref

    # ------------------------------------------------------------------
    # Propriedades
    # ------------------------------------------------------------------

    @property
    def plataforma(self):
        """Plataforma detectada."""
        return self._plataforma

    @property
    def resolucao(self):
        """Valor máximo do ADC (steps)."""
        return self._ADC_MAX

    @property
    def v_ref(self):
        """Tensão de referência configurada."""
        return self._v_ref

    # ------------------------------------------------------------------
    # Representação
    # ------------------------------------------------------------------

    def __repr__(self):
        return (
            f"ADConverter("
            f"pino={self._pino}, "
            f"plataforma='{self._plataforma}', "
            f"resolucao={self._ADC_MAX}, "
            f"v_ref={self._v_ref}V)"
        )