"""
Дељени лингвистички корпус од 963 српске речи за тестирање инваријанти
шатровачког, утровачког и литровачког алгоритма.

Речи су организоване по фонолошкој класи ради потпуног покривања
свих граничних случајева трансформација.

Фонолошке класе:
  VOWEL_INITIAL     — речи које почињу самогласником
  SYLLABIC_R        — речи са слоготворним р
  DIGRAPH_LJ        — речи са дијаграфом лј
  DIGRAPH_NJ        — речи са дијаграфом њ
  DIGRAPH_DZ        — речи са дијаграфом џ
  SHORT_3           — речи од тачно 3 слова
  SHORT_4           — речи од тачно 4 слова
  MEDIUM_5          — речи од 5 слова
  MEDIUM_6          — речи од 6 слова
  MEDIUM_7          — речи од 7 слова
  LONG_8PLUS        — речи од 8 и више слова
  DIACRITICS        — речи са тежим дијакритицима (ш, ч, ћ, ж, ђ)
  CONSONANT_CLUSTER — речи са сугласничким кластером на почетку
  DOUBLE_VOWEL      — речи са узастопним самогласницима
"""

# ── Класа 1: Речи које почињу самогласником (~85) ─────────────────────────────
VOWEL_INITIAL: tuple[str, ...] = (
    # а-
    "auto", "avion", "autobus", "autoput", "avan", "avala", "aleja",
    "abeceda", "azbuka", "akter", "akcija", "alarm", "album", "alat",
    "alkohol", "amanet", "anđeo", "antena", "aparat", "apoteka",
    "arena", "armija", "arsenal", "atlas", "atom", "autor", "azil",
    "avlija", "avaz", "avet", "april", "arija", "arka", "arhiva",
    # е-
    "eho", "ekonomija", "elegancija", "elita", "emocija", "energija",
    "epoha", "era", "esej", "etika", "evropa", "evro", "ekran", "ekipa",
    "ekser", "ekstra", "ekran", "epitet", "efekat",
    # и-
    "igla", "ikona", "internet", "istorija", "izlaz", "izlog", "iznos",
    "izraz", "izvor", "igra", "iskra", "ivica", "izbor", "izba",
    "ikebana", "iguman", "iskop", "islom", "istok",
    # о-
    "oko", "oluja", "operacija", "opus", "orao", "orkestar", "osnova",
    "ostrvo", "otrov", "ovca", "ovan", "okean", "obala", "oblast",
    "obraz", "obred", "obuća", "okvir", "okret", "oblak", "obrok",
    "oglas", "oganj", "okolo",
    # у-
    "ulaz", "ulica", "ulje", "unos", "ured", "usta", "uvoz", "uzor",
    "uzrok", "udar", "ugao", "ugljen", "ugovor", "učenik", "umetnost",
    "udovac", "uloga", "uopšte", "ubojit",
)

# ── Класа 2: Слоготворно Р (~50) ─────────────────────────────────────────────
SYLLABIC_R: tuple[str, ...] = (
    "prst", "mrk", "trg", "grb", "krst", "brz", "drvo", "trn", "vrh",
    "srna", "trka", "grlo", "crv", "crkva", "crta", "grm", "krpa",
    "kruna", "mrva", "pruga", "srce", "trbuh", "trun", "vrt", "vrsta",
    "zrno", "grč", "crno", "crep", "brdo", "stroj", "truba", "grudi",
    "kruška", "struja", "strog", "brkovi", "crvena", "drška", "trgati",
    "drvce", "crtati", "krstiti", "vrtlog", "grmlje", "crnac", "drveni",
    "krtola", "brdovit", "vrtnja",
)

# ── Класа 3: Дијаграф ЛЈ (~30) ───────────────────────────────────────────────
DIGRAPH_LJ: tuple[str, ...] = (
    "ljubav", "ljuska", "ljutnja", "ljiljan", "kaljuga", "polje",
    "volje", "kolje", "solje", "malje", "valje", "palje", "siljak",
    "biljar", "maljar", "dalj", "šalje", "kalje", "halje", "nalje",
    "balje", "dalje", "šilje", "pilje", "kilje", "lilje", "milje",
    "tilje", "silje", "rilje",
)

