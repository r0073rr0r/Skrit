CORPUS_36_WORDS: tuple[str, ...] = (
    "zemun",
    "zakon",
    "matori",
    "pishtolj",
    "bazen",
    "mačka",
    "značka",
    "đavo",
    "riba",
    "ribi",
    "grize",
    "rep",
    "beograd",
    "brate",
    "trava",
    "kuća",
    "prozor",
    "škola",
    "žurka",
    "čamac",
    "ljudi",
    "njiva",
    "džep",
    "prst",
    "mrk",
    "cvet",
    "sunce",
    "voda",
    "kamen",
    "most",
    "autobus",
    "program",
    "šifra",
    "enkripcija",
    "ulaz",
    "izlaz",
)

CORPUS_36_TEXT = " ".join(CORPUS_36_WORDS)

EXPECTED_SATRO_36 = (
    "munze konza matori shtoljpi zenba čkama čkazna vođa bari biri zegri pre gradbeo "
    "tebra vatra ćaku zorpro laško rkažu macča dilju vanji pdže stpr rkm tcve ncesu "
    "davo menka stmo tobusau grampro fraši nkripcijae lazu zlazi"
)

EXPECTED_UTRO_36 = (
    "umunzazenje ukonzazanje utorizamanje ushtoljzapinje uzenzabanje učkazamanje "
    "učkazaznanje uvozađanje ubazarinje ubizarinje uzezagrinje upzarenje ugradzabeonje "
    "utezabranje uvazatranje ućazakunje uzorzapronje ulazaškonje urkazažunje umaczačanje "
    "udizaljunje uvazanjinje upzadženje ustzaprnje urkzamnje utzacvenje uncezasunje "
    "udazavonje umenzakanje ustzamonje utobuszaaunje ugramzapronje ufrazašinje "
    "unkripcijazaenje ulazzaunje uzlazzainje"
)

EXPECTED_LEET_SATRO_36 = (
    "m00n23 k0n24 70r1m4 5h70ljp1 23nb4 čk4m4 čk42n4 v0đ4 b4r1 b1r1 23gr1 pr3 gr4db30 "
    "73br4 v47r4 ć4k00 20rpr0 l4šk0 rk4ž00 m4cč4 d1lj00 v4nj1 pdž3 57pr rkm 7cv3 nc3500 "
    "d4v0 m3nk4 57m0 70b005400 gr4mpr0 fr4š1 nkr1pc1j43 l4200 2l421"
)

EXPECTED_LEET_UTRO_36 = (
    "00mun24zen73 00kon24zan73 00tori24man73 00shtolj24pin73 00zen24ban73 00čka24man73 "
    "00čka24znan73 00vo24đan73 00ba24rin73 00bi24rin73 00ze24grin73 00p24ren73 00grad24beon73 "
    "00te24bran73 00va24tran73 00ća24kun73 00zor24pron73 00la24škon73 00rka24žun73 00mac24čan73 "
    "00di24ljun73 00va24njin73 00p24džen73 00st24prn73 00rk24mn73 00t24cven73 00nce24sun73 "
    "00da24von73 00men24kan73 00st24mon73 00tobus24aun73 00gram24pron73 00fra24šin73 "
    "00nkripcija24en73 00laz24un73 00zlaz24in73"
)

EXPECTED_BASIC_LEET_DIRECT_36 = (
    "23m00n 24k0n m470r1 p15h70lj 8423n m4čk4 2n4čk4 đ4v0 r184 r181 6r123 r3p 8306r4d "
    "8r473 7r4v4 k00ć4 pr020r šk0l4 ž00rk4 č4m4c lj00d1 nj1v4 dž3p pr57 mrk cv37 500nc3 "
    "v0d4 k4m3n m057 400708005 pr06r4m š1fr4 3nkr1pc1j4 00l42 12l42"
)
