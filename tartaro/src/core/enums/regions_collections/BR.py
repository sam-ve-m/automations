from enum import Enum


class AcaoBR(Enum):
    initial_part = [
        "general_information_abalustre",
        "assets_identifications_refinitiv",
        "text_translated_general_information_refinitiv",
    ]
    main_brands = ["general_information_refinitiv"]
    general = ["general_information_morningstar"]
    financial = ["financial_information_morningstar"]
    financial_indicators = ["financial_information_morningstar"]
    balance_sheet = []
    market_announcements = ["street_events_refinitiv"]


class BDRdeAcao(Enum):
    initial_part = [
        "general_information_abalustre",
        "assets_identifications_refinitiv",
        "text_translated_general_information_refinitiv",
    ]
    main_brands = ["general_information_refinitiv"]
    general = [
        "general_information_b3",
        "general_information_morningstar",
    ]
    financial = ["financial_information_morningstar"]
    financial_indicators = ["financial_information_morningstar"]
    balance_sheet = []
    market_announcements = ["street_events_refinitiv"]


class Opcoes(Enum):
    initial_part = []


class Futuros(Enum):
    initial_part = ["general_information_b3"]
    general = [
        "general_information_b3",
        "general_information_cedro",
        "general_information_morningstar",
    ]


class Fiis(Enum):
    initial_part = ["assets_identifications_refinitiv"]
    general = ["general_information_morningstar"]
    financial = ["financial_information_morningstar"]


class EtfBR(Enum):
    initial_part = [
        "assets_identifications_refinitiv",
        "text_translated_general_information_refinitiv",
    ]
    general = ["general_information_morningstar"]
    market_announcements = []


class BDRdeEtf(Enum):
    initial_part = [
        "assets_identifications_refinitiv",
        "text_translated_general_information_refinitiv",
    ]
    general = ["general_information_b3"]
    market_announcements = []
