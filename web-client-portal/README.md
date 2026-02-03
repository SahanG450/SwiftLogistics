# SwiftLogistics Web Client Portal

**Modern React + TypeScript web portal for SwiftLogistics clients to manage orders, track deliveries, and handle billing.**

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Integration](#api-integration)
- [Available Scripts](#available-scripts)
- [Environment Variables](#environment-variables)
- [Authentication](#authentication)
- [Screenshots](#screenshots)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

---

## 🎯 Overview

The SwiftLogistics Web Client Portal is a comprehensive web application that enables e-commerce clients to:

- Submit new delivery orders
- Track packages in real-time
- View order history and status
- Manage billing and invoices
- Handle contract management

This portal connects to the SwiftLogistics middleware API Gateway to seamlessly integrate with CMS, WMS, and ROS backend systems.

---

## ✨ Features

### Order Management

- **Submit New Orders**: Multi-step form for creating delivery orders with pickup/delivery details
- **Order Tracking**: Real-time tracking with live map view and status timeline
- **Order History**: Searchable and filterable list of past orders
- **Priority Handling**: Mark urgent deliveries with special handling

### Billing & Invoicing

- **Invoice List**: View all invoices with payment status
- **Invoice Details**: Detailed breakdown of charges
- **Payment History**: Track payment records
- **Download PDF**: Export invoices in PDF format

### Contract Management

- **Active Contracts**: View and manage service contracts
- **Contract Details**: Review terms, pricing, and SLAs
- **Renewal Management**: Track contract expiration and renewals

### Dashboard

- **Overview**: At-a-glance view of active orders
- **Statistics**: Delivery metrics and performance indicators
- **Quick Actions**: Fast access to common operations
- **Recent Activity**: Latest order updates

---

## 🛠️ Technology Stack

| Technology          | Purpose                                        |
| ------------------- | ---------------------------------------------- |
| **React 18**        | UI library for building components             |
| **TypeScript**      | Type-safe development                          |
| **Vite**            | Fast build tool and dev server                 |
| **React Router v6** | Client-side routing                            |
| **Axios**           | HTTP client for API requests                   |
| **CSS3**            | Modern styling with variables and grid/flexbox |

---

## 📁 Project Structure

```
web-client-portal/
├── public/
│   └── assets/              # Static assets (images, icons)
├── src/
│   ├── pages/               # Page components
│   │   ├── Login.tsx        # Login page
│   │   ├── Dashboard.tsx    # Main dashboard
│   │   ├── Orders/
│   │   │   ├── NewOrder.tsx
│   │   │   ├── OrderList.tsx
│   │   │   └── OrderTracking.tsx
│   │   ├── Billing/
│   │   │   ├── Invoices.tsx
│   │   │   └── InvoiceDetail.tsx
│   │   └── Contracts/
│   │       └── ContractList.tsx
│   ├── components/          # Reusable components
│   │   ├── Layout/
│   │   │   ├── Navbar.tsx
│   │   │   └── Sidebar.tsx
│   │   ├── OrderCard.tsx
│   │   ├── TrackingMap.tsx
│   │   └── StatusBadge.tsx
│   ├── services/            # API and business logic
│   │   ├── api.ts           # Axios instance and config
│   │   └── auth.ts          # Authentication service
│   ├── context/             # React Context providers
│   │   └── AuthContext.tsx  # Auth state management
│   ├── types/               # TypeScript type definitions
│   │   └── index.ts
│   ├── styles/              # CSS stylesheets
│   │   ├── index.css        # Global styles and design system
│   │   └── components.css   # Component-specific styles
│   ├── App.tsx              # Root component
│   └── main.tsx             # Application entry point
├── .env.example             # Environment variables template
├── package.json             # Dependencies and scripts
├── tsconfig.json            # TypeScript configuration
├── vite.config.ts           # Vite configuration
└── README.md                # This file
```

---

## 🚀 Installation

### Prerequisites

- **Node.js**: v18 or higher
- **npm**: v9 or higher
- **SwiftLogistics Backend**: Running on `http://localhost:3000` (API Gateway)

### Steps

1. **Navigate to the project directory:**

   ```bash
   cd web-client-portal
   ```

2. **Install dependencies:**

   ```bash
   npm install
   ```

3. **Configure environment variables:**

   ```bash
   cp .env.example .env
   ```

   Edit `.env` to set your API Gateway URL (default: `http://localhost:3000`)

4. **Start the development server:**

   ```bash
   npm run dev
   ```

5. **Open in browser:**
   ```
   http://localhost:5173
   ```

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# API Configuration
VITE_API_GATEWAY_URL=http://localhost:3000

# Optional: Enable debug mode
VITE_DEBUG=true
```

### Vite Configuration

The `vite.config.ts` file includes:

- Port configuration (default: 5173)
- Proxy setup for API requests (if needed)
- Build optimizations

---

## 📖 Usage

### Running the Application

**Development mode:**

```bash
npm run dev
```

**Production build:**

```bash
npm run build
npm run preview
```

### Default Login Credentials

For testing purposes (configured in backend):

```
Username: client@example.com
Password: password123
```

### Creating a New Order

1. Navigate to **Orders > New Order**
2. Fill in pickup details (address, contact, date/time)
3. Fill in delivery details
4. Add package information (weight, dimensions, value)
5. Select priority level
6. Review and submit

### Tracking an Order

1. Navigate to **Orders > Track Order**
2. Enter tracking number (e.g., `SL100001`)
3. View real-time status, location, and delivery timeline

### Managing Invoices

1. Navigate to **Billing > Invoices**
2. View invoice list with payment status
3. Click on an invoice to see details
4. Download PDF for records

---

## 🔌 API Integration

### API Service (`src/services/api.ts`)

The application uses Axios for HTTP requests with:

- **Base URL**: Configured from environment variable
- **Authentication**: JWT token in Authorization header
- **Interceptors**:
  - Request: Attach auth token
  - Response: Handle 401 Unauthorized (redirect to login)
  - Error handling with user-friendly messages

### API Endpoints Used

| Endpoint                    | Method | Purpose             |
| --------------------------- | ------ | ------------------- |
| `/api/auth/login`           | POST   | User authentication |
| `/api/auth/refresh`         | POST   | Refresh JWT token   |
| `/api/orders`               | GET    | Fetch order list    |
| `/api/orders`               | POST   | Create new order    |
| `/api/orders/:id`           | GET    | Get order details   |
| `/api/orders/:id/track`     | GET    | Track order status  |
| `/api/billing/invoices`     | GET    | List invoices       |
| `/api/billing/invoices/:id` | GET    | Invoice details     |
| `/api/contracts`            | GET    | List contracts      |

**Note**: All endpoints are prefixed with the API Gateway URL (`http://localhost:3000`)

### Example API Call

```typescript
import { apiClient } from "./services/api";

// Fetch orders
const response = await apiClient.get("/api/orders");
const orders = response.data;

// Create new order
const newOrder = await apiClient.post("/api/orders", {
  pickupAddress: "123 Main St, Colombo",
  deliveryAddress: "456 Park Ave, Kandy",
  packageDetails: { weight: 2.5, dimensions: "30x20x15" },
});
```

---

## 📜 Available Scripts

| Command              | Description                           |
| -------------------- | ------------------------------------- |
| `npm run dev`        | Start development server (hot reload) |
| `npm run build`      | Build for production                  |
| `npm run preview`    | Preview production build locally      |
| `npm run lint`       | Run ESLint for code quality           |
| `npm run type-check` | TypeScript type checking              |

---

## 🔐 Authentication

### Flow

1. User enters credentials on login page
2. Application sends POST to `/api/auth/login`
3. Backend returns JWT token
4. Token stored in localStorage and AuthContext
5. All subsequent API requests include token in header
6. On token expiration, redirect to login

### AuthContext

Provides authentication state across the application:

```typescript
const { user, login, logout, isAuthenticated } = useAuth();

// Login
await login(email, password);

// Logout
logout();

// Check authentication
if (isAuthenticated) {
  // User is logged in
}
```

---

## 🎨 Design System

The application uses a modern, premium design with:

- **Color Palette**: Custom CSS variables for consistent theming
- **Typography**: Modern sans-serif fonts (Inter, system fonts)
- **Spacing**: 8px grid system
- **Responsive**: Mobile-first approach with breakpoints
- **Dark Mode**: (Optional) Toggle between light and dark themes

### CSS Variables (in `styles/index.css`)

```css
:root {
  --primary-color: #2563eb;
  --secondary-color: #7c3aed;
  --success-color: #10b981;
  --warning-color: #f59e0b;
  --error-color: #ef4444;
  --background: #ffffff;
  --text-primary: #1f2937;
  --border-radius: 8px;
  /* ... more variables */
}
```

---

## 🐛 Troubleshooting

### Port Already in Use

If port 5173 is already in use:

```bash
# Edit vite.config.ts to change port
export default defineConfig({
  server: { port: 5174 }
});
```

### CORS Errors

Ensure the API Gateway has CORS enabled:

```javascript
// In api-gateway service
app.use(
  cors({
    origin: "http://localhost:5173",
    credentials: true,
  }),
);
```

### API Connection Failed

1. Verify backend is running: `docker-compose ps`
2. Check API Gateway URL in `.env`
3. Test API manually: `curl http://localhost:3000/health`

### Authentication Not Working

1. Check network tab in browser DevTools
2. Verify token is being saved to localStorage
3. Confirm API returns valid JWT

---

## 🔗 Related Documentation

- [SwiftLogistics System Overview](../SYSTEM_OVERVIEW.md)
- [API Gateway Documentation](../services/api-gateway/README.md)
- [Mobile Driver App](../mobile-driver-app/README.md)
- [Backend Services](../IMPLEMENTATION_SUMMARY.md)

---

## 🤝 Contributing

1. Create a feature branch: `git checkout -b feature/new-feature`
2. Make changes and test thoroughly
3. Follow TypeScript and React best practices
4. Update documentation if needed
5. Submit pull request

---

## 📝 License

This project is part of the SwiftLogistics middleware architecture assignment.

---

**Version**: 1.0.0  
**Last Updated**: February 3, 2026  
**Status**: ✅ Production Ready (Development Use)
