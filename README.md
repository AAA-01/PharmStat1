# PharmStat1

Instrukcja Obsługi Użytkownika Aplikacji Santo Pharmstat


**1. Wprowadzenie**
   
1.1 Cel aplikacji

Aplikacja Santo Pharmstat została zaprojektowana w celu ułatwienia analizy danych statystycznych i jakościowych w branży farmaceutycznej. Umożliwia szybkie i intuicyjne przetwarzanie informacji oraz generowanie czytelnych wyników w postaci wykresów, tabel i wskaźników statystycznych.

1.2 Kluczowe funkcje

Obsługa wielu języków: Polski, angielski i rosyjski interfejs użytkownika.
Modułowa analiza danych: Statystyki opisowe, histogramy, wykresy BoxPlot, karty kontrolne ImR, analiza zdolności procesowej, regresja dla stabilności oraz analiza temperatury i wilgotności.
Wygodne zarządzanie danymi: Łatwe wczytywanie plików Excel i przeglądanie wyników w czasie rzeczywistym.
Bezpieczne przechowywanie danych: Brak potrzeby instalacji – dane przetwarzane są w chmurze.

1.3 Wymagania systemowe

Aplikacja Santo Pharmstat działa w całości przez przeglądarkę internetową i nie wymaga instalacji lokalnej. Użytkownicy muszą mieć dostęp do internetu oraz aktualnej wersji przeglądarki wspierającej nowoczesne technologie webowe (np. Google Chrome, Mozilla Firefox, Microsoft Edge).

**2. Dostęp do aplikacji**
   
2.1 Jak uruchomić aplikację

Aplikacja Santo Pharmstat jest hostowana na platformie Streamlit i dostępna pod adresem:
https://santo-pharmstat1.streamlit.app/
Aby uruchomić aplikację:
Otwórz preferowaną przeglądarkę internetową.
Wprowadź adres https://santo-pharmstat1.streamlit.app/ w pasku adresu.
Naciśnij Enter, aby załadować aplikację.
Po załadowaniu aplikacji wybierz preferowany język z rozwijanego menu po lewej stronie.

2.2 Wymagania dotyczące przeglądarki internetowej

Aby zapewnić prawidłowe działanie aplikacji, zaleca się korzystanie z najnowszych wersji przeglądarek:
Google Chrome (zalecane)
Mozilla Firefox
Microsoft Edge
Safari (na systemach macOS)
Minimalne wymagania:
Obsługa JavaScript.
Wsparcie dla HTML5 i CSS3.
Stabilne połączenie internetowe o przepustowości co najmniej 1 Mbps.
Problemy z kompatybilnością: Starsze wersje przeglądarek mogą nie wspierać wszystkich funkcji aplikacji, co może prowadzić do nieprawidłowego wyświetlania elementów lub błędów wczytywania danych.

**3. Nawigacja po interfejsie**

3.1 Wybór języka

Po uruchomieniu aplikacji Santo Pharmstat pierwszym krokiem jest wybór języka interfejsu. W lewym panelu bocznym znajduje się rozwijane menu umożliwiające wybór spośród trzech dostępnych języków:
Polski
English (Angielski)
Русский (Rosyjski)
Wybór języka automatycznie dostosowuje cały interfejs aplikacji do wybranego tłumaczenia.

3.2 Menu główne i podstrony

Po wybraniu języka użytkownik może poruszać się po aplikacji za pomocą menu bocznego, które zawiera listę dostępnych modułów analizy danych:
Statystyki opisowe
Histogramy
Wykresy BoxPlot
Karty kontrolne ImR
Analiza zdolności procesowej
Regresja dla stabilności
Analiza temperatury i wilgotności
Kliknięcie w nazwę modułu przekierowuje do odpowiedniej podstrony, gdzie można wczytać dane i przeprowadzić analizę.

3.3 Wczytywanie danych

Aplikacja umożliwia wczytywanie danych w formacie Excel (.xlsx, .xls). Proces wczytywania danych jest podobny w każdym z modułów:
Wybierz plik: Kliknij przycisk „Wybierz plik Excel”, aby otworzyć okno dialogowe i wskazać plik z danymi.
Podgląd danych: Po wczytaniu pliku aplikacja wyświetli podgląd pierwszych kilku wierszy danych, aby umożliwić szybkie sprawdzenie poprawności.
Wybór kolumn do analizy: W niektórych modułach możesz wskazać konkretne kolumny, które chcesz analizować.
Analiza: Po wczytaniu i skonfigurowaniu danych aplikacja automatycznie wygeneruje wyniki analizy, które będą widoczne w głównym obszarze strony.
W przypadku błędów w formacie pliku lub danych, aplikacja wyświetli stosowny komunikat z informacjami o problemie.

