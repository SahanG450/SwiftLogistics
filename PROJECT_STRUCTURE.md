# SwiftLogistics - Complete Project Overview

## 📦 Project Structure

```
SwiftLogistics/
│
├── 📁 frontend/                        # All Frontend Applications
│   ├── swifttrack-logistics/           # Admin Dashboard (React + shadcn/ui)
│   ├── web-client-portal/              # Client Portal (React + Vite)
│   └── mobile-driver-app/              # Driver App (React Native + Expo)
│
├── 📁 services/                        # All Backend Services
│   ├── api-gateway/
│   ├── orchestrator/
│   ├── notification-service/
│   ├── adapters/
│   └── mocks/
│
├── 📁 doc/                             # Documentation
├── 📁 scripts/                         # Utility Scripts
├── 📁 shared/                          # Shared Utilities
│
├── 🐳 docker-compose.yml
├── 📖 FRONTEND_QUICKSTART.md
├── 📖 SYSTEM_OVERVIEW.md
└── 📖 README.md
```

---

## 🎨 Frontend Applications

All frontend apps are in the `frontend/` folder:

### 1. swifttrack-logistics (Admin Dashboard)

**Path:** `frontend/swifttrack-logistics/`

- React 18.3 + TypeScript + Vite
- shadcn/ui component library (55+ components)
- TailwindCSS for styling
- Dark/Light theme support

```bash
cd frontend/swifttrack-logistics
npm install
npm run dev
```

### 2. web-client-portal (Client Portal)

**Path:** `frontend/web-client-portal/`

- React 19.2 + TypeScript + Vite
- Order management for clients
- Authentication system

```bash
cd frontend/web-client-portal
npm install
npm run dev
```

### 3. mobile-driver-app (Driver Mobile App)

**Path:** `frontend/mobile-driver-app/`

- React Native 0.81.5 + Expo
- GPS tracking & delivery management
- Photo capture for proof of delivery

```bash
cd frontend/mobile-driver-app
npm install
npx expo start
```

---

## 🔧 Backend Services

All backend services are in the `services/` folder:

- **API Gateway** - Main API entry point
- **Orchestrator** - Business logic coordination
- **Notification Service** - Email/SMS notifications
- **Adapters** - External integrations
- **Mocks** - Testing services

```bash
docker-compose up -d
```

---

## 🚀 Quick Start

### 1. Start Backend

```bash
docker-compose up -d
```

### 2. Start a Frontend App

```bash
# Admin Dashboard
cd frontend/swifttrack-logistics && npm install && npm run dev

# OR Client Portal
cd frontend/web-client-portal && npm install && npm run dev

# OR Mobile App
cd frontend/mobile-driver-app && npm install && npx expo start
```

---

## 📊 Technology Stack

**Frontend:**
| App | Framework | UI Library |
|-----|-----------|------------|
| swifttrack-logistics | React 18.3 + Vite | shadcn/ui + Tailwind |
| web-client-portal | React 19.2 + Vite | Custom CSS |
| mobile-driver-app | React Native + Expo | React Native |

**Backend:**

- Node.js + TypeScript
- RabbitMQ, MongoDB
- Docker + Docker Compose

---

## 🔗 Ports

| Service             | Port        |
| ------------------- | ----------- |
| API Gateway         | 3000        |
| Frontend Apps (web) | 5173        |
| Mobile App (Expo)   | 8081        |
| MongoDB             | 27017       |
| RabbitMQ            | 5672, 15672 |

---

## 📖 Documentation

- **Frontend:** [frontend/README.md](frontend/README.md)
- **Frontend Setup:** [FRONTEND_QUICKSTART.md](FRONTEND_QUICKSTART.md)
- **System Overview:** [SYSTEM_OVERVIEW.md](SYSTEM_OVERVIEW.md)
- **API Docs:** [doc/README.md](doc/README.md)

---

**Version:** 2.0.0  
**Updated:** February 3, 2026
