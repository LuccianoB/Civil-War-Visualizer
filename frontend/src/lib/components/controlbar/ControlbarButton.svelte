<script>
    export let toggleable = false;
    export let active = false;
    export let onClick = () => {};
    export let ariaLabel = "";

    function handleClick() {
        if (toggleable) {
            active = !active;
        }
        onClick();
    }
</script>

<button 
    class:active 
    on:click={handleClick} 
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
    }

    .bg {
        position: absolute;
        inset: 0;
        background-color: var(--sidebar-icon);
        border-radius: 10px;
        opacity: 0;
        transition: opacity 0.2s ease-in-out;
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

    /* Icon color */
    .controlbar-button :global(svg) {
        fill: var(--sidebar-icon);
    }

    /* Active icon color */
    .controlbar-button.active :global(svg) {
        fill: var(--sidebar-background);
    }
</style>