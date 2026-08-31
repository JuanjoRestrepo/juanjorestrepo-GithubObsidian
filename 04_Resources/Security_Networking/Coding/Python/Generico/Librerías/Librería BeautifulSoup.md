---
title: "Librería BeautifulSoup"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

```python
from bs4 import BeautifulSoup

# HTML de ejemplo
html_content = '''
<html>
<head><title>Ejemplo</title></head>
<body>
<div class="content">Contenido 1</div>
<div class="content">Contenido 2</div>
<div class="footer">Pie de página</div>
</body>
</html>
'''

# Crear el objeto BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Encontrar todos los elementos con la clase 'content'
content_divs = soup.find_all('div', class_='content')

# Imprimir el texto de cada elemento
for div in content_divs:
    print(div.text)
```
![[Pasted image 20240609123141.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
