<script>
    import { Marker, Popup } from "svelte-maplibre-gl";
    export let battles = [];

    function getVictoryColor(victory) {
        switch (victory) {
            case "Union": return "#4169E1";
            case "Confederate": return "#808080";
            case "Draw": return "#FFD700";
            default: return "#888888";
        }
    }

    function parseCoordinates(coordString) {
        const match = coordString.match(/Point\(([^ ]+) ([^)]+)\)/);
        if (match) {
            return [parseFloat(match[1]), parseFloat(match[2])];
        }
        throw new Error("Invalid coordinate string");
    }
</script>

{#each battles as battle (battle.qid)}
    {@const coords = parseCoordinates(battle.wikidata_coordinates)}
    {@const color = getVictoryColor(battle.Victory)}
    <Marker lnglat={coords}>
        {#snippet content()}
            <div class="marker" style="--victory-color: {color}">
                <span class="material-symbols-outlined">swords</span>
            </div>
        {/snippet}
        <Popup>
            <div class="popup-content">
                <h3>{battle.Battle}</h3>
                <p><strong>Victor:</strong> {battle.Victory}</p>
                <p><strong>Date:</strong> {battle.Date}</p>
                <p><strong>Location:</strong> {battle.State}</p>
            </div>
        </Popup>
    </Marker>
{/each}

<style>
    .marker {
        width: 30px;
        height: 30px;
        background-color: var(--victory-color);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 18px;
        cursor: pointer;
    }
    .popup-content {
        font-size: 1em;
    }
    .popup-content h3 {
        margin-top: 0;
    }
</style>
