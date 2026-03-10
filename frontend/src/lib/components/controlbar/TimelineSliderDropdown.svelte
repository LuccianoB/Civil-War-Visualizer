<script>
    import { currentDate } from '$lib/store';

    const minDate = '1861-04-12';
    const maxDate = '1865-05-26';
    const minTimestamp = new Date(minDate).getTime();
    const maxTimestamp = new Date(maxDate).getTime();

    function handleSliderChange(e) {
        const timestamp = parseInt(e.target.value);
        const newDate = new Date(timestamp);
        currentDate.set(newDate);
    }

    let sliderValue = $derived(new Date($currentDate).getTime());
</script>

<div class="timeline-slider-dropdown">
    <div class="slider-content">
        <input
            type="range"
            min={minTimestamp}
            max={maxTimestamp}
            step={24 * 60 * 60 * 1000}
            value={sliderValue}
            onchange={handleSliderChange}
            oninput={handleSliderChange}
            class="slider"
        />
    </div>
</div>

<style>
    .timeline-slider-dropdown {
        background: var(--sidebar-deep-background);
        padding: 1rem;
        border-radius: 0 0 0.5rem 0.5rem;
        margin-top: 1px;
        width: 100%;
        box-sizing: border-box;
    }

    .slider-content {
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
    }

    .date-display {
        text-align: center;
        margin: 0;
        color: var(--sidebar-icon);
        font-size: 1rem;
        font-weight: 600;
    }

    .slider {
        width: 100%;
        cursor: pointer;
        accent-color: var(--sidebar-icon);
    }

    .slider::-webkit-slider-thumb {
        cursor: pointer;
    }

    .slider::-moz-range-thumb {
        cursor: pointer;
    }
</style>
