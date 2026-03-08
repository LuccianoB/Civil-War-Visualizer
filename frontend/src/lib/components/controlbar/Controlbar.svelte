<script>
    import ControlbarButton from './ControlbarButton.svelte';
    import CalendarIcon from '../icons/CalendarIcon.svelte';
    import KeyIcon from '../icons/KeyIcon.svelte';
</script>

<div class="controlbar bg-vr(--sidebar-background) rounded-lg">
    <div class="upper_controlbar">
    </div>
    <div class="lower_controlbar">
    </div>
</div>

<style>
    .controlbar {
        position: absolute;
        top: 1rem;
        left: 1rem;
        display: flex;
        flex-direction: column;
        z-index: 1000; /* Ensure it sits above the map */
    }
</style>