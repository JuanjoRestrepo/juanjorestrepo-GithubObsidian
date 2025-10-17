



```python
user_search = (entry.get("searchQuery") or "").strip()
if user_search and ("mcdonald" in user_search.lower()):
    heuristic_query = user_search
else:
    base = user_search if user_search else addr_label
    heuristic_query = f"McDonald's {base}".strip()

```


🔸 **En resumen:**

|Tipo|Qué es|Cómo se usa en el scraper|
|---|---|---|
|**DOM**|Estructura visible de la página|Se usa para leer precios y textos con `page.inner_text()`|
|**XHR / Fetch**|Peticiones en segundo plano (JSON)|Se interceptan con `page.on("response")` para obtener delivery/service fees|
|**NEXT_DATA**|Objeto JSON embebido en el HTML|Se evalúa directamente con `page.evaluate()` para extraer datos internos|



Explicación paso a paso:

1. **Lee la query del CSV:**
    
    - `entry.get("searchQuery")` puede venir del campo `searchQuery` o ser vacío.
        
    - Ejemplo: `"Polanco, CDMX"` o `"McDonald's Polanco"`.
        
2. **Caso 1:** si la query del usuario **ya menciona "mcdonald"**,  
    entonces no se altera:
    
```python
heuristic_query = "McDonald's Polanco"
```
    
	Porque ya es suficientemente específica.
    
3. **Caso 2:** si **no menciona "mcdonald"**,  
    el código **la enriquece automáticamente** para guiar la búsqueda:
    
```python
heuristic_query = f"McDonald's {base}"
```

    
    donde `base` es la dirección o barrio (`addr_label`).

Ejemplo:

- addressLabel = "Condesa"
- searchQuery = ""  
	👉 Resultado: `"McDonald's Condesa"`