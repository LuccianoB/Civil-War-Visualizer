<script>
import Map from './lib/components/Map.svelte';
import battleData from './lib/data/enriched_battles.json';
import Controlbar from './lib/components/controlbar/Controlbar.svelte';
import { currentDate } from './lib/store.js';
import {filterBattlesByDate} from './lib/utils/battleFilter.js';

// Convert Date to YYYY-MM-DD string for filtering
let currentDateString = $derived($currentDate.toISOString().split('T')[0]);

let filteredBattles = $derived(
    filterBattlesByDate(battleData, currentDateString)
);
</script>

<main class="flex flex-col w-full h-screen bg-[#736B60]">
  

    <!-- Control Bar -->
    <Controlbar />

    <div class="flex-1">
        <Map battles={filteredBattles} />
    </div>
</main>
