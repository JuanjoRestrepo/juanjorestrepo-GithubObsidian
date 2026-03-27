
## 1.1 Base de datos: PostgreSQL vs MongoDB

**Decisión recomendada: PostgreSQL**
**Por qué:**
- Relaciones claras: `User → Tasks (1:N)`
- Integridad referencial (clave foránea)
- Mejor percepción en backend tradicional
- Más alineado con APIs REST estructuradas

**Conclusión:**  
→ Usaremos **PostgreSQL + ORM (Prisma)**

---
## 1.2 ORM / Query Builder
**Opciones:**
- Prisma ✅ (recomendado)
- TypeORM (más pesado, menos moderno)
- Knex (más bajo nivel)

**Decisión: Prisma**
**Por qué:**
- Tipado fuerte (ideal con TypeScript)
- Migrations simples
- Muy bien visto en pruebas técnicas
- Reduce bugs en persistence layer

---
## 1.3 Arquitectura en capas (obligatorio)

**Estructura propuesta (mejorada)**

```bash
src/
│
├── api/
│   ├── routes/
│   ├── middlewares/
│
├── controllers/
├── services/
├── persistence/
│   ├── repositories/
│   ├── prisma/
│
├── models/           # Tipos / interfaces
├── schemas/          # AJV validation
├── config/           # env singleton
├── utils/
├── errors/
│
├── app.ts
└── server.ts
```

---
## 1.4 Patrón de diseño clave

Vamos a usar:

|Patrón|Uso|
|---|---|
|**Singleton**|Configuración (.env)|
|**Repository**|Acceso a DB|
|**Service Layer**|Lógica de negocio|
|**Middleware**|Auth + errores|
|**DTO / Schema**|Validación|

---
## 1.5 Autenticación
**Stack:**
- bcrypt → `hashing`
- jsonwebtoken → `JWT`

**Decisión importante:**
- Token stateless (sin refresh tokens para simplificar)
- Payload mínimo: `userId`

---
## 1.6 Validación
El PDF recomienda AJV .

**Decisión:**
- AJV + JSON Schema
- Validación en middleware

## 1.7 Manejo de errores

Implementaremos:

```typescript
BaseError
 ├── ValidationError
 ├── AuthError
 ├── NotFoundError
 ├── ForbiddenError
```

- Un middleware global

---
## 1.8 Swagger
Usaremos:
- swagger-jsdoc
- swagger-ui-express