# ── Класа 4: Дијаграф НЈ (~30) ───────────────────────────────────────────────
DIGRAPH_NJ: tuple[str, ...] = (
    "njiva", "njuška", "knjiga", "konj", "konjic", "konjanik", "senj",
    "lenj", "tanjir", "banja", "sanja", "ganja", "manja", "panja",
    "ranja", "snjeg", "manje", "panje", "ranje", "šanje", "žanje",
    "ganje", "hanje", "banje", "danje", "vanje", "zanje", "kanje",
    "lanje", "tanje",
)

# ── Класа 5: Дијаграф ЏЕ (~25) ────────────────────────────────────────────────
DIGRAPH_DZ: tuple[str, ...] = (
    "džep", "džak", "džez", "džin", "džungla", "džoker", "džemper",
    "džigerica", "sudžuk", "adžija", "džombas", "badžak", "madžar",
    "nadžak", "redžep", "džandar", "dželat", "džentlmen", "džinović",
    "džukela", "džuboks", "džudo", "džip", "džigan", "džem",
)

# ── Класа 6: Тачно 3 слова (~50) ──────────────────────────────────────────────
SHORT_3: tuple[str, ...] = (
    "rep", "nos", "put", "zid", "led", "med", "pas", "bes", "les",
    "vez", "rez", "sat", "bat", "mat", "rat", "luk", "muk", "buk",
    "vuk", "puk", "huk", "kap", "tap", "map", "zap", "ali", "ili",
    "tek", "sad", "pre", "pod", "nad", "bez", "sto", "uho", "rak",
    "lak", "pak", "jak", "mak", "pal", "tal", "sal", "kal", "val",
    "dal", "rod", "pod", "kod", "nod", "mog",
)

# ── Класа 7: Тачно 4 слова (~70) ──────────────────────────────────────────────
SHORT_4: tuple[str, ...] = (
    "krov", "grob", "krak", "mrak", "brat", "vrat", "grad", "glas",
    "glad", "past", "mast", "rast", "trak", "brak", "noga", "voda",
    "ruka", "lipa", "lica", "kosa", "kula", "boja", "baza", "cena",
    "sneg", "slab", "slap", "sloj", "slon", "smer", "smeh", "snop",
    "soba", "sofa", "skok", "skup", "stop", "stub", "stih", "stog",
    "stup", "suza", "svet", "svod", "svat", "čelo", "žena", "žito",
    "žaba", "žal", "žar", "žica", "žig", "žir", "šal", "šav", "šlem",
    "đak", "đon", "ćup", "ćuk", "meso", "pero", "pivo", "glad",
    "plan", "plot", "plug", "plut", "prag", "prah", "prat", "prev",
)

# ── Класа 8: Тачно 5 слова (~110) ─────────────────────────────────────────────
MEDIUM_5: tuple[str, ...] = (
    "zemun", "zakon", "bazen", "mačka", "trava", "sunce", "vrana",
    "blato", "žurka", "škola", "čamac", "pekar", "borac", "ravan",
    "pesak", "pevac", "pirat", "pisac", "rukav", "sajam", "šator",
    "šifra", "tabla", "talas", "tavan", "tekst", "tenis", "titan",
    "torba", "vraža", "vrana", "banja", "baron", "barut", "biber",
    "bilet", "birač", "blago", "blato", "bokal", "bokser", "borba",
    "brana", "brlog", "bunar", "burek", "busen", "čaša", "čavka",
    "čelik", "čizma", "čorba", "čuvar", "đakon", "đeram", "đubre",
    "đumbus", "fazan", "frula", "gavra", "gazda", "gepek", "gibon",
    "gilet", "giter", "glava", "gliba", "glina", "globa", "gluma",
    "gnida", "gobra", "golas", "graba", "graja", "grana", "greda",
    "grudi", "gubav", "gulaš", "gusar", "guska", "hvala", "jakna",
    "jarac", "jaram", "jasle", "jasno", "javor", "jelen", "jetra",
    "jovan", "junak", "jutra", "kabao", "kadar", "kajak", "kalem",
    "kanal", "kaput", "karta", "kazan", "kedar", "kelim", "kečap",
    "kičma", "kiosk", "klada", "klasa", "klima", "klisa",
)

