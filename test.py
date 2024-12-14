from magry6542_hovedinnlevering2 import finnResultat, partiKode, lesStemmer, Parti, kretsNr,partiNavn,lesValg



#stemmer = lesStemmer()

def flestStemmer(valgresultat,parti1,parti2):
    kode1=partiKode(parti1)
    kode2=partiKode(parti2)
    if 'ukjent parti' in [kode1,kode2]:
        return 'ukjent parti'
    stemmer1=finnResultat(valgresultat,kode1)
    stemmer2=finnResultat(valgresultat,kode2)
    if stemmer1==stemmer2:
        return f'{parti1} og {parti2} fikk like mange stemmer ({stemmer1})'
    elif stemmer1>stemmer2:
        return f'{parti1} fikk flest stemmer ({stemmer1})'
    else: return f'{parti2} fikk flest stemmer ({stemmer2})'

#print(flestStemmer(stemmer, 'arbeiderpartiet', 'h'))

def småpartier(resultatfortegnelse, kretsNavn):
    krets=kretsNr(kretsNavn)
    for stemmetall in resultatfortegnelse[krets]:
        antallStemmer=stemmetall.antall
        if antallStemmer<20:
            parti=partiNavn(stemmetall.parti)
            print(f'{parti} fikk {stemmetall.antall} stemmer')

x = lesValg('stemmer2013.txt')

småpartier(x,'damsgård')
