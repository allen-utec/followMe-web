<script lang="ts">
  import Map from "./components/Map.svelte";
  import Share from "./components/Share.svelte";
  import { getUserId, randomId, type ILocation } from "./utils";

  const [, tenantId, remoteRouteId] = location.pathname
    .toLowerCase()
    .split("/");

  // Redirect to incognito if tenantId is not provided
  if (!tenantId) {
    location.href = `${location.origin}/incognito`;
  }

  const userId = getUserId();
  let routeId = null;
  let remoteRoute = [];
  let counter = 0;

  function handleShare() {
    if (!tenantId || !userId || routeId) return;

    routeId = randomId();
  }

  function handleLocationFound({ detail }: CustomEvent) {
    console.table(detail);

    if (remoteRouteId || !(tenantId && userId && routeId)) return;

    const payload = {
      tenant_id: tenantId,
      user_id: userId,
      route_id: routeId,
      location: {
        latlng: detail.location,
        timestamp: Date.now(),
      } as ILocation,
      counter: ++counter,
    };

    fetch(`${import.meta.env.VITE_FOLLOWME_API}/locations`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
  }

  if (tenantId && remoteRouteId) {
    setInterval(() => {
      fetch(
        `${
          import.meta.env.VITE_FOLLOWME_API
        }/locations/${tenantId}/${remoteRouteId}`
      )
        .then<ILocation[]>((res) => res.json())
        .then((data) => data.sort((a, b) => a.timestamp - b.timestamp))
        .then((data) => {
          remoteRoute = data.map((e) => e.latlng);
        })
        .catch(console.error);
    }, 1000);
  }
</script>

<main>
  <div id="content">
    <h1>Sígueme!</h1>

    {#if remoteRouteId}
      <p>Estás siguiendo a <strong>{remoteRouteId}</strong></p>
    {/if}

    {#if !remoteRouteId}
      <button type="button" on:click={handleShare}>
        Compartir Mi Ubicación!
      </button>
    {/if}

    <Share {tenantId} {routeId} />

    <Map on:locationFound={handleLocationFound} {remoteRoute} />
  </div>
</main>

<style>
</style>
