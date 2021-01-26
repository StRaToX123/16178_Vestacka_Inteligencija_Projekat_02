# Broj Indeksa : 16178
# Ime i prezime : Pavle Marinković 
# Naslov rada : Implementacija genetskog algoritma za rešavanje rasporeda na fakultetu

# Gledao sam da kompletan kod bude u jednom .py fajlu radi lakse distribucije.
# Opis rada aplikacije i druge informacije se mogu naci u izveštaju "Izvestaj.pdf"


#########################################################
#########################################################
#########################################################
#########################################################

import random
import copy


class Predmet(object):
	id = -1 # static varijabla za ovu klasu, svaka instanca uzme svoj id u svojoj __init__ funkciji
	def __init__(self, ime, *args, **kwargs):
		self.id = Predmet.id + 1
		Predmet.id = self.id
		self.ime = ime
		return super().__init__(*args, **kwargs)

class GrupaStudenata(object):
	id = -1 # static varijabla za ovu klasu, svaka instanca uzme svoj id u svojoj __init__ funkciji
	def __init__(self, imeGrupe, brojStudenataUGrupi, *args, **kwargs):
		self.id = GrupaStudenata.id + 1
		GrupaStudenata.id = self.id
		self.ime = imeGrupe
		self.Predavanjeovi = None # lista Predavanja koje pohadja ova grupa studenata  
		self.brojStudenataUGrupi = brojStudenataUGrupi
		return super().__init__(*args, **kwargs)


class Predavanje(object):
	svi = [] # lista svih instanci ove klase
	def __init__(self, predmet, profesor, grupeStudenata, trajanjePredavanja, *args, **kwargs):
		self.predmet = predmet
		self.profesor = profesor
		self.grupeStudenata = grupeStudenata
		self.ukupanBrojStudenata = 0
		self.trajanjePredavanja = trajanjePredavanja
		Predavanje.svi.append(self)
		# Racunanje ukupanBrojStudenata
		for grupaStudenata in grupeStudenata:
			self.ukupanBrojStudenata = self.ukupanBrojStudenata + grupaStudenata.brojStudenataUGrupi

		return super().__init__(*args, **kwargs)

	def __str__(self):
		rezultatString = "Pred: "
		rezultatString += self.predmet.ime
		rezultatString += " Prof: "
		rezultatString += self.profesor.ime
		rezultatString += " Grupe: "
		for i in range(len(self.grupeStudenata)):
			rezultatString += str(self.grupeStudenata[i].ime)
			rezultatString += " "

		return rezultatString


class Profesor(object):
	id = -1 # static varijabla za ovu klasu, svaka instanca uzme svoj id u svojoj __init__ funkciji
	def __init__(self, ime, *args, **kwargs):
		self.id = Profesor.id + 1
		Profesor.id = self.id
		self.ime = ime
		self.Predavanjeovi = None # lista Predavanja koje ovaj profesor predaje 
		return super().__init__(*args, **kwargs)

class Amfiteatar(object):
	id = -1 # static varijabla za ovu klasu, svaka instanca uzme svoj id u svojoj __init__ funkciji
	count = 0 # ukupan broj instanci klase Amfiteatar
	svi = []
	def __init__(self, ime, brojStolica, *args, **kwargs):
		self.id = Amfiteatar.id + 1
		Amfiteatar.id = self.id
		Amfiteatar.count = Amfiteatar.count + 1
		self.ime = ime
		self.brojStolica = brojStolica
		Amfiteatar.svi.append(self)
		return super().__init__(*args, **kwargs)

