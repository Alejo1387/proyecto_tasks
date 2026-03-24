# TaskTracker - Hoja de Ruta de Desarrollo

> Desarrollar un gestor de tareas profesional desde cero, con arquitectura moderna y preparado para producción.

**Principios**: Cada tarea es pequeña, clara y orientada al aprendizaje. No hay código directo aquí, solo guías.

---

## 📋 FASES DEL PROYECTO

### **FASE 0: SETUP INICIAL** (Conocimientos generales)
Objetivos: Configurar entorno local, entender estructura, preparar herramientas

#### Backend Setup
- [ ] Investigar: ¿Qué es un virtual environment en Python? ¿Por qué es importante?
  - *Tarea*: Crear un virtual environment en `BackEnd/` usando `venv`
  - Verifica que `python -m venv` funciona en tu SO

- [ ] Investigar: ¿Qué es `requirements.txt` y cómo gestiona dependencias?
  - *Tarea*: Crear `BackEnd/requirements.txt` con las dependencias iniciales necesarias:
    - `fastapi`
    - `uvicorn`
    - `sqlalchemy`
    - `psycopg2-binary` (para PostgreSQL)
    - `python-dotenv` (para variables de entorno)
    - `pyjwt` (para JWT)
    - `python-multipart`
    - `email-validator`

- [ ] Instalar todas las dependencias en el virtual environment
  - Verifica que `pip list` muestra los paquetes

- [ ] Crear archivo `.env` en `BackEnd/` para variables de entorno (NO commitear)
  - Estructura inicial: `DATABASE_URL`, `SECRET_KEY`, `EMAIL_USER`, `EMAIL_PASSWORD`
  - Crear `.gitignore` si no existe (incluir `.env`, `venv/`, `__pycache__/`)

- [ ] Investigar: ¿Qué son las variables de entorno y por qué no debes commitear `.env`?

#### Frontend Setup
- [ ] Investigar: ¿Qué es `package-lock.json`? ¿Por qué hace falta?
  - *Tarea*: Verificar que existe en `FrontEnd/` (ya debería estar)

- [ ] Verificar instalación de dependencias React
  - Ejecutar `npm install` en `FrontEnd/` (si necesita actualizar)
  - Verificar que `node_modules/` contiene las dependencias

- [ ] Investigar: ¿Qué son TypeScript y cómo ayuda en grandes proyectos?
  - *Tarea*: Revisar `tsconfig.json` en `FrontEnd/`
  - Entender qué hace cada configuración clave

- [ ] Agregar dependencias necesarias para Frontend:
  - Investigar cuál es el mejor router para React (hint: react-router)
  - Investigar estado global (hint: Context API vs Redux vs Zustand)
  - Instalar las herramientas elegidas (sin decisión del senior, TÚ investiga las pros/cons)

#### DevOps Setup
- [ ] Investigar: ¿Para qué sirve Docker? ¿Qué es una imagen vs un contenedor?

- [ ] Crear estructura de carpetas Docker:
  - `BackEnd/Dockerfile` (aún vacío, lo llenarás después)
  - `FrontEnd/Dockerfile` (aún vacío)
  - `docker-compose.yml` en raíz del proyecto

- [ ] Investigar: ¿Qué es `docker-compose`? ¿Por qué usarlo en lugar de `docker` a secas?

---

### **FASE 1: ARQUITECTURA BACKEND**
Objetivos: Estructura sólida, configuración centralizada, modelos de BD

#### 1.1 - Configuración centralizada
- [ ] Investigar: ¿Qué es configuración de aplicación? ¿Por qué no hardcodear valores?

- [ ] Crear `BackEnd/app/core/config.py`:
  - Clase `Settings` que lee variables de `.env`
  - Métodos para obtener `DATABASE_URL`, `SECRET_KEY`, etc.
  - Investigar: ¿Cómo usar `pydantic` para validar configuración?

- [ ] Crear `BackEnd/app/core/security.py`:
  - Funciones para hashear contraseñas (investigar: ¿qué es bcrypt?)
  - Función para verificar contraseñas
  - Funciones para generar y validar JWT tokens
  - Investigar: ¿Cómo funciona JWT? ¿Qué payload incluir?

