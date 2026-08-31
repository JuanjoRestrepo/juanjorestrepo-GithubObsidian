---
title: "Librería Pyautogui"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Para controlar acciones del ordenador, por ejemplo para copiar y pegar cosas, donde vamos a automatizar la comprobación de muchos correos dentro de la web de haveibeenpwned:
```python
import webbrowser
import time
import pyperclip
import pyautogui
 

documento = open('escribir_correos.txt','r')
documento = documento.read().split('\n')

# Ahora aquí ordenamos que se escriba con el teclado:

for email in documento:

    webbrowser.open_new("https://haveibeenpwned.com/")
    time.sleep(3)
    pyperclip.copy(email) # Copiamos en portapapeles los email.
    pyautogui.hotkey('ctrl', 'v', interval = 0.15) # Los pegamos en la web.
    pyautogui.press("enter")
```
Y se abre una por una en pestañas distintas:
![[Pasted image 20230108141815.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
