---
title: "Conectar Python con ChatGPT"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Para conectar Python con chatgpt debemos primero obtener la API de openai dentro de su página web, donde podemos registrarnos, además de instalar la librería openai con el comando pip install openain; y a continuación con este código ya podemos utilizarlo:
```python
import openai

# Almacena tu clave de API como una cadena
API_KEY = "PONER API"

# Configura tus credenciales de OpenAI
openai.api_key = API_KEY

# Envía una solicitud al modelo de ChatGPT para generar una respuesta
response = openai.Completion.create(
    engine="davinci",
    prompt="Hola, ¿cómo estás?",
    temperature=0.5,
    max_tokens=50,
    n=1,
    stop=None,
)

# Imprime la respuesta generada por ChatGPT
print(response.choices[0].text.strip())
```
Y esta es la respuesta:
![[Pasted image 20230413114917.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