#### 1.2 - Base de datos y modelos
- [ ] Investigar: ¿Qué es un ORM? ¿Cómo SQLAlchemy facilita trabajar con BD?

- [ ] Crear `BackEnd/app/data/database.py`:
  - Configurar conexión a SQLite (desarrollo) y PostgreSQL (producción)
  - Crear `SessionLocal` para manejar sesiones
  - Investigar: ¿Qué es una sesión en BD? ¿Por qué es importante cerrarla?

- [ ] Crear `BackEnd/app/models/user.py`:
  - Modelo SQLAlchemy para tabla `users`
  - Campos: `id`, `username`, `email`, `password_hash`, `created_at`, `updated_at`
  - Investigar: ¿Qué es una relación 1-a-N? ¿Cómo se implementa en SQLAlchemy?

- [ ] Crear `BackEnd/app/models/task.py`:
  - Modelo SQLAlchemy para tabla `tasks`
  - Campos: `id`, `user_id` (FK), `name`, `description`, `start_date`, `end_date`, `status`, `created_at`, `updated_at`
  - Status enum: `"En espera"`, `"En proceso"`, `"Finalizado"`
  - Relación con User (un usuario puede tener muchas tareas)

- [ ] Crear `BackEnd/app/models/__init__.py`:
  - Exportar todos los modelos para fácil importación

- [ ] Investigar: ¿Qué son las migraciones? ¿Por qué usarlas en lugar de crear tablas manualmente?
  - (Nota: Haremos esto en fase posterior con Alembic si avanzamos)

#### 1.3 - Schemas Pydantic (Validación de datos)
- [ ] Investigar: ¿Qué es Pydantic? ¿Por qué no usar los modelos SQLAlchemy directamente en APIs?

- [ ] Crear `BackEnd/app/schemas/user.py`:
  - Schema `UserRegister`: email, username, password (con validaciones)
  - Schema `UserLogin`: username, password
  - Schema `UserResponse`: id, username, email (SIN contraseña)
  - Schema `PasswordReset`: email
  - Schema `PasswordResetConfirm`: code, new_password
  - Investigar: ¿Cómo validar formato de email? ¿Qué es una contraseña fuerte?

- [ ] Crear `BackEnd/app/schemas/task.py`:
  - Schema `TaskCreate`: name, description, start_date, end_date
  - Schema `TaskUpdate`: name, description, start_date, end_date, status
  - Schema `TaskResponse`: id, user_id, name, description, start_date, end_date, status, created_at, updated_at
  - Schema `TaskListResponse`: lista de TaskResponse

- [ ] Crear `BackEnd/app/schemas/__init__.py`:
  - Exportar todos los schemas

#### 1.4 - Servicios (Lógica de negocio)
- [ ] Investigar: ¿Cuál es la diferencia entre endpoints y servicios? ¿Por qué separarlos?

- [ ] Crear `BackEnd/app/services/user_service.py`:
  - `create_user(db, user_data)`: crear usuario nuevo
    - Validar que email no existe
    - Hashear contraseña
    - Guardar en BD
    - Investigar: ¿Qué hacer si hay error de integridad (email duplicado)?

  - `get_user_by_email(db, email)`: recuperar usuario por email
  - `get_user_by_username(db, username)`: recuperar usuario por username
  - `get_user_by_id(db, user_id)`: recuperar usuario por ID
  - `verify_password(db, user_id, password)`: verificar contraseña

  - `request_password_reset(db, email)`:
    - Generar código de 8 dígitos
    - Guardar código en BD con timestamp de expiración
    - (Después: enviar por email)
    - Investigar: ¿Cómo generar códigos seguros?

  - `reset_password(db, email, code, new_password)`:
    - Validar código no expirado
    - Validar contraseña nueva
    - Actualizar contraseña
    - Limpiar código usado

