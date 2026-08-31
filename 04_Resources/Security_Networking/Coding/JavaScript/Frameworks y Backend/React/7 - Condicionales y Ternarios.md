---
title: "7 - Condicionales y Ternarios"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

# OPERADOR TERNARIO
Un operador ternario en React (o en cualquier código JavaScript) es una forma concisa de realizar una operación condicional. Se utiliza para evaluar una expresión y devolver un valor basado en esa evaluación. La sintaxis básica del operador ternario es:
```javascript
condición ? expresiónSiVerdadera : expresiónSiFalsa
```
Por ejemplo vamos a tener el siguiente código, donde vamos a evaluar si una variable es true o false:
![[Pasted image 20240712164431.png]]
```javascript
const Items = ({ nombre, visto }) => {
    return (
        <li>{nombre} {visto ? '✅' : '❌'}</li> // Operador ternario
    )
}

export const ListadoApp = () => {
    return (
        <>
            <div>ListadoApp</div>
            <ol>
                <Items nombre="Instalación básica" visto={true} />
                <Items nombre="Uso de Vite" visto={true} />
                <Items nombre="Componentes" visto={true} />
                <Items nombre="Variables" visto={true} />
                <Items nombre="Props" visto={true} />
                <Items nombre="Eventos" visto={true} />
                <Items nombre="useState" visto={false} />
                <Items nombre="Redux" visto={false} />
            </ol>
        </>
    )
}
```
De esta forma, si visto es true, se va a imprimir el tick verde, y si no lo es, se imprimirá la X:
![[Pasted image 20240712164405.png]]
Aunque también podemos hacer que en caso de que se cumpla la condición, que ejecute el tick verde, pero si no, que no haga nada y salga del condicional:
```javascript
const Items = ({ nombre, visto }) => {
    return (
        <li>{nombre} {visto && '✅'}</li> // Operador ternario
    )
}

export const ListadoApp = () => {
    return (
        <>
            <div>ListadoApp</div>
            <ol>
                <Items nombre="Instalación básica" visto={true} />
                <Items nombre="Uso de Vite" visto={true} />
                <Items nombre="Componentes" visto={true} />
                <Items nombre="Variables" visto={true} />
                <Items nombre="Props" visto={true} />
                <Items nombre="Eventos" visto={true} />
                <Items nombre="useState" visto={false} />
                <Items nombre="Redux" visto={false} />
            </ol>
        </>
    )
}
```
![[Pasted image 20240712164535.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
