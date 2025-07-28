<script lang="ts">
  import { onMount } from "svelte"
  import { MurmuringBoidsBackground } from "murmuring-boids"

  let name = "world"

  // Read query parameters
  let params: URLSearchParams
  let canvas: HTMLCanvasElement | null = null
  let debug = false
  onMount(() => {
    // Read query parameters
    params = new URLSearchParams(window.location.search)
    if (params.has("debug")) {
      debug = true
    }

    // Init background
    if (canvas) {
      const background = new MurmuringBoidsBackground(window, canvas)
      background.start(5001, debug, {})
    }
  })
</script>

<main>
  <canvas bind:this={canvas}></canvas>
</main>

<style>
  main {
    width: 100vw;
    height: 100vh;
    overflow: hidden;
  }
  canvas {
    display: block;
    width: 100vw;
    height: 100vh;
    position: absolute;
    top: 0;
    left: 0;
  }
</style>
