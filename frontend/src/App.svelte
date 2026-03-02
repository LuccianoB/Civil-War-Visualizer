<script>
import Map from './lib/components/Map.svelte';
</script>

<main class="flex flex-col w-full h-screen bg-[#EFD6AC]">
    <!-- Header -->
    <header class="bg-slate-800 text-white p-6  flex justify-center">
        <h1 class="text-3xl font-bold">Civil War Battle Visualizer</h1>
    </header>

    <div class="bg-white border-b border-grey-200 p-4 shadow-sm">
        <div class="max-w-6xl mx-auto">
            <!-- Timeline slider will go here ---->
            <p class="text-gray-600 text-sm">Timeline slider coming soon...</p>
        </div>
    </div>
    <div class="flex-1">
        <Map />
    </div>
</main>
