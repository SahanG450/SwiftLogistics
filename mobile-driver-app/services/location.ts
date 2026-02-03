import * as Location from 'expo-location';
import { api } from './api';

/**
 * Location Service for Mobile Driver App
 * Handles GPS tracking, permissions, and location updates
 */

export interface LocationCoords {
  lat: number;
  lng: number;
  accuracy?: number;
  altitude?: number | null;
  heading?: number | null;
  speed?: number | null;
}

/**
 * Request location permissions
 */
export const requestLocationPermission = async (): Promise<boolean> => {
  try {
    const { status } = await Location.requestForegroundPermissionsAsync();
    
    if (status !== 'granted') {
      console.error('[Location] Permission denied');
      return false;
    }
    
    console.log('[Location] Permission granted');
    return true;
  } catch (error) {
    console.error('[Location] Failed to request permission:', error);
    return false;
  }
};

/**
 * Get current location
 */
export const getCurrentLocation = async (): Promise<LocationCoords | null> => {
  try {
    const hasPermission = await requestLocationPermission();
    if (!hasPermission) return null;
    
    const location = await Location.getCurrentPositionAsync({
      accuracy: Location.Accuracy.High,
    });
    
    const coords: LocationCoords = {
      lat: location.coords.latitude,
      lng: location.coords.longitude,
      accuracy: location.coords.accuracy || undefined,
      altitude: location.coords.altitude,
      heading: location.coords.heading,
      speed: location.coords.speed,
    };
    
    console.log('[Location] Current location:', coords);
    return coords;
  } catch (error) {
    console.error('[Location] Failed to get current location:', error);
    return null;
  }
};

/**
 * Start watching location (for real-time tracking during deliveries)
 */
export const startLocationTracking = async (
  driverId: string,
  callback: (location: LocationCoords) => void,
  updateInterval: number = 30000 // Default: update every 30 seconds
): Promise<Location.LocationSubscription | null> => {
  try {
    const hasPermission = await requestLocationPermission();
    if (!hasPermission) return null;
    
    const subscription = await Location.watchPositionAsync(
      {
        accuracy: Location.Accuracy.High,
        timeInterval: updateInterval,
        distanceInterval: 50, // Update if moved 50 meters
      },
      async (location) => {
        const coords: LocationCoords = {
          lat: location.coords.latitude,
          lng: location.coords.longitude,
          accuracy: location.coords.accuracy || undefined,
          altitude: location.coords.altitude,
          heading: location.coords.heading,
          speed: location.coords.speed,
        };
        
        // Call callback
        callback(coords);
        
        // Send to backend
        try {
          await api.driver.updateLocation(driverId, {
            lat: coords.lat,
            lng: coords.lng,
          });
        } catch (error) {
          console.error('[Location] Failed to update location on server:', error);
        }
      }
    );
    
    console.log('[Location] Started tracking');
    return subscription;
  } catch (error) {
    console.error('[Location] Failed to start tracking:', error);
    return null;
  }
};

/**
 * Stop location tracking
 */
export const stopLocationTracking = (
  subscription: Location.LocationSubscription | null
): void => {
  if (subscription) {
    subscription.remove();
    console.log('[Location] Stopped tracking');
  }
};

/**
 * Calculate distance between two coordinates (Haversine formula)
 * Returns distance in kilometers
 */
export const calculateDistance = (
  from: LocationCoords,
  to: LocationCoords
): number => {
  const R = 6371; // Earth's radius in kilometers
  
  const dLat = toRadians(to.lat - from.lat);
  const dLng = toRadians(to.lng - from.lng);
  
  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(toRadians(from.lat)) *
      Math.cos(toRadians(to.lat)) *
      Math.sin(dLng / 2) *
      Math.sin(dLng / 2);
  
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  const distance = R * c;
  
  return distance;
};

/**
 * Convert degrees to radians
 */
const toRadians = (degrees: number): number => {
  return degrees * (Math.PI / 180);
};

/**
 * Format distance for display
 */
export const formatDistance = (distanceKm: number): string => {
  if (distanceKm < 1) {
    return `${Math.round(distanceKm * 1000)} m`;
  }
  return `${distanceKm.toFixed(1)} km`;
};

export const locationService = {
  requestLocationPermission,
  getCurrentLocation,
  startLocationTracking,
  stopLocationTracking,
  calculateDistance,
  formatDistance,
};

export default locationService;
