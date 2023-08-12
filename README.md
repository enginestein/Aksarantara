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

print(transliterate.process("hk", "siddham", "mataram"))
print(transliterate.process("autodetect", "iast", "அம்மாவை வணங்குகிறேன்"))
print(transliterate.process("hk", "Tamil", "அம்மாவை வணங்குகிறேன்", False))
print(transliterate.process("HK","Tamil","அம்மாவை வணங்குகிறேன்", False, post_options=["TamilSubScript", "TamilRemoveApostrophe"]))
print(transliterate.process("Thai", "Devanagari", "ภุทธัง สะระณัง คัจฉามิ", pre_options=["ThaiOrthography"]))
print(transliterate.process("autodetect", "IAST", "สวัสดีประเทศชาติ"))
print(transliterate.process("autodetect", "Vatteluttu", "สวัสดีประเทศชาติ"))
print(transliterate.auto_detect("வாழ்க இந்தியா"))
print(transliterate.process("Devanagari", "IAST", "सर्वे भवन्तु सुखिनः", pre_options=["RemoveSchwaHindi"]))
print(transliterate.process("deva", "taml", "वन्दे मातरम ", param="script_code"))
print(transliterate.process("te", "ur", "వందే భారత్ మాతరం", param="lang_code"))
print(transliterate.process("odia", "ho", "వందే భారత్ మాతరం", param="lang_name"))
print(transliterate.process("hindi", "kannada", "वन्दे मातरम ", param="lang_name"))
print(transliterate.process("devanagari", "granthapandya", "धर्म"))
print(transliterate.process("hi", "pa", "वन्दे मातरम ", param="lang_code"))
print(transliterate.process("deva", "arab", "वन्दे मातरम ", param="script_code"))
print(transliterate.process("autodetect", "latn-iast", "वन्दे मातरम ", param="script_code"))
print(transliterate.process("la-HK", "pa-guru", "namo buddhAya", param="lang_code"))
print(transliterate.process("hi-Deva", "hi-kthi", "वन्दे मातरम ", param="lang_code"))
print(transliterate.process("hi-Deva", "mak", "वन्दे मातरम ", param="lang_code"))
print(transliterate.process("hi-Deva", "cyrl", "वन्दे मातरम ", param="script_code"))
print(transliterate.process("sa-Deva", "ru", "वन्दे मातरम ", param="lang_code"))
print(transliterate.process("deva", "taml", "वन्दे मातरम ", param="script_code"))
print(transliterate.process("te", "ur", "వందే భారత్ మాతరం", param="lang_code"))
print(transliterate.process("odia", "ho", "వందే భారత్ మాతరం", param="lang_name"))
print(transliterate.process("Devanagari", "Phnx", "वयं अभियंताः स्मः"))
print(transliterate.process("HK", "Syrc", "buddha"))
```
