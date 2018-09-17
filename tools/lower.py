mesaj_gonderme = 0
buyukAlfabe = "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ"
kucukAlfabe = "abcçdefgğhıijklmnoöprsştuüvyz"


def lower(text:str):
    newText=str()
    if text == None:
        return 
    for i in text:
        if i in buyukAlfabe:
            index = buyukAlfabe.index(i)
            newText +=kucukAlfabe[index]
        else:
            newText +=i

    return newText