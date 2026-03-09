<script>
import Map from './lib/components/Map.svelte';
import battleData from './lib/data/enriched_battles.json';
import Controlbar from './lib/components/controlbar/Controlbar.svelte';

let currentDate = $state('1861-04-12'); // Default to the start of the Civil War

let filteredBattles = $derived(
    battleData.filter(b =>
        b.start_date <= currentDate && 
        b.end_date >= currentDate
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
