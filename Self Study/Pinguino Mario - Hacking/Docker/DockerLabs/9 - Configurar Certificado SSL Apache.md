---
title: "9 - Configurar Certificado SSL Apache"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

```bash
# Use Debian as base image
FROM debian:latest

# Install Apache
RUN apt-get update && apt-get install -y apache2 openssl

# Generate self-signed SSL certificate
RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/ssl/private/apache-selfsigned.key \
    -out /etc/ssl/certs/apache-selfsigned.crt \
    -subj "/C=US/ST=California/L=San Francisco/O=Your Organization/OU=Your Unit/CN=example.com"

RUN mkdir -p /var/www/html/https

# Transfer custom index.html files
COPY index_http.html /var/www/html/index.html
COPY index_https.html /var/www/html/https/index.html

# Enable SSL module
RUN a2enmod ssl

# Configure virtual hosts for port 80 and port 443
COPY 000-default.conf /etc/apache2/sites-available/000-default.conf
COPY default-ssl.conf /etc/apache2/sites-available/default-ssl.conf

# Enable the sites
RUN a2ensite 000-default.conf
RUN a2ensite default-ssl.conf

# Start Apache service
CMD service apache2 start && tail -f /dev/null
```

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