- [ ] Crear `BackEnd/app/services/task_service.py`:
  - `create_task(db, user_id, task_data)`: crear tarea
  - `get_task(db, task_id, user_id)`: obtener tarea (validar que pertenece al usuario)
  - `get_user_tasks(db, user_id)`: obtener todas las tareas del usuario
  - `get_user_tasks_in_progress(db, user_id)`: filtro para "En proceso"
  - `update_task(db, task_id, user_id, task_data)`: actualizar tarea
  - `delete_task(db, task_id, user_id)`: eliminar tarea
  - `update_task_status_automatic(db)`: función para actualizar estados automáticos basado en fechas
    - ¿Quién llama a esto? (Investigar: ¿cron jobs? ¿background tasks?)

- [ ] Crear `BackEnd/app/services/email_service.py`:
  - `send_password_reset_email(email, code)`: enviar email con código
  - Investigar: ¿Cómo usar Gmail SMTP? ¿Qué es una "app password"?
  - (Por ahora: template simple en texto)

#### 1.5 - Dependencias inyectadas
- [ ] Investigar: ¿Qué es inyección de dependencias? ¿Por qué FastAPI lo usa?

- [ ] Crear `BackEnd/app/core/dependencies.py`:
  - `get_db()`: dependencia para obtener sesión de BD
  - `get_current_user()`: dependencia para obtener usuario autenticado desde JWT
  - Investigar: ¿Cómo extraer JWT del header `Authorization`?
  - `verify_jwt_token(token)`: verificar y decodificar JWT

---

### **FASE 2: ENDPOINTS BACKEND**
Objetivos: APIs REST completas y seguras

#### 2.1 - Autenticación
- [ ] Crear `BackEnd/app/APIs/auth.py`:
  - `POST /auth/register`: registrar nuevo usuario
    - Validar datos con schema `UserRegister`
    - Llamar a `create_user` del servicio
    - Retornar token JWT si es exitoso
    - Investigar: ¿Qué status codes HTTP devolver?

  - `POST /auth/login`: login con credenciales
    - Validar datos con schema `UserLogin`
    - Buscar usuario, verificar contraseña
    - Generar y retornar JWT
    - Investigar: ¿Qué incluir en el JWT payload? ¿Cuánto tiempo debe expirar?

  - `POST /auth/request-password-reset`: solicitar código de reset
    - Recibir `email`
    - Llamar a `request_password_reset`
    - Responder que se envió código (SIN revelar si email existe)
    - Investigar: ¿Por qué es importante no revelar si un email existe?

  - `POST /auth/reset-password`: cambiar contraseña con código
    - Validar con schema `PasswordResetConfirm`
    - Llamar a `reset_password`
    - Retornar mensaje de éxito

  - `GET /auth/me`: obtener datos del usuario actual
    - Requiere autenticación (JWT)
    - Retornar usuario autenticado sin contraseña
    - Investigar: ¿Cómo marcar un endpoint como "requiere auth"?

#### 2.2 - Tareas
- [ ] Crear `BackEnd/app/APIs/tasks.py`:
  - `POST /tasks`: crear nueva tarea
    - Requiere autenticación
    - Validar con schema `TaskCreate`
    - Llamar a `create_task` del servicio
    - Retornar tarea creada

  - `GET /tasks`: obtener todas las tareas del usuario
    - Requiere autenticación
    - Filtro opcional por status
    - Retornar lista de tareas con paginación (investigar: ¿por qué pagination?)

  - `GET /tasks/in-progress`: obtener tareas "En proceso"
    - Requiere autenticación
    - Usar `get_user_tasks_in_progress`

  - `GET /tasks/{task_id}`: obtener tarea específica
    - Requiere autenticación
    - Validar que pertenece al usuario

  - `PUT /tasks/{task_id}`: actualizar tarea
    - Requiere autenticación
    - Validar datos con schema `TaskUpdate`

  - `DELETE /tasks/{task_id}`: eliminar tarea
    - Requiere autenticación
    - Validar que pertenece al usuario

  - `PATCH /tasks/{task_id}/mark-complete`: marcar tarea como finalizada
    - Requiere autenticación
    - Actualizar status a "Finalizado"

