<script>
    let { toggleable = false, active = false, onClick = () => {}, ariaLabel = "" } = $props();

    function handleClick() {
        onClick();
    }
</script>

<button 
    class:active 
    onclick={handleClick}
    class="controlbar-button"
    aria-label={ariaLabel}
>
    <div class="bg"></div>
    <slot name="icon" />
</button>

<style>
    .controlbar-button {
        position: relative;
        background: transparent;
        border: none;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 0.25rem;
        color: var(--sidebar-icon);
    }

    .bg {
        position: absolute;
        inset: 0;
        background-color: var(--sidebar-icon);
        border-radius: 10px;
        opacity: 0;
        transition: opacity 0.2s ease-in-out;
        z-index: -1;
    }

    /* Hover background*/
    .controlbar-button:hover:not(.active) .bg{
        opacity: 0.25;
    }

    /* Active background */
    .controlbar-button.active .bg {
        background-color: var(--sidebar-icon);
        opacity: 1;
    }

    .controlbar-button.active {
        color: var(--sidebar-background);
    }

    .controlbar-button.active :global(.material-symbols-outlined) {
        color: var(--sidebar-background);
    }

    /* Icon styling */
    .controlbar-button :global(.material-symbols-outlined) {
        width: var(--control-bar-icon-size);
        height: var(--control-bar-icon-size);
        transition: color 0.2s ease-in-out;
        color: inherit;
        line-height: 1;
        display: inline-flex;
        align-items: center;
        justify-content: center;
    }
</style>