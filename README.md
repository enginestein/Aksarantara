# Aksarantara

Aksarantara is a framework specially for **Sanskrit** enthausists supporting indic, eastern, roman and other language transliteration. Aksarantara is also written in [Ruby](https://github.com/enginestein/aksarantara.rb) and [PHP](https://github.com/enginestein/aksarantara.php) but this Python version is the best. The PHP and Ruby version need further updates.

# Usage

To install Aksarantara

```powershell
pip install aksarantara
```

To use Aksarantara

the `transliterate.process` function is the main function which has following parameters:

```python
transliterate.process(src, tgt, txt, nativize = True, pre_options = [], post_options = [])
```

| Paremeter  | Usage |
| ------------- | ------------- |
| src: str  | Used to provide the source transliteration script |
| tgt: str  | Used to provide target transliteration script  |
| txt: str  | Provide text to be transliterated  |
| navitize: bool  | navitize the text  |
| pre_options: list  | Options to customize input (source) string for processing |
| post_options: list  | Options to customize output (target) string for processing |

## Usage in code

```python
from aksrantara import transliterate

print(transliterate.process("hk", "siddham", "buddhaH"))
print(transliterate.process("autodetect", "iast", "சித்தம்_சூதம்"))
print(transliterate.process("HK", "Tamil", "மங்கள", False))

print(
    transliterate.process(
        "HK",
        "Tamil",
        "பிரஹ்ஸ்பதி கங்கா",
        False,
        post_options=["TamilSubScript", "TamilRemoveApostrophe"],
    )
)
print(
    transliterate.process(
        "Thai", "Devanagari", "ภุทธัง สะระณัง คัจฉามิ", pre_options=["ThaiOrthography"]
    )
)
print(transliterate.process("autodetect", "IAST", "ภุทธัง สะระณัง คัจฉามิ"))
print(transliterate.process("autodetect", "Vatteluttu", "ภุทธัง สะระณัง คัจฉามิ"))
print(transliterate.auto_detect("சித்தம்_சூதம்"))
print(
    transliterate.process(
        "Devanagari",
        "IAST",
        "धर्म भारत की श्रमण परम्परा से निकला धर्म और दर्शन है",
        pre_options=["RemoveSchwaHindi"],
    )
)
print(transliterate.process("deva", "taml", "धर्म भारत की ", param="script_code"))
print(transliterate.process("te", "ur", "ధర్మ భారత", param="lang_code"))
print(transliterate.process("odia", "ho", "ଧର୍ମ ଭାରତ", param="lang_name"))
print(transliterate.process("hindi", "kannada", "धर्म भारत की ", param="lang_name"))
print(transliterate.process("devanagari", "granthapandya", "धर्म"))
print(transliterate.process("hi", "pa", "धर्म भारत की ", param="lang_code"))
print(transliterate.process("deva", "arab", "धर्म भारत की ", param="script_code"))
print(
    transliterate.process(
        "autodetect", "latn-iast", "धर्म भारत की ", param="script_code"
    )
)
print(transliterate.process("la-HK", "pa-guru", "namo buddhAya", param="lang_code"))
print(transliterate.process("hi-Deva", "hi-kthi", "धर्म भारत की ", param="lang_code"))
print(transliterate.process("hi-Deva", "mak", "धर्म भारत की ", param="lang_code"))
print(transliterate.process("hi-Deva", "cyrl", "धर्म भारत की ", param="script_code"))
print(transliterate.process("sa-Deva", "ru", "धर्म भारत की ", param="lang_code"))
print(transliterate.process("deva", "taml", "धर्म भारत की ", param="script_code"))
print(transliterate.process("te", "ur", "ధర్మ భారత", param="lang_code"))
print(transliterate.process("odia", "ho", "ଧର୍ମ ଭାରତ", param="lang_name"))
print(transliterate.process("Devanagari", "Phnx", "तांश्च"))
print(transliterate.process("HK", "Syrc", "buddha"))
```
