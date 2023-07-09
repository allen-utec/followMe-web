import L from "leaflet";

export interface ILocation {
  latlng: L.LatLng;
  timestamp: number;
}

export function randomId() {
  return Math.random().toString(36).substring(2, 8);
}

export function getUserId() {
  let userId = localStorage.getItem("userId");

  if (!userId) {
    userId = randomId();
    localStorage.setItem("userId", userId);
  }

  return userId;
}

export function diffInMinutes(timestamp?: number) {
  if (!timestamp) {
    return 0;
  }
  const diffMinutes = Math.ceil(Math.abs(Date.now() - timestamp) / 1000 / 60);
  return diffMinutes;
}
