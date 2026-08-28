---
title: "Modelo TCP-IP"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

El modelo TCP/IP significa Protocolo de Control de Transmisión/Protocolo de Internet, es un conjunto de protocolos de red que se utiliza para la comunicación en Internet y en redes similares. Se trata del estándar para la comunicación en red. El modelo TCP/IP consta de cuatro capas principales, que son:

1. **Capa de red** Esta capa se encarga de enviar los paquetes de datos a través de la red. El protocolo principal utilizado en esta capa es el Protocolo de Internet (IP), que se encarga de enrutar los datos de manera eficiente a través de la red.

Protocolos que funcionan en esta capa --> IP, ICMP, ARP, OSPF, BGP o RIP.

2. **Capa de transporte:** Esta capa se encarga de proporcionar un transporte confiable de datos entre los dispositivos finales. Los protocolos más comunes utilizados en esta capa son el Protocolo de Control de Transmisión (TCP), que garantiza la entrega de los datos de manera ordenada y confiable, y el Protocolo de Datagramas de Usuario (UDP), que se utiliza para aplicaciones que requieren una entrega rápida pero no necesariamente fiable de los datos.

Protocolos que funcionan en esta capa --> TCP y UDP.

3. **Capa de aplicación:** Esta es la capa más cercana al usuario y se utiliza para soportar aplicaciones de red. Incluye una variedad de protocolos que permiten funciones como el correo electrónico (SMTP), la transferencia de archivos (FTP), la resolución de nombres de dominio (DNS), y la navegación web (HTTP).

Protocolos que funcionan en esta capa --> HTTP, FTP, SMTP, DNS, SNMP, Telnet, SSH, DHCP.

4. **Capa de enlace de datos** Se encarga de proporcionar un enlace de datos fiable y eficiente a través de un medio de comunicación físico entre dos dispositivos de red adyacentes. 

Protocolos que funcionan en esta capa --> Ethernet, ARP, PPP, Wi-Fi.

5.  **Capa física** Se encarga de la transmisión física de bits a través de un medio de comunicación de red. La función principal de la capa física es proporcionar un medio de transmisión para la transferencia de bits entre dispositivos conectados a la red.

Protocolos que funcionan en esta capa --> Ethernet, Wi-Fi, DSL o SDSL.

El modelo TCP/IP es una parte fundamental de la infraestructura de Internet y ha permitido el desarrollo de una amplia gama de aplicaciones y servicios en línea. Aunque otros modelos de red, como el modelo OSI (Interconexión de Sistemas Abiertos), también son populares, el modelo TCP/IP sigue siendo el más ampliamente utilizado en la actualidad.

## Corrección conceptual: TCP/IP no tiene cinco capas

La explicación anterior mezcla el modelo TCP/IP con el modelo OSI. En su formulación habitual, TCP/IP tiene **cuatro capas**: aplicación, transporte, internet y acceso a red/enlace. La capa física y la de enlace se separan en el modelo OSI; en TCP/IP suelen agruparse en acceso a red. Además, ARP se ubica normalmente en el límite entre enlace e internet según la implementación, por lo que no conviene tratarlo como un protocolo de enrutamiento IP.

| TCP/IP | Relación aproximada con OSI | Responsabilidad | Ejemplos |
| --- | --- | --- | --- |
| Aplicación | Aplicación, presentación y sesión | Protocolo que usa la aplicación | HTTP(S), DNS, SMTP, SSH |
| Transporte | Transporte | Comunicación extremo a extremo y puertos | TCP, UDP, QUIC |
| Internet | Red | Direccionamiento y encaminamiento entre redes | IPv4/IPv6, ICMP |
| Acceso a red | Enlace y física | Tramas y transmisión en el medio local | Ethernet, Wi-Fi, PPP |

### Implicación para diagnóstico y defensa

1. Delimita primero el síntoma: resolución de nombre (DNS), conexión/puerto (TCP/UDP), ruta IP o enlace local.
2. No infieras seguridad por capa: TLS protege una sesión de aplicación sobre transporte, pero no sustituye autenticación, autorización ni validación de entrada.
3. Documenta IP origen/destino, puerto, protocolo, hora y alcance autorizado antes de capturar o analizar tráfico.

Esta separación permite relacionar esta nota con [[Modelo OSI]] sin confundir abstracciones. Para contenedores y clústeres, los mismos principios explican por qué los Pods son efímeros y los Services aportan una abstracción de red estable. [Kubernetes: Services](https://kubernetes.io/docs/concepts/services-networking/service/)

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