#### 2.3 - Integración en main.py
- [ ] Actualizar `BackEnd/app/main.py`:
  - Importar routers de `auth` y `tasks`
  - Incluir routers con prefijos (`/api/auth`, `/api/tasks`)
  - Investigar: ¿Por qué usar prefijos en las rutas?
  - Mantener health check `/`

- [ ] Investigar: ¿Qué es CORS? ¿Por qué lo necesito?
  - Configurar CORS en FastAPI para que el frontend pueda acceder al backend
  - Especificar solo orígenes permitidos (no `*` en producción)

#### 2.4 - Manejo de errores
- [ ] Investigar: ¿Cuál es la diferencia entre `HTTPException`, `ValueError`, etc.?

- [ ] Crear `BackEnd/app/utils/exceptions.py`:
  - Excepciones personalizadas:
    - `UserAlreadyExists`
    - `UserNotFound`
    - `InvalidCredentials`
    - `TokenExpired`
    - `TaskNotFound`
    - `UnauthorizedAccess`

  - Investigar: ¿Cómo mapear estas excepciones a respuestas HTTP?

- [ ] Agregar exception handlers en `main.py`:
  - Manejar cada excepción personalizada
  - Retornar JSON con mensaje y status code apropiado
  - Investigar: ¿Cómo loguear errores para debugging?

---

### **FASE 3: ARQUITECTURA FRONTEND**
Objetivos: Estructura componentes, manejo de estado, comunicación con backend

#### 3.1 - Estructura de carpetas
- [ ] Investigar: ¿Cuál es la estructura estándar de proyectos React profesionales?

- [ ] Crear estructura en `FrontEnd/src/`:
  ```
  src/
  ├── components/       # Componentes reutilizables pequeños
  ├── pages/           # Páginas/vistas principales
  ├── services/        # Lógica (API calls, etc)
  ├── contexts/        # Context API para estado global
  ├── hooks/           # Custom hooks
  ├── types/           # Tipos TypeScript
  ├── utils/           # Utilidades
  ├── styles/          # Estilos globales
  ├── App.tsx
  └── main.tsx
  ```

#### 3.2 - Tipos TypeScript
- [ ] Crear `FrontEnd/src/types/index.ts`:
  - Tipos para `User`: id, username, email
  - Tipos para `Task`: id, name, description, start_date, end_date, status
  - Tipos para respuestas API
  - Tipos para errores
  - Investigar: ¿Cómo crear tipos reutilizables?

#### 3.3 - Servicio API
- [ ] Crear `FrontEnd/src/services/api.ts`:
  - Configurar cliente HTTP (fetch o axios)
  - Investigar: ¿Fetch vs Axios? ¿Ventajas de cada uno?
  - Agregar interceptor para incluir JWT en headers
  - Métodos para:
    - `register(email, username, password)`
    - `login(username, password)`
    - `getCurrentUser()`
    - `requestPasswordReset(email)`
    - `resetPassword(email, code, newPassword)`
    - `getTasks()`
    - `getTasksInProgress()`
    - `getTask(taskId)`
    - `createTask(taskData)`
    - `updateTask(taskId, taskData)`
    - `deleteTask(taskId)`
    - `markTaskComplete(taskId)`

#### 3.4 - Contexto de autenticación
- [ ] Investigar: ¿Qué es Context API? ¿Cuándo usarlo vs Redux?

- [ ] Crear `FrontEnd/src/contexts/AuthContext.tsx`:
  - Estado: `user`, `isAuthenticated`, `isLoading`, `error`
  - Acciones: `login`, `register`, `logout`, `getCurrentUser`
  - Guardar token en `localStorage` (investigar: ¿es seguro? ¿alternativas?)
  - Providar a toda la app en `main.tsx`

- [ ] Crear `FrontEnd/src/hooks/useAuth.ts`:
  - Hook personalizado para acceder al contexto fácilmente
  - Retornar: user, isAuthenticated, login, register, logout

#### 3.5 - Contexto de tareas
- [ ] Crear `FrontEnd/src/contexts/TaskContext.tsx`:
  - Estado: `tasks`, `tasksInProgress`, `isLoading`, `error`
  - Acciones: `fetchTasks`, `fetchTasksInProgress`, `createTask`, `updateTask`, `deleteTask`, `markComplete`
  - Providar a toda la app

