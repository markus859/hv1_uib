# oppgave 1 a
class Parti:
    def __init__(self, kode, parti) -> None:
        self.kode: str =  kode
        self.parti: str = parti 

    def skriv(self):
        print(f'{self.parti} ({self.kode})', f' Valgår: {self.aar}' if self.aar != [] else '')



def partiNavn(inpt:str) -> str:
    global partier 
    for i in partier:
        if i.kode == inpt.upper() or i.parti.lower().strip() == inpt.lower():
            return i.parti.strip()
    
    return 'ukjent parti'


# c
def partiKode(inpt:str) -> str:
    global partier 
    for i in partier:
        if i.parti.lower().strip() == inpt.lower() or i.kode == inpt.upper():
            return i.kode
        
    return 'ukjent parti'


# d
class StemmeTall:
    def __init__(self, kode, antall) -> None:
        self.parti: str = kode
        self.antall: int = antall
        self.merknad: str | None = None

    def skriv(self) -> None:
        print(f'{self.parti}:{self.antall} {f'Merknad: {self.merknad}' if self.merknad != None else ''}')

    def leggTilMerknad(self, merk:str) -> None:
        if self.merknad == None:
            self.merknad = merk
        else:
            self.merknad = self.merknad + ' / ' + merk


# e
def lesStemmer() -> list[StemmeTall]:
    global partier 
    stemmer: list[StemmeTall] = []
    # bruk denne for å slippe å skrive inn for hvert parti
    #slipp_aa_skrive: list[int] = [4,5,4,3,2,3,4,5,4,3,3,3,3,3,3,3,3,3,3,3,3,3,3,33]
    #index: int = 0
    for i in partier:
        antall: int = int(input(f'Antall stemmer for {i.parti}'))
        #antall = slipp_aa_skrive[index]
        #index += 1
        instance: StemmeTall = StemmeTall(kode=i.kode, antall=antall)
        stemmer.append(instance)
    
    return stemmer


def finnResultat(valgresultat: list[StemmeTall], inpt:str) -> int | None:
    parti_kode = partiKode(inpt)
    for i in valgresultat:
        if i.parti == parti_kode:
            return i.antall
        
    return None


# oppgave 2
def lesPartier() -> list[Parti]:
    partier: list[Parti] = []

    f = open('partier.txt', 'r', encoding='UTF-8')
    for line in f:
        s = line.strip().split(',')

        instance = Parti(kode=s[0], parti=s[1])
        partier.append(instance)

    f.close()
    return partier

partier = lesPartier()


# Oppgave 3 a 
def lesKretser() -> dict[int,str]:
    f = open('kretser.txt', 'r', encoding='UTF-8')
    d2 = False
    kretser: dict[int,str] = {}
    for line in f:
        navn = ''
        kode = ''
        for karakter in line:
            if karakter == ',':
                d2 = True
            elif karakter == '\n':
                break
            elif d2:
                navn += karakter
            else:
                kode += karakter 
        kretser[int(kode)] = navn
        d2 = False
    f.close()
    return kretser

kretser = lesKretser()


# b 
def kretsNr(inpt) -> int | str:
    global kretser

    # gjør inpt til int hvis det er mulig 
    try: inpt = int(inpt)
    except: inpt = str(inpt)

    if type(inpt) == int:
        if inpt in kretser.keys():
            return inpt
        return 'ukjent krets'
    
    for i in kretser: 
        if kretser[i].lower() == inpt.lower():
            return i
    return 'ukjent krets'


def lesValg(fil:str) -> dict:
    # samarbeidet med Mikkel 
    f = open(f'{fil}', 'r', encoding='UTF-8')

    resultat: dict[int,list[StemmeTall]] = {}

    gjeldende_krets: int = -1
    for line in f:
        # hopper over første linje 
        if gjeldende_krets == -1:
            gjeldende_krets = 0
            continue
        
        splitet = line.strip().split(',')
        krets = splitet[0]
        kode = splitet[1]
        stemmer = int(splitet[2])

        if gjeldende_krets != int(krets):
            gjeldende_krets = int(krets)

        instanceS: StemmeTall = StemmeTall(kode=kode, antall=stemmer)

        if gjeldende_krets not in resultat:
            resultat[gjeldende_krets] = [instanceS]
        else:
            resultat[gjeldende_krets].append(instanceS)

    f.close()
    return resultat

