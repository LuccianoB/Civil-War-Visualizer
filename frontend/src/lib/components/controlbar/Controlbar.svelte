<script>
    import ControlbarButton from './ControlbarButton.svelte';
    import { KeyIcon, CalendarIcon, LogoIcon, DoublearrowIcon, ArrowIcon, ClockArrowDownIcon, MapsettingsIcon, PlaybuttonIcon, PausebuttonIcon, InfoIcon } from '$lib/components/icons';
    import { currentDate } from '$lib/store';
    
    let playbackSpeed = "1";

    function addDays(date, days) {
        const result = new Date(date);
        result.setDate(result.getDate() + days);
        return result;
    }

    function previousDay() {
        currentDate.set(addDays($currentDate, -1));
    }

    function nextDay() {
        currentDate.set(addDays($currentDate, 1));
    }

    function previousMonth() {
        currentDate.set(addDays($currentDate, -30));
    }

    function nextMonth() {
        currentDate.set(addDays($currentDate, 30));
    }
</script>

<div class="controlbar">
    <div class="upper_controlbar">
        <div>
            <LogoIcon width="2.5rem" height="2.5rem" />
        </div>
        <div class="top-right-buttons">
            <ControlbarButton ariaLabel="Key" toggleable={true}>
                <KeyIcon slot="icon" />
            </ControlbarButton>
            <ControlbarButton ariaLabel="Map Settings" toggleable={true}>
                <MapsettingsIcon slot="icon" />
            </ControlbarButton>
            <ControlbarButton ariaLabel="Info" toggleable={true}>
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
            <ControlbarButton ariaLabel="Previous Month" onClick={previousMonth}>
                <DoublearrowIcon slot="icon" rotate={180} />
            </ControlbarButton>
            <ControlbarButton ariaLabel="Previous Day" onClick={previousDay}>
                <ArrowIcon slot="icon" rotate={180} />
            </ControlbarButton>
            <div ariaLabel="selected Date" class="selected-date">
                {$currentDate.toLocaleDateString('en-US', { month: '2-digit', day: '2-digit', year: 'numeric' })}
            </div>
            <ControlbarButton ariaLabel="Next Day" onClick={nextDay}>
                <ArrowIcon slot="icon" />
            </ControlbarButton>
            <ControlbarButton ariaLabel="Next Month" onClick={nextMonth}>
                <DoublearrowIcon slot="icon" />
            </ControlbarButton>
        </div>
        <ControlbarButton ariaLabel="Timeline-toggle" toggleable={true}>
            <ClockArrowDownIcon slot="icon" />
        </ControlbarButton>
        <ControlbarButton ariaLabel="Select Date by Calendar" toggleable={true}>
            <CalendarIcon slot="icon"/>
        </ControlbarButton>
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
        padding: 0.2rem 0.5rem;
    }

    .upper_controlbar {
        border-bottom: 1px solid var(--sidebar-deep-background);
    }

    .lower_controlbar {
        border-top: 1px solid var(--sidebar-deep-background);
        --control-bar-icon-size: var(--control-lower-bar-icon-size);
        padding-top: 0.3rem;
        gap: 0.5rem;
    }

    .top-right-buttons {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .date-management-control {
        display: flex;
        align-items: center;
        margin-inline: 0.5rem;
    }

    .selected-date {
        margin: 0 0.5rem;
        color: var(--sidebar-icon);
        font-size: 1.25rem;
        font-weight: bold;
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