
class polinom():
    
    def __init__(self, *argv):
        if len(argv) == 1 and type(argv[0]) is list:
            self.__poly = argv[0]
            if self.__poly == []:
                self.__poly = [0, 0]
            return
        self.__poly = list(argv)
        if self.__poly == []:
            self.__poly = [0, 0]
            return
        if type(self.__poly) != list:
            raise Exception("Nepodprt vnos")
        self.popExtraNicle()
        
    def __str__(self, presledekNaZacetku = False):
        '''Vrne zapis polinoma, ki je pripravljen na izpis --> string'''
        if self.__poly == [0, 0]:
            return "0"
        self.popExtraNicle()
        polinom = ""
        for i in range(len(self)):
            koef = self[i]
            if i == len(self)-1:
                if koef > 0:
                    polinom += " + " + str(koef)
                elif koef < 0:
                    polinom += " - " + str(abs(koef))
                elif len(self) == 1:
                    polinom = "0"
                continue
            
            eks = len(self) - i -1
            
            # ČE ŽELIŠ DA NA ZAČETKU NI PRESLEDKA MED ZNAKOM IN KOEFICIENTOM
            if presledekNaZacetku:
                if i == 0:
                    if koef > 0:
                        polinom += " +" + str(koef) +"x^" + str(eks)
                    elif koef < 0:
                        polinom += " -" + str(abs(koef)) +"x^" + str(eks)
                    continue
            
            if koef > 0:
                polinom += " + " + str(koef) +"x^" + str(eks)
            elif koef < 0:
                polinom += " - " + str(abs(koef)) +"x^" + str(eks)
        
        polinom = polinom.strip()
        return polinom
    
    def __repr__(self):
        '''Ob klicu funkcije print(polinom) izpiše polinom'''
        return str(self)
    
    def __add__(self, other):
        '''Ko je v pythonu uporabljen + desno od spremenljivke, ki je tipa polinom je klicana
        ta funkcija, ki nato polinomu prišteje vrednost, ki je desno od njega'''
        if type(other) is float or type(other) is int:
            output = polinom()
            output.copy(self)
            output[-1] += other
            return output
        output = []
        dolzina1 = len(self)
        dolzina2 = len(other)
        razlika = dolzina1 - dolzina2
        if razlika > 0:
            for i in range(0, dolzina1):
                if i < razlika:
                    output.append(self[i])
                    continue
                output.append(self[i] + other[i - razlika])
            return polinom(output)
        if razlika < 0:
            razlika *= -1
            for i in range(0, dolzina2):
                if i < razlika:
                    output.append(other[i])
                    continue
                output.append(other[i] + self[i - razlika])
            return polinom(output)
        for i in range(dolzina1):
            output.append(self[i] + other[i])
        return polinom(output)
    
    def __radd__(self, other):
        if type(other) is float or type(other) is int:
            output = polinom()
            output.copy(self)
            output[-1] += other
            return output
    
    def __sub__(self, other):
        '''Ko je v pythonu uporabljen "-" desno od spremenljivke, ki je tipa polinom je klicana
        ta funkcija, ki nato polinomu prišteje nasprotno vrednost, ki je desno od njega'''
        if type(other) is float or type(other) is int:
            output = polinom()
            output.copy(self)
            output[-1] -= other
            return output
        output = []
        for i in range(0, len(other)):
            output.append(other[i] * (-1))
        return self + polinom(output)
    
    def __rsub__(self, other):
        if type(other) is float or type(other) is int:
            output = polinom()
            output = self * (-1)
            output[-1] += other
            return output
    
    def __len__(self):
        '''Ta funkcija je klicana, ko je uporabljena metoda len() na spremenljivki tipa polinom.
        Vrne število koeficientov tega polinoma(vkjlučno z ničelnimi)'''
        self.popExtraNicle()
        return len(self.__poly)

    def __mul__(self, other):
        '''Ta funkcija je poklicana ko desno od spremenljivke tipa polinom nastopa znak "*".
        Ta funkcija nato zmnoži ta polinom z številom/polinomom desno od njega.'''
        if type(other) is int or type(other) is float:
            output = []
            for k in self.__poly:
                output.append(k * other)
            return polinom(output)
        if type(other) is polinom:
            p1 = polinom()
            p2 = polinom()
            p1.copy(self)
            p2.copy(other)
            r  = len(p1) - len(p2)
            if r > 0:
                p2.rshift(r)
            if r < 0:
                p1.rshift(abs(r))
            output = polinom()
            l = len(p1) - 1
            for k1 in p1.__poly:
                pol = []
                for k2 in p2.__poly:
                    pol.append(k2 * k1)
                p = polinom(pol)
                p.lshift(l)
                output += p
                l -= 1
            output.popExtraNicle()
            return output

    def __rmul__(self, other):
        '''Ta funkcija je poklicana v primeru, da je levo od polinoma znak "*" in je
        na drugi strani znaka spremenljivka, ki nima vgrajenega deljenja s polinomi'''
        if type(other) is int or type(other) is float:
            output = []
            for k in self.__poly:
                output.append(k * other)
            return polinom(output)
        else:
            raise Exception("Nepodrt tip deljenja.")
    
    def __truediv__(self, other):
        '''Ta funkcija je poklicana v primeru, da se desno od spremenljivke tipa polinom nahaja
        znak "/". Funkcija nato deli polinom s številom ali polinomom, ki je na drugi strani.
        V primeru, da je polinom večji od prvega, vrne napako.'''
        if type(other) is int or type(other) is float:
            output = []
            for k in self:
                output.append(k/other)
            return polinom(output)
        
        if type(other) is polinom:
            if len(self) < len(other):
                raise Exception("Drugi polinom je vecji od prvega")
            pol1 = polinom()
            pol1.copy(self)
            rez = polinom()
            while pol1.stopnja() >= other.stopnja():
                r = polinom()
                kolicnik = pol1[0]/other[0]
                r[1] = kolicnik 
                r.lshift(pol1.stopnja() - other.stopnja())
                rez += r
                p = other * kolicnik
                p.lshift(pol1.stopnja() - other.stopnja())
                pol = pol1 - p
                pol1 = pol
            return (rez, pol1)      

    def __getitem__(self, key):
        '''Ta funkcija je poklicana, ko je v programu potrebovana vrednost nekega i-tega polinomovega
        koeficienta.
        npr.: vodilni_koeficient = polinom1[0]'''
        return self.__poly[key]
    
    def __setitem__(self, key, val):
        '''Ta funkcija je poklicana, ko je v programu spremjenjena vrednost nekega i-tega polinomovega
        koeficienta.
        npr.: polinom[0] = 2'''
        l = self.__poly
        l[key] = val
        self.__poly = l
        self.popExtraNicle()
    
    def __delitem__(self, key):
        '''Ta funkcija je poklicana, ko je v programu izbrisana vrednost nekega i-tega polinomovega
        koeficienta. Ta vrednost je spremenjena v 0. Ker vodilni koeficient ne sme biti enak 0 je
        v tem primeru izbrisano prvo mesto seznama.
        npr.: del polinom1[0]'''
        self.__poly[key] = 0
        self.popExtraNicle()
        
    def __eq__(self, other):
        '''Ta funkcija je poklicna, ko nekje znotraj programa preverjamo enakost
        dveh polinomov.'''
        if self.__poly == other.__poly:
            return True
        else: 
            return False
    
    def __ne__(self, other):
        '''Ta funkcija je poklicna, ko nekje znotraj programa preverjamo neenakost
        dveh polinomov.'''
        if self.__poly == other.__poly:
            return False
        else: 
            return True
        
    def lshift(self, n):
        '''Ta funkcija polinom pomnoži z x^n.'''
        l = self.__poly
        for i in range(n):
            l.append(0)
        self.__poly = l
    
    def rshift(self, n):
        '''Ta funkcija polinomu doda ničelni vodilni koeficient/več koeficientov. Uporabna je le v 
        primerih, ko je željena enaka dolžina dveh polinomov.
        Npr. seštevanje in odštevanje''' 
        l = self.__poly
        for i in range(n):
            l.insert(0, 0)
        self.__poly = l
    
    def copy(self, other):
        '''Ta funkcija kopira vrednost drugega polinoma vase. Koristna je za olajšanje
        bralnosti berljivosti določenih programov'''
        self.__poly = other.__poly
    
    def raw(self):
        '''Ta funkcija vrne "surov" zapis polinoma, takšno, kot je shranjena v pomnilniku''' 
        return self.__poly
    
    def popExtraNicle(self):
        '''Ta funkcija izbriše kakršne koli ničelne vodilne koeficiente.''' 
        sez = self.__poly
        while True:
            if len(sez) == 1:
                return
            if sez[0] == 0:
                sez.pop(0)
            else:
                break
        self.__poly = sez
        
    def hornerjevAlgoritem(self, n):
        '''Ta funkcija izvede hornerjev algoritem za nek n. Vrne tuple v obliki (k(x), o)
        Kjer sta k(x) količnik in o ostanek. o je tudi vrednost polinoma v n''' 
        if self.stopnja() == 0:
            raise Exception("Polinom je stopnje 0")
        kx = self
        for i in range(1, len(self)):
            kx[i] = kx[i - 1] * n + kx[i]
        o = kx[-1]
        kx.pop(-1)
        return (kx, o)
    
    def vrednost(self, x):
        '''Ta funkcija vrne vrednost polinoma za nek določen x.''' 
        output = 0
        for i in range(len(self)):
            output += self.__poly[i] * x**(len(self) - i - 1)
        return output
    
    def stopnja(self):
        '''Ta funkcija vrne stopnjo polinoma. Uporabna kvečjemu za olajšanje berljivosti''' 
        self.popExtraNicle()
        return len(self) - 1
    
    def pop(self, i):
        '''Ta funkcija izbriše mesto iz seznama koeficientov v polinomu. --> !pride do zamikov koeficientov!''' 
        lst = self.__poly
        lst.pop(i)
        self.__poly = lst
        
    def odvod(self):
        '''Ta funkcija vrne odvod polinoma''' 
        p1 = polinom()
        p1.copy(self)
        for i in range(p1.stopnja()):
            p1[i] = p1[i] * (p1.stopnja() - i)
        p1.pop(-1)
        return p1
    
    def dolIntegral(self, a, b):
        p1 = polinom()
        p1.copy(self)
        for i in range(p1.stopnja()):
            p1[i] = p1[i] * 1/(p1.stopnja() -i + 1)
        p1.lshift(1)
        return p1.vrednost(b) - p1.vrednost(a)