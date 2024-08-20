from enum import Enum


class AcaoUS(Enum):
    initial_part = [
        "general_information_polygon",
        "assets_identifications_refinitiv",
        "text_translated_general_information_refinitiv",
    ]
    main_brands = [
        "general_information_refinitiv",
    ]
    general = ["general_information_polygon"]
    financial = ["general_information_polygon"]
    balance_sheet = []
    market_announcements = ["street_events_refinitiv"]


class EtfUS(Enum):
    initial_part = [
        "general_information_polygon",
        "assets_identifications_refinitiv",
        "text_translated_general_information_refinitiv",
    ]
    general = ["general_information_polygon"]
    market_announcements = []


class ADRdeAcao(Enum):
    initial_part = [
        "general_information_polygon",
        "assets_identifications_refinitiv",
        "text_translated_general_information_refinitiv",
    ]
    main_brands = [
        "general_information_refinitiv",
    ]
    general = ["general_information_polygon"]
    financial = ["general_information_polygon"]
    financial_indicators = []
    balance_sheet = []
    market_announcements = ["street_events_refinitiv"]


class ADRdeEtf(Enum):
    initial_part = []
    general = []
    financial = []
    market_announcements = []