- [ ] Crear `FrontEnd/src/hooks/useTasks.ts`:
  - Hook para acceder a contexto de tareas

#### 3.6 - Rutas
- [ ] Investigar: ¿Cómo funciona React Router v6?

- [ ] Crear `FrontEnd/src/App.tsx`:
  - Configurar rutas principales:
    - `/login` - Página login (público)
    - `/register` - Página registro (público)
    - `/forgot-password` - Página recuperación (público)
    - `/reset-password/:token` - Página cambio contraseña (público)
    - `/dashboard` - Dashboard principal (protegido)
    - Rutas no encontradas: 404

  - Investigar: ¿Cómo proteger rutas? (ProtectedRoute component)
  - Investigar: ¿Cómo hacer redirect si no estás autenticado?

---

### **FASE 4: COMPONENTES Y PÁGINAS FRONTEND**
Objetivos: UI funcional para cada feature

#### 4.1 - Componentes comunes
- [ ] Crear `FrontEnd/src/components/Navbar.tsx`:
  - Logo/Nombre de app
  - Nombre de usuario (si autenticado)
  - Botón logout
  - Investigar: ¿Componentes de UI? ¿Tailwind CSS? ¿Material UI?

- [ ] Crear `FrontEnd/src/components/Sidebar.tsx`:
  - Mostrar usuario autenticado
  - Botón "Ver todas las tareas"
  - Botón "Cerrar sesión"

- [ ] Crear `FrontEnd/src/components/Loading.tsx`:
  - Spinner/loader reutilizable

- [ ] Crear `FrontEnd/src/components/ErrorMessage.tsx`:
  - Mostrar errores en formato consistente

#### 4.2 - Páginas de autenticación
- [ ] Crear `FrontEnd/src/pages/LoginPage.tsx`:
  - Formulario: username/email, password
  - Validación en cliente
  - Llamar a `login()` del contexto
  - Redirect a `/dashboard` si exitoso
  - Mostrar errores
  - Link a registro y recuperación de contraseña

- [ ] Crear `FrontEnd/src/pages/RegisterPage.tsx`:
  - Formulario: email, username, password, confirm password
  - Validaciones:
    - Email formato válido
    - Contraseña suficientemente fuerte
    - Contraseñas coinciden
  - Llamar a `register()` del contexto
  - Redirect a `/login` si exitoso

- [ ] Crear `FrontEnd/src/pages/ForgotPasswordPage.tsx`:
  - Formulario: email
  - Llamar a `requestPasswordReset()`
  - Mostrar mensaje: "Revisa tu correo"

- [ ] Crear `FrontEnd/src/pages/ResetPasswordPage.tsx`:
  - Formulario: código de 8 dígitos, nueva contraseña, confirmar contraseña
  - Validaciones de contraseña
  - Llamar a `resetPassword()`
  - Redirect a login si exitoso

#### 4.3 - Dashboard y gestión de tareas
- [ ] Crear `FrontEnd/src/pages/DashboardPage.tsx`:
  - Layout con Sidebar + contenido principal
  - Mostrar tareas "En proceso"
  - Botón para "Ver todas las tareas"
  - Botón para "Crear nueva tarea"

- [ ] Crear `FrontEnd/src/pages/AllTasksPage.tsx`:
  - Lista de todas las tareas del usuario
  - Filtro por status
  - Búsqueda por nombre
  - Acciones: editar, eliminar, marcar completo

- [ ] Crear `FrontEnd/src/components/TaskCard.tsx`:
  - Mostrar: nombre, descripción, fechas, status
  - Botones: editar, marcar completo, eliminar
  - Colores diferentes según status

- [ ] Crear `FrontEnd/src/components/TaskForm.tsx`:
  - Formulario para crear/editar tarea
  - Campos: nombre, descripción, fecha inicio, fecha fin
  - Validar fechas (inicio < fin)
  - Investigar: ¿Componente date picker? (rechazar inputs manuales inseguros)

