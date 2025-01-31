from dynaconf import Dynaconf

settings = Dynaconf(
    settings_files=['settings.json', '.secrets.json'],
    envvar_prefix="MSVC",
    load_dotenv=True
)