
```json

{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "ScopusArticle",
  "description": "Esquema de metadatos para artículos extraídos desde la API de Scopus",
  "type": "object",
  "properties": {
    "title": {
      "type": "string",
      "description": "Título del artículo"
    },
    "authors": {
      "type": "string",
      "description": "Lista de autores"
    },
    "abstract": {
      "type": "string",
      "description": "Resumen o abstract del artículo"
    },
    "journal": {
      "type": "string",
      "description": "Nombre de la revista o publicación"
    },
    "year": {
      "type": "integer",
      "minimum": 1900,
      "maximum": 2100,
      "description": "Año de publicación"
    },
    "doi": {
      "type": "string",
      "pattern": "^10\\.\\d{4,9}/[-._;()/:A-Z0-9]+$",
      "description": "Identificador DOI"
    },
    "link": {
      "type": "string",
      "format": "uri",
      "description": "URL al registro del artículo"
    },
    "source_query": {
      "type": "string",
      "description": "Término de búsqueda usado en la API"
    },
    "retrieved_date": {
      "type": "string",
      "format": "date",
      "description": "Fecha en que se extrajo el registro"
    }
  },
  "required": ["title", "authors", "journal", "year", "doi", "link", "source_query", "retrieved_date"],
  "additionalProperties": false
}

```


# Esquema Json Final

```json

{

  "$schema": "https://json-schema.org/draft/2020-12/schema",

  "title": "ScopusArticle",

  "description": "Metadatos de artículo extraídos de Scopus",

  "type": "object",

  "properties": {

    "title": { "type": "string" },

    "authors": { "type": "string" },

    "abstract": { "type": "string" },

    "journal": { "type": "string" },

    "year": { "type": "integer", "minimum": 1900, "maximum": 2100 },

    "doi": { "type": "string", "pattern": "^10\\.\\d{4,9}/[-._;()/:A-Z0-9]+$" },

    "link": { "type": "string", "format": "uri" },

    "source_query": { "type": "string" },

    "retrieved_date": { "type": "string", "format": "date" }

  },

  "required": [

    "title",

    "authors",

    "abstract",

    "journal",

    "year",

    "doi",

    "link",

    "source_query",

    "retrieved_date"

  ],

  "additionalProperties": false

}

```


