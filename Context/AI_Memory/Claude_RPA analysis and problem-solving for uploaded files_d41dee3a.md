---
title: "RPA analysis and problem-solving for uploaded files"
date: 2026-08-25T19:44:32.826162Z
tags: [ai_memory, claude_context]
summary: ""
---

### Human
Analyze deeply all of those files i put on your context and use your RPA Skill to understand the context and what is the problem, and possible solutions

### Assistant
# Diagnóstico RPA — Peru New Vehicles (Main3.xaml)

He revisado los cinco archivos a fondo (Main.xaml, Main3.xaml, InvokePowerAutomateMail.xaml, project.json, entry-points.json). Main3 es efectivamente la versión más madura — tiene manejo de excepciones tipado (`BusinessRuleException` vs `SystemException`), validaciones de negocio en "Get Data", y un flujo transaccional completo de Autoline en "Per invoice". Pero también contiene los tres problemas que describes, y el código expone las causas raíz con bastante precisión — no hace falta especular tanto como parece necesario a primera vista.

## 1. El error "Date text=X - Not expected=Y" — tu hipótesis del calendario Juliano es incorrecta, pero apuntas al síntoma correcto

Rastreé el mensaje hasta `RetryScope_12` → `LogMessage_33`, cuya condición de éxito está en `CheckTrue_2`:

```
Expression="[not String.IsNullOrEmpty(FechaDocumentoText) AndAlso FechaDocumentoText <> FechaDocumentoTextRef]"
```

Esto es clave: **la validación no comprueba que la fecha escrita sea correcta — solo comprueba que el texto del campo "Fecha documento" cambió respecto a lo que tenía antes de escribir** (`FechaDocumentoTextRef` se captura en `GetValue_2`, *antes* del `TypeInto`). No hay ningún cálculo Juliano de negocio aquí; los dos números son simplemente lo que `GetValue` devuelve del control `automationid='26712'` (un `KCMLDBEdit_32`, control legado tipo MFC/VB del cliente Kerridge/CDK). Estos controles frecuentemente exponen en su propiedad de valor UI Automation el **buffer interno del dato** (a veces un serial de fecha OLE/Julian-like) en lugar del texto renderizado, sobre todo si `GetValue` se ejecuta antes de que el control termine su repintado post-`[k(tab)]`. La diferencia de 31 días entre ambos valores es consistente con dos hipótesis, y la evidencia en el código favorece claramente la segunda:

**Hipótesis A (timing/UI Automation):** el `GetValue` lee el control antes de que Autoline recalcule internamente el valor tras el tab, capturando un estado transitorio.

**Hipótesis B — la más probable, con evidencia directa en el código:** hay un bloque completo de normalización de formato de fecha (`dd/mm/yyyy` → `MM/dd/yyyy`) en la sección "Get Data" del `ExcelForEachRowX_1`, envuelto en `ui:CommentOut DisplayName="Comment Out" IdRef="CommentOut_11"` — **está deshabilitado**. Ese bloque comentado hacía exactamente lo que se necesita: si `DateFormat = "dd/mm/yyyy"` y `Not IsDate(CurrentRow("F.FACTURA"))`, convertía el string. Al estar comentado, **el bot toma el texto crudo de "F.FACTURA" del Excel y lo escribe directamente en el campo de Autoline sin normalizar**. Si el usuario ingresa fechas en formato día/mes/año (estándar peruano/español) y Autoline las interpreta como mes/día/año, cualquier fecha con día ≤ 12 se desplaza de mes — exactamente el patrón de "31 días de diferencia" que describes, y exactamente lo que ese bloque comentado estaba diseñado para prevenir.

**Solución concreta:** (1) reactivar/reescribir esa normalización de fecha usando la columna `DateFormat` del Config sheet, aplicada de forma robusta con `CultureInfo.InvariantCulture` y `DateTime.TryParseExact`, no `CDate` implícito (que depende de la configuración regional del SO de la VM); (2) corregir la condición de `CheckTrue_2` para que valide **igualdad contra el valor esperado parseado**, no solo "que cambió" — hoy esa retry-scope puede pasar como "éxito" una fecha incorrecta simplemente porque es diferente a la anterior.

## 2. Sincronización con OneDrive — la causa está en mezclar dos mecanismos de acceso al mismo archivo

Esto es arquitectónicamente el problema más serio. El flujo accede al Excel de **dos formas distintas** dentro de la misma ejecución:

