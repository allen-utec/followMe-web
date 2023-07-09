<script lang="ts">
  import { createEventDispatcher } from "svelte";
  import { FollowMap } from "../utils/FollowMap";

  export let remoteRoute = [];
  export let routeFinished = false;

  let map: FollowMap;

  const dispatchRoute = createEventDispatcher();
  const dispatchStopLocation = createEventDispatcher();

  document.addEventListener("DOMContentLoaded", () => {
    map = new FollowMap();

    map.onLocation = (e) => {
      dispatchRoute("locationFound", { location: e });
    };

    map.onLocationStop = () => {
      dispatchStopLocation("locationStop");
    };
  });

  $: if (map && remoteRoute.length) {
    map.setRoute(remoteRoute, routeFinished);
  }
</script>

<div id="map" />

<style>
  #map {
    width: 320px;
    height: 600px;
    border: 1px solid #ccc;
    border-radius: 8px;
    margin: 16px auto;
  }

  @media screen and (max-width: 640px) {
    #map {
      height: 500px;
    }
  }
</style>
