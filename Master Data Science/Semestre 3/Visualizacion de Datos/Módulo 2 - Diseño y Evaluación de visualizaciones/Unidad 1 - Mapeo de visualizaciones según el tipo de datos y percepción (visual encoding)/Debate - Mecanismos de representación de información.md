---
title: "Debate - Mecanismos de representación de información"
date: 2026-08-27
tags:
  - maestria
  - semestre-3
  - visualizacion-datos
  - apuntes
status: reference
---


# **Mecanismos de Representación de Información sobre la COVID-19 en Colombia: Un Análisis de los Desafíos y las Oportunidades**

Durante la pandemia de COVID-19 en Colombia, la comunicación de datos epidemiológicos fue esencial para la toma de decisiones informadas. Instituciones como el Instituto Nacional de Salud (INS), el Ministerio de Salud y las secretarías de salud locales desplegaron herramientas visuales —tableros interactivos, gráficos de líneas, mapas y paneles de indicadores— que permitieron seguir la evolución del virus y garantizar acceso abierto a información actualizada [1], [2]. No obstante, la efectividad comunicativa dependió en gran medida del diseño visual y la contextualización de los datos [3].

#### Análisis de los mecanismos de representación

Por un lado, el tablero del INS destacó por consolidar datos estructurados con filtros por departamento, municipio, grupo etario y género, lo que facilitó un monitoreo detallado [1]. Sin embargo, la acumulación de elementos visuales —mapas, gráficos y tablas superpuestos— generó sobrecarga cognitiva, especialmente en audiencias no especializadas [4].

Además, muchas visualizaciones no especificaban si la fecha correspondía a notificación, diagnóstico o inicio de síntomas, lo que causó ambigüedad temporal [3]; tampoco incluyeron narrativa explicativa ni definiciones de términos técnicos como “letalidad” o “positividad” [6].

En contraste, el panel **SaluData Bogotá** presentó una interfaz más clara, con segmentación territorial precisa e indicadores visibles al primer vistazo [2]. Aún así, se beneficiaría de introducir tasas por 100 000 habitantes y líneas de tendencia para evidenciar cambios diarios [5].

Simultáneamente, el Gobierno Nacional lanzó el **Safe Economic Reactivation Dashboard**, desarrollado junto con el Banco Mundial. Este tablero incorporó datos en tiempo real sobre contagios, capacidad hospitalaria y potencial de reactivación económica en más de 1 100 municipios, incluyendo desglose por género y etnia, lo que favoreció decisiones más equitativas y contextualizadas [0].

![[Pasted image 20250810173523.png]]

Captura de pantalla del Panel de Reactivación Económica Segura [0]

Adicionalmente, se utilizó un panel web interactivo hecho en Power BI (INS), que permitió llevar un seguimiento económico y sanitario de cinco grandes ciudades (Bogotá, Medellín, Cali, Barranquilla y Cartagena) con filtros dinámicos, análisis en escalas lineales y semilogarítmicas, y cálculo de letalidad por municipio [6], [5].

Por el lado de Cali, un estudio enfocado entre abril y julio de 2021 presentó una visualización combinada de casos diarios, muertes, vacunación diaria, distribución de variantes del virus y el índice Rt, lo que refleja cómo una presentación clara puede integrar múltiples dimensiones temporales, espaciales y genómicos en una sola visualización [9]

![[Pasted image 20250810173537.png]]

Interfaz de datos demográficos de la plataforma web AMORE (cifras absolutas) [10]

Asimismo, los mapas temáticos basados en TAZ (como el presentado arriba) ilustran cómo segmentar la ciudad con base en condiciones socioeconómicas y acceso a servicios, lo cual es extremadamente relevante para mostrar desigualdades geográficas y de infraestructura de salud en Cali

![[Pasted image 20250810173552.png]]

_Distribución de la población de las ZAT de Cali 2020 según estratificación económica de la vivienda y tiempos de viaje [10]_

Asimismo, los mapas temáticos basados en TAZ (como el presentado arriba) ilustran cómo segmentar la ciudad con base en condiciones socioeconómicas y acceso a servicios, lo cual es extremadamente relevante para mostrar desigualdades geográficas y de infraestructura de salud en Cali (véase figura anterior). 

#### Lecciones de diseño global

