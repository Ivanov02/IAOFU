**IAOFU - Data Mining with Riot Games API** <br />
Acest proiect extrage date din API-ul Riot Games și le salvează pentru analiză. Mai jos sunt pașii necesari pentru a configura și rula proiectul.

**Setare Git**
Urmează acest ghid pentru a conecta GitHub cu PyCharm, dacă este necesar: https://www.jetbrains.com/help/pycharm/github.html#register-existing-account

**Instalarea pachetelor necesare** <br />
Deschide linia de comandă ca administrator și rulează comanda:

python -m pip install requests

**Ascunderea cheii API:** <br />
Creează un fișier numit api_connection.py și adaugă următoarea linie pentru a stoca cheia API:

api_key = "your_key"

Acest lucru asigură că cheia ta API este protejată și nu este expusă într-un repository public.

**Cum se mineaza datele:** <br />
Pas 1: 
În fișierul main.py pune codul intr-o bucla while True cu sleep de 120 secunde

Pas 2:
Comentează funcția user_inputs() și introduce valori fixe în locul ei:

user_name = "Vonavi" <br />
user_tag_name = "EUNE" <br />
number_of_matches = 10 <br />

Pas 3: 
Rulând scriptul modificat, acesta va prelua continuu date despre meciuri, care vor fi salvate în fișierul output.csv.
