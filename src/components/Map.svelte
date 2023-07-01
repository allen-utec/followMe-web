<script lang="ts">
  import { createEventDispatcher } from "svelte";
  import { FollowMap } from "../utils/FollowMap";

  let map: FollowMap;

  const dispatchRoute = createEventDispatcher();

  document.addEventListener("DOMContentLoaded", () => {
    map = new FollowMap();

    map.onLocation = (e) => {
      dispatchRoute("locationFound", { location: e });
    };
  });
</script>

<div id="map" />

<style>
  #map {
    width: 320px;
    height: 600px;
    border: 1px solid #ccc;
    border-radius: 8px;
  }

  @media screen and (max-width: 640px) {
    #map {
      height: 500px;
    }
  }
</style>