Revisiones internacionales subrayan que, aunque los dashboards fueron esenciales para monitorear indicadores clave (contagios, muertes y recuperaciones), muchos se diseñaron apresuradamente y estaban poco orientados al análisis profundo [7]. Esto presenta una oportunidad para futuros despliegues: priorizar la claridad visual, reducir la sobrecarga, enriquecer la interactividad y guiar a los usuarios mediante narrativas visuales [8].

#### Propuestas de mejora

- **Narrativa y contexto**: añadir textos explicativos sobre términos técnicos, eventos cruciales (cuarentenas, variantes) y patrones destacables.
    
- **Contextualización per cápita**: emplear tasas por población para comparaciones equitativas entre regiones.
    
- **Estandarización y accesibilidad**: unificar colores, escalas y formatos; mejorar contraste y tipografía; utilizar paletas aptas para daltónicos.
    
- **Interactividad ampliada**: incorporar filtros por edad, ubicación, fecha e indicador; permitir descarga de datos.
    
- **Segmentación inclusiva**: incluir variables de género y etnia para visibilizar impactos diferenciales.
    
- **Equilibrio informativo-análisis**: diseñar dashboards que informen y orienten al análisis reflexivo, como lo evidencian las lecciones aprendidas a nivel global.
    

**Conclusión**

Los mecanismos de representación de información fueron fundamentales para la gobernanza de la pandemia en Colombia. No obstante, su efectividad comunicativa estuvo condicionada por el diseño visual y la contextualización. Las visualizaciones claras, estandarizadas, accesibles e inclusivas no solo mejoran la comprensión pública, sino que también fortalecen la confianza institucional y permiten acciones más equitativas en situaciones de crisis futuras.

**Referencias:**

[0] World Bank, “Guiding Complex Decision-Making During the COVID-19 Crisis: Colombia Improves Data Collection Through a Real-Time Safe Economic Reactivation Dashboard,” 2021.

[1] Instituto Nacional de Salud (INS), “Tablero oficial de la situación COVID-19 en Colombia.” Disponible en: [https://www.ins.gov.co/Noticias/Paginas/coronavirus-casos.aspx](https://www.ins.gov.co/Noticias/Paginas/coronavirus-casos.aspx)

[2] SaluData - Observatorio de Salud de Bogotá, “Datos que salvan.” [En línea]. Disponible en: [https://saludata.saludcapital.gov.co/osb/datos-que-salvan/](https://saludata.saludcapital.gov.co/osb/datos-que-salvan/)

[3] C. Ardura, “Visualización de datos COVID-19 en Colombia,” 2020. [En línea].Disponible en: [https://ardura.co/200920_covid19_colombia.html](https://ardura.co/200920_covid19_colombia.html)

[4] M. L. Montes Rojas, J. González Vélez y M. L. Pier Castello, “El diseño de información en la visualización interactiva de prensa para la cobertura de la pandemia COVID-19,” _Revista 180_, no. 50, pp. 18–31, 2022.

[5] Organización Mundial de la Salud (OMS), “Tablero global de la situación COVID-19.” Disponible en: [https://data.who.int/dashboards/covid19/deaths?n=o](https://data.who.int/dashboards/covid19/deaths?n=o)

[6] Scielo, “Circulación de información relacionada con la salud en Colombia: el caso de la infodemia… pandemia por COVID-19,” _Revista de Salud Pública_, vol. 22, no. 2, pp. 214–219, 2020.

[7] A. S. Asadzadeh et al., “Characteristics and specifications of dashboards developed for the ...” BMC Public Health, 2021.

[8] A. Arleo et al., “Reflections on the Use of Dashboards in the Covid-19 Pandemic,” arXiv, Feb. 2025.

[9] L. H. Patiño _et al._, “Epidemiological Dynamics of SARS-CoV-2 Variants During Social Protests in Cali, Colombia,” _Frontiers in Medicine_, vol. 9, Mar. 2022, doi: [https://doi.org/10.3389/fmed.2022.863911](https://doi.org/10.3389/fmed.2022.863911).

[10] L. G. Cuervo _et al._, ‘Improving accessibility to radiotherapy services in Cali, Colombia: Cross-sectional equity analyses using Open Data and Big Data Travel Times from 2020 - International Journal for Equity in health’, _BioMed Central_. BioMed Central, Aug-2024.
