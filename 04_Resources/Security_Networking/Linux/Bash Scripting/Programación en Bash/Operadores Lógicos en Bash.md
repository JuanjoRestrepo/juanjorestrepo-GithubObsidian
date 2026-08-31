---
title: "Operadores Lógicos en Bash"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

### MAYOR, IGUAL O MENOR QUE OTRO DATO
Vamos a ver el funcionamiento de los indicadores de igual, mayor o menor que otro dato en bash:
```bash
# Comparación de números enteros
a=5
b=3

if [ $a -gt $b ]; then # INDICADOR MAYOR QUE
  echo "$a es mayor que $b"
fi

if [ $a -eq $b ]; then #INDICADOR IGUAL QUE
  echo "$a es igual a $b"
else
  echo "$a no es igual a $b"
fi

if [ $a -lt $b ]; then # INDICADOR MENOR QUE
  echo "$a es menor que $b"
else
  echo "$a no es menor que $b"
fi
```
### OPERADOR LÓGICO OR
Para validar si se cumple una condición o también puede cumplirse la otra, por ejemplo para comprobar si existe un determinado archivo o no:
```bash
# Verificamos si un archivo existe o no
if [ -f archivo1.txt ] || [ -f archivo2.txt ]; then
  echo "Al menos uno de los archivos existe"
else
  echo "Ninguno de los archivos existe"
fi
```

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
