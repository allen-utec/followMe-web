<script lang="ts">
  interface Props {
    route?: any;
    consoleOpened?: boolean;
  }

  let { route = [], consoleOpened = false }: Props = $props();
</script>

<div id="console" class:openend={consoleOpened}>
  <ul>
    {#each route as coord}
      <li>
        <span>Lat: {coord.lat}</span><span>Lng: {coord.lng}</span>
      </li>
    {/each}
  </ul>
</div>

<style>
  #console {
    position: absolute;
    width: 500px;
    height: 100%;
    top: 0;
    background: #000;
    right: -500px;
    padding: 0;
    z-index: 9999;
    overflow: scroll;
  }

  #console.openend {
    right: 0;
    animation-name: slidein;
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

  @media screen and (max-width: 640px) {
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
