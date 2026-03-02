<script lang="ts">
    import 'maplibre-gl/dist/maplibre-gl.css'
    import { MapLibre, Marker, Popup } from 'svelte-maplibre-gl'

    let { battles = [] } = $props()

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
    class="w-full h-[80vh]"
    style="https://tiles.openfreemap.org/styles/liberty"
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

</MapLibre>
