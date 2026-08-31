---
title: "0 - Primeros Pasos con React"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Lo primero será crear el proyecto ejecutando el siguiente comando:
```javascript
npm create vite
```
Y se nos habrá creado el proyecto:
![[Pasted image 20240707201514.png]]
Nos ubicamos dentro y ejecutamos los siguientes comandos:
```javascript
cd react-app  
npm install  
npm run dev
```
Una vez hecho todo lo anterior ya tendremos react funcionando:
![[Pasted image 20240707201944.png]]
![[Pasted image 20240707202003.png]]
Nos habrá generado la siguiente estructura, donde en el directorio public se pondrán los archivos que queramos que los usuarios puedan descargar, y en src es donde haremos nuestro proyecto:
![[Pasted image 20240707202154.png]]
### INSTALAR BOOTSTRAP
Lo instalamos de esta forma:
```bash
npm i bootstrap@5.3.3
```
![[Pasted image 20240707204559.png]]
Ahora que hemos instalado bootstrap, podremos eliminar el contenido del index.css y App.css:
![[Pasted image 20240707204659.png]]
Y podremos eliminar también la siguiente línea:
![[Pasted image 20240707204809.png]]
Y en su lugar podemos cargar bootstrap:
![[Pasted image 20240707204912.png]]
### Explicación Archivos del Proyecto

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
