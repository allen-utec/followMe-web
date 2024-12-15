<script lang="ts">
  import { FollowMap } from "../utils/FollowMap";

  interface Props {
    remoteRoute?: L.LatLng[];
    routeFinished?: boolean;
    locationFound: (o: { latlng: L.LatLng }) => void;
    locationStop: () => void;
  }

  let {
    remoteRoute = [],
    routeFinished = false,
    locationFound,
    locationStop,
  }: Props = $props();

  let map: FollowMap = $state();

  document.addEventListener("DOMContentLoaded", () => {
    map = new FollowMap();
    map.onLocation = (e) => locationFound({ latlng: e });
    map.onLocationStop = () => locationStop();
  });

  $effect(() => {
    if (map && remoteRoute.length) {
      map.setRoute(remoteRoute, routeFinished);
    }
  });
</script>

<div id="map"></div>

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
