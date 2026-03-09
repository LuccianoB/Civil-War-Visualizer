<script lang="ts">
    import 'maplibre-gl/dist/maplibre-gl.css'
    import { MapLibre, Marker, Popup, NavigationControl, ScaleControl} from 'svelte-maplibre-gl'

    let { battles = [] } = $props()

    let style = "https://tiles.openfreemap.org/styles/liberty"

    // light: https://tiles.openfreemap.org/styles/liberty
    // dark: https://tiles.openfreemap.org/styles/dark

    function parseCoordinates(coordString: string): [number, number] {
        // Extract numbers from "Point(lat lng)"
        const match = coordString.match(/Point\(([^ ]+) ([^)]+)\)/)
        if (match) {
            return [parseFloat(match[1]), parseFloat(match[2])]
        }
        throw new Error("Invalid coordinate string")
    }
</script>


<MapLibre
    class="w-full h-full"
    style={style}
    center={[-77, 37]}
    zoom={5}
>

    {#each battles as battle}
    {@const coords = parseCoordinates(battle.wikidata_coordinates)}
        <Marker
            lnglat={coords}
        >
            <Popup>
                <h3>{battle.Battle}</h3> 
                <p>Victor: {battle.Victory}</p>
            </Popup>
        </Marker>
    {/each}

    <NavigationControl />
    <ScaleControl/>

</MapLibre>
