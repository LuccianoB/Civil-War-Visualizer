<script lang="ts">
    let {currentDate = $bindable('1861-04-12')} = $props();

    // Convert date string to timestamp (milliseconds since epoch)
    function dateToTimestamp(dateStr: string): number {
        return new Date(dateStr).getTime();
    }

    // Convert timestamp back to date string (YYYY-MM-DD)
    function timestampToDate(timestamp: number): string {
        const date = new Date(timestamp);
        return date.toISOString().split('T')[0];
    }

    const minDate = '1861-04-12';
    const maxDate = '1865-05-26';
    const minTimestamp = dateToTimestamp(minDate);
    const maxTimestamp = dateToTimestamp(maxDate);

    let sliderValue = $state(dateToTimestamp(currentDate));

    $effect(() => {
        currentDate = timestampToDate(sliderValue);
    });
</script>

<div class="flex flex-col items-center justify-center w-full p-4">
    <div>
        <p class="mb-3 text-lg font-semibold">
            {new Date(sliderValue).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })}
        </p>
    </div>
    <input class ="w-full ml-5 mr-5"
        type="range"
        min={minTimestamp} 
        max={maxTimestamp} 
        step={24 * 60 * 60 * 1000}
        bind:value={sliderValue}
    />
</div>