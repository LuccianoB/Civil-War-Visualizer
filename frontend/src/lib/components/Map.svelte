<script lang="ts">
    import 'maplibre-gl/dist/maplibre-gl.css'
    import { MapLibre, Marker, Popup, NavigationControl, ScaleControl} from 'svelte-maplibre-gl'
    import BattleMarker from './BattleMarker.svelte';

    let { battles = [] } = $props()

    let style = "https://tiles.openfreemap.org/styles/liberty"

    // light: https://tiles.openfreemap.org/styles/liberty
    // dark: https://tiles.openfreemap.org/styles/dark

</script>


<MapLibre
    class="w-full h-full"
    style={style}
    center={[-77, 37]}
    zoom={5}
>
    <BattleMarker battles={battles} />
    <NavigationControl />
    <ScaleControl/>

</MapLibre>