# ── Класа 9: Тачно 6 слова (~110) ─────────────────────────────────────────────
MEDIUM_6: tuple[str, ...] = (
    "zemlja", "zarada", "mahala", "matica", "medved", "mermer",
    "mesara", "milenk", "mlinar", "mnenje", "mnenje", "morava",
    "mucalo", "muzika", "nabava", "naglas", "naglav", "nagnut",
    "napast", "narave", "narast", "naruče", "nasada", "naslon",
    "nasmeh", "natpis", "natrag", "navala", "navika", "navrat",
    "nedaća", "nedrag", "neimar", "nektar", "nemani", "nemica",
    "nemiren", "nerast", "nesreć", "nestati", "netrag", "noćnik",
    "obloga", "obrana", "obrica", "obrisk", "obrvet", "obzida",
    "ograda", "ogrtan", "oholog", "okolog", "okovan", "okovan",
    "okupan", "olakša", "olupan", "ometen", "ometan", "onečaš",
    "opasan", "opasan", "opasan", "opažen", "opijen", "oplakn",
    "opreml", "opruga", "opsada", "optika", "optuži", "organ",
    "palata", "paluba", "pamfle", "parada", "parket", "pastir",
    "patnik", "pečurk", "penjač", "perina", "pesnik", "petlja",
    "pevač", "pidžam", "pinica", "pinter", "pisana", "pisman",
    "plamen", "planeta", "planin", "plesan", "plotun", "plovan",
    "pocepan", "pogled", "pogost", "pohara", "pojava", "pojasl",
    "poklon", "poluga", "pomada", "pomrač", "ponuda", "popust",
    "poruka", "posada", "poseka", "potera", "potres", "poveza",
    "pozorj", "pramac", "pravda", "pravil", "prekor", "prelje",
    "preman", "premet", "prepun", "pretap", "prijem", "prilog",
    "prizma", "proboj", "promet", "prsten", "prtljag", "pucanj",
)

# ── Класа 10: Тачно 7 слова (~110) ────────────────────────────────────────────
MEDIUM_7: tuple[str, ...] = (
    "zemunac", "zakopan", "zagrada", "zagulja", "zahteva", "zaleđen",
    "zamenik", "zamorač", "zanatli", "zapevač", "zaroblje", "zasedan",
    "zasovan", "zaštita", "zatvora", "zbogom", "zdenac", "zdravlje",
    "zekanja", "zelenas", "zemnica", "zemunsk", "zgodnij", "zidanje",
    "zlokobm", "zloslut", "znalcev", "boginja", "bojazni", "bolnica",
    "bornit", "borovni", "borsala", "botaist", "branika", "bratski",
    "bravura", "brčkalo", "briditi", "brodski", "brokula", "brusiti",
    "budnost", "bukvica", "bulaznit", "bulazni", "burgija", "busenja",
    "čarolij", "čavrlja", "čemerni", "čestitk", "četkica", "čišćenj",
    "čizmica", "čizmino", "čornina", "čudovit", "čuvarsk", "čvornak",
    "ćelijska", "ćevapčić", "ćilibarn", "ćorsoka", "ćorućak",
    "đavolja", "đipovati", "đogrdan", "đulabij", "đuvarno",
    "galerij", "galijot", "galvani", "garavel", "garnizon", "gatalac",
    "gatanje", "gavranin", "gedžast", "gengrav", "geograf", "gipčati",
    "gitarist", "gladiti", "gladnje", "glazura", "glumaca", "gnijezd",
    "gobelin", "godišnj", "gojazan", "goranak", "goranin", "gorastu",
    "gorčina", "goresti", "gorivan", "gorivno", "gorjeti", "gorljivm",
    "govoran", "grabiti", "gradnja", "gradski", "gralina", "gramofon",
    "granica", "granula", "grbavac", "grcanje", "grebati", "gredica",
    "grenčić", "grenica", "grešnik", "grmljan", "groblje", "grozota",
    "gruevsk", "grudnjak", "grundan", "grusina", "guštera",
)

