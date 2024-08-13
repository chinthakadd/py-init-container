from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="_INIT_",
    settings_files=['settings.toml', '.secrets.toml'],
)
 
# `envvar_prefix` = export envvars with `export _INIT_FOO=bar`.
# `settings_files` = Load these files in the order.
# print(settings.mongo_url)