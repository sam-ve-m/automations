from enum import Enum


from src.core.enums.regions_collections.BR import (
    AcaoBR,
    BDRdeAcao,
    Opcoes,
    Futuros,
    Fiis,
    EtfBR,
    BDRdeEtf,
)
from src.core.enums.regions_collections.US import (
    AcaoUS,
    EtfUS,
    ADRdeAcao,
    ADRdeEtf,
)


class QuoteTypes(Enum):
    acao_br = AcaoBR
    bdr_de_acao = BDRdeAcao
    opcoes = Opcoes
    futuros = Futuros
    fiis = Fiis
    etf_br = EtfBR
    bdr_de_etf = BDRdeEtf
    acao_us = AcaoUS
    etf_us = EtfUS
    adr_de_acao = ADRdeAcao
    adr_de_etf = ADRdeEtf


class QuoteTypesConstraints(Enum):
    acao_br = "BR:stock:local"
    bdr_de_acao = "BR:stock:DR"
    opcoes = "BR:option:local"
    futuros = "BR:future:local"
    fiis = "BR:fii:local"
    etf_br = "BR:etf:local"
    bdr_de_etf = "BR:etf:DR"
    acao_us = "US:stock:local"
    etf_us = "US:etf:local"
    adr_de_acao = "US:stock:DR"
    adr_de_etf = "US:etf:DR"
