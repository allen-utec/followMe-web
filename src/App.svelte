<script lang="ts">
  import Map from "./components/Map.svelte";
  import Console from "./components/Console.svelte";

  let route = [];
  let consoleOpened = false;

  function handleToggleConsole() {
    consoleOpened = !consoleOpened;
  }

  function handleLocationFound({ detail }) {
    route = route.concat(detail.location);
  }

  function handleShare() {}
</script>

<main>
  <div id="content" class:openend={consoleOpened}>
    <h1>Sígueme!</h1>

    <button type="button" style="margin-bottom: 32px;" on:click={handleShare}>
      Compartir Mi Ubicación!
    </button>

    <Map on:locationFound={handleLocationFound} />

    <a class="console-link" href="#!" on:click={handleToggleConsole}>
      {consoleOpened ? "hide" : "show"} console
    </a>
  </div>

  <Console {route} {consoleOpened} />
</main>

<style>
  #content {
    margin-right: 0;
  }

  #content.openend {
    margin-right: 500px;
    animation-name: shrink;
    animation-duration: 0.2s;
  }

  .console-link {
    display: block;
    padding: 8px;
  }

  @media screen and (max-width: 640px) {
    #content.openend {
      margin-right: 0;
      animation: none;
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