class Hromozom(object):
	def __init__(self, *args, **kwargs):
		self.dobrota = 0
		self.termini = None # lista gde je svaki elemenat predstavlja jedan sat u jednom dan u jednom amfiteatru, svaki elemenat je lista Predavanja kojima je dat taj termin
		self.mapaPredavanja = [] # lista gde je svaki elemenat lista ciji je prvi elemenat Predavanje, a drugi index liste termini gde se taj Predavanje prvo pojavljuje
		return super().__init__(*args, **kwargs)


	def IzracunajDobrotu(self, brojDanaURasporedu, brojSatiUDanu):
		poeni = 0
		brojTerminaUDanu = brojSatiUDanu * Amfiteatar.count
		for i in range(len(self.mapaPredavanja)):
			indexTermina = self.mapaPredavanja[i][1]
			PredavanjeKojiRazmatramo = self.mapaPredavanja[i][0]
			kojiDan = int(indexTermina / brojTerminaUDanu) # kog dana u rasporedu se pada ovaj Predavanje 
			kojeVreme = indexTermina % brojSatiUDanu # u kom satu u toku dana se pada ovaj Predavanje
			
			# Provera da li se desava neko predavanje u istom terminu u istom amfiteatru
			postojeVisePredavanjaUIstomAmfiteatru = False
			for j in range(PredavanjeKojiRazmatramo.trajanjePredavanja)[::-1]:
				if(len(self.termini[indexTermina + j])) > 1:
					postojeVisePredavanjaUIstomAmfiteatru = True
					break

			if postojeVisePredavanjaUIstomAmfiteatru == False:
				poeni = poeni + 1

			# Provera da li amfiteatar u koji je smesten Predavanje ima dovoljno mesta
			if Amfiteatar.svi[int(indexTermina / brojSatiUDanu) % Amfiteatar.count].brojStolica >= PredavanjeKojiRazmatramo.ukupanBrojStudenata:
				poeni = poeni + 1

			# Provera da li se profesori ili grupe preklapaju sa profesorima i grupama
			# koje imaju Predavanje u isto ovo vreme ali u drugim amfiteatrima
			vreme = kojiDan * brojTerminaUDanu + kojeVreme
			postojiPreklapanjeProfesora = False
			postojiPreklapanjeGrupaStudenata = False
			breakEarly = False
			for j in range(Amfiteatar.count): # za svaki amfiteatar
				for k in range(PredavanjeKojiRazmatramo.trajanjePredavanja)[::-1]: # za sve termine koje pokriva ovaj Predavanje
					for p in range(len(self.termini[vreme + k])): # prolazimo kroz ostale Predavanjeove u tim terminima i proveravamo sledece
						PredavanjeSaKojimUporedjujemo = self.termini[vreme + k][p]
						# da li su u pitanju razliciti Predavanjeovi
						if PredavanjeKojiRazmatramo != PredavanjeSaKojimUporedjujemo:
							# da li se pojavljuje isti profesor u oba termina
							if (PredavanjeKojiRazmatramo.profesor.id == PredavanjeSaKojimUporedjujemo.profesor.id) and (not postojiPreklapanjeProfesora):
								postojiPreklapanjeProfesora = True
							
							# da li se pojavljuju iste grupe studenata u oba termina
							for h in range(len(PredavanjeKojiRazmatramo.grupeStudenata)):
								for g in range(len(PredavanjeSaKojimUporedjujemo.grupeStudenata)):
									if PredavanjeKojiRazmatramo.grupeStudenata[h] == PredavanjeSaKojimUporedjujemo.grupeStudenata[g]:
										postojiPreklapanjeGrupaStudenata = True
										break

								if postojiPreklapanjeGrupaStudenata == True:
									break

							# mozemo da zavrsimo ispitivanje ranije ako postoji i poklapanje profesora i poklapanje grupa studenata
							if (postojiPreklapanjeProfesora == True) and (postojiPreklapanjeGrupaStudenata == True):
								breakEarly = True

						if breakEarly == True:
							break
					if breakEarly == True:
						break
				if breakEarly == True:
					break

				vreme = vreme + brojSatiUDanu
				#indexTermina += brojSatiUDanu

			if postojiPreklapanjeProfesora == False:
				poeni = poeni + 1

			if postojiPreklapanjeGrupaStudenata == False:
				poeni = poeni + 1


		# Nakon sto smo obisli sve Predavanjeove i imamo konacan broj poena
		self.dobrota = float(poeni) / (len(Predavanje.svi) * 4)



	def Odstampaj(self, brojDanaURasporedu, brojSatiUDanu):
		resultString = ""
		for i in range(brojDanaURasporedu):
			print('Dan broj {0}:'.format(i))
			for j in range(Amfiteatar.count):
				print('    Amfiteatar {0}:'.format(j))
				for k in range(brojSatiUDanu):
					print('        Sat {0}:'.format(k))
					terminIndex = (i * Amfiteatar.count * brojSatiUDanu) + ((j * brojSatiUDanu) + k)
					for p in range(len(self.termini[terminIndex])):
						print('            {0}'.format(self.termini[terminIndex][p])) # printa objekat tipa Predavanje




	def OdrediNajboljeHromozome(hromozomi, maxBrojNajboljihHromozoma): # Vraca listu najboljih hromozoma od svih prosledjenih kao argument hromozomi
		najboljiHromozomi = []
		# za sorting algoritam
		def SortirajPoDobroti(e):
			return e[0].dobrota

		for i in range(len(hromozomi)):
			najboljiHromozomi.append([hromozomi[i], i, hromozomi[i].dobrota])
			najboljiHromozomi.sort(key=SortirajPoDobroti)
			if len(najboljiHromozomi) > maxBrojNajboljihHromozoma:
				najboljiHromozomi.pop(0)

		return najboljiHromozomi
	

	def Crossover(self, drugiHromozom, verovatnocaZaCrossover, brojCrossOverGranica, brojDanaURasporedu, brojSatiUDanu):
		# Ako se desava crossover onda pravimo novi hromozom
		noviHromozom = Hromozom()
		noviHromozom.termini = []
	

		# Prvo proverimo da li ce da se desi Crossover
		if random.randint(0, 100) > verovatnocaZaCrossover:
			noviHromozom.dobrota = self.dobrota
			for i in range(0, len(self.mapaPredavanja)):
				noviHromozom.mapaPredavanja.append(copy.copy(self.mapaPredavanja[i]))
		
		
			for i in range(0, len(self.termini)):
				noviHromozom.termini.append(copy.copy(self.termini[i]))
			
		
			return noviHromozom
		


		for i in range(len(self.termini)):
			noviHromozom.termini.append([])

		# lista indeksa u mapiKlasa hromozoma gde se desava promena od kog roditelja uzimamo Predavanjeove
		crossoverGranice = [] 
		for i in range(brojCrossOverGranica):
			while True:
				crossoverGranica = random.randint(0, len(self.mapaPredavanja) - 1)
				if crossoverGranica not in crossoverGranice:
					crossoverGranice.append(crossoverGranica)
					break

		# Sada kada znamo crossover granice mozemo da iskombinujemo dva hromozoma
		koJePrvi = False
		if random.randint(0, 1) == 1:
			koJePrvi = True
		for i in range(len(self.mapaPredavanja)):
			if koJePrvi == False:
				noviHromozom.mapaPredavanja.append(copy.copy(self.mapaPredavanja[i]))
				# Popunimo termine
				for j in range(self.mapaPredavanja[i][0].trajanjePredavanja)[::-1]:
					noviHromozom.termini[self.mapaPredavanja[i][1] + j].append(self.mapaPredavanja[i][0])

			else:
				noviHromozom.mapaPredavanja.append(copy.copy(drugiHromozom.mapaPredavanja[i]))
				# Popunimo termine
				for j in range(drugiHromozom.mapaPredavanja[i][0].trajanjePredavanja)[::-1]:
					noviHromozom.termini[drugiHromozom.mapaPredavanja[i][1] + j].append(drugiHromozom.mapaPredavanja[i][0])

			if i in crossoverGranice:
				koJePrvi = not koJePrvi


		noviHromozom.IzracunajDobrotu(brojDanaURasporedu, brojSatiUDanu)
		return noviHromozom


	def Mutacija(self, verovatnocaMutacija, brojPermutacijaUJednojMutaciji, brojDanaURasporedu, brojSatiUDanu):
		for i in range(brojPermutacijaUJednojMutaciji):
			# izaberemo random Predavanje iz mape Predavanja
			indexmapaPredavanja = random.randint(0, len(self.mapaPredavanja) - 1)
			# odredjivanje termina u koji ce mo da smestimo random izabrano Predavanje iz mape Predavanja
			kojiDan = random.randint(0, brojDanaURasporedu - 1)
			kojiAmfiteatar = random.randint(0, Amfiteatar.count - 1)
			kojeVreme = random.randint(0, brojSatiUDanu - self.mapaPredavanja[indexmapaPredavanja][0].trajanjePredavanja)
			noviTerminIndex = (kojiDan * Amfiteatar.count * brojSatiUDanu) + ((kojiAmfiteatar * brojSatiUDanu) + kojeVreme)

			# za svaki sat trajanja ovog Predavanjea
			for j in range(self.mapaPredavanja[indexmapaPredavanja][0].trajanjePredavanja)[::-1]:
				# izbrisati iz trenutnog termina
				self.termini[self.mapaPredavanja[indexmapaPredavanja][1] + j].remove(self.mapaPredavanja[indexmapaPredavanja][0])
				# dodati Predavanje u novi termin
				self.termini[noviTerminIndex + j].append(self.mapaPredavanja[indexmapaPredavanja][0])

			# Azurirati pocetni index za ovo Predavanje u mapi Predavanja
			self.mapaPredavanja[indexmapaPredavanja][1] = noviTerminIndex

		self.IzracunajDobrotu(brojDanaURasporedu, brojSatiUDanu)
		return None





