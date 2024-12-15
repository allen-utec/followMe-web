<script lang="ts">
  import domtoimage from "dom-to-image";
  import Map from "./components/Map.svelte";
  import Share from "./components/Share.svelte";
  import User from "./components/User.svelte";
  import { getUser, diffInMinutes, getRouteId } from "./utils";
  import { getRoute, postLocation, postRoute } from "./utils/followAPI";

  const parsedUrl = new URL(location.href);
  const tenantId = parsedUrl.searchParams.get("t");
  const remoteRouteId = parsedUrl.searchParams.get("r");

  // Redirect to public tenant when is not provided.
  if (!tenantId) {
    location.href = `${location.origin}?t=public`;
  }

  let routeId = $state<string>(null);
  let remoteRoute = $state<L.LatLng[]>([]);
  let routeFinished = $state(false);

  const user = getUser();
  let counter = 0;
  let routeSaved = false;

  function handleShare() {
    if (!tenantId || !user || routeId) return;

    routeId = getRouteId();
  }

  function handleLocationFound({ latlng }: { latlng: L.LatLng }) {
    console.log(latlng);

    if (remoteRouteId) return updateRouteInMap();

    if (!tenantId || !user || !routeId) return;

    postLocation({
      tenant_id: tenantId,
      user_id: user.id,
      route_id: routeId,
      location: { latlng, timestamp: Date.now() },
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
      const route = await getRoute(tenantId, remoteRouteId);
      remoteRoute = route.map((e) => e.latlng);

      if (diffInMinutes(route.at(-1)?.timestamp) > 2) {
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
        <p>La ruta ha terminado! <br /><strong>{remoteRouteId}</strong></p>
      {:else}
        <p>Estás siguiendo a <br /><strong>{remoteRouteId}</strong></p>
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
    <div>
      <small><strong>tenant:</strong> {tenantId}</small>
    </div>
    <User {user} />
  </div>
  {#if routeId}
    <div>
      <small><strong>ruta:</strong> {routeId}</small>
    </div>
  {/if}
</main>

<style>
  #info {
    display: flex;
    gap: 8px;
    justify-content: center;
    flex-wrap: wrap;
  }
</style>
