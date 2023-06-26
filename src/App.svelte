<script lang="ts">
  import L from "leaflet";
  import "leaflet/dist/leaflet.css";

  let consoleOpened = false;
  let map: L.Map;
  let routeCoords = [];

  document.addEventListener("DOMContentLoaded", () => {
    map = L.map("map").fitWorld();

    L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 19,
      attribution:
        '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    }).addTo(map);

    map.locate({ setView: true, maxZoom: 16, watch: true });

    map.on("locationfound", onLocationFound);
  });

  function toggleConsole() {
    consoleOpened = !consoleOpened;
  }

  function onLocationFound(e: L.LocationEvent) {
    routeCoords = routeCoords.concat(e.latlng);

    if (routeCoords.length === 1) {
      L.polyline(routeCoords, { color: "blue" }).addTo(map);
    } else {
      map.eachLayer((layer) => {
        if (layer instanceof L.Polyline) {
          layer.setLatLngs(routeCoords);
        } else if (layer instanceof L.Marker) {
          layer.remove();
        }
      });
    }

    L.marker(e.latlng).addTo(map).bindPopup("Aquí tas tú!").openPopup();
  }
</script>

<main>
  <div id="content" class:openend={consoleOpened}>
    <h1>Sígueme!</h1>

    <button type="button" style="margin-bottom: 32px;">
      Compartir Mi Ubicación!
    </button>

    <div id="map" />

    <a class="console-link" href="#!" on:click={toggleConsole}>
      {consoleOpened ? "hide" : "show"} console</a
    >
  </div>

  <div id="console" class:openend={consoleOpened}>
    <ul>
      {#each routeCoords as coord}
        <li>
          <span>Lat: {Number(coord.lat).toFixed(6)}</span><span
            >Lng: {Number(coord.lng).toFixed(6)}</span
          >
        </li>
      {/each}
    </ul>
  </div>
</main>

<style>
  #map {
    width: 320px;
    height: 600px;
    border: 1px solid #ccc;
    border-radius: 8px;
  }

  #console {
    position: absolute;
    width: 500px;
    height: 100%;
    top: 0;
    background: #000;
    right: -500px;
    padding: 0;
    z-index: 9999;
  }

  #console.openend {
    right: 0;
    animation-name: slidein;
    animation-duration: 0.2s;
  }

  #content {
    margin-right: 0;
  }

  #content.openend {
    margin-right: 500px;
    animation-name: shrink;
    animation-duration: 0.2s;
  }

  #console > ul {
    list-style: none;
    padding: 0;
    margin: 0;
  }

  #console > ul > li {
    color: #ddd;
    padding: 2px 8px;
    border-bottom: 1px solid #999;
    display: flex;
    gap: 8px;
  }

  .console-link {
    display: block;
    padding: 8px;
  }

  @media screen and (max-width: 640px) {
    #map {
      height: 500px;
    }

    #content.openend {
      margin-right: 0;
      animation: none;
    }

    #console {
      width: 100%;
      height: 50%;
    }
  }

  @keyframes slidein {
    from {
      right: -500px;
    }
    to {
      right: 0;
    }
  }

  @keyframes shrink {
    from {
      margin-right: 0;
    }
    to {
      margin-right: 500px;
    }
  }
</style>
