import post_processing as PP
import Map as GM


def ApplyScriptDefaults(Strng, Source, Target, PostOptions=[]):
    Options = []

    if Target in GM.IndicScripts:
        Options += []

    if Target == "Telugu":
        Options += [
            "NasalToAnusvara",
            "MToAnusvara",
            "TeluguRemoveNukta",
            "TeluguRemoveAeAo",
        ]

    elif Target == "Kannada":
        Options += ["NasalToAnusvara", "MToAnusvara"]

    elif Target == "Nandinagari":
        Options += ["NasalToAnusvara"]

    elif Target == "Hebrew":
        Options += ["HebrewVetVav", "HebrewnonFinalShort"]

    elif Target == "Malayalam":
        Options += [
            "MalayalamAnusvaraNasal",
            "MToAnusvara",
            "MalayalamremoveHistorical",
        ]

    elif Target == "Tamil":
        Options += ["TamilNaToNNa", "AnusvaraToNasal", "TamilpredictDentaNa"]

    elif Target == "Bengali":
        if "BengaliRaBa" in PostOptions:
            Options += ["YaToYYa", "AnusvaraToNasal", "BengaliConjunctVB"]
        else:
            Options += ["VaToBa", "YaToYYa", "AnusvaraToNasal", "BengaliConjunctVB"]

    elif Target == "MeeteiMayek":
        Options += ["MeeteiMayekremoveHistorical"]

    elif Target == "Limbu":
        Options += ["LimburemoveHistorical"]

    elif Target == "Assamese":
        Options += ["YaToYYa", "AnusvaraToNasal"]

    elif Target == "Oriya":
        Options += ["OriyaVa", "YaToYYa", "AnusvaraToNasal"]

    elif Target == "Chakma":
        Options += ["YaToYYa"]

    elif Target == "Gurmukhi":
        Options += [
            "GurmukhiCandrabindu",
            "GurmukhiTippiBindu",
            "GurmukhiTippiGemination",
        ]

    elif Target == "Saurashtra":
        Options += ["SaurashtraHaru"]

    elif Target == "Ahom":
        Options += ["AhomClosed"]

    elif Target == "Tibetan":
        Options += ["TibetanRemoveVirama", "TibetanRemoveBa"]

    elif Target == "Thaana":
        Options += ["ThaanaRemoveHistorical"]

    elif Target == "Avestan":
        Options += ["AvestanConventions"]

    elif Target == "Sundanese":
        Options += ["SundaneseRemoveHistoric"]

    elif Target == "Multani":
        Options += ["MultaniAbjad"]

    elif Target == "Modi":
        Options += ["ModiRemoveLong"]

    elif Target == "WarangCiti":
        Options += ["WarangCitiModernOrthogaphy"]

    elif Target == "Latn":
        if Source == "Arab":
            Options += ["arabizeLatn"]
        elif Source == "Arab-Ur" or Source == "Arab-Pa" or Source == "Arab-Fa":
            Options += ["urduizeLatn"]
        elif Source == "Syrn":
            Options += ["syricizeLatn"]
        elif Source == "Syrj" or Source == "Hebr":
            Options += ["hebraizeLatn"]

    elif Target == "Arab":
        Options += ["ArabRemoveAdditions"]

    else:
        Options += []

    for Option in Options:
        if Option.find(Target) != -1:
            Strng = getattr(PP, Option)(Strng)
        else:
            Strng = getattr(PP, Option)(Strng, Target)

    return Strng