- Durante todo el proceso (`ExcelApplicationCard` repetido en "Get Data", en cada iteración de "Per invoice", y en el manejo de excepciones), `WorkbookPath="[templateFile]"` es una **URL de SharePoint/OneDrive** (ver el default en `Main3.xaml.json` y `entry-points.json`: `https://inchcapeuk-my.sharepoint.com/...New Vehicles_trigger%20-%20test%20copy.xlsx...`).
- En el bloque `Finally`, el guardado final usa `SaveExcelFileAsX` con una **ruta de archivo local**: `"C:\Users\"+Username+"\OneDrive - Inchcape\Peru New Vehicles\Results\..."`.

Abrir un workbook por URL de SharePoint fuerza a Excel/UiPath a resolver el archivo a través del cliente OneDrive (placeholders "Files On-Demand"), mientras que el guardado final escribe directamente al filesystem local sincronizado. Esto crea una carrera clásica: si OneDrive todavía está subiendo el cambio anterior cuando el bot vuelve a abrir el archivo por URL (lo hace **en cada invoice**, no una sola vez), puede obtener una copia desactualizada, generar conflictos de versión, o bloquear el archivo — que es exactamente lo que reportas y por lo que el usuario necesita crear copias.

**Por qué "Always keep on this device" y desactivar sincronización de red no resuelven el problema de fondo:** esas mitigaciones actúan sobre el cliente OneDrive, pero no eliminan la causa raíz, que es *arquitectónica*: el bot re-resuelve el archivo contra la nube en cada iteración del loop en vez de trabajar sobre una sesión de Excel local persistente y sincronizar una sola vez al final.

