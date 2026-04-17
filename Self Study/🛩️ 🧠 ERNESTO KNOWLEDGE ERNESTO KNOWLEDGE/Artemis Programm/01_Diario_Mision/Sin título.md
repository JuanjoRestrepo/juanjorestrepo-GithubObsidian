---
title: "Bitácora Artemis II: De la Tierra a la Luna y el Regreso"
date: 2026-04-14
tags:
  - artemis
  - espacio
  - GNC
  - reentrada
  - telemetria
  - diario
  - Space
  - NASA
status: completado
---

# Diario de Misión: Artemis II (Cápsula "Integrity")

> [!info] Metadatos de la Misión
> **Tripulación:** Reid Wiseman (Comandante), Victor Glover (Piloto), Christina Koch (Misión), Jeremy Hansen (CSA).
> **Infraestructura:** Cápsula Orion + Módulo de Servicio Europeo (ESM).
> **Duración Total:** 10 días.
> **Récord Establecido:** Distancia máxima de 252,756 millas de la Tierra (Superando al Apolo 13).

## 1. Reflexión Personal
*(Escribe aquí tus impresiones. Ejemplo: El amerizaje de la cápsula Orion en el Pacífico marca un hito en la validación de nuestros sistemas de control y navegación en el espacio profundo. Observar la ejecución impecable de la Inyección Translunar (TLI) y la precisión del sistema GNC durante la reentrada atmosférica demuestra el nivel de madurez técnica de esta generación...)*

## 2. Cronología Operativa (Flight Timeline)

> [!timeline] Hitos Críticos de la Misión
> - **Lanzamiento (1 Abril 2026, 18:35 EDT):** Despegue nominal desde el Pad 39B en el Kennedy Space Center.
> - **Inyección Translunar (1-2 Abril 2026):** Encendido del motor principal completado sin anomalías. El sistema GNC demostró una precisión estricta, manteniendo los márgenes de estabilidad en el lazo de control durante toda la maniobra.
> - **Récord de Distancia (6 Abril 2026, 1:56 p.m. EDT):** La tripulación alcanzó 252,756 millas de la Tierra.
> - **Sobrevuelo Lunar y LOS (6 Abril 2026):** Aproximación máxima a 4,067 millas sobre la superficie lunar. Pérdida de Señal (LOS) temporal desde las 6:44 p.m. hasta las 7:25 p.m. EDT por ocultación. Observación del "Earthset".
> - **Amerizaje (10 Abril 2026, 8:07 p.m. EDT):** Impacto controlado en el Océano Pacífico, frente a las costas de San Diego. 

## 3. Dinámica de Reentrada y Aerotermodinámica

Durante el reingreso, el escudo térmico de la Orion tuvo que disipar cantidades masivas de energía cinética. La tasa de calentamiento convectivo en el punto de estancamiento se puede aproximar mediante relaciones empíricas estándar de aerotermodinámica:

$$\dot{q} = C \sqrt{\rho} V^3$$

*Donde $C$ es una constante geométrica del vehículo, $\rho$ es la densidad atmosférica local y $V$ es la velocidad de reentrada (cercana a Mach 32).*

A los 5,400 pies, los paracaídas de frenado (drogue) se cortaron para dar paso al despliegue de los tres paracaídas principales, reduciendo la velocidad terminal a menos de 200 ft/s antes del contacto con el agua.

## 4. Evidencia Científica y Multimedia

### Diagrama de la Trayectoria (Canvas)
![[Trayectoria_Artemis2_GNC.canvas]]
*(Nota: Crea un archivo Canvas en Obsidian donde conectes nodos con las fases de vuelo: LEO -> TLI -> Órbita Lunar -> Reentrada).*

### Videos y Telemetría

<iframe width="560" height="315" src="https://www.youtube.com/embed/j3Pq35gm4qA" title="NASA Artemis II Daily News Conference" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

<iframe width="560" height="315" src="https://www.youtube.com/embed/BXrIuIT4H4k?si=Dnc8I4o-5Px6fYHq" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

<iframe width="560" height="315" src="https://www.youtube.com/embed/rSN3Mlq7B8w?si=rHMKmrYIXR02umKv" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>


### Referencias y Literatura
- `[@NASA2026Artemis2_Updates]` - NASA Blogs. (2026). *Artemis II Flight Day 10: Live Re-Entry Updates*. Recuperado el 10 de Abril de 2026.
- `[[Paper_Analisis_Termico_Orion.pdf]]` - *(Enlaza aquí los PDF técnicos sobre el escudo térmico y los algoritmos de control LQR utilizados en la nave).*
