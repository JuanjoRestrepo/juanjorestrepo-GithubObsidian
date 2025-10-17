
El archivo `scrapers/utils.py` centraliza funciones **auxiliares** y **genéricas** que otros scripts (como `resolver.py`, `rappi_scraper.py`, `playwright_poc.py`) necesitan.  
Incluye utilidades para:

- Manejo de tiempo y retrasos aleatorios (anti-bloqueo de bots).
    
- Limpieza de cadenas numéricas (precios).
    
- Reintentos con backoff exponencial.
    
- Guardado de JSONs y logs.
    
- Capturas de pantalla seguras.
    

Estas funciones reducen duplicación

