<script>
    import ControlbarButton from './ControlbarButton.svelte';
    import { KeyIcon, CalendarIcon, LogoIcon, DoublearrowIcon, ArrowIcon, DownArrow, MapsettingsIcon, PlaybuttonIcon, PausebuttonIcon, InfoIcon } from '$lib/components/icons';
    let playbackSpeed = "1";
</script>

<div class="controlbar">
    <div class="upper_controlbar">
        <div>
            <LogoIcon width="3rem" height="3rem" />
        </div>
        <div class="top-right-buttons">
            <ControlbarButton ariaLabel="Key">
                <KeyIcon slot="icon" />
            </ControlbarButton>
            <ControlbarButton ariaLabel="Map Settings">
                <MapsettingsIcon slot="icon" />
            </ControlbarButton>
            <ControlbarButton ariaLabel="Info">
                <InfoIcon slot="icon" />
            </ControlbarButton>
        </div>
    </div>
    <div class="lower_controlbar">
        <ControlbarButton ariaLabel="Play">
            <PlaybuttonIcon slot="icon" />
        </ControlbarButton>
        <ControlbarButton ariaLabel="Pause">
            <span slot="icon" class="playback-speed">{playbackSpeed}x</span>
        </ControlbarButton>
        <div class="date-management-control">
            <ControlbarButton ariaLabel="Previous Month">
                <DoublearrowIcon slot="icon" />
            </ControlbarButton>
            <ControlbarButton ariaLabel="Previous Day">
                <ArrowIcon slot="icon" />
            </ControlbarButton>
            <div>06-02-1864</div>
            <ControlbarButton ariaLabel="Next Day">
                <ArrowIcon slot="icon" rotate={180} />
            </ControlbarButton>
            <ControlbarButton ariaLabel="Next Month">
                <DoublearrowIcon slot="icon" rotate={180} />
            </ControlbarButton>


                

        </div>
    </div>
</div>

<style>
    .controlbar {
        background: var(--sidebar-background);
        border-radius: 0.5rem;
        position: absolute;
        top: 1rem;
        left: 1rem;
        display: flex;
        flex-direction: column;
        z-index: 1000; /* Ensure it sits above the map */
    }

    .upper_controlbar, .lower_controlbar {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: center;
        padding: 0.2rem 1.5rem;
    }

    .top-right-buttons {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .date-management-control {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .playback-speed {
        width: var(--control-bar-icon-size);
        height: var(--control-bar-icon-size);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        font-weight: bold;
        color: var(--sidebar-icon);
    }

    :global(.rotate-180) {
        transform: rotate(180deg);
    }
</style>