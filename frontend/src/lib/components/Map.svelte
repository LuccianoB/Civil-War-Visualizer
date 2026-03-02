<script lang="ts">
    import 'maplibre-gl/dist/maplibre-gl.css'
    import { MapLibre } from 'svelte-maplibre-gl'
</script>


<MapLibre
    class="w-full h-[80vh]"
    style="https://tiles.openfreemap.org/styles/liberty"
    center={[-77, 37]}
    zoom={5}
>
</MapLibre>