**4. Opis modułów aplikacji**

4.1 Statystyki opisowe
Moduł Statystyki opisowe umożliwia szybkie obliczanie podstawowych miar statystycznych, takich jak średnia, mediana, odchylenie standardowe, minimum i maksimum. Narzędzie to jest przydatne do wstępnej analizy danych i identyfikacji podstawowych trendów.
Jak korzystać z modułu:
Wczytaj plik Excel zawierający dane pomiarowe.
Wybierz kolumny, dla których chcesz obliczyć statystyki opisowe.
Wyniki zostaną wyświetlone w formie tabeli, zawierającej kluczowe miary statystyczne.
Funkcje dodatkowe:
Ocena normalności rozkładu za pomocą testu Shapiro-Wilka.
Obliczanie wskaźników skośności i kurtozy.
Moduł umożliwia szybką ocenę jakości danych przed przejściem do bardziej zaawansowanych analiz.

4.2 Histogramy
Moduł Histogramy umożliwia wizualizację rozkładu danych oraz ocenę ich zgodności z rozkładem normalnym. Histogramy są przydatne do identyfikacji wzorców w danych, takich jak asymetria lub obecność wartości odstających.
Jak korzystać z modułu:
Wczytaj plik Excel zawierający dane pomiarowe.
Wybierz kolumnę do analizy, z której chcesz wygenerować histogram.
Histogram zostanie wygenerowany automatycznie wraz z oceną normalności rozkładu.
Funkcje dodatkowe:
Wyświetlanie statystyk opisowych dla wybranej kolumny.
Obliczanie wskaźników skośności i kurtozy.
Test Shapiro-Wilka do oceny normalności rozkładu.
Moduł pozwala na szybką i intuicyjną analizę wizualną danych, co ułatwia identyfikację nieprawidłowości przed przeprowadzeniem bardziej zaawansowanych analiz.

4.3 Wykresy BoxPlot
Moduł Wykresy BoxPlot służy do wizualizacji rozkładu danych oraz identyfikacji wartości odstających. Wykresy pudełkowe (BoxPlot) pozwalają na szybkie porównanie rozkładów różnych zestawów danych.
Jak korzystać z modułu:
Wczytaj plik Excel zawierający dane pomiarowe.
Wybierz kolumny do analizy, z których chcesz wygenerować wykresy BoxPlot.
Wykresy zostaną wygenerowane automatycznie, pokazując medianę, kwartyle oraz wartości odstające.
Funkcje dodatkowe:
Wyświetlanie statystyk opisowych dla wybranych kolumn.
Możliwość porównania rozkładów dla wielu zmiennych jednocześnie.
Moduł ułatwia identyfikację nieprawidłowości w danych, takich jak wartości skrajne lub nietypowe rozkłady.

4.4 Karty Kontrolne ImR
Moduł Karty Kontrolne ImR umożliwia monitorowanie stabilności procesów poprzez analizę wartości indywidualnych (I) i ruchomego rozstępu (MR). Karty kontrolne są narzędziem stosowanym w statystycznej kontroli procesów (SPC).
Jak korzystać z modułu:
Wczytaj plik Excel zawierający dane pomiarowe.
Plik powinien zawierać dwie kolumny: identyfikator próbki (czas/ID) oraz wartości pomiarowe.
Wykresy zostaną wygenerowane automatycznie, pokazując wartości indywidualne oraz ruchomy rozstęp.
Funkcje dodatkowe:
Ocena normalności rozkładu za pomocą testu Shapiro-Wilka.
Identyfikacja punktów poza granicami kontrolnymi.
Ocena stabilności procesu na podstawie reguł Shewharta.
Moduł pozwala na bieżące monitorowanie jakości procesów produkcyjnych i szybką identyfikację potencjalnych problemów.

