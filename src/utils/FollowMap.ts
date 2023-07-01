import L from "leaflet";

export class FollowMap {
  centerMap: boolean = true;

  onLocation: (e: L.LatLng) => void;

  private map: L.Map;

  private marker: L.Marker;

  private route = [];

  private polyline = { color: "blue", opacity: 0.5, weight: 8 };

  private markIcon = L.divIcon({
    html: '<i class="emoji" style="font-size: 28px;">🙈</i>',
    className: "custom-icon",
    iconAnchor: [14, 28],
    iconSize: [28, 28],
  });

  constructor() {
    this.map = L.map("map").fitWorld();

    L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 19,
      attribution:
        '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    }).addTo(this.map);

    this.map.locate({ setView: false, maxZoom: 18, watch: true });

    this.map.on("locationfound", this.onLocationFound.bind(this));
  }

  private onLocationFound(e: L.LocationEvent) {
    this.route.push(e.latlng);

    this.updatePolyline();

    this.updateMarker(e.latlng);

    // center position in map
    if (this.centerMap) {
      this.map.setView(e.latlng, 18);
    }

    // emit location
    if (this.onLocation) {
      this.onLocation(e.latlng);
    }
  }

  private updatePolyline() {
    // if route is empty, create a new polyline
    if (this.route.length === 1) {
      L.polyline(this.route, this.polyline).addTo(this.map);
    } else {
      this.map.eachLayer((layer) => {
        if (layer instanceof L.Polyline) {
          layer.setLatLngs(this.route);
        }
      });
    }
  }

  private updateMarker(latlng: L.LatLng) {
    // if marker is empty, create a new marker
    if (!this.marker) {
      this.marker = L.marker(latlng, { icon: this.markIcon }).addTo(this.map);
    } else {
      this.marker.setLatLng(latlng);
    }
  }
}
