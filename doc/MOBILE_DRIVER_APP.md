# SwiftLogistics Mobile Driver App

**React Native mobile application for delivery drivers using Expo**

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
- [Testing](#testing)
- [Building for Production](#building-for-production)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

The SwiftLogistics Mobile Driver App is a comprehensive mobile solution that enables delivery drivers to:

- View their daily delivery manifest
- Navigate optimized routes
- Update delivery status in real-time
- Capture proof of delivery (photos/signatures)
- Communicate with dispatch
- Track their performance metrics

This app connects to the SwiftLogistics middleware API Gateway and integrates with ROS (Route Optimization System), WMS (Warehouse Management), and CMS (Client Management) backend services.

---

## ✨ Features

### 📋 Manifest Management

- **Daily Manifest**: View all assigned deliveries for the day
- **Package Details**: Access complete package information
- **Prioritization**: See urgent deliveries highlighted
- **Search & Filter**: Quickly find specific packages

### 🗺️ Route Navigation

- **Optimized Routes**: Follow AI-optimized delivery sequences
- **Map Integration**: Visual map with all delivery waypoints
- **GPS Tracking**: Real-time location tracking
- **Turn-by-turn**: Navigation assistance
- **Route Deviation Alerts**: Notifications for off-route drivers

### 📦 Delivery Operations

- **Mark as Delivered**: Quick status updates
- **Mark as Failed**: Record delivery failures with reasons
- **Proof of Delivery**:
  - Photo capture
  - Signature collection
  - Location and timestamp recording
- **Special Instructions**: View customer delivery notes

### 📊 Driver Dashboard

- **Today's Stats**: Deliveries completed, pending, failed
- **Performance Metrics**: On-time delivery rate, efficiency
- **Earnings**: Track daily/weekly compensation
- **Notifications**: Real-time updates and alerts

### 🔐 Security

- **Secure Authentication**: JWT-based login
- **Offline Mode**: Cache data for areas with poor connectivity
- **Data Encryption**: Secure storage of sensitive information

---

## 🛠️ Technology Stack

| Technology            | Purpose                             |
| --------------------- | ----------------------------------- |
| **React Native**      | Cross-platform mobile framework     |
| **Expo**              | Development platform and tooling    |
| **TypeScript**        | Type-safe development               |
| **Expo Router**       | File-based navigation               |
| **React Native Maps** | Map and location services           |
| **Expo Camera**       | Photo capture for proof of delivery |
| **Expo Location**     | GPS tracking                        |
| **Axios**             | HTTP client for API requests        |
| **AsyncStorage**      | Local data persistence              |

---

## 📁 Project Structure

```
mobile-driver-app/
├── app/                      # Expo Router screens
│   ├── (auth)/
│   │   ├── login.tsx         # Login screen
│   │   └── _layout.tsx       # Auth layout
│   ├── (tabs)/
│   │   ├── manifest.tsx      # Daily manifest screen
│   │   ├── route.tsx         # Route navigation screen
│   │   ├── profile.tsx       # Driver profile
│   │   └── _layout.tsx       # Tabs layout
│   ├── delivery/
│   │   └── [id].tsx          # Individual delivery details
│   └── _layout.tsx           # Root layout
├── components/
│   ├── DeliveryCard.tsx      # Package/delivery card component
│   ├── RouteMap.tsx          # Map with route visualization
│   ├── ProofOfDelivery.tsx   # POD capture component
│   ├── StatusBadge.tsx       # Status indicator
│   └── LoadingSpinner.tsx    # Loading state
├── services/
│   ├── api.ts                # API client configuration
│   ├── auth.ts               # Authentication service
│   ├── location.ts           # GPS and location tracking
│   └── storage.ts            # AsyncStorage wrapper
├── context/
│   ├── AuthContext.tsx       # Authentication state
│   └── LocationContext.tsx   # Location tracking state
├── hooks/
│   ├── useManifest.ts        # Hook for manifest data
│   ├── useLocation.ts        # Hook for location services
│   └── useDelivery.ts        # Hook for delivery operations
├── types/
│   └── index.ts              # TypeScript type definitions
├── constants/
│   ├── config.ts             # App configuration
│   └── colors.ts             # Color palette
├── utils/
│   ├── formatters.ts         # Date/number formatters
│   └── validators.ts         # Input validation
├── assets/                   # Images, fonts, etc.
├── app.json                  # Expo configuration
├── package.json              # Dependencies
├── tsconfig.json             # TypeScript config
├── .env.example              # Environment template
└── README.md                 # This file
```

---

## 🚀 Installation

### Prerequisites

- **Node.js**: v18 or higher
- **npm**: v9 or higher
- **Expo CLI**: Installed globally or via npx
- **Android Studio** (for Android) or **Xcode** (for iOS on Mac)
- **SwiftLogistics Backend**: Running on accessible network

### Steps

1. **Navigate to the project directory:**

   ```bash
   cd mobile-driver-app
   ```

2. **Install dependencies:**

   ```bash
   npm install
   ```

3. **Configure environment variables:**

   ```bash
   cp .env.example .env
   ```

   Edit `.env` to set your API Gateway URL

4. **Start Expo development server:**

   ```bash
   npx expo start
   ```

5. **Run on device/emulator:**
   - **Android**: Press `a` or scan QR code with Expo Go app
   - **iOS**: Press `i` (Mac only) or scan QR code with Camera app
   - **Web**: Press `w` for web version

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# API Configuration
# For Android Emulator, use 10.0.2.2 instead of localhost
API_GATEWAY_URL=http://10.0.2.2:3000

# For iOS Simulator
# API_GATEWAY_URL=http://localhost:3000

# For physical device on same network
# API_GATEWAY_URL=http://192.168.1.100:3000

# Enable debug logging
DEBUG=true
```

### Expo Configuration (`app.json`)

Key settings in `app.json`:

```json
{
  "expo": {
    "name": "SwiftLogistics Driver",
    "slug": "swiftlogistics-driver",
    "version": "1.0.0",
    "orientation": "portrait",
    "icon": "./assets/icon.png",
    "splash": {
      "image": "./assets/splash.png",
      "resizeMode": "contain",
      "backgroundColor": "#2563eb"
    },
    "ios": {
      "supportsTablet": true,
      "bundleIdentifier": "com.swiftlogistics.driver"
    },
    "android": {
      "adaptiveIcon": {
        "foregroundImage": "./assets/adaptive-icon.png",
        "backgroundColor": "#2563eb"
      },
      "package": "com.swiftlogistics.driver",
      "permissions": ["ACCESS_FINE_LOCATION", "CAMERA"]
    }
  }
}
```

---

## 📖 Usage

### Running the App

**Development mode:**

```bash
npx expo start
```

**Android:**

```bash
npm run android
# or
npx expo start --android
```

**iOS (Mac only):**

```bash
npm run ios
# or
npx expo start --ios
```

**Web:**

```bash
npm run web
```

### Default Login Credentials

For testing (configured in backend):

```
Username: driver@example.com
Password: password123
```

### Daily Workflow

1. **Login**: Enter credentials
2. **View Manifest**: See all assigned deliveries
3. **Start Route**: Begin navigation
4. **Navigate**: Follow optimized route on map
5. **Deliver Package**:
   - Mark as delivered
   - Capture photo proof
   - Get signature
   - Add delivery notes
6. **Next Stop**: Continue to next delivery
7. **Complete Route**: Finish all deliveries
8. **View Summary**: Check daily statistics

---

## 🔌 API Integration

### API Service (`services/api.ts`)

The app uses Axios for HTTP requests with:

- **Base URL**: Configured from environment variable
- **Authentication**: JWT token in Authorization header
- **Interceptors**: Auto-attach token, handle auth errors
- **Offline Support**: Queue requests when offline

### API Endpoints Used

| Endpoint                          | Method | Purpose                |
| --------------------------------- | ------ | ---------------------- |
| `/api/auth/login`                 | POST   | Driver authentication  |
| `/api/manifests/driver/:driverId` | GET    | Get driver's manifest  |
| `/api/manifests/:id/start`        | POST   | Start delivery route   |
| `/api/manifests/:id/complete`     | POST   | Complete route         |
| `/api/orders/:id/mark-delivered`  | POST   | Mark package delivered |
| `/api/orders/:id/mark-failed`     | POST   | Mark delivery failed   |
| `/api/orders/:id/upload-proof`    | POST   | Upload POD photo       |
| `/api/driver/stats`               | GET    | Get driver statistics  |

### Example API Call

```typescript
import { apiClient } from "./services/api";

// Get today's manifest
const manifest = await apiClient.get(`/api/manifests/driver/${driverId}`);

// Mark as delivered
await apiClient.post(`/api/orders/${orderId}/mark-delivered`, {
  timestamp: new Date().toISOString(),
  location: { lat: 6.9271, lng: 79.8612 },
  proofPhoto: photoUri,
  signature: signatureData,
  notes: "Delivered to recipient",
});
```

---

## 📜 Available Scripts

| Command             | Description                            |
| ------------------- | -------------------------------------- |
| `npm start`         | Start Expo development server          |
| `npm run android`   | Run on Android emulator/device         |
| `npm run ios`       | Run on iOS simulator/device (Mac only) |
| `npm run web`       | Run in web browser                     |
| `npx expo prebuild` | Generate native projects               |
| `npx expo build`    | Build for production                   |

---

## 🧪 Testing

### Testing on Devices

**Android Emulator:**

1. Open Android Studio
2. Start an AVD (Android Virtual Device)
3. Run `npm run android`

**Physical Device:**

1. Install Expo Go app from App Store/Play Store
2. Run `npx expo start`
3. Scan QR code with Expo Go (Android) or Camera (iOS)
4. Ensure device is on same network as development machine

### Network Configuration

For physical devices to access localhost backend:

1. Find your computer's local IP: `ipconfig` (Windows) or `ifconfig` (Mac/Linux)
2. Update `.env`: `API_GATEWAY_URL=http://192.168.1.XXX:3000`
3. Ensure backend allows connections from local network

---

## 📦 Building for Production

### Android APK

```bash
# Install EAS CLI
npm install -g eas-cli

# Configure EAS
eas build:configure

# Build APK
eas build -p android --profile preview
```

### iOS App

```bash
# Build for iOS (requires Mac)
eas build -p ios --profile preview
```

---

## 🐛 Troubleshooting

### Cannot Connect to API

**Problem**: App shows "Network Error" or cannot reach backend

**Solutions**:

1. Check API_GATEWAY_URL in `.env`
2. For Android emulator, use `10.0.2.2` instead of `localhost`
3. For physical device, use your computer's local IP address
4. Verify backend is running: `docker-compose ps`
5. Check firewall settings

### Build Errors

**Problem**: Build fails with dependency issues

**Solutions**:

```bash
# Clear cache
npx expo start -c

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install

# Reset Metro bundler
npx expo start --reset-cache
```

### Location/Camera Permissions

**Problem**: App crashes when accessing camera or location

**Solutions**:

1. Check permissions in `app.json`
2. Grant permissions in device settings
3. Rebuild app after adding permissions

### Expo Go Limitations

Some features require custom native code and won't work in Expo Go:

- Background location tracking
- Certain push notification features

For full functionality, build a development build:

```bash
npx expo prebuild
npx expo run:android
```

---

## 🔗 Related Documentation

- [SwiftLogistics System Overview](../SYSTEM_OVERVIEW.md)
- [API Gateway Documentation](../services/api-gateway/README.md)
- [Web Client Portal](../web-client-portal/README.md)
- [Expo Documentation](https://docs.expo.dev/)
- [React Native Documentation](https://reactnative.dev/)

---

## 📱 Supported Platforms

- **Android**: Android 5.0 (API 21) and higher
- **iOS**: iOS 13 and higher
- **Web**: Modern browsers (for testing only)

---

## 🔐 Security Considerations

- **Authentication**: JWT tokens stored in secure AsyncStorage
- **HTTPS**: Use HTTPS in production
- **API Keys**: Never commit API keys to version control
- **Permissions**: Request only necessary permissions
- **Data Validation**: Validate all user inputs
- **Secure Storage**: Use Expo SecureStore for sensitive data

---

## 📝 License

This project is part of the SwiftLogistics middleware architecture assignment.

---

**Version**: 1.0.0  
**Last Updated**: February 3, 2026  
**Status**: ✅ Development Ready
