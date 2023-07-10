<script lang="ts">
  import domtoimage from "dom-to-image";
  import Map from "./components/Map.svelte";
  import Share from "./components/Share.svelte";
  import { getUserId, randomId, type ILocation, diffInMinutes } from "./utils";

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
  let routeFinished = false;
  let routeSaved = false;

  function handleShare() {
    if (!tenantId || !userId || routeId) return;

    routeId = randomId();
  }

  function handleLocationFound({ detail }: CustomEvent) {
    console.table(detail);

    if (remoteRouteId) {
      return updateRouteInMap();
    }

    if (!tenantId || !userId || !routeId) return;

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

  function handleLocationStop() {
    if (!tenantId || !remoteRouteId || routeSaved) return;

    domtoimage
      .toPng(document.getElementById("map"))
      .then((base64Image: string) => {
        const payload = {
          tenantId,
          remoteRouteId,
          image: base64Image.split(";base64,").pop(),
        };

        return fetch(`${import.meta.env.VITE_FOLLOWME_API}/routes`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });
      })
      .then((res) => {
        if (!res.ok) throw new Error(res.statusText);
        routeSaved = true;
      })
      .catch(console.error);
  }

  async function updateRouteInMap() {
    if (routeFinished) return;

    try {
      const { data } = await fetch(
        `${
          import.meta.env.VITE_FOLLOWME_API
        }/locations/${tenantId}/${remoteRouteId}`
      ).then<{ data: ILocation[] }>((res) => {
        if (!res.ok) throw new Error(res.statusText);
        return res.json();
      });

      remoteRoute = data
        .sort((a, b) => a.timestamp - b.timestamp)
        .map((e) => e.latlng);

      if (diffInMinutes(data[data.length - 1]?.timestamp) > 5) {
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
      <button type="button" on:click={handleShare}>
        Compartir Mi Ubicación!
      </button>
    {/if}

    <Share {tenantId} {routeId} />

    <Map
      on:locationFound={handleLocationFound}
      on:locationStop={handleLocationStop}
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
