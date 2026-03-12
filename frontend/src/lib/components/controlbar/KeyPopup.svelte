<script>
    let { oneventchange = () => {} } = $props();
    
    // Attach escape key listener to window
    $effect(() => {
        const listener = (e) => {
            if (e.key === 'Escape') {
                oneventchange?.();
            }
        };
        
        window.addEventListener('keydown', listener);
        
        return () => {
            window.removeEventListener('keydown', listener);
        };
    });

    const legendItems = [
        { color: '#4169E1', label: 'Union Victory' },
        { color: '#808080', label: 'Confederate Victory' },
        { color: '#FFD700', label: 'Draw' }
    ];
</script>

<div class="key-popup" role="dialog" tabindex="-1">
    <div class="key-header">
        <h3>Battle Legend</h3>
    </div>
    <div class="key-content">
        <p class="key-description">Marker colors indicate battle outcomes:</p>
        <div class="legend-grid">
            {#each legendItems as item}
                <div class="legend-item">
                    <div class="legend-color" style="background-color: {item.color}">
                        <span class="material-symbols-outlined">swords</span>
                    </div>
                    <span class="legend-label">{item.label}</span>
                </div>
            {/each}
        </div>
    </div>
</div>

<style>
    .key-popup {
        position: absolute;
        top: 0;
        left: 100%;
        margin-left: 0.5rem;
        background: var(--sidebar-background);
        border: 1px solid var(--sidebar-deep-background);
        border-radius: 0.5rem;
        padding: 1rem;
        min-width: 240px;
        z-index: 1001;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .key-header {
        margin-bottom: 1rem;
    }

    .key-header h3 {
        margin: 0;
        font-size: 1rem;
        color: var(--sidebar-icon);
        font-weight: bold;
    }

    .key-content {
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
    }

    .key-description {
        margin: 0 0 0.5rem 0;
        font-size: 0.875rem;
        color: var(--sidebar-icon);
        opacity: 0.8;
    }

    .legend-grid {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }

    .legend-item {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }

    .legend-color {
        width: 30px;
        height: 30px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 16px;
        flex-shrink: 0;
    }

    .legend-label {
        font-size: 0.9rem;
        color: var(--sidebar-icon);
    }
</style>
