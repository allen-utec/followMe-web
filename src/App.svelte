<script lang="ts">
  import L from "leaflet";
  import "leaflet/dist/leaflet.css";

  let consoleOpened = false;

  document.addEventListener("DOMContentLoaded", () => {
    navigator.geolocation.getCurrentPosition(function (position) {
      const lat = position.coords.latitude;
      const lon = position.coords.longitude;

      const map = L.map(document.getElementById("map"), {
        center: [lat, lon],
        zoom: 16,
      });

      L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
        maxZoom: 19,
        attribution:
          '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
      }).addTo(map);
    });
  });

  function toggleConsole() {
    consoleOpened = !consoleOpened;
  }
</script>

<main>
  <div id="content" class:openend={consoleOpened}>
    <h1>Sígueme!</h1>

    <button type="button" style="margin-bottom: 32px;">
      Compartir Mi Ubicación!
    </button>

    <div id="map" />
    <a href="#!" on:click={toggleConsole}>
      {consoleOpened ? "hide" : "show"} console</a
    >
  </div>

  <div id="console" class:openend={consoleOpened} />
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
    width: 640px;
    height: 100%;
    top: 0;
    background: #000;
    right: -640px;
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
    margin-right: 640px;
    animation-name: shrink;
    animation-duration: 0.2s;
  }

  @keyframes slidein {
    from {
      right: -640px;
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
      margin-right: 640px;
    }
  }
</style>