4.5 Analiza Zdolności Procesowej
Moduł Analiza Zdolności Procesowej pozwala na ocenę, na ile proces produkcyjny jest w stanie spełniać określone wymagania specyfikacyjne. Wskaźniki Cp i Cpk pomagają określić zdolność procesu do utrzymania jakości.
Jak korzystać z modułu:
Wczytaj plik Excel zawierający dane pomiarowe.
Ustaw dolną (LSL) i górną (USL) granicę specyfikacji oraz wartość docelową (Target).
Wykres analizy zdolności procesowej oraz wskaźniki Cp i Cpk zostaną wygenerowane automatycznie.
Funkcje dodatkowe:
Obliczanie wskaźników Cp i Cpk.
Wizualizacja danych z oznaczeniem granic specyfikacji.
Przegląd szczegółowych statystyk, takich jak średnia, odchylenie standardowe i mediana.
Moduł umożliwia identyfikację problemów związanych z jakością oraz ocenę, czy proces produkcyjny jest zgodny z wymaganiami.

4.6 Regresja dla Stabilności
Moduł Regresja dla Stabilności umożliwia analizę trendów w danych stabilnościowych za pomocą regresji liniowej. Pomaga to ocenić trwałość i stabilność produktów w czasie.
Jak korzystać z modułu:
Wczytaj plik Excel zawierający dane stabilności.
Wybierz serie do analizy, które chcesz wyświetlić na wykresie.
Wykres z liniami regresji oraz tabela z parametrami regresji zostaną wygenerowane automatycznie.
Funkcje dodatkowe:
Wyświetlanie współczynnika korelacji (r), nachylenia i wyrazu wolnego.
Oznaczanie granic specyfikacji na wykresie.
Przeglądanie szczegółowych wyników analizy regresji.
Moduł wspiera analizę danych stabilnościowych, pozwalając na ocenę długoterminowej jakości produktów.

4.7 Analiza Temperatury i Wilgotności
Moduł Analiza Temperatury i Wilgotności umożliwia monitorowanie danych środowiskowych, takich jak temperatura i wilgotność, oraz identyfikację przekroczeń ustalonych limitów.
Jak korzystać z modułu:
Wczytaj plik Excel zawierający dane temperatury i wilgotności.
Ustaw limity temperatury i wilgotności za pomocą suwaków.
Wykresy temperatury i wilgotności wraz z oznaczeniem przekroczeń limitów zostaną wygenerowane automatycznie.
Funkcje dodatkowe:
Obliczanie podstawowych statystyk, takich jak średnia, minimum, maksimum i współczynnik zmienności (RSD).
Identyfikacja momentów przekroczenia limitów oraz ich wizualizacja na wykresie.
Możliwość dostosowania zakresów granicznych według potrzeb użytkownika.
Moduł pozwala na bieżącą kontrolę warunków środowiskowych, co jest kluczowe w procesach wymagających utrzymania stałych parametrów otoczenia.

**5 Najczęściej Zadawane Pytania (FAQ)**
W tej sekcji znajdziesz odpowiedzi na najczęściej pojawiające się pytania dotyczące korzystania z aplikacji Santo Pharmstat.

5.1 Jakie formaty plików są obsługiwane przez aplikację?
Aplikacja obsługuje pliki w formatach Excel: .xlsx oraz .xls. Upewnij się, że dane w plikach są prawidłowo sformatowane i zgodne z wymaganiami poszczególnych modułów.

5.2 Co zrobić, jeśli pojawia się błąd podczas wczytywania pliku?
Sprawdź, czy plik jest w odpowiednim formacie.
Upewnij się, że plik nie jest uszkodzony.
Zweryfikuj, czy dane w pliku są zgodne z wymaganym układem kolumn.

5.3 Jak zmienić język aplikacji?
W aplikacji dostępne są trzy języki: polski, angielski i rosyjski. Możesz zmienić język w ustawieniach aplikacji lub na stronie głównej.

5.4 Czy mogę eksportować wyniki analizy?
Tak, wyniki analiz (wykresy, tabele) można pobrać bezpośrednio z aplikacji w formatach graficznych lub arkuszach kalkulacyjnych.

5.5 Jakie są minimalne wymagania systemowe do korzystania z aplikacji?
Aplikacja działa w przeglądarkach internetowych takich jak Google Chrome, Mozilla Firefox czy Microsoft Edge. Wymagane jest połączenie z internetem.

5.6 Co zrobić, jeśli aplikacja nie działa prawidłowo?
Odśwież stronę przeglądarki.
Sprawdź połączenie internetowe.
Skontaktuj się z administratorem aplikacji, jeśli problem będzie się powtarzał.
W przypadku dodatkowych pytań lub problemów skontaktuj się z działem wsparcia technicznego.

#   P h a r m S t a t 1  
 