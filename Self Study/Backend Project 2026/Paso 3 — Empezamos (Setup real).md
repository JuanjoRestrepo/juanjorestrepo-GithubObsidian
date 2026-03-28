
## 3.1 Inicializar proyecto

31. [x] Inicializar proyecto
```bash
mkdir task-manager-api
cd task-manager-api

npm init -y

npm install express cors dotenv bcrypt jsonwebtoken
npm install -D typescript ts-node-dev @types/node @types/express @types/bcrypt @types/jsonwebtoken
```

## 3.2 TypeScript config

32. [x] Inicializar proyecto
```bash
npx tsc --init
```

## 3.3 Prisma + PostgreSQL
33. [x] Inicializar proyecto
```bash
npm install prisma --save-dev
npm install @prisma/client

npx prisma init
```

OUTPUT
```bash
Initialized Prisma in your project

  prisma/
    schema.prisma
  prisma.config.ts
  .env
  .gitignore

Next, choose how you want to set up your database:

CONNECT EXISTING DATABASE:
  1. Configure your DATABASE_URL in prisma.config.ts
  2. Run prisma db pull to introspect your database.

CREATE NEW DATABASE:
  Local: npx prisma dev (runs Postgres locally in your terminal)
  Cloud: npx create-db (creates a free Prisma Postgres database)

Then, define your models in prisma/schema.prisma and run prisma migrate dev to apply your schema.

Learn more: https://pris.ly/getting-started
```


## 3.4 .env
```env
PORT=3000
DATABASE_URL="postgresql://user:password@localhost:5432/tasks_db"
JWT_SECRET=supersecret
```


