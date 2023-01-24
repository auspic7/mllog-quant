APP_KEY = "PSD3fjNAsCVyUkLcMpeecb1MUscrbC0EFO9j"
APP_SECRET = "G+lUkQtueAT4oiUdBoUvvNSWZP1ZwYZVzlv52AUFZq9k41N6gTNvl6m/guDJqD8T1X8BYkXPa112hj10AmAntbDENthu3xu6cNY3DjoODTwpYp0+4ZPm4BU+rPwhzDA+d57+qmi/K9PXgrcvRhP8krU9ADWFZuljcZGL5wpcA7L/5foeaLI="

VIRTUAL = True

if VIRTUAL:
    URL_BASE = "https://openapivts.koreainvestment.com:29443" #모의투자서비스
    CANO = "50077658"
    ACNT_PRDT_CD = "01"
else:
    URL_BASE = "https://openapi.koreainvestment.com:9443"
