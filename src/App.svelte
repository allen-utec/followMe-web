<script lang="ts">
  import domtoimage from "dom-to-image";
  import Map from "./components/Map.svelte";
  import Share from "./components/Share.svelte";
  import { getUserId, randomId, diffInMinutes } from "./utils";
  import { getRoute, postLocation, postRoute } from "./utils/followAPI";

  const [, tenantId, remoteRouteId] = location.pathname
    .toLowerCase()
    .split("/");

  // Redirect to incognito if tenantId is not provided
  if (!tenantId) {
    location.href = `${location.origin}/incognito`;
  }

  let routeId = $state(null);
  let remoteRoute = $state([]);
  let routeFinished = $state(false);

  const userId = getUserId();
  let counter = 0;
  let routeSaved = false;

  function handleShare() {
    if (!tenantId || !userId || routeId) return;

    routeId = randomId();
  }

  function handleLocationFound({ location }: { location: L.LatLng }) {
    console.table(location);

    if (remoteRouteId) return updateRouteInMap();

    if (!tenantId || !userId || !routeId) return;

    postLocation({
      tenant_id: tenantId,
      user_id: userId,
      route_id: routeId,
      location: { latlng: location, timestamp: Date.now() },
      counter: ++counter,
    });
  }

  function handleLocationStop() {
    if (!tenantId || !remoteRouteId || routeSaved) return;

    domtoimage
      .toPng(document.getElementById("map"))
      .then((base64Image: string) =>
        postRoute({
          tenantId,
          remoteRouteId,
          image: base64Image.split(";base64,").pop(),
        }),
      )
      .then(() => {
        routeSaved = true;
      })
      .catch(console.error);
  }

  async function updateRouteInMap() {
    if (routeFinished) return;

    try {
      const { data } = await getRoute(tenantId, remoteRouteId);

      remoteRoute = data
        .sort((a, b) => a.timestamp - b.timestamp)
        .map((e) => e.latlng);

      if (diffInMinutes(data[data.length - 1]?.timestamp) > 2) {
        routeFinished = true;
      } else {
        setTimeout(updateRouteInMap, 2000);
      }
    } catch (error) {
      console.error(error);
    }
  }
</script>

<main>
  <div id="content">
    <h1>Sígueme!</h1>

    {#if remoteRouteId}
      {#if routeFinished}
        <p>La ruta de <strong>{remoteRouteId}</strong> ha terminado.</p>
      {:else}
        <p>Estás siguiendo a <strong>{remoteRouteId}</strong></p>
      {/if}
    {/if}

    {#if !remoteRouteId}
      <button type="button" onclick={handleShare}>
        Compartir Mi Ubicación!
      </button>
    {/if}

    <Share {tenantId} {routeId} />

    <Map
      locationFound={handleLocationFound}
      locationStop={handleLocationStop}
      {remoteRoute}
      {routeFinished}
    />
  </div>

  <div id="info">
    <small><strong>tenant:</strong> {tenantId}</small>
    <small><strong>user:</strong> {userId}</small>
    {#if routeId}
      <small><strong>route:</strong> {routeId}</small>
    {/if}
  </div>
</main>

<style>
  #info {
    display: flex;
    gap: 8px;
    justify-content: center;
  }
</style>