valg13: dict[int,list[StemmeTall]] = lesValg('stemmer2013.txt')
valg17: dict[int,list[StemmeTall]] = lesValg('stemmer2017.txt')
valg21: dict[int,list[StemmeTall]] = lesValg('stemmer2021.txt')


# oppgave 6
def kretsResultat(valg, krets, parti) -> None:
    krets_kode = kretsNr(krets)
    parti_kode = partiKode(parti)

    if parti_kode == 'ukjent parti': 
        print(parti_kode) 
        return
    elif krets_kode == 'ukjent krets': 
        print(krets_kode) 
        return
    
    stemmetall: list[StemmeTall] = valg[krets_kode]
    
    for i in stemmetall:
        if i.parti == parti_kode:
            print(i.antall)
            return


#oppgave 7
def samlet(valg:dict[int,list[StemmeTall]] ) -> dict[str, int]:
    fortegnelse: dict[str, int] = {}

    for krets, stemmetall_liste in valg.items():
        for stemmetall in stemmetall_liste:
            if stemmetall.parti not in fortegnelse:
                fortegnelse[stemmetall.parti] = stemmetall.antall
            else:
                fortegnelse[stemmetall.parti] += stemmetall.antall

    return fortegnelse


#oppgave 7
def prosentfordeling(valg:dict[int,list[StemmeTall]] ) -> dict[str, tuple]:
    fortegnelse: dict[str, tuple] = {}
    total: int = 0

    for krets, stemmetall_liste in valg.items():
        for stemmetall in stemmetall_liste:
            if stemmetall.parti not in fortegnelse:
                fortegnelse[stemmetall.parti] = stemmetall.antall
            else:
                fortegnelse[stemmetall.parti] += stemmetall.antall
            total += stemmetall.antall

    # legger inn tuple med prosentfordeling og antall stemmer for gjenbruk
    for kode, antall in fortegnelse.items():
        fortegnelse[kode] = (round(antall/total * 100, 2), antall)

    return fortegnelse


# Oppgave 9
# samarbeidet med mikkel 
def kretsOversikt(valg) -> None:
    
    while True:
        inpt = input('Krets: ').lower()

        if inpt == 'slutt':
            break

        krets_kode = kretsNr(inpt)

        if krets_kode == 'ukjent krets':
            print(krets_kode)
            continue

        krets_list = valg[krets_kode]

        total: int = 0
        for i in krets_list:
            total += i.antall 
        
        for i in krets_list:
            navn = partiNavn(i.parti)
            print(f'{navn} fikk {i.antall} stemmer({round(i.antall/total*100, 2)}%)')


# Oppgave 10
#samarbeidet med mikkel 
def kretsNavn(kode) -> str:
    f = open('kretser.txt', 'r', encoding='UTF-8')
    navn = ''
    for line in f:
        if line.startswith(kode):
            navn = line.split(',')[1]
    f.close()
    return navn.strip()


def partiOversikt(valg, parti_navn) -> None:
    parti_kode = partiKode(parti_navn)
    parti_navnC = partiNavn(parti_navn)

    lavest = None
    lav_krets = [0]
    hoyest = None
    hoy_krets = [0]
    
    parti_data = prosentfordeling(valg)[parti_kode]
    
    #krets(stemmer parti, stemmer totalt)
    mathidathi: dict[int, float] = {}

    for key, value in valg.items():
        stemmer = 0
        t = 0
        for i in value:
            t += i.antall
            if i.parti != parti_kode:
                continue
            stemmer = i.antall
            break
        mathidathi[key] = round(stemmer / t * 100, 2    )

    for key, value in mathidathi.items():

        if lavest is None and hoyest is None:
            lavest = value 
            hoyest = value 
            continue 

        if value <= lavest:
            lavest = value 
            if mathidathi[lav_krets[-1]] > value:
                del lav_krets[-1]
            lav_krets.append(key)

        elif value >= hoyest:
            hoyest = value 
            if mathidathi[hoy_krets[-1]] < value:
                if len(hoy_krets) > 1:
                    del hoy_krets[-1]
            hoy_krets.append(key)

    lk = ''
    for i in lav_krets:
        lk += kretsNavn(str(i))+', '
    hk = ''
    for i in hoy_krets:
        hk += kretsNavn(str(i))+', '

    print(f'{parti_navnC} fikk {parti_data[1]} stemmer ({parti_data[0]}%)')
    print(f'Høyest oppslutning ({hoyest}%): {hk}')
    print(f'Lavest oppslutning ({lavest}%): {lk}')

    return

