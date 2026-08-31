---
title: "UiPath Troubleshooting: PDF Data Extraction in Chrome"
aliases:
  - "UiPath Troubleshooting - PDF Data Extraction in Chrome"
  - "PDF Data Extraction in Chrome"
tags: [rpa, uipath, automation, reframework]
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-31
category: "Troubleshooting & UI Frameworks"
level: "Enterprise Advanced (2026)"
source: "Self Study REFramework (2026)"
year: 2026
related:
  - "[[20. Open Each PDF in Microsoft Edge-Chrome-Etc|Browser PDF Automation (2026)]]"
  - "[[24. Get Text and Self-Healing Selectors|Get Text & Selectors (2026)]]"
  - "[[3. RegEX Builder|Foundations: Regex Builder (2023)]]"
  - "[[1. Extracting Data From PDF|Foundations: PDF Data Extraction (2023)]]"
  - "[[MOC-UiPath]]"
---

# UiPath Troubleshooting: PDF Data Extraction in Chrome

## Overview

This guide outlines the methodology for resolving data extraction issues when reading local PDF files directly within Google Chrome using UiPath.
- Standard UI scraping tools (such as the `Get Text` activity) often fail when handling PDFs in Chrome.    
- This failure occurs because Chrome utilizes its own built-in PDF viewer plugin.
- Standard UiPath selectors treat this entire viewer window as a single graphic or canvas element.
- Consequently, UiPath cannot reliably inspect or target internal DOM elements or text layers inside the browser's PDF viewer.

## Recommended Alternatives

Before relying on UI scraping, consider the following best practices for PDF extraction:

- **Download and Read Locally:** Save the PDF locally (via a `Click` or `Download File` activity) and utilize the dedicated `Read PDF Text` activity for digital text or the `Read PDF with OCR` activity for scanned images.
- **Computer Vision (CV):** If the document must be read directly on the screen, use the `CV Get Text` activity, which parses screen elements visually.
- **Headless/HTTP Extraction:** If the PDF has a direct web URL, use an `HTTP Request` activity to download it in the background without visually launching Chrome.

## Workaround: UI Extraction for Local Chrome PDFs (`file:///`)

If project constraints require opening a local PDF directly in Chrome (e.g., within an REFramework Performer processing `file:///` URLs), follow this configuration to bypass standard selector limitations.

### 1. Environment Configuration (Crucial Fix)

By default, Chrome blocks extensions from interacting with local file URLs. This causes UiPath to only see a generic `role='grouping'` container instead of the actual text.

- Open Google Chrome and navigate to `chrome://extensions`.
- Locate the **UiPath Web Automation** extension and click **Details**.
- Toggle **ON** the setting for **Allow access to file URLs**.
- Restart Chrome to apply the changes.

### 2. UI Framework Adjustment

If the default selector highlights the entire page as a single block even after enabling file access:
- During the "Indicate on Screen" process, press `F4` on your keyboard to cycle through the available UI Frameworks.
- Switch from the "Default" (UIA) framework to **Active Accessibility (AA)**.
- AA mode can often penetrate Chrome's PDF container to identify individual text elements.

### 3. Data Extraction & Activity Configuration

When Chrome forces the text into a multi-line block that cannot be individually selected (e.g., mixing dates, phone numbers, and invoice numbers), extract the entire block and parse it using Regular Expressions (Regex).

**A. Get Text Activity:**

- **Target:** Select the overarching text block on the screen.
- **Properties Setup:**  
    - Clear the `Output element` field completely. Leaving a string variable here will cause a `BC30311` validation error (attempting to convert a String to a UiElement). 
    - In the `Text value (Out)` field, press `Ctrl + K` to declare a new String variable (e.g., `str_WholeBlock`).

**B. Assign Activity (Regex Parsing):**

- Place an `Assign` activity immediately after the `Get Text` activity to isolate the target data.
- **To:** `out_InvoiceNumber` (String variable)
- **Value:** `System.Text.RegularExpressions.Regex.Match(str_WholeBlock, "\d+(?=\s*)$").Value.Trim`

**Regex Logic Explanation:**
- `\d+`: Targets a sequence of digits.
- `(?=\s*)$`: A positive lookahead ensuring the digits are located at the absolute end (`$`) of the text block, ignoring trailing spaces. This successfully isolates the final invoice number while bypassing unrelated numbers (like phone numbers) located earlier in the text block.

---

## Contexto de Estudio y Arquitectura Cruzada (Cross-Links)
- **MOC Maestro**: [[MOC-UiPath]]
- **Navegación e Ingesta de PDFs**: Se integra con el flujo de apertura y visualización en [[20. Open Each PDF in Microsoft Edge-Chrome-Etc]].
- **Extracción y Validación de Datos**: Técnicas combinadas de [[24. Get Text and Self-Healing Selectors]] y expresiones regulares con [[3. RegEX Builder]].

### Documentos Relacionados:
- [[20. Open Each PDF in Microsoft Edge-Chrome-Etc|Browser PDF Automation (2026)]]
- [[24. Get Text and Self-Healing Selectors|Get Text & Selectors (2026)]]
- [[3. RegEX Builder|Foundations: Regex Builder (2023)]]
- [[1. Extracting Data From PDF|Foundations: PDF Data Extraction (2023)]]
- [[15. Using Try Catch for Exception Handling in UiPath|Exception Handling (2026)]]
- [[MOC-UiPath]]