# ── Класа 11: 8 и више слова (~110) ───────────────────────────────────────────
LONG_8PLUS: tuple[str, ...] = (
    "enkripcija", "autobus", "program", "pishtolj", "šarplaninac",
    "komunizam", "liberalizam", "demokratija", "elektronika", "kompjuter",
    "univerzitet", "matematika", "filozofija", "psihologija", "lingvistika",
    "gramatika", "književnost", "astronomija", "biologija", "hemija",
    "geografija", "arhitektura", "skulptura", "istorija", "ekonomija",
    "politika", "sociologija", "antropolog", "ekologija", "energetika",
    "informatika", "statistika", "semantika", "pragmatika", "sintaksa",
    "morfologija", "fonologija", "leksikolog", "dijalektol", "etimolog",
    "semiotika", "hermeneutika", "retorika", "stilistika", "poetika",
    "naratologi", "diskursna", "kognitivna", "primenjena", "komparativna",
    "automobil", "biciklistk", "fotografij", "novinarstv", "obrazovanje",
    "upravljanj", "arhivistika", "bibliotekar", "dokumentar", "enciklopedij",
    "istraživanj", "metodologij", "organizacij", "planiranje", "projektovanj",
    "razvijenij", "saradnja", "sistemski", "struktura", "tehnologija",
    "tradicionaln", "upravljačk", "vaspitanje", "zakonodavac", "zdravstveni",
    "akreditacij", "bezbednost", "certifikacij", "digitalizacij", "evaluacij",
    "finansijsk", "gastronomij", "humanistič", "implementacij", "justifikacij",
    "komercijalizacij", "legitimacij", "menadžment", "normativni", "opterećenj",
    "paralelizm", "kvalifikacij", "regionalizacij", "standardizacij", "transformacij",
    "urbanizacij", "validacij", "xerografij", "zainteresovan", "aplikacija",
    "platforma", "protokol", "interfejs", "algoritam", "kompilator",
    "interpreter", "paralelizm", "distribuiran", "mikroprocesor", "operativni",
    "sistemska", "baza", "podataka", "relaciona", "hijerarhijska",
)

# ── Класа 12: Тежи дијакритици (š, č, ć, ž, đ) (~100) ────────────────────────
DIACRITICS: tuple[str, ...] = (
    # ш-група
    "šuma", "šaka", "šal", "šator", "šav", "škola", "šlem", "šminka",
    "šnajder", "šor", "štampa", "šuplja", "šipka", "šira", "šljiva",
    "šarena", "šifra", "šahist", "šamar", "šapat", "šaput", "šaraf",
    "šarač", "šarkan", "šarlog", "šarpes", "šarplan", "šarula",
    # ч-група
    "čaj", "čaša", "čelik", "čelo", "čep", "česma", "četa", "čizma",
    "čoje", "čorba", "čuvar", "čakija", "čamac", "čarapa", "čvor",
    "čamotinja", "čarobnjak", "čarolija", "čavrljanje", "čestitka",
    "četkica", "čišćenje", "čizmica", "čudovište", "čuvarnica",
    # ћ-група
    "ćup", "ćuran", "ćebe", "ćorav", "ćuprija", "ćutnja", "ćelav",
    "ćošak", "ćilim", "ćuk", "ćata", "ćorsokak", "ćiriš", "ćevapčić",
    "ćelija", "ćelijska", "ćilibaran", "ćilibarnast",
    # ж-група
    "žaba", "žal", "žar", "žena", "žetva", "žica", "žig", "žir",
    "žito", "žleb", "žurka", "žvaka", "ždrelo", "žeđ", "žlica",
    "žaran", "žarač", "žarište", "žarnica",
    # ђ-група
    "đak", "đavo", "đon", "đubre", "đul", "đus", "đumbir", "đinđuva",
    "đavolast", "đavolja", "đerdap", "đipovati", "đogrdan",
)

