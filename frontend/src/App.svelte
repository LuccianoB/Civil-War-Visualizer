<script>
import Map from './lib/components/Map.svelte';
import battleData from './lib/data/enriched_battles.json';
import TimelineSlider from './lib/components/TimelineSlider.svelte';

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

    <div class="bg-white border-b border-grey-200 p-4 shadow-sm">
            <TimelineSlider bind:currentDate />
    </div>
    <div class="flex-1">
        <Map battles={filteredBattles} />
    </div>
</main>
