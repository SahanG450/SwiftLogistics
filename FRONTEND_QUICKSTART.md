# SwiftLogistics Frontend Setup - Quick Start Guide

This guide will help you set up and run both frontend applications for SwiftLogistics:

1. **Web Client Portal** - React + Vite web application for clients
2. **Mobile Driver App** - React Native + Expo mobile application for drivers

---

## 📋 Prerequisites

Before starting, ensure you have:

### Required Software

- **Node.js**: v18 or higher - [Download](https://nodejs.org/)
- **npm**: v9 or higher (comes with Node.js)
- **Docker** and **Docker Compose** (for backend services)
- **Git** (to clone the repository)

### For Mobile Development

- **Android Development**:
  - Android Studio with Android SDK
  - Android Emulator or physical device
- **iOS Development** (Mac only):
  - Xcode with iOS SDK
  - iOS Simulator or physical device

### Backend Services

- SwiftLogistics middleware must be running
- API Gateway accessible on `http://localhost:3000`

---

## 🚀 Quick Start

### Step 1: Start Backend Services

First, ensure the SwiftLogistics backend is running:

```bash
# Navigate to project root
cd /home/snake/UCSC/UCSC/Year\ 2/sem\ 2/Middleware\ Architecture\ SCS2314/Assignment\ 4/SwiftLogistics

# Start all backend services
docker-compose up -d

# Verify services are running
docker-compose ps

# Check API Gateway health
curl http://localhost:3000/health
```

### Step 2: Setup Web Client Portal

```bash
# Navigate to web portal directory
cd web-client-portal

# Install dependencies (already done if following setup)
npm install

# Create environment file
cp .env.example .env

# Start development server
npm run dev
```

The web portal will be available at: **http://localhost:5173**

### Step 3: Setup Mobile Driver App

```bash
# Navigate to mobile app directory
cd mobile-driver-app

# Install dependencies (already done if following setup)
npm install

# Create environment file
cp .env.example .env

# Start Expo development server
npx expo start
```

Then:

- Press **`a`** to open in Android emulator
- Press **`i`** to open in iOS simulator (Mac only)
- Scan QR code with Expo Go app on physical device

---

## 🔧 Configuration

### Web Portal Configuration

Edit `web-client-portal/.env`:

```env
VITE_API_GATEWAY_URL=http://localhost:3000
VITE_DEBUG=true
```

### Mobile App Configuration

Edit `mobile-driver-app/.env`:

```env
# For Android Emulator
API_GATEWAY_URL=http://10.0.2.2:3000

# For iOS Simulator
# API_GATEWAY_URL=http://localhost:3000

# For physical device (use your computer's local IP)
# API_GATEWAY_URL=http://192.168.1.XXX:3000

DEBUG=true
```

**Finding your local IP:**

- **Linux/Mac**: `ifconfig | grep "inet "`
- **Windows**: `ipconfig`

---

## 👤 Default Test Credentials

### Client Login (Web Portal)

```
Email: client@example.com
Password: password123
```

### Driver Login (Mobile App)

```
Email: driver@example.com
Password: password123
```

---

## 📱 Testing the Applications

### Web Client Portal Test Flow

1. **Login**
   - Navigate to http://localhost:5173
   - Enter client credentials
   - Click "Login"

2. **Submit New Order**
   - Go to "Orders" → "New Order"
   - Fill in pickup details:
     - Address: 123 Main St, Colombo
     - Contact: John Doe, +94771234567
     - Date: Today's date
   - Fill in delivery details:
     - Address: 456 Park Ave, Kandy
     - Contact: Jane Smith, +94779876543
   - Add package details:
     - Weight: 2.5 kg
     - Dimensions: 30x20x15 cm
   - Select priority: STANDARD
   - Submit order

3. **Track Order**
   - Go to "Orders" → "Track Order"
   - Enter tracking number (e.g., SL100001)
   - View real-time status and location

4. **View Invoices**
   - Go to "Billing" → "Invoices"
   - View invoice list
   - Click on invoice to see details

### Mobile Driver App Test Flow

1. **Login**
   - Open app on device/emulator
   - Enter driver credentials
   - Tap "Login"

2. **View Manifest**
   - See today's assigned deliveries
   - Review package details
   - Check delivery addresses

3. **Start Delivery**
   - Tap "Start Route"
   - View optimized route on map
   - Navigate to first delivery

4. **Mark as Delivered**
   - Arrive at delivery location
   - Tap "Mark as Delivered"
   - Capture proof of delivery photo
   - Get recipient signature (optional)
   - Add delivery notes
   - Submit

5. **View Stats**
   - Go to "Profile" tab
   - View today's stats:
     - Deliveries completed
     - Deliveries pending
     - On-time delivery rate

---

## 🛠️ Development Workflow

### Web Portal Development

```bash
cd web-client-portal

# Start dev server with hot reload
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run linter
npm run lint

# Type check
npm run type-check
```

### Mobile App Development

```bash
cd mobile-driver-app

# Start Expo dev server
npx expo start

# Run on Android
npm run android

# Run on iOS (Mac only)
npm run ios

# Run on web (for testing only)
npm run web

# Clear cache and restart
npx expo start -c
```

---

## 🔍 Troubleshooting

### Web Portal Issues

#### Port Already in Use

```bash
# Change port in vite.config.ts
export default defineConfig({
  server: { port: 5174 }
});
```

#### CORS Errors

Ensure API Gateway has CORS enabled for `http://localhost:5173`

#### API Connection Failed

1. Verify backend is running: `docker-compose ps`
2. Check API Gateway: `curl http://localhost:3000/health`
3. Verify `.env` file has correct API_GATEWAY_URL

### Mobile App Issues

#### Cannot Connect to Backend

**Android Emulator:**

- Use `10.0.2.2` instead of `localhost`
- Update `.env`: `API_GATEWAY_URL=http://10.0.2.2:3000`

**iOS Simulator:**

- Use `localhost`
- Update `.env`: `API_GATEWAY_URL=http://localhost:3000`

**Physical Device:**

1. Find your computer's IP: `ifconfig` or `ipconfig`
2. Update `.env`: `API_GATEWAY_URL=http://192.168.1.XXX:3000`
3. Ensure device and computer are on same WiFi network
4. Check firewall allows connections on port 3000

#### Build Errors

```bash
# Clear cache and reinstall
cd mobile-driver-app
rm -rf node_modules package-lock.json
npm install
npx expo start -c
```

#### Expo Go Limitations

Some features require development build:

```bash
npx expo prebuild
npm run android  # or npm run ios
```

---

## 📂 Project Structure

```
SwiftLogistics/
├── web-client-portal/          # Web application for clients (React)
│   ├── src/
│   │   ├── pages/              # React pages/routes
│   │   ├── components/         # Reusable UI components
│   │   ├── services/           # API and auth services
│   │   ├── context/            # React Context providers
│   │   ├── types/              # TypeScript types
│   │   └── styles/             # CSS stylesheets
│   ├── public/                 # Static assets
│   ├── .env                    # Environment config
│   ├── package.json
│   └── README.md               # Detailed web portal docs
│
├── mobile-driver-app/          # Mobile app for drivers (React Native)
│   ├── app/                    # Expo Router screens
│   ├── components/             # React Native components
│   ├── services/               # API, auth, location services
│   ├── context/                # Context providers
│   ├── assets/                 # Images, fonts
│   ├── .env                    # Environment config
│   ├── app.json                # Expo configuration
│   ├── package.json
│   └── README.md               # Detailed mobile app docs
│
├── ui/                         # Additional UI resources (optional)
├── services/                   # Backend services
├── docker-compose.yml          # Backend orchestration
└── FRONTEND_QUICKSTART.md      # This file
```

---

## 📚 Additional Documentation

- **Web Client Portal**: See `web-client-portal/README.md` for detailed documentation
- **Mobile Driver App**: See `mobile-driver-app/README.md` for detailed documentation
- **Backend Services**: See `SYSTEM_OVERVIEW.md` for architecture details
- **API Documentation**: Access Swagger UI at backend service ports

---

## 🎯 Next Steps

1. **Customize UI/UX**: Modify components and styles to match branding
2. **Add Features**: Implement additional functionality as needed
3. **Testing**: Write unit and integration tests
4. **Deployment**: Build and deploy to production environments
5. **Monitoring**: Set up error tracking and analytics

---

## 📞 Support

For issues or questions:

1. Check the detailed README files for each application
2. Review troubleshooting sections
3. Check backend service logs: `docker-compose logs -f`
4. Verify API endpoint responses

---

## ✅ Verification Checklist

Before deploying to production:

### Web Portal

- [ ] Environment variables configured correctly
- [ ] API endpoints returning expected data
- [ ] Authentication flow working
- [ ] Order submission functional
- [ ] Tracking dashboard displaying data
- [ ] Invoices loading correctly
- [ ] Responsive design tested on mobile browsers

### Mobile App

- [ ] Environment variables configured for target platform
- [ ] Login working on both Android and iOS
- [ ] Manifest loading correctly
- [ ] Location permissions granted
- [ ] Map displaying delivery routes
- [ ] Photo capture working
- [ ] Status updates saving to backend
- [ ] Tested on physical devices

### Integration

- [ ] Backend services all running
- [ ] API Gateway accessible
- [ ] CORS configured correctly
- [ ] Authentication tokens working
- [ ] Real-time updates functioning
- [ ] Error handling graceful

---

**Version**: 1.0.0  
**Last Updated**: February 3, 2026  
**Status**: ✅ Development Ready
