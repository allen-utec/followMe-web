import L from "leaflet";

export interface ILocation {
  latlng: L.LatLng;
  timestamp: number;
}

export interface ILocationPayload {
  tenant_id: string;
  user_id: string;
  route_id: string;
  location: ILocation;
  counter: number;
}

export interface IRoutePayload {
  tenantId: string;
  remoteRouteId: string;
  image: string;
}

export interface IUser {
  id: string;
  name: string;
  email?: string;
}
