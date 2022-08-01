[![python_test](https://github.com/vil02/pi2022/actions/workflows/python_test.yml/badge.svg)](https://github.com/vil02/pi2022/actions/workflows/python_test.yml)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=vil02_pi2022&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=vil02_pi2022)
[![CodeFactor](https://www.codefactor.io/repository/github/vil02/pi2022/badge)](https://www.codefactor.io/repository/github/vil02/pi2022)

Materiały do referatu _Problemy optymalizacyjne i symulowane wyżarzanie_ wygłoszonego podczas [XVI Święta Liczby &pi;](https://us.edu.pl/wydzial/wnst/wspolpraca/szkoly/swieto-liczby-pi/).
Prezentacja jest dostępna [tutaj](./generated/pi2022.pdf) ([pobierz](https://raw.githubusercontent.com/vil02/pi2022/master/generated/pi2022.pdf)).

Folder [`python`](./python) zawiera skrypty użyte do wygenerowania animacji oraz grafik użytych w prezentacji.
[`build_document.sh`](build_document.sh) _buduje_ cały dokument (zob. [`build_document.yml`](.github/workflows/build_document.yml)).

Animacje są utworzone w oparciu o pakiet [`animate`](https://ctan.org/pkg/animate).
W celu ich poprawnego wyświetlania [plik pdf z prezentacją](./generated/pi2022.pdf) musi być otworzony przez [jeden ze wspieranych programów](https://gitlab.com/agrahn/animate#requirements).
