# System Rezerwacji Wizyt w Przychodni

## Opis projektu
System Rezerwacji Wizyt w Przychodni to aplikacja webowa stworzona w Django, której celem jest usprawnienie zarządzania wizytami lekarskimi, kontami pacjentów i lekarzy oraz obsługą urlopów.  
Projekt umożliwia działanie trzem typom użytkowników: **pacjentom**, **lekarzom** i **administratorom**.

Aplikacja została zaprojektowana z myślą o prostocie obsługi, przejrzystym interfejsie oraz łatwości dalszego rozwoju. Projekt powstał w ramach praktyki nauki frameworka Django oraz tworzenia systemów zarządzania danymi w aplikacjach webowych.

## Wymagania
Przed uruchomieniem projektu należy upewnić się, że masz zainstalowane:
- **Python 3.10+**
- **PIP**
- **wirtualne środowisko (venv)**

## Uruchamianie projektu
1. **Sklonuj repozytorium:**
   ```bash
   git clone https://github.com/jwk99/rezerwacje.git
2. **Wejdź do katalogu projektu:**
   ```bash
   cd rezerwacje
3. **Utwórz środowisko wirtualne i je aktywuj:**
   ```bash
   python -m venv venv
   venv\Scripts\activate (dla Windows)
   source venv/bin/activate (dla Linux)
4. **Zainstaluj wymagania:**
   ```bash
   pip install -r requirements.txt
5. **Zastosuj migracje baz danych:**
   ```bash
   python manage.py migrate
7. **Uruchom serwer deweloperski:**
   ```bash
   python manage.py runserver
8. **Wejdź w przeglądarce na adres:**
- http://127.0.0.1:8000/accounts/login Do rozpoczęcia prac na projekcie.
- http://127.0.0.1:8000/admin By uzyskać dostęp do panelu administratora systemu.

8. **W razie problemów z uruchomieniem, użyć ponownie cd rezerwacje**
9. **W razie wystąpienia błędów z uruchamianiem skryptów z punktu 3.:**
Uruchom cmd.exe jako Administrator
   ```bash
   cd rezerwacje
   t.bat (jest to plik wsadowy zawierający polecenia dla cmd.exe pozwalający obejść brak uprawnień Administratora)

## Typy kont i funkcjonalności
### Lekarz
- Może przeglądać swoje wizyty.
- Może zgłaszać wnioski o urlop lub zwolnienie lekarskie (z możliwością dodania dokumentu).
- Może podejmować zastępstwa za innych lekarzy, jeśli nie ma konfliktu terminów.

### Pacjent
- Może rezerwować wizyty u lekarzy.
- Może przeglądać swoje rezerwacje.
- Może anulować lub zmieniać wizyty.

### Administrator
Ma dostęp do panelu administracyjnego z kilkoma widgetami:
- Grafik lekarzy – przegląd harmonogramów (w trakcie implementacji).
- Edytuj wizyty – przegląd i edycja wszystkich wizyt w systemie.
- Wnioski o wolne – zatwierdzanie lub odrzucanie wniosków urlopowych i zwolnień.
- Rejestracja wizyt – możliwość tworzenia nowych wizyt bezpośrednio z panelu.
- Dodawanie kont – tworzenie nowych kont lekarzy i pacjentów.

## Struktura interfejsu

Interfejs oparty jest o system widgetów, które dynamicznie przełączają widoki w obrębie jednej strony:
- Każdy moduł (grafik, wizyty, konta, wnioski) działa wewnątrz jednego panelu.
- Widoki ładują się asynchronicznie (AJAX), co poprawia responsywność i wygodę pracy.

## Aktualny stan projektu

- Rejestracja kont pacjentów i lekarzy
- Rejestracja wizyt
- Obsługa wniosków o wolne i zwolnień lekarskich
- Panel administratora
- Mechanizm zastępstw lekarzy
- W trakcie: integracja wniosków z blokadą rezerwacji
- W trakcie: widok grafiku lekarzy

## Planowane funkcje

- Statystyki i wykresy obłożenia lekarzy (dla admina)
- Pełny grafik lekarzy w widoku kalendarza
- System powiadomień e-mail
- Automatyczna blokada rezerwacji podczas zatwierdzonego urlopu
- Eksport danych (np. raport miesięczny wizyt)

## Autor

jwk99

## Licencja

Projekt udostępniony do celów edukacyjnych.
Użycie komercyjne lub modyfikacja wymaga zgody autora.

