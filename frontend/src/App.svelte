<script>
import Map from './lib/components/Map.svelte';
import battleData from './lib/data/enriched_battles.json';
import Controlbar from './lib/components/controlbar/Controlbar.svelte';
import { currentDate } from './lib/store.js';

// Convert Date to YYYY-MM-DD string for filtering
let currentDateString = $derived($currentDate.toISOString().split('T')[0]);

let filteredBattles = $derived(
    battleData.filter(b =>
        b.start_date <= currentDateString && 
        b.end_date >= currentDateString
    )
)
</script>

<main class="flex flex-col w-full h-screen bg-[#736B60]">
    <!-- Header -->
    <header class="bg-[#171C45] text-white p-6  flex justify-center">
        <h1 class="text-3xl font-bold">Civil War Battle Visualizer</h1>
    </header>

    <!-- Control Bar -->
    <Controlbar />

    <div class="flex-1">
        <Map battles={filteredBattles} />
    </div>
</main>
