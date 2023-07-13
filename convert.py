import Map as GM, fixer as CF, pre_processing as PrP
import post_processing as PP
import East.SiddhamRanjana as SR
import data as FB
import string
import re
from functools import cmp_to_key
import json
import trans

def TamilSort(x, y):
    if "\u0B83" in x[0] and len(x[0]) != 1:
        return -1
    elif x[0] < y[0]:
        return 1
    else:
        return 0


def lenSort(x, y):
    if len(x[0]) > len(y[0]):
        return -1
    else:
        return 0


def convertInter(Strng, Source):
    ScriptAll = (
        GM.Vowels
        + GM.Consonants
        + GM.CombiningSigns
        + GM.Numerals
        + GM.Signs
        + GM.Aytham
    )
    SourceScript = GM.CrunchSymbols(ScriptAll, Source)
    TargetScript = GM.CrunchSymbols(ScriptAll, GM.Inter)
    ScriptMapAll = sorted(zip(SourceScript, TargetScript), key=cmp_to_key(lenSort))

    for x, y in ScriptMapAll:
        Strng = Strng.replace(x, y)

    return Strng


def convertScript(Strng, Source, Target):
    charPairs = []
    Schwa = "\uF000"
    DepV = "\u1E7F"

    if Source in GM.LatinScripts and Target in GM.IndicScripts:
        try:
            Strng = getattr(CF, "Fix" + Source)(Strng, reverse=True)
        except AttributeError:
            pass

        if Source in ["IAST", "ISO", "ISOPali", "Titus"]:
            Strng = Strng.replace("ŭ", "u\u00D7")

        Strng = Strng.replace("{}", "\u200C")
        Strng = Strng.replace("()", "\u200D")

        Strng = CF.VedicSvarasLatinIndic(Strng, Source)

        punc = (
            "("
            + "|".join(
                ["\u005C" + x for x in list(string.punctuation)]
                + ["\s"]
                + [
                    x.replace(".", "\.")
                    for x in GM.CrunchSymbols(GM.Signs, Source)[1:3]
                ]
            )
            + ")"
        )

        sOm, tOm = GM.CrunchList("OmMap", Source)[0], GM.CrunchList("OmMap", Target)[0]

        Strng = re.sub(punc + sOm + punc, r"\1" + tOm + r"\2", Strng)
        Strng = re.sub("^" + sOm + punc, tOm + r"\1", Strng)
        Strng = re.sub(punc + sOm + "$", r"\1" + tOm, Strng)
        Strng = re.sub("^" + sOm + "$", tOm, Strng)

        punc = "(\s)"

        Strng = re.sub(punc + sOm + punc, r"\1" + tOm + r"\2", Strng)
        Strng = re.sub("^" + sOm + punc, tOm + r"\1", Strng)
        Strng = re.sub(punc + sOm + "$", r"\1" + tOm, Strng)
        Strng = re.sub("^" + sOm + "$", tOm, Strng)

        SourceOld = Source

        Strng = convertInter(Strng, Source)
        Source = GM.Inter
        Strng = PrP.RomanPreFix(Strng, Source)

        Strng = Strng.replace("ṿ×_", "ṿ")
        Strng = Strng.replace("ṿ×_", "ṿ")

        ha = GM.CrunchSymbols(GM.Consonants, Source)[32]
        charPairs = []

        for charList in GM.ScriptAll:
            TargetScript = GM.CrunchSymbols(GM.retCharList(charList), Target)
            if charList == "VowelSigns":
                SourceScript = [
                    DepV + x for x in GM.CrunchSymbols(GM.VowelSigns, Source)
                ]
            else:
                SourceScript = GM.CrunchSymbols(GM.retCharList(charList), Source)

            ScriptMap = list(zip(SourceScript, TargetScript))

            ScriptMap.sort(reverse=True)
            charPairs = charPairs + ScriptMap

        charPairs = sorted(charPairs, key=cmp_to_key(lenSort))

        for x, y in charPairs:
            Strng = Strng.replace(x, y)

        Strng = Strng.replace(
            "_" + GM.CrunchSymbols(GM.Vowels, Target)[2],
            GM.CrunchSymbols(GM.Vowels, Target)[2],
        )
        Strng = Strng.replace(
            "_" + GM.CrunchSymbols(GM.Vowels, Target)[4],
            GM.CrunchSymbols(GM.Vowels, Target)[4],
        )

        vir = GM.CrunchList("ViramaMap", Target)[0]
        Strng = Strng.replace(vir + "[]", "\u200D" + vir)

        if Source in ["Inter"]:
            Strng = Strng.replace("\u00D7", vir)

        Strng = CF.FixIndicOutput(Strng, Source, Target)

    elif Source in GM.LatinScripts and Target in GM.LatinScripts:
        try:
            Strng = getattr(CF, "Fix" + Source)(Strng, reverse=True)
        except AttributeError:
            pass

        ScriptAll = (
            GM.Vowels
            + GM.Consonants
            + GM.CombiningSigns
            + GM.Numerals
            + GM.Signs
            + GM.Aytham
        )

        Strng = convertInter(Strng, Source)

        SourceScript = GM.CrunchSymbols(ScriptAll, GM.Inter)
        TargetScript = GM.CrunchSymbols(ScriptAll, Target)
        ScriptMapAll = list(zip(SourceScript, TargetScript))

        for x, y in ScriptMapAll:
            Strng = Strng.replace(x, y)

        Strng = CF.PostFixRomanOutput(Strng, Source, Target)

    elif Source in GM.IndicScripts and Target in GM.IndicScripts:
        Strng = PrP.RemoveJoiners(Strng)

        Strng = CF.ShiftDiacritics(Strng, Source, reverse=True)
        try:
            Strng = getattr(CF, "Fix" + Source)(Strng, reverse=True)
        except AttributeError:
            pass

        punc = (
            "("
            + "|".join(
                ["\u005C" + x for x in list(string.punctuation)]
                + ["\s"]
                + [
                    x.replace(".", "\.")
                    for x in GM.CrunchSymbols(GM.Signs, Source)[1:3]
                ]
            )
            + ")"
        )

        sOm, tOm = GM.CrunchList("OmMap", Source)[0], GM.CrunchList("OmMap", Target)[0]

        if len(sOm) != 1:
            Strng = re.sub(punc + sOm + punc, r"\1" + tOm + r"\2", Strng)
            Strng = re.sub("^" + sOm + punc, tOm + r"\1", Strng)
            Strng = re.sub(punc + sOm + "$", r"\1" + tOm, Strng)
            Strng = re.sub("^" + sOm + "$", tOm, Strng)

        if len(sOm) == 1:
            Strng = Strng.replace(sOm, tOm)

        for charList in GM.ScriptAll:
            SourceScript = GM.CrunchSymbols(GM.retCharList(charList), Source)
            TargetScript = GM.CrunchSymbols(GM.retCharList(charList), Target)

            ScriptMap = list(zip(SourceScript, TargetScript))

            ScriptMap.sort(reverse=True)
            charPairs = charPairs + ScriptMap

        charPairs = sorted(charPairs, key=cmp_to_key(lenSort))

        for x, y in charPairs:
            Strng = Strng.replace(x, y)

        Strng = CF.FixIndicOutput(Strng, Source, Target)

    elif Source in GM.IndicScripts and Target in GM.LatinScripts:
        Strng = PrP.RemoveJoiners(Strng)
        Strng = CF.ShiftDiacritics(Strng, Source, reverse=True)
        try:
            Strng = getattr(CF, "Fix" + Source)(Strng, reverse=True)
        except AttributeError:
            pass

        sOm, tOm = GM.CrunchList("OmMap", Source)[0], GM.CrunchList("OmMap", Target)[0]

        Strng = Strng.replace(sOm, tOm)

        for charList in GM.ScriptAll:
            SourceScript = GM.CrunchSymbols(GM.retCharList(charList), Source)
            if charList == "Consonants":
                TargetScript = [
                    x + Schwa for x in GM.CrunchSymbols(GM.Consonants, Target)
                ]
            elif charList == "Vowels":
                TargetScript = [DepV + x for x in GM.CrunchSymbols(GM.Vowels, Target)]
            else:
                TargetScript = GM.CrunchSymbols(GM.retCharList(charList), Target)

            ScriptMap = list(zip(SourceScript, TargetScript))
            ScriptMap.sort(reverse=True)
            charPairs = charPairs + ScriptMap

        charPairs = sorted(charPairs, key=cmp_to_key(lenSort))

        if Source == "RomanSemitic":
            unasp = ["k", "g", "c", "j", "t", "d", "p", "b", "ɽ", "ʈ", "ɖ", "r"]
            charPairsH = [(x, y) for x, y in charPairs if "ʰ" in x]
            charPairsNotH = [(x, y) for x, y in charPairs if "ʰ" not in x]
            charPairs = charPairsNotH + charPairsH
            for x, y in charPairs:
                if x in unasp:
                    Strng = re.sub(x + "(?!(ʰ|\u0324))", y, Strng)
                else:
                    Strng = Strng.replace(x, y)

        else:
            for x, y in charPairs:
                Strng = Strng.replace(x, y)

        Strng = CF.FixRomanOutput(Strng, Target)

        Strng = CF.VedicSvarsIndicLatin(Strng)

        Strng = CF.PostFixRomanOutput(Strng, Source, Target)

    elif Source in GM.SemiticScripts and Target in GM.SemiticScripts:
        try:
            Strng = getattr(CF, "Fix" + Source.replace("-", "_"))(
                Strng, Source, reverse=True
            )
        except AttributeError:
            pass

        tr = trans.Transliterator()

        if Source == "Ugar":
            Strng = Strng.replace("𐎟", " ")

        Strng = tr.tr(Strng, sc=Source, to_sc=Target)

        Strng = CF.FixSemiticOutput(Strng, Source, Target)

    elif Source in (GM.IndicScripts + GM.LatinScripts) and Target in GM.SemiticScripts:
        tr = trans.Transliterator()

        Strng = convertScript(Strng, Source, "RomanSemitic")

        Strng = Strng.replace("QQ", "").replace("mQ", "")
        if "Arab" not in Target and "Hebr" not in Target and "Latn" not in Target:
            Strng = re.sub("(.)" + "\u033D" + r"\1", r"\1", Strng)

        Strng = PP.FixSemiticRoman(Strng, Target)

        if "Arab" in Target or Target in ["Hebr", "Syre", "Syrj", "Syrn", "Thaa"]:
            Strng = PP.insertARomanSemitic(Strng)

        Strng = tr.tr(Strng, sc="Latn", to_sc=Target)

        Strng = CF.FixSemiticOutput(Strng, Source, Target)

    elif Source in GM.SemiticScripts and Target in (GM.IndicScripts + GM.LatinScripts):
        try:
            Strng = getattr(CF, "Fix" + Source.replace("-", "_"))(
                Strng, Source, reverse=True
            )
        except AttributeError:
            pass

        tr = trans.Transliterator()

        Strng = tr.tr(Strng, sc=Source, to_sc="Latn")

        Strng = CF.FixSemiticOutput(Strng, Source, Target)

        Strng = PrP.FixSemiticRoman(Strng, Source)

        Strng = convertScript(Strng, "RomanSemitic", Target)

        if Source == "Ugar":
            Strng = Strng.replace("𐎟", " ")

    Strng = PP.default(Strng)

    return Strng