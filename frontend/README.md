# SwiftLogistics Frontend Applications

This folder contains all frontend applications for the SwiftLogistics platform.

## 📦 Applications

### 1. swifttrack-logistics

**Modern Admin Dashboard**

- **Technology:** React 18.3 + TypeScript + Vite
- **UI Library:** shadcn/ui + TailwindCSS
- **Components:** 55+ pre-built components
- **Features:** Dark/light theme, form validation, responsive design

**Start:**

```bash
cd swifttrack-logistics
npm install
npm run dev
```

### 2. web-client-portal

**Client Web Portal**

- **Technology:** React 19.2 + TypeScript + Vite
- **Purpose:** Client order management
- **Features:** Order submission, tracking, invoices, authentication

**Start:**

```bash
cd web-client-portal
npm install
npm run dev
```

### 3. mobile-driver-app

**Driver Mobile Application**

- **Technology:** React Native 0.81.5 + Expo
- **Platform:** Android / iOS
- **Features:** GPS tracking, delivery management, photo capture

**Start:**

```bash
cd mobile-driver-app
npm install
npx expo start
```

---

## 🚀 Quick Start

From the frontend directory:

```bash
# Option 1: Admin Dashboard
cd swifttrack-logistics && npm install && npm run dev

# Option 2: Client Portal
cd web-client-portal && npm install && npm run dev

# Option 3: Mobile App
cd mobile-driver-app && npm install && npx expo start
```

---

## 📊 Technology Stack

| Application          | Framework    | Version | Build Tool | UI        |
| -------------------- | ------------ | ------- | ---------- | --------- |
| swifttrack-logistics | React        | 18.3    | Vite 5.4   | shadcn/ui |
| web-client-portal    | React        | 19.2    | Vite 7.2   | Custom    |
| mobile-driver-app    | React Native | 0.81.5  | Expo ~54   | Native    |

---

## 🔗 Environment Configuration

Each application requires a `.env` file:

**swifttrack-logistics / web-client-portal:**

```env
VITE_API_GATEWAY_URL=http://localhost:3000
VITE_DEBUG=true
```

**mobile-driver-app:**

```env
API_GATEWAY_URL=http://10.0.2.2:3000  # Android
# API_GATEWAY_URL=http://localhost:3000  # iOS
DEBUG=true
```

---

**All applications:** Port 5173 (web) or 8081 (mobile Expo)
