import gettext
import json
import locale
from pathlib import Path

from babel.messages.pofile import read_po
from babel.messages.mofile import write_mo

DEFAULT_LOCALE = "en_US"
SYSTEM_LOCALE = locale.getdefaultlocale()[0]
TRANSLATIONS = {}

with open("locales.json", encoding="utf-8") as file:
    LOCALES = json.load(file)

for locale_ in LOCALES:
    if locale_ == DEFAULT_LOCALE:
        TRANSLATIONS[locale_] = gettext.NullTranslations()
        continue

    path = Path("locales") / locale_ / "LC_MESSAGES"
    with (path / "messages.po").open(encoding="utf-8") as file:
        catalog = read_po(file, ignore_obsolete=True)
    with (path / "messages.mo").open("wb") as file:
        write_mo(file, catalog)
    TRANSLATIONS[locale_] = gettext.translation("messages", "locales", [locale_])
