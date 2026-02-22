from enum import Enum
from typing import Annotated, Literal

from pydantic import BaseModel, Field


class Language(str, Enum):
    AR = "ar"  # Arabic
    ZH = "zh"  # Chinese
    CS = "cs"  # Czech
    NL = "nl"  # Dutch
    DE = "de"  # German
    HI = "hi"  # Hindi
    HU = "hu"  # Hungarian
    IT = "it"  # Italian
    JA = "ja"  # Japanese
    KO = "ko"  # Korean
    PL = "pl"  # Polish
    PT = "pt"  # Portuguese
    RU = "ru"  # Russian
    ES = "es"  # Spanish
    TR = "tr"  # Turkish
    EN = "en"  # English
    BN = "bn"  # Bangla with bangla models


class Turn(BaseModel):
    text: str
    language_id: Language = "en"
    gender: Literal["male", "female"] = "female"
    person_id: Literal[1, 2]


class RequestSchema(BaseModel):
    turns: Annotated[list[Turn], Field(min_length=1)]
    stich_delay: float = 0.5


# chosen_profiles = [
#     # English (en)
#     ("en", " Barbora MacLean", "female"),
#     ("en", "Adde Michal", "male"),
#     # Spanish (es)
#     ("es", "Alma María", "female"),
#     ("es", "Luis Moray", "male"),
#     # French (fr)
#     ("fr", "Alexandra Hisakawa", "female"),
#     ("fr", "Xavier Hayasaka", "male"),
#     # German (de)
#     ("de", "Tanja Adelina", "female"),
#     ("de", "Aaron Dreschner", "male"),
#     # Italian (it)
#     ("it", "Sofia Hellen", "female"),
#     ("it", "Eugenio Mataracı", "male"),
#     # Portuguese (pt)
#     ("pt", "Camilla Holmström", "female"),
#     ("pt", "Ferran Simen", "male"),
#     # Polish (pl)
#     ("pl", "Zofija Kendrick", "female"),
#     ("pl", "Baldur Sanjin", "male"),
#     # Turkish (tr)
#     ("tr", "Vjollca Johnnie", "female"),
#     ("tr", "Ilkin Urbano", "male"),
#     # Russian (ru)
#     ("ru", "Asya Anara", "female"),
#     ("ru", "Viktor Eka", "male"),
#     # Dutch (nl)
#     ("nl", "Uta Obando", "female"),
#     ("nl", "Ludvig Milivoj", "male"),
#     # Czech (cs)
#     ("cs", "Barbora MacLean", "female"),
#     ("cs", "Damjan Chapman", "male"),
#     # Arabic (ar)
#     ("ar", "Ige Behringer", "female"),
#     ("ar", "Badr Odhiambo", "male"),
#     # Chinese (zh-cn)
#     ("zh", "Maja Ruoho", "female"),
#     ("zh", "Royston Min", "male"),
#     # Hungarian (hu)
#     ("hu", "Szofi Granger", "female"),
#     ("hu", "Filip Traverse", "male"),
#     # Korean (ko)
#     ("ko", "Lilya Stainthorpe", "female"),
#     ("ko", "Viktor Menelaos", "male"),
#     # Japanese (ja) (apt dependency is huge)
#     ("ja", "Narelle Moon", "female"),
#     ("ja", "Kazuhiko Atallah", "male"),
#     # Hindi (hi)
#     ("hi", "Tanja Adelina", "female"),
#     ("hi", "Viktor Menelaos", "male"),
# ]

chosen_profiles = {
    # English (en)
    "en_female_1": "Claribel Dervla",
    "en_female_2": "Barbora MacLean",
    "en_male_1": "Adde Michal",
    "en_male_2": "Abrahan Mack",
    # Spanish (es)
    "es_female_1": "Alma María",
    "es_female_2": "Ana Florence",
    "es_male_1": "Luis Moray",
    "es_male_2": "Marcos Rudaski",
    # French (fr)
    "fr_female_1": "Alexandra Hisakawa",
    "fr_female_2": "Gracie Wise",
    "fr_male_1": "Xavier Hayasaka",
    "fr_male_2": "Zacharie Aimilios",
    # German (de)
    "de_female_1": "Tanja Adelina",
    "de_female_2": "Alison Dietlinde",
    "de_male_1": "Aaron Dreschner",
    "de_male_2": "Wulf Carlevaro",
    # Italian (it)
    "it_female_1": "Sofia Hellen",
    "it_female_2": "Gitta Nikolina",
    "it_male_1": "Eugenio Mataracı",
    "it_male_2": "Gilberto Mathias",
    # Portuguese (pt)
    "pt_female_1": "Camilla Holmström",
    "pt_female_2": "Rosemary Okafor",
    "pt_male_1": "Ferran Simen",
    "pt_male_2": "Dionisio Schuyler",
    # Polish (pl)
    "pl_female_1": "Zofija Kendrick",
    "pl_female_2": "Lidiya Szekeres",
    "pl_male_1": "Baldur Sanjin",
    "pl_male_2": "Damien Black",
    # Turkish (tr)
    "tr_female_1": "Vjollca Johnnie",
    "tr_female_2": "Tammie Ema",
    "tr_male_1": "Ilkin Urbano",
    "tr_male_2": "Viktor Eka",
    # Russian (ru)
    "ru_female_1": "Asya Anara",
    "ru_female_2": "Tammy Grit",
    "ru_male_1": "Viktor Eka",
    "ru_male_2": "Torcull Diarmuid",
    # Dutch (nl)
    "nl_female_1": "Uta Obando",
    "nl_female_2": "Annmarie Nele",
    "nl_male_1": "Ludvig Milivoj",
    "nl_male_2": "Damjan Chapman",
    # Czech (cs)
    "cs_female_1": "Barbora MacLean",
    "cs_female_2": "Nova Hogarth",
    "cs_male_1": "Damjan Chapman",
    "cs_male_2": "Craig Gutsy",
    # Arabic (ar)
    "ar_female_1": "Suad Qasim",
    "ar_female_2": "Henriette Usha",
    "ar_male_1": "Ilkin Urbano",
    "ar_male_2": "Ige Behringer",
    # Chinese (zh)
    "zh_female_1": "Maja Ruoho",
    "zh_female_2": "Chandra MacFarland",
    "zh_male_1": "Royston Min",
    "zh_male_2": "Kazuhiko Atallah",
    # Hungarian (hu)
    "hu_female_1": "Szofi Granger",
    "hu_female_2": "Daisy Studious",
    "hu_male_1": "Filip Traverse",
    "hu_male_2": "Kumar Dahl",
    # Korean (ko)
    "ko_female_1": "Lilya Stainthorpe",
    "ko_female_2": "Lidiya Szekeres",
    "ko_male_1": "Viktor Menelaos",
    "ko_male_2": "Royston Min",
    # Japanese (ja)
    "ja_female_1": "Narelle Moon",
    "ja_female_2": "Alexandra Hisakawa",
    "ja_male_1": "Kazuhiko Atallah",
    "ja_male_2": "Xavier Hayasaka",
    # Hindi (hi)
    "hi_female_1": "Brenda Stern",
    "hi_female_2": "Tanja Adelina",
    "hi_male_1": "Viktor Menelaos",
    "hi_male_2": "Kumar Dahl",
}


def get_speaker(language_code: str, gender: str, person_id: int) -> str:
    try:
        speaker_id = f"{language_code}_{gender}_{person_id}"
        return chosen_profiles[speaker_id]
    except KeyError as e:
        raise e
