import pandas as pd
from unidecode import unidecode


def limpiar_texto(valor):
    """Normaliza y limpia cadenas de texto."""
    if valor is None or pd.isnull(valor):
        return ""
    return unidecode(str(valor).strip()).lower()
