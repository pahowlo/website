<script lang="ts">
  import { onMount } from "svelte"
  import { MurmuringBoidsBackground } from "murmuring-boids"

  let name = "world"

  // Define top-left and bottom-right as percentages (0-1)
  const topLeft = { x: 0, y: 0 }
  const bottomRight = { x: 1, y: 1 }

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
      const background = new MurmuringBoidsBackground(window, canvas, {
        topLeft: topLeft,
        bottomRight: bottomRight,
      })
      background.start(1000, debug)
    }
  })
</script>

<main>
  <canvas bind:this={canvas}></canvas>
</main>

<style>
  canvas {
    display: block;
    overflow: hidden;
  }
</style>
