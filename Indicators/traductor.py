
    ## Traducción de Prefijos
    def traductor(valor):
        print(valor.split(" "))
        val,pref = valor.split(" ")
        val = int(val) * Prefijos[pref]
        return val
