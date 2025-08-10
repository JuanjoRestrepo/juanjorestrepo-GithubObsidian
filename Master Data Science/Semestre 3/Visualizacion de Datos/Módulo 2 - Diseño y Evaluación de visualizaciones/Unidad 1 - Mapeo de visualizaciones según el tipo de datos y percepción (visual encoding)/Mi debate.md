# **Mecanismos de Representación de Información sobre la COVID-19 en Colombia: Un Análisis de los Desafíos y las Oportunidades**

Durante la pandemia de COVID-19 en Colombia, la comunicación de datos epidemiológicos jugó un papel decisivo en la toma de decisiones y en informar a la ciudadanía. Instituciones como el Instituto Nacional de Salud (INS), el Ministerio de Salud y secretarías de salud locales desplegaron herramientas visuales —tableros interactivos, gráficos de líneas, mapas y paneles de indicadores— para mostrar la evolución del virus y garantizar acceso abierto a la información [1], [2]. No obstante, la claridad comunicativa de estas herramientas dependió en gran medida de su diseño visual y de la contextualización de los datos [3].

### Análisis de los mecanismos de representación

El tablero del INS se destacó por consolidar datos estructurados con opciones de filtro por departamento, municipio, grupo etario y género, lo que permitió un monitoreo detallado [1]. Aun así, el exceso de elementos visuales en una sola interfaz —como mapas, gráficos y tablas superpuestos— pudo causar sobrecarga cognitiva, especialmente para audiencias no especializadas [4].

Además, muchas visualizaciones no precisaban si la fecha correspondía a notificación, diagnóstico o inicio de síntomas, lo que generó ambigüedad temporal [3]. Tampoco incluían narrativa explicativa o definiciones de términos técnicos como “letalidad” o “positividad”, lo que afectaba interpretación y podía incentivar percepciones equivocadas [6].

Contrastando con lo anterior, el panel de **SaluData Bogotá** ofreció una interfaz más clara, con segmentación territorial precisa e indicadores visibles al primer vistazo [2]. Sin embargo, se beneficiaría de añadir tasas por 100 000 habitantes y líneas de tendencia para visualizar las variaciones diarias [5].

Además, el Gobierno Nacional lanzó el **Safe Economic Reactivation Dashboard**, desarrollado en colaboración con el Banco Mundial. Este incluyó datos en tiempo real sobre contagios, capacidad sanitaria y capacidad para reactivar sectores económicos en más de 1 100 municipios, con desglose por género y etnia, facilitando decisiones equitativas y contextualizadas [0].

Herramientas basadas en inteligencia de negocios también resultaron valiosas. Un panel web interactivo basado en datos del INS permitió seguimiento económico y sanitario en cinco ciudades principales (Bogotá, Medellín, Cali, Barranquilla y Cartagena). La plataforma, construida en Microsoft Power BI, incluía filtros dinámicos y análisis de tendencias —en escalas lineales y semilogarítmicas— así como cálculo de letalidad municipal, brindando una visión clara y flexible para la toma de decisiones [6], [5].

### Lecciones de diseño global

Las revisiones internacionales muestran que los dashboards fueron esenciales para monitorear contagios, muertes, recuperaciones y pruebas; aunque muchos fueron principalmente informativos, no siempre apoyaban el análisis profundo [7]. Reflexiones recientes destacan que los dashboards se diseñaron apresuradamente y sin considerar audiencias específicas. Esto dejó lecciones clave para futuros desarrollos: la necesidad de claridad visual, menor sobrecarga, interactividad significativa y narrativas que guíen al usuario [8].

### Propuestas de mejora

- **Narrativa y contexto**: acompañar visualizaciones con textos que expliquen términos técnicos, eventos clave (como cuarentenas o variantes emergentes), y patrones de comportamiento [3], [4].
- **Contextualización per cápita**: utilizar tasas por población para comparar regiones de distinto tamaño de forma justa [5].
- **Estandarización y accesibilidad**: uniformizar colores, escalas y formatos; mejorar contraste y tipografía; usar paletas amigables para personas daltónicas [6].
- **Interactividad ampliada**: permitir filtros por edad, localidad, fecha e indicador; incluir opciones de descarga de datos para transparencia [1], [6].
- **Segmentación inclusiva**: incorporar variables como género y etnia —ya implementadas en el dashboard de reactivación económica— para visibilizar impactos desiguales [0].
- **Equilibrio informativo-informativo**: diseñar dashboards que no solo informen, sino también ayuden a interpretar y analizar, como destacan estudios globales [7].

### Conclusión

Los mecanismos de representación de información empleados durante la pandemia fueron clave para la gobernanza y el empoderamiento ciudadano. No obstante, el diseño, la claridad y la contextualización determinaron su impacto real. Visualizaciones simples, estandarizadas, accesibles y contextualizadas no solo mejoran la comprensión, sino que fortalecen la confianza institucional y permiten respuestas más equitativas y efectivas ante crisis futuras.

---

**Referencias IEEE**

[0] _World Bank_, “Guiding Complex Decision-Making During the COVID-19 Crisis: Colombia Improves Data Collection Through a Real-Time Safe Economic Reactivation Dashboard,” 2021. [En línea].

[1] Instituto Nacional de Salud (INS), “Tablero oficial de la situación COVID-19 en Colombia.” [En línea]. Disponible en: [https://www.ins.gov.co/Noticias/Paginas/coronavirus-casos.aspx](https://www.ins.gov.co/Noticias/Paginas/coronavirus-casos.aspx) [Accedido: 10-ago-2025].

[2] SaluData - Observatorio de Salud de Bogotá, “Datos que salvan.” [En línea]. Disponible en: [https://saludata.saludcapital.gov.co/osb/datos-que-salvan/](https://saludata.saludcapital.gov.co/osb/datos-que-salvan/) [Accedido: 10-ago-2025].

[3] C. Ardura, “Visualización de datos COVID-19 en Colombia,” 2020. [En línea].

[4] M. L. Montes Rojas, J. González Vélez y M. L. Pier Castello, “El diseño de información en la visualización interactiva de prensa para la cobertura de la pandemia COVID-19,” _Revista 180_, no. 50, pp. 18–31, 2022.

[5] Organización Mundial de la Salud (OMS), “Tablero global de la situación COVID-19.” [En línea]. Disponible en: [https://data.who.int/dashboards/covid19/deaths?n=o](https://data.who.int/dashboards/covid19/deaths?n=o) [Accedido: 10-ago-2025].

[6] Scielo, “Circulación de información relacionada con la salud en Colombia: el caso de la infodemia… pandemia por COVID-19,” _Revista de Salud Pública_, vol. 22, no. 2, pp. 214–219, 2020. [En línea].

[7] A. S. Asadzadeh _et al_., “Characteristics and specifications of dashboards developed for the ...” _BMC Public Health_, 2021.

[8] A. Arleo _et al_., “Reflections on the Use of Dashboards in the Covid-19 Pandemic,” _arXiv_, Feb. 2025.