- [ ] Crear `FrontEnd/src/components/TaskList.tsx`:
  - Mostrar lista de tareas
  - Usar TaskCard para cada tarea
  - Mensaje si no hay tareas

---

### **FASE 5: LÓGICA DE NEGOCIO AVANZADA**
Objetivos: Funcionalidades complexas, actualizaciones automáticas

#### 5.1 - Estados automáticos de tareas
- [ ] Investigar: ¿Cómo actualizar estados basado en fechas?
  - ¿En el frontend? ¿En el backend? ¿Ambos?

- [ ] Implementar en backend (`task_service.py`):
  - Función `update_task_statuses()` que:
    - Hoy < start_date → "En espera"
    - start_date <= Hoy <= end_date → "En proceso"
    - Hoy > end_date y status ≠ "Finalizado" → ¿"Vencida"? (ajusta según reqs)

  - Preguntar: ¿Cuándo ejecutar? ¿Cada request? ¿Cron job? ¿WebSocket?

- [ ] Implementar en frontend:
  - Mostrar visualmente estados automáticos
  - Si tarea "En proceso" expira, actualizar estado
  - Investigar: ¿Debo revalidar desde el servidor?

#### 5.2 - Recuperación de contraseña mejorada
- [ ] Actualizar email service:
  - Usar template HTML en lugar de texto plano
  - Incluir link con código (opcional: link directo)
  - Incluir información de seguridad

- [ ] Investigar: ¿Qué hacer si usuario intenta reset con email no registrado?
  - Política: responder siempre "Revisa tu correo" (no revelar usuarios)

#### 5.3 - Notificaciones
- [ ] Investigar: ¿Cómo notificar al usuario de cambios?
  - Opciones: Toast messages, banners, email
  - (Basic para ahora: Toast en el frontend)

- [ ] Crear sistema de notificaciones simple:
  - `FrontEnd/src/components/Toast.tsx`
  - Contexto de notificaciones (o integrar en contexto existente)

---

### **FASE 6: TESTING**
Objetivos: Asegurar calidad del código

#### 6.1 - Testing Backend
- [ ] Investigar: ¿Qué es testing? ¿Qué frameworks existen para Python?
  - Hint: `pytest`, `unittest`

- [ ] Crear `BackEnd/tests/` directorio

- [ ] Escribir tests para servicios (`tests/test_services/`):
  - `test_user_service.py`: tests para crear usuario, login, reset password
  - `test_task_service.py`: tests para crear, actualizar, eliminar tareas
  - Investigar: ¿Cómo usar fixtures? ¿Cómo mock BD?

- [ ] Escribir tests para endpoints (`tests/test_APIs/`):
  - `test_auth.py`: tests para endpoints de autenticación
  - `test_tasks.py`: tests para endpoints de tareas
  - Investigar: ¿TestClient de FastAPI?

- [ ] Ejecutar tests localmente:
  - `pytest` desde `BackEnd/`
  - Verificar que todos pasen

#### 6.2 - Testing Frontend
- [ ] Investigar: ¿Qué es testing en React? ¿Vitest? ¿Jest?

- [ ] Crear `FrontEnd/__tests__/` o similar

- [ ] Escribir tests básicos:
  - Tests que componentes renderizen sin errores
  - Tests que botones disparen acciones
  - Investigar: ¿React Testing Library?

---

### **FASE 7: DOCKERIZACIÓN**
Objetivos: Containerizar para producción

#### 7.1 - Backend Dockerfile
- [ ] Investigar: ¿Cómo funciona un Dockerfile? ¿Multi-stage builds?

- [ ] Crear `BackEnd/Dockerfile`:
  - Stage 1 (dev): instalar dependencias, copiar código
  - Stage 2 (prod): optimizar, reducir tamaño
  - Usar imagen oficial de Python
  - Exponer puerto 8000
  - CMD: ejecutar `uvicorn app.main:app --host 0.0.0.0 --port 8000`

- [ ] Crear `BackEnd/.dockerignore`:
  - Excluir: `__pycache__`, `.pyc`, venv, etc.