if __name__ == '__main__': 
	# Ovo su neke od globalnih promenljivih potrebne za rad genetskog algoritma
	brojDanaURasporedu = 5
	brojSatiUDanu = 12
	brojHromozomaUPopulaciji = 100
	brojCrossOverGranica = 2
	brojPermutacijaUJednojMutaciji = 2
	verovatnocaCrossover = 80 # od 100
	verovatnocaMutacija = 3 # od 100
	brojNovihHromozomaUSvakomKoraku = 8
	maxBrojNajboljihHromozoma = 5

	# Prvo ce mo napraviti sve klase koje ucestvuju u algoritmu
	# Sve profesore, grupe studenata, predmete i module
	
	# Profesori :
	profesor01 = Profesor("Nikola M.")
	profesor02 = Profesor("Natasa T.")
	profesor03 = Profesor("Stefan N.")
	profesor04 = Profesor("Filip Z.")
	profesor05 = Profesor("Andjela M.")
	profesor06 = Profesor("Svetoslav I.")
	profesor07 = Profesor("Bozidar K.")
	profesor08 = Profesor("Nevena S.")
	profesor09 = Profesor("Sima S.")
	profesor10 = Profesor("Petar T.")
	profesor11 = Profesor("Monika F.")
	profesor12 = Profesor("Danica V.")
	profesor13 = Profesor("Nebojsa L.")

	# Predmeti :
	predmet01 = Predmet("Web Programiranje")
	predmet02 = Predmet("Fizika")
	predmet03 = Predmet("Vestacka Inteligencija")
	predmet04 = Predmet("Uvod U Racunarstvo")
	predmet05 = Predmet("Multimedija")
	predmet06 = Predmet("Matematika")
	predmet07 = Predmet("Engleski")
	predmet08 = Predmet("Grafika")

	# Amfiteatri
	amfiteatar01 = Amfiteatar("Amfiteatar 01", 24)
	amfiteatar02 = Amfiteatar("Amfiteatar 02", 60)

	# Grupe Studenata
	grupaStudenata01 = GrupaStudenata("Grupa 01", 19)
	grupaStudenata02 = GrupaStudenata("Grupa 02", 19)
	grupaStudenata03 = GrupaStudenata("Grupa 03", 19)
	grupaStudenata04 = GrupaStudenata("Grupa 04", 19)

	# Predavanjeovi
	Predavanje01 = Predavanje(predmet01, profesor01, [grupaStudenata01, grupaStudenata02], 2)
	Predavanje02 = Predavanje(predmet01, profesor01, [grupaStudenata03, grupaStudenata04], 2)
	Predavanje03 = Predavanje(predmet01, profesor09, [grupaStudenata01], 3)
	Predavanje04 = Predavanje(predmet01, profesor09, [grupaStudenata02], 3)
	Predavanje05 = Predavanje(predmet01, profesor09, [grupaStudenata03], 3)
	Predavanje06 = Predavanje(predmet01, profesor09, [grupaStudenata04], 3)
	Predavanje07 = Predavanje(predmet02, profesor02, [grupaStudenata03, grupaStudenata04], 2)
	Predavanje08 = Predavanje(predmet02, profesor02, [grupaStudenata01, grupaStudenata02], 2)
	Predavanje09 = Predavanje(predmet02, profesor03, [grupaStudenata01], 2)
	Predavanje10 = Predavanje(predmet02, profesor03, [grupaStudenata02], 2)
	Predavanje11 = Predavanje(predmet02, profesor03, [grupaStudenata03], 2)
	Predavanje12 = Predavanje(predmet02, profesor03, [grupaStudenata04], 2)	
	Predavanje13 = Predavanje(predmet04, profesor04, [grupaStudenata03, grupaStudenata04], 2)	
	Predavanje14 = Predavanje(predmet04, profesor04, [grupaStudenata01, grupaStudenata02], 2)	
	Predavanje15 = Predavanje(predmet06, profesor05, [grupaStudenata01, grupaStudenata02, grupaStudenata03], 2)	
	Predavanje16 = Predavanje(predmet05, profesor07, [grupaStudenata01, grupaStudenata02, grupaStudenata03], 2)	
	Predavanje17 = Predavanje(predmet05, profesor07, [grupaStudenata01, grupaStudenata02], 2)
	Predavanje18 = Predavanje(predmet05, profesor10, [grupaStudenata03], 2)
	Predavanje19 = Predavanje(predmet03, profesor08, [grupaStudenata02], 2)
	Predavanje20 = Predavanje(predmet03, profesor08, [grupaStudenata03], 2)
	Predavanje21 = Predavanje(predmet03, profesor12, [grupaStudenata01], 2)
	Predavanje22 = Predavanje(predmet03, profesor12, [grupaStudenata04], 2)	
	Predavanje23 = Predavanje(predmet07, profesor11, [grupaStudenata04], 2)	
	Predavanje24 = Predavanje(predmet08, profesor13, [grupaStudenata04], 2)	

	# Stvaranje referenci izmedju grupe studenata i Predavanja
	grupaStudenata01.Predavanjeovi = [Predavanje01, Predavanje03, Predavanje08, Predavanje09, Predavanje14, Predavanje15, Predavanje16, Predavanje17, Predavanje21]
	grupaStudenata02.Predavanjeovi = [Predavanje01, Predavanje04, Predavanje08, Predavanje10, Predavanje14, Predavanje15, Predavanje16, Predavanje17, Predavanje19]
	grupaStudenata03.Predavanjeovi = [Predavanje02, Predavanje05, Predavanje07, Predavanje11, Predavanje13, Predavanje15, Predavanje16, Predavanje18, Predavanje20]
	grupaStudenata04.Predavanjeovi = [Predavanje02, Predavanje06, Predavanje07, Predavanje12, Predavanje13, Predavanje22, Predavanje23, Predavanje24]

	# Stvaranje referenci izmedju profesora i Predavanja
	profesor01.Predavanjeovi = [Predavanje01, Predavanje02]
	profesor02.Predavanjeovi = [Predavanje07, Predavanje08]
	profesor03.Predavanjeovi = [Predavanje09, Predavanje10, Predavanje11, Predavanje12]
	profesor04.Predavanjeovi = [Predavanje13, Predavanje14]
	profesor05.Predavanjeovi = [Predavanje15]
	profesor06.Predavanjeovi = []
	profesor07.Predavanjeovi = [Predavanje16, Predavanje17]
	profesor08.Predavanjeovi = [Predavanje19, Predavanje20]
	profesor09.Predavanjeovi = [Predavanje03, Predavanje04, Predavanje05, Predavanje06]
	profesor10.Predavanjeovi = [Predavanje18]
	profesor11.Predavanjeovi = [Predavanje23]
	profesor12.Predavanjeovi = [Predavanje21, Predavanje22]
	profesor13.Predavanjeovi = [Predavanje24]

	# Sada kada su relacije izmedju objekata popunjene
	# Treba napraviti inicialnu populaciju hromozoma
	brojTerminaUHromozomu = brojDanaURasporedu * brojSatiUDanu * Amfiteatar.count # broj dana u raspored * broj sati u jednom radnom danu * broj amfiteatara
	hromozomi = []
	for i in range(brojHromozomaUPopulaciji):
		hromozom = Hromozom()
		hromozom.termini = []
		for j in range(brojTerminaUHromozomu):
			hromozom.termini.append([])

		for j in range(len(Predavanje.svi)):
			kojiDan = random.randint(0, brojDanaURasporedu - 1)
			kojiAmfiteatar = random.randint(0, Amfiteatar.count - 1)
			kojeVreme = random.randint(0, brojSatiUDanu - Predavanje.svi[j].trajanjePredavanja)
			terminIndex = kojiDan * Amfiteatar.count * brojSatiUDanu + kojiAmfiteatar * brojSatiUDanu + kojeVreme

			# Popuni termine u ovom hromozome za svaki sat Predavanjea
			for k in range(Predavanje.svi[j].trajanjePredavanja)[::-1]:
				hromozom.termini[terminIndex + k].append(Predavanje.svi[j])

			# Dodaj ovaj Predavanje u mapu Predavanja 
			hromozom.mapaPredavanja.append([Predavanje.svi[j], terminIndex])

		# Izracunavanje dobrote hromozoma
		hromozom.IzracunajDobrotu(brojDanaURasporedu, brojSatiUDanu)
		# dodavanje novo nastalog hromozoma u inicialnu populaciju
		hromozomi.append(hromozom)


	

	
	najboljiHromozomiInicialni = Hromozom.OdrediNajboljeHromozome(hromozomi, maxBrojNajboljihHromozoma)
	najboljiHromozomiIndeksi = []
	najboljiHromozomiDobrote = []
	for i in range(len(najboljiHromozomiInicialni)):
		najboljiHromozomiIndeksi.append(najboljiHromozomiInicialni[i][1])
		najboljiHromozomiDobrote.append(najboljiHromozomiInicialni[i][2])


	brojGeneracija = 0
	# Sada kada imamo inicialnu populaciju hromozoma i znamo koji su najbolji, mozemo zapoceti sa algoritmom
	while True:
		print("Trenutna generacija : {0}, najbolji hromozom: {1}".format(brojGeneracija, najboljiHromozomiDobrote[-1]))

		# Prvo ide provera da li smo dosli do kraja
		if najboljiHromozomiDobrote[-1] >= 1.0:
			break


		# ako nismo dosli do kraja onda idemo dalje
		# prvo pravimo decu
		for i in range(0, brojNovihHromozomaUSvakomKoraku):
			# Izaberemo nasumicno dva hromozoma
			hromozomRoditelj01 = hromozomi[najboljiHromozomiIndeksi[random.randint(0, maxBrojNajboljihHromozoma - 1)]]
			hromozomRoditelj02 = hromozomi[random.randint(0, brojHromozomaUPopulaciji - 1)]

			# Uradimo Crossover
			crossoverRezultat = hromozomRoditelj01.Crossover(hromozomRoditelj02, verovatnocaCrossover, brojCrossOverGranica, brojDanaURasporedu, brojSatiUDanu)
			crossoverRezultat.Mutacija(verovatnocaMutacija, brojPermutacijaUJednojMutaciji, brojDanaURasporedu, brojSatiUDanu)

			# Sada treba ubaciti novi hromozom u populaciju, ali ne smemo da zamenimo neki hromozom iz liste najboljiHromozomi
			while True:
				index = random.randint(0, brojHromozomaUPopulaciji - 1)
				if index not in najboljiHromozomiIndeksi: # ako nije u najboljim hromozomima
					# onda mozemo da ga zamenimo
					hromozomi[index] = crossoverRezultat
					# Probamo da ubacimo novi hromozom u listu najboljih
					for j in range(len(najboljiHromozomiDobrote))[::-1]:
						if crossoverRezultat.dobrota > najboljiHromozomiDobrote[j]:
							if (j + 1) > (len(najboljiHromozomiDobrote) - 1):
								najboljiHromozomiDobrote.append(crossoverRezultat.dobrota)
								najboljiHromozomiIndeksi.append(index)
							else:
								najboljiHromozomiDobrote.insert(j + 1, crossoverRezultat.dobrota)
								najboljiHromozomiIndeksi.insert(j + 1, index)
								
							najboljiHromozomiDobrote.pop(0)
							najboljiHromozomiIndeksi.pop(0)
							break

					break



		brojGeneracija = brojGeneracija + 1

	# Ako smo zavrsimo sa petljom znaci da imamo rezultat, samo ga jos treba i odstampati
	#print("Pronadjen je hromozom sa ")
	hromozomi[najboljiHromozomiIndeksi[-1]].Odstampaj(brojDanaURasporedu, brojSatiUDanu) 
