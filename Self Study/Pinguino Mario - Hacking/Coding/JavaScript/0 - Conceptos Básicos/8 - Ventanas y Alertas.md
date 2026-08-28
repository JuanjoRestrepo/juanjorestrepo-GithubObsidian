---
title: "8 - Ventanas y Alertas"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

En JavaScript, puedes usar ventanas y alertas para interactuar con los usuarios y mostrar información. Aquí hay un resumen de las funciones más comunes que puedes utilizar:
**Alert**
```javascript
let mensaje = 'Soy una ventana'

alert(mensaje);
```
![[Pasted image 20241014121700.png]]
**Confirm**
La función confirm() muestra un cuadro de diálogo con un mensaje y dos botones: "Aceptar" y "Cancelar". Devuelve true si el usuario hace clic en "Aceptar" y false si hace clic en "Cancelar".
```javascript
let resultado = confirm("¿Estás seguro de que deseas continuar?");
if (resultado) {
    alert("Has hecho clic en Aceptar.");
} else {
    alert("Has hecho clic en Cancelar.");
}
```
![[Pasted image 20241014121748.png]]
**Prompt**
La función prompt() muestra un cuadro de diálogo que solicita al usuario que ingrese información. Devuelve el valor ingresado como una cadena, o null si el usuario hace clic en "Cancelar".
```javascript
let nombre = prompt("Por favor, introduce tu nombre:");
if (nombre) {
    alert("Hola, " + nombre + "!");
} else {
    alert("No se ingresó ningún nombre.");
}
```
![[Pasted image 20241014121849.png]]
Y si ponemos un dato, se imprime en la propia ventana:
![[Pasted image 20241014121904.png]]
**Ventanas Personalizadas**
Además de las alertas estándar, puedes crear ventanas emergentes personalizadas utilizando la función window.open(). Esto te permite abrir una nueva ventana del navegador.
```javascript
let nuevaVentana = window.open("https://www.ejemplo.com", "Ejemplo", "width=600,height=400");
```
![[Pasted image 20241014122030.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
