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
  - Sklonuj repozytorium:

  - Wejdź do katalogu projektu:

  - Utwórz środowisko wirtualne i je aktywuj:

  - Zainstaluj wymagania:

  - Zastosuj migracje baz danych:

  - Uruchom serwer deweloperski:

  - Wejdź w przeglądarce na adres:

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

