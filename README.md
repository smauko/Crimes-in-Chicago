# Crimes in Chicago
Izrada baze podataka i skladista podatka o zločinima u Chicago-u uz primjenu CDC tehnike za inkrementalno punjenje

## Korištenje
1. U Python folderu nalazi se skripta 'Ucitavanje podataka u bazu', nju otvorite u editoru za Python i prilagodite MySQL podatke za konekciju.
2. U MySQL folderu skriptu Baza podataka izvršite samo do UPDATE dijela.
3. Pokrenite Python skriptu.
4. Nakon toga izvršite skriptu Skladište podataka.
5. Odradite sve transformacije u Pentaho folderu (naravno sa vašim podacima za MySQL konekciju)
6. Odradite prva 2 UPDATE-a u skripti Baza podataka.
7. Opet odradite sve transformacije.
8. Odradite zadnji UPDATE.
9. Opet pokrenite sve transformacije kako biste ažurirali skladište podataka s finalnim promjenama.

## Napomene:
Provjerite da su sve konekcije ispravno podešene (npr. korisničko ime, lozinka i naziv baze podataka).
Redoslijed koraka je ključan kako bi se osigurala točnost inkrementalnog punjenja i povijesnog praćenja podataka.
Ako koristite Pentaho, provjerite da su sve transformacije uspješno izvršene bez pogrešaka.

    
