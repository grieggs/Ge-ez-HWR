import editdistance
import re


def g_families(in_str):
    families = {"hoy" : ["ሀ","ሁ","ሂ","ሃ","ሄ","ህ","ሆ"],
    "lawe":["ለ","ሉ","ሊ","ላ","ሌ","ል","ሎ","ሏ"],
    "hawt" : ["ሐ","ሑ","ሒ","ሓ","ሔ","ሕ","ሖ","ሗ"],
    "may" : ["መ","ሙ","ሚ","ማ","ሜ","ም","ሞ","ሟ","ፙ"],
    "sawt" : ["ሠ","ሡ","ሢ","ሣ","ሤ","ሥ","ሦ","ሧ"],
    "res" : ["ረ","ሩ","ሪ","ራ","ሬ","ር","ሮ","ሯ","ፘ"],
    "sat" : ["ሰ","ሱ","ሲ","ሳ","ሴ","ስ","ሶ","ሷ"],
    "caf" : ["ቀ","ቁ","ቂ","ቃ","ቄ","ቅ","ቆ","ቋ"],
    "bet" : ["በ","ቡ","ቢ","ባ","ቤ","ብ","ቦ","ቧ"],
    "tawe" : ["ተ","ቱ","ቲ","ታ","ቴ","ት","ቶ","ቷ"],
    "harm" : ["ኀ","ኁ","ኂ","ኃ","ኄ","ኅ","ኆ","ኋ"],
    "nahas" : ["ነ","ኑ","ኒ","ና","ኔ","ን","ኖ","ኗ"],
    "alf" : ["አ","ኡ","ኢ","ኣ","ኤ","እ","ኦ","ኧ"],
    "kaf" : ["ከ","ኩ","ኪ","ካ","ኬ","ክ","ኮ","ኳ"],
    "wawe" : ["ወ","ዉ","ዊ","ዋ","ዌ","ው","ዎ"],
    "ayn" : ["ዐ","ዑ","ዒ","ዓ","ዔ","ዕ","ዖ"],
    "zay" : ["ዘ","ዙ","ዚ","ዛ","ዜ","ዝ","ዞ","ዟ"],
    "yaman" : ["የ","ዩ","ዪ","ያ","ዬ","ይ","ዮ"],
    "dant" : ["ደ","ዱ","ዲ","ዳ","ዴ","ድ","ዶ","ዷ"],
    "gaml" : ["ገ","ጉ","ጊ","ጋ","ጌ","ግ","ጎ","ጓ"],
    "tayt" : ["ጠ","ጡ","ጢ","ጣ","ጤ","ጥ","ጦ","ጧ"],
    "payt" : ["ጰ","ጱ","ጲ","ጳ","ጴ","ጵ","ጶ","ጷ"],
    "saday" : ["ጸ","ጹ","ጺ","ጻ","ጼ","ጽ","ጾ","ጿ"],
    "sappa" : ["ፀ","ፁ","ፂ","ፃ","ፄ","ፅ","ፆ"],
    "af" : ["ፈ","ፉ","ፊ","ፋ","ፌ","ፍ","ፎ","ፏ","ፚ"],
    "psa" : ["ፐ","ፑ","ፒ","ፓ","ፔ","ፕ","ፖ","ፗ"],
    "cw" : ["ቈ","ቊ","ቋ","ቌ","ቍ"],
    "hw" : ["ኈ","ኊ","ኋ","ኌ","ኍ"],
    "kw" : ["ኰ","ኲ","ኳ","ኴ","ኵ"],
    "gw"  : ["ጐ","ጒ","ጓ","ጔ","ጕ "]}

    replace = {"hoy": "0",
                "lawe": "1",
                "hawt": "2",
                "may": "3",
                "sawt": "4",
                "res": "5",
                "sat": "6",
                "caf": "7",
                "bet": "8",
                "tawe": "9",
                "harm": "q",
                "nahas": "w",
                "alf": "e",
                "kaf": "r",
                "wawe": "t",
                "ayn": "y",
                "zay": "u",
                "yaman": "i",
                "dant": "o",
                "gaml": "p",
                "tayt": "a",
                "payt": "s",
                "saday": "d",
                "sappa": "f",
                "af": "g",
                "psa": "h",
                "cw": "j",
                "hw": "k",
                "kw": "l",
                "gw": "z"}
    # print(len(families))
    out = ""
    other = "፼፵፴(፪)፱፲ጕ፻ ፰፳፡ዠ፯፺ሽ:ሸ፸ሻ፶።፩.፬፣]፷፫፹፭፮"
    for x in in_str:
        good = False
        for y in families:
            if x in families[y]:
                out += replace[y]
                good = True
        if not good:
            out += x
    return out


def fcer(r,h):
    r = g_families(r)
    h = g_families(h)
    r = u' '.join(r.split())
    h = u' '.join(h.split())
    return err(r, h)

def cer(r, h):
    #Remove any double or trailing
    # r = r.lower()
    # h = h.lower()
    # r = re.sub(r'([^\s\w]|_)+', '', r)
    # h = re.sub(r'([^\s\w]|_)+', '', h)
    r = u' '.join(r.split())
    h = u' '.join(h.split())
    return err(r, h)

def err(r, h):
    dis = editdistance.eval(r, h)
    if len(r) == 0.0:
        return len(h)

    return float(dis) / float(len(r))

def wer(r, h):
    # r = r.lower()
    # h = h.lower()
    # r = re.sub(r'([^\s\w]|_)+', '', r)
    # h = re.sub(r'([^\s\w]|_)+', '', h)
    r = r.split()
    h = h.split()

    return err(r,h)