**Solución recomendada:**
1. Al inicio de "Per invoice", abrir el Excel **una sola vez** con una ruta de archivo local real (no URL), y mantener esa instancia de Excel abierta durante todo el `ForEachRow` (usando `Excel Process Scope` + una sola `Use Excel File`), escribiendo/guardando en memoria/local en cada iteración sin reabrir.
2. Eliminar por completo el acceso por URL de SharePoint durante la ejecución. Al arrancar, descargar el archivo fuente vía **Microsoft Graph / SharePoint connector** (`UiPath.MicrosoftOffice365.Activities`, que ya está referenciado en el proyecto) a una ruta de trabajo local aislada (`C:\Bots\PNV\Work\`), fuera de la carpeta sincronizada de OneDrive.
3. Al finalizar (éxito o excepción, en el `Finally`), subir el resultado de vuelta a SharePoint vía el mismo connector Graph, en una sola operación atómica — no dependiendo del cliente de sincronización de OneDrive en absoluto.

Esto resuelve simultáneamente el problema de sincronización *y* es la mejora de rendimiento más grande disponible (ver punto 3).

## 3. Por qué el bot tarda 4–5 min vs. 2 min humano

No es un solo culpable — son cuatro factores acumulativos, todos visibles en el XAML:

**a) Reapertura de Excel por URL en cada invoice.** Como se describe arriba, cada `ExcelApplicationCard` con `WorkbookPath=[templateFile]` fuerza a Excel a resolver contra SharePoint/OneDrive. Esto solo, multiplicado por N facturas, puede añadir 10-30s por factura innecesariamente.

**b) Anti-patrón de retry anidado.** `RetryScope_10` (NumberOfRetries=3, RetryInterval=5s) envuelve **toda** la lógica de una factura — desde `Prep Autoline` (matar kclient, relanzarlo, reloguear) hasta el registro completo de la transacción, ~90+ actividades. Dentro de ese scope hay además `RetryScope`s locales más finos y correctos (p. ej. `RetryScope_11`, `RetryScope_20/21` validando `TipoPolizaExtractedText`). El problema: si cualquiera de esos retries internos agota sus 3 intentos y lanza, el `RetryScope_10` exterior **reinicia toda la factura desde cero** — mata kclient, vuelve a loguearse, reabre Proveedores, re-teclea todo. Un glitch de timing en un solo campo puede convertir una factura de 2 min en 3 réplicas completas de 60+ pasos de UI Automation.

**c) Múltiples `OnUiElementAppear` con `RepeatForever=True` y timeouts de 15-20s en cascada secuencial.** Cuenta al menos seis instancias de este patrón (`OnUiElementAppear_1`, `_4`, `_7`, `_9`, `_11`, `_13`, `_15`) actuando como "vigías de popup" que **no** aparecen la mayoría de las veces (son manejo de excepción, no flujo normal). Cada uno que no dispara consume tiempo antes de continuar, y al estar encadenados secuencialmente (no en paralelo), pueden sumar fácilmente 30-90s por factura de espera "vacía".

**d) `Click`/`SetFocus` duplicados y delays fijos.** Varios `Delay Duration="00:00:05"` explícitos (relanzamiento de kclient, apertura de Excel) más el patrón `SetFocus` + `Click` en casi cada botón — aporta robustez pero también overhead constante.

**Priorización de la solución (mayor impacto primero):**
1. Separar los retries: que el `RetryScope` interno de cada acción crítica maneje su propia recuperación (reintentar el campo específico), y que solo un fallo *catastrófico* de sesión (kclient caído) dispare el reinicio completo — hoy todo colapsa al mismo nivel.
2. Reemplazar los `OnUiElementAppear RepeatForever` que actúan como manejo de excepción por un patrón `TryCatch` + `Element Exists` con timeout corto (2-3s) donde aplique, en vez de esperas de 15-20s por defecto.
3. Resolver el punto 2 (Excel local persistente) elimina la reapertura por invoice.
4. Reactivar la explicit "Salir" (exit) del documento al final de cada factura — está **comentada** (`CommentOut_51` envolviendo `RetryScope_25`). Sin cerrar la ventana "Entrada remesas de documentos" explícitamente, cada iteración siguiente hereda ventanas abiertas que pueden generar ambigüedad de selectores y forzar reintentos silenciosos — contribuyendo tanto a lentitud como a fragilidad.

## 4. Riesgos adicionales que encontré (no mencionados pero relevantes)

- **Aritmética de moneda con `CDbl`:** el balance check `If CDbl(TOTAL COSTE USD) + CDbl(lastTransactionRef) <> 0` (que marca la fila como "Review data please" y la salta) usa `Double` para montos financieros. El error de redondeo de punto flotante puede producir falsos positivos en facturas cuyo balance es correcto, generando saltos innecesarios. Recomiendo `Decimal` en toda la cadena de cálculo de montos.
- **Confirmación "Sobre escribir" (overwrite) auto-clickeada dos veces** (`RetryScope_23` y `RetryScope_19`) sin logging explícito de cuándo se dispara. En un flujo de posteo contable, un overwrite silencioso sobre un documento existente es un riesgo de integridad de datos — debería loguearse como warning cada vez que ese branch se ejecuta, como mínimo.
- **Validación de horario de licencia invertida/sospechosa:** `If DateTime.Now.Hour < 13 Then Throw` usa `DateTime.Now` (hora del sistema de la VM), no una zona horaria explícita de Perú. Si la VM no está en UTC-5, esta condición puede fallar en horarios inesperados — vale la pena verificar `TimeZoneInfo` explícitamente en vez de confiar en el reloj local del sistema.
- **`templateFile` por defecto apunta a "...test copy.xlsx"** tanto en `Main3.xaml.json` como en `entry-points.json`. Si Main3 se ejecuta en producción sin sobrescribir ese argumento, está operando sobre el archivo de prueba — esto por sí solo podría explicar parte de la confusión sobre "cambios que no se guardan donde el usuario espera".
- **Credenciales/config hardcoded:** el email destinatario (`maria.fawcett@inchcape.com`), cuentas contables (`0100950500`, `0900870001`, etc.), y códigos fijos (IVA "Z", clasificación "5", tipo documento "P13") están embebidos como literales en el XAML en vez de en el Config sheet o un Orchestrator Asset — cualquier cambio de plan de cuentas requiere republicar el paquete.

## Plan de acción sugerido (orden de impacto/esfuerzo)

1. **Reactivar y corregir la normalización de fecha** (Get Data) + corregir `CheckTrue_2` para validar igualdad real — resuelve directamente tu error reportado.
2. **Desacoplar el acceso a Excel de OneDrive**: descarga única vía Graph al inicio, sesión Excel local persistente durante el loop, subida única al final — resuelve sincronización y aporta la mayor ganancia de velocidad.
3. **Aplanar la jerarquía de retries** para que fallos puntuales no disparen relogin completo de Autoline.
4. **Reactivar el cierre explícito del documento** por factura.
5. Migrar montos a `Decimal` y agregar logging al branch de "Sobre escribir".

¿Quieres que profundice en alguno de estos —por ejemplo, que te arme el pseudocódigo/diseño concreto del reemplazo de la sesión de Excel local, o que revisemos línea por línea la lógica de las 4 transacciones contables para confirmar que los montos calculados (T2/T4 sin `TypeInto` visible de monto) son intencionales?

### Human
EN RESUMEN, ME INTERESA QUE ESTO FUNCIONE, QUE SEA 100% FUNCIONAL, YA A FUTURO HAREMOS LAS POSIBLES MEJORAS, OPTIMIZACIONES Y USO DE MEJORES PRACTICES

Y lo que mejor consideres para cumplir con ese objetivo de funcionalidad total por ahora. Ya sea, revisar el pseudocódigo/diseño concreto del reemplazo de la sesión de Excel local o revisar línea por línea la lógica de las 4 transacciones contables para confirmar que los montos calculados (T2/T4 sin `TypeInto` visible de monto) son intencionales

### Assistant

```
This block is not supported on your current device yet.
```