#### 7.2 - Frontend Dockerfile
- [ ] Crear `FrontEnd/Dockerfile`:
  - Stage 1: build con Node
  - Stage 2: servir con Nginx
  - Investigar: ¿Por qué Nginx? ¿Alternativas?

- [ ] Crear `FrontEnd/.dockerignore`:
  - Excluir: `node_modules`, archivo build anterior

#### 7.3 - docker-compose.yml
- [ ] Investigar: ¿Cómo funciona docker-compose?

- [ ] Crear/actualizar `docker-compose.yml`:
  - Servicio `backend`: imagen del Dockerfile de FastAPI
  - Servicio `frontend`: imagen del Dockerfile de React
  - Servicio `db`: PostgreSQL (o SQLite en dev)
  - Volúmenes para persistencia
  - Variables de entorno desde `.env`
  - Networks para comunicación entre servicios
  - Investigar: ¿Health checks?

- [ ] Probar localmente:
  - `docker-compose up` desde raíz del proyecto
  - Acceder a http://localhost:3000 (frontend)
  - Acceder a http://localhost:8000 (backend)

#### 7.4 - Optimización de imágenes
- [ ] Investigar: ¿Cómo reducir el tamaño de imágenes Docker?

- [ ] Aplicar optimizaciones:
  - Usar imágenes base pequeñas (ej: `python:3.11-slim`)
  - Combinar RUN commands
  - Usar `.dockerignore`
  - Limpiar caches en Docker

---

### **FASE 8: DEPLOYMENT**
Objetivos: Publicar en producción

#### 8.1 - Preparación
- [ ] Investigar: ¿Qué es un VPS? ¿Alternativas? (DigitalOcean, AWS, Heroku, Railway, Render, etc)
  - Pros/cons de cada uno para un proyecto pequeño

- [ ] Crear archivo `.env.example`:
  - Template de variables de entorno (SIN valores reales)
  - Documentar qué es cada variable

- [ ] Actualizar documentación en `README.md`:
  - Cómo instalar localmente
  - Cómo ejecutar con docker-compose
  - Cómo hacer deploy
  - Estructura del proyecto

#### 8.2 - Considerar: CI/CD
- [ ] Investigar: ¿Qué es CI/CD? ¿GitHub Actions?

- [ ] Crear `.github/workflows/`:
  - Pipeline para ejecutar tests automáticamente
  - Pipeline para build y push a Docker registry (opcional)
  - Trigger: en cada push a main

#### 8.3 - Considerar: Base de datos en producción
- [ ] Investigar: ¿PostgreSQL en contenedor vs servicio gestionado?
  - Para pequeño proyecto: servicio gestionado (ej: Supabase, Heroku Postgres)
  - Backup automático
  - Monitoreo

- [ ] Migrar a PostgreSQL:
  - Investigar Alembic para migraciones
  - Crear migraciones iniciales
  - Documentar proceso de migración

---

### **FASE 9: MEJORAS Y PULIDO**
Objetivos: Experiencia de usuario, seguridad adicional, monitoreo

#### 9.1 - Seguridad en profundidad
- [ ] Investigar: ¿Qué es CSRF? ¿CORS seguro?
  - Configurar CORS correctamente (solo orígenes permitidos)

- [ ] Investigar: ¿Qué es rate limiting?
  - Implementar en FastAPI: limitar requests por IP/usuario

- [ ] Investigar: ¿Cómo proteger contraseñas? Validaciones adicionales
  - Requisitos: longitud mín, caracteres especiales, números, mayúsculas

- [ ] Investigar: ¿Qué es HTTPS? ¿Certificados SSL?
  - En producción: usar HTTPS obligatoriamente
  - Let's Encrypt (gratuito)

#### 9.2 - Logging y monitoreo
- [ ] Investigar: ¿Qué eventos loguear?
  - Logins/logouts
  - Errores de autenticación
  - Cambios de contraseña
  - Acciones en tareas

- [ ] Implementar logging en backend:
  - Usar módulo `logging` de Python
  - Diferentes niveles: DEBUG, INFO, WARNING, ERROR
  - Guardar en archivos o servicio de logging

