---
title: "Librería Keyboard"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Sirve para registrar las pulsaciones de teclas de mi teclado:
```python
import keyboard

def on_key_event(e):
    print(f'Tecla presionada: {e.name}') # Imprimimos la tecla presionada

# Registrar la función de devolución de llamada
keyboard.on_press(on_key_event)

# Mantener el programa en ejecución
keyboard.wait('esc')
```
![[Pasted image 20231216103220.png]]
Esto se puede utilizar para recoger palabras enteras, por ejemplo de la siguiente forma:
```python
import keyboard

current_word = ""

def on_key_event(e):
    global current_word

    if e.event_type == keyboard.KEY_DOWN:
        if e.name == 'space':
            print(f'Palabra ingresada: {current_word}')
            current_word = ""
        else:
            current_word += e.name

# Registrar la función de devolución de llamada
keyboard.hook(on_key_event)

# Mantener el programa en ejecución
keyboard.wait('esc')
```

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