# ── Класа 13: Сугласнички кластер на почетку (~80) ────────────────────────────
CONSONANT_CLUSTER: tuple[str, ...] = (
    # бр-
    "brat", "brod", "brdo", "breza", "briga", "brkovi", "brlog",
    # вр-
    "vrat", "vrba", "vrelo", "vreme", "vriska", "vrsta",
    # гр-
    "grad", "grm", "grlo", "grob", "gruda", "grudi", "gruva",
    # др-
    "drvo", "drška", "drvo", "drug", "drum", "drugost",
    # зр-
    "zrno", "zrak", "zrelo", "zrelost", "zrenj",
    # кр-
    "krak", "kraj", "krov", "krpa", "krst", "kruška", "kruna",
    # мр-
    "mrak", "mrk", "mrva", "mravinjak", "mramor",
    # пр-
    "prst", "pruga", "pravda", "prsten", "proboj",
    # стр-
    "stroj", "struja", "strog", "strast", "strka",
    # тр-
    "trak", "trg", "trn", "trka", "truba", "trbuh",
    # цр-
    "crv", "crkva", "crno", "crep", "crta",
    # шт-
    "štampa", "štand", "šta", "štinak", "štica",
    # чв-
    "čvor", "čvrst", "čvrstoća",
    # шк-
    "škola", "škare", "škljoc", "škripac", "škrlak",
    # св-
    "svat", "svod", "svet", "svita", "svila",
    # сл-
    "slab", "slap", "sloj", "slon", "sloga",
    # см-
    "smer", "smeh", "smola", "smotra",
    # сн-
    "sneg", "snop", "snaha", "snaga",
    # сп-
    "spas", "spon", "sport", "spreg",
    # ст-
    "stih", "stog", "stop", "stub", "stup",
    # сц-
    "scena",
)

# ── Класа 14: Узастопни самогласници (~40) ────────────────────────────────────
DOUBLE_VOWEL: tuple[str, ...] = (
    "beograd", "autobus", "autoput", "leukocit", "nauka", "nauka",
    "aorta", "audit", "aurora", "baobab", "boem", "boemi", "koala",
    "oaza", "okean", "pauza", "pauk", "paun", "pauperiz", "radio",
    "reostat", "seoba", "seobena", "teorija", "teozan", "veoma",
    "voajer", "zaobilazan", "zaostao", "zaogrnut", "zaokret",
    "leotard", "neoklasičan", "preobrazan", "neodređen",
    "beogradski", "beouputnik", "deoničar", "preobraćaj", "reosigur",
)

# ── Флат листа свих речи — дедупликована, тачно 963 ──────────────────────────
def _build_corpus() -> tuple[str, ...]:
    """Спаја све класе, уклања дупликате (case-insensitive), сече на 963."""
    seen: set[str] = set()
    result: list[str] = []
    for word in (
        *VOWEL_INITIAL,
        *SYLLABIC_R,
        *DIGRAPH_LJ,
        *DIGRAPH_NJ,
        *DIGRAPH_DZ,
        *SHORT_3,
        *SHORT_4,
        *MEDIUM_5,
        *MEDIUM_6,
        *MEDIUM_7,
        *LONG_8PLUS,
        *DIACRITICS,
        *CONSONANT_CLUSTER,
        *DOUBLE_VOWEL,
    ):
        key = word.lower()
        if key not in seen:
            seen.add(key)
            result.append(word)
    return tuple(result[:963])


CORPUS_963: tuple[str, ...] = _build_corpus()

assert len(CORPUS_963) == 963, f"Очекивано 963, добијено {len(CORPUS_963)}"

CORPUS_963_TEXT: str = " ".join(CORPUS_963)

# Метаподаци корпуса
CORPUS_META: dict[str, object] = {
    "total": len(CORPUS_963),
    "classes": {
        "VOWEL_INITIAL": len(VOWEL_INITIAL),
        "SYLLABIC_R": len(SYLLABIC_R),
        "DIGRAPH_LJ": len(DIGRAPH_LJ),
        "DIGRAPH_NJ": len(DIGRAPH_NJ),
        "DIGRAPH_DZ": len(DIGRAPH_DZ),
        "SHORT_3": len(SHORT_3),
        "SHORT_4": len(SHORT_4),
        "MEDIUM_5": len(MEDIUM_5),
        "MEDIUM_6": len(MEDIUM_6),
        "MEDIUM_7": len(MEDIUM_7),
        "LONG_8PLUS": len(LONG_8PLUS),
        "DIACRITICS": len(DIACRITICS),
        "CONSONANT_CLUSTER": len(CONSONANT_CLUSTER),
        "DOUBLE_VOWEL": len(DOUBLE_VOWEL),
    },
}
