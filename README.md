# Epidemimodellering-stokastisk

Detta projekt studerar smittspridningsdynamik med hjälp av deterministiska och stokastiska modeller (Gillespies algoritm / SSA). Projektet utgår från grundläggande SIR-modeller och vidareutvecklas till en utökad SEIRDVM-modell baserad på Folkhälsomyndighetens modellering för covid-19.

## Projektbeskrivning
Syftet är att analysera hur smitta, inkubationstid, dödlighet, vaccination och mörkertal samverkar i en avgränsad population (t.ex. Ångströmlaboratoriet i Uppsala, N=1000).

## Innehållande modeller:
1. SIR: Standardmodell för mottagliga, infekterade och tillfrisknade (S, I, R).
2. SEIR: Lägger till inkubationstid (E).
3. SEIRD: Lägger till dödlighet (D).
4. SEIRDV: Lägger till kontinuerlig vaccinationshastighet (V).
5. SEIRDVM (Egen modell): Utökad modell med mörkertal (M), där både kända och okända fall bidrar till smittspridningen i samhället.

## Filstruktur
* `SIR_modell.py` - Innehåller startvärden, parametervektorer, stoikiomatriser och propensitetsfunktioner för de olika modellerna.
* `gillespie.py` – Implementerar Gillespies algoritm (SSA) och plottar stokastiska trajektorier över tid.