- [ ] Investigar: ¿Qué es Sentry? ¿Otros servicios de error tracking?

#### 9.3 - UX/UI mejoras
- [ ] Investigar: ¿Cuál es la mejor librería de componentes UI?
  - Opciones: Shadcn/ui, Material UI, Tailwind, daisyUI

- [ ] Mejorar diseño del frontend:
  - Paleta de colores consistente
  - Tipografía profesional
  - Responsive design (mobile, tablet, desktop)
  - Dark mode (opcional)

- [ ] Accesibilidad:
  - Alt text en imágenes
  - ARIA labels
  - Navegación con teclado
  - Investigar: WCAG 2.1

#### 9.4 - Analytics básico
- [ ] Considerar: ¿Quiero saber cómo usan la aplicación?
  - Opciones: Google Analytics, Mixpanel, custom logging

---

### **FASE 10: DOCUMENTACIÓN Y FINALES**
Objetivos: Código mantenible, listo para otros desarrolladores

#### 10.1 - Documentación de código
- [ ] Documentar funciones complejas:
  - Docstrings en Python (Google style o NumPy)
  - JSDoc en JavaScript/TypeScript
  - ¿Cómo documentar una API (OpenAPI/Swagger)?

- [ ] Crear `BackEnd/API_DOCS.md`:
  - Documenta cada endpoint
  - Ejemplos de request/response
  - Códigos de error posibles
  - Investigar: generar automáticamente con Swagger

#### 10.2 - README mejorado
- [ ] Actualizar `README.md` con:
  - Descripción del proyecto
  - Tech stack
  - Cómo instalar
  - Cómo ejecutar (local y docker)
  - Estructura de carpetas
  - Cómo contribuir
  - Licencia
  - Contacto/autor

#### 10.3 - Checklist de lanzamiento
- [ ] Antes de lanzar a producción:
  - [ ] Todos los tests pasan
  - [ ] No hay secrets en git
  - [ ] Variables de entorno configuradas
  - [ ] HTTPS habilitado
  - [ ] Backups automáticos de BD
  - [ ] Logging configurado
  - [ ] Errores monitoreados (Sentry o similar)
  - [ ] Performance baseline (carga mínima aceptable)
  - [ ] Documentación actualizada

#### 10.4 - Post-lanzamiento
- [ ] Monitorear en producción:
  - Errores en logs
  - Performance
  - Experiencia de usuario

- [ ] Recopilar feedback:
  - ¿Qué funciona? ¿Qué no?
  - Priorizar mejoras futuras

---

## 📊 MATRIZ DE DEPENDENCIAS

```
FASE 0: Setup ┐
              ├─> FASE 1: Arquitectura Backend ┐
              ├─> FASE 3: Arquitectura Frontend ┐
              ├─> FASE 7: Docker ┐
                                 ├─> FASE 2: Endpoints Backend ─┬─> FASE 5: Lógica avanzada ┐
                                                                  ├─> FASE 4: UI Frontend ─┤
                                                                                            ├─> FASE 6: Testing ┐
                                                                                                               ├─> FASE 8: Deployment
                                                                                                               ├─> FASE 9: Mejoras
                                                                                                               └─> FASE 10: Documentación
```

---

## 🎯 PRÓXIMOS PASOS

1. ✅ Leer este TODO.md completamente
2. ⏭️ Empezar por **FASE 0: Setup Inicial** (Backend Setup primero)
3. 📚 Investigar cada concepto listado (no saltear)
4. 💻 Implementar pequeño paso a pequeño paso
5. ✔️ Marcar cada checkbox cuando completes la tarea
6. 🤔 Si tienes dudas, investiga antes de preguntar

---

## 📌 NOTAS FINALES

- **Este documento es vivo**: Actualízalo con lo que aprendas
- **No hay prisa**: Cada fase es una oportunidad de aprender
- **Principio DRY**: Don't Repeat Yourself - reutiliza código
- **Testing first**: Escribe tests mientras desarrollas, no después
- **Git commits claros**: Un cambio = Un commit pequeño
- **Seguridad desde el inicio**: No lo dejes para después

**¡Adelante, dev! 🚀**
