<script>
    import { currentDate } from '$lib/store';
    
    let { dateValue = new Date(), oneventchange = () => {} } = $props();
    
    // Civil War date range
    const minDate = new Date('1861-04-12');
    const maxDate = new Date('1865-05-26');
    
    // Weekday headers (abbreviated)
    const weekDays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    
    let displayMonth = $state(0);
    let displayYear = $state(2000);
    let showMonthYearSelector = $state(false);
    
    // Reactive updates when dateValue changes
    $effect(() => {
        displayMonth = dateValue.getMonth();
        displayYear = dateValue.getFullYear();
    });
    
    function getDaysInMonth(year, month) {
        return new Date(year, month + 1, 0).getDate();
    }
    
    function getFirstDayOfMonth(year, month) {
        return new Date(year, month, 1).getDay();
    }
    
    function isDateInRange(date) {
        return date >= minDate && date <= maxDate;
    }
    
    function selectDate(day) {
        const selectedDate = new Date(displayYear, displayMonth, day);
        if (isDateInRange(selectedDate)) {
            currentDate.set(selectedDate);
            oneventchange?.();
        }
    }
    
    function previousMonth() {
        if (displayMonth === 0) {
            displayMonth = 11;
            displayYear--;
        } else {
            displayMonth--;
        }
    }
    
    function nextMonth() {
        if (displayMonth === 11) {
            displayMonth = 0;
            displayYear++;
        } else {
            displayMonth++;
        }
    }
    
    function selectMonthYear(month, year) {
        displayMonth = month;
        displayYear = year;
        showMonthYearSelector = false;
    }
    
    function getAvailableMonthYears() {
        const options = [];
        const startYear = minDate.getFullYear();
        const endYear = maxDate.getFullYear();
        const startMonth = minDate.getMonth();
        const endMonth = maxDate.getMonth();
        
        for (let year = startYear; year <= endYear; year++) {
            const yearStart = year === startYear ? startMonth : 0;
            const yearEnd = year === endYear ? endMonth : 11;
            
            for (let month = yearStart; month <= yearEnd; month++) {
                options.push({ month, year });
            }
        }
        
        return options;
    }
    
    const availableMonthYears = $derived(getAvailableMonthYears());
    
    function getCalendarDays() {
        const firstDay = getFirstDayOfMonth(displayYear, displayMonth);
        const daysInMonth = getDaysInMonth(displayYear, displayMonth);
        const daysInPrevMonth = getDaysInMonth(displayYear, displayMonth - 1);
        
        const days = [];
        
        // Previous month's trailing days
        for (let i = firstDay - 1; i >= 0; i--) {
            days.push({
                day: daysInPrevMonth - i,
                isCurrentMonth: false,
                isPrevMonth: true,
                monthOffset: -1
            });
        }
        
        // Current month's days
        for (let i = 1; i <= daysInMonth; i++) {
            days.push({
                day: i,
                isCurrentMonth: true,
                isPrevMonth: false,
                monthOffset: 0
            });
        }
        
        // Next month's leading days
        const remainingCells = 42 - days.length; // 6 rows * 7 days
        for (let i = 1; i <= remainingCells; i++) {
            days.push({
                day: i,
                isCurrentMonth: false,
                isPrevMonth: false,
                monthOffset: 1
            });
        }
        
        return days;
    }
    
    const monthNames = ['January', 'February', 'March', 'April', 'May', 'June', 
                       'July', 'August', 'September', 'October', 'November', 'December'];
    
    const calendarDays = $derived(getCalendarDays());
    const isSelectedDate = (day, isCurrentMonth) => {
        if (!isCurrentMonth) return false;
        return dateValue.getDate() === day && 
               dateValue.getMonth() === displayMonth && 
               dateValue.getFullYear() === displayYear;
    };
</script>

<div class="calendar-popup">
    <div class="calendar-header">
        <button class="nav-button" onclick={previousMonth} aria-label="Previous month">
            &lt;
        </button>
        <button class="month-year" onclick={() => { showMonthYearSelector = !showMonthYearSelector; }} aria-label="Select month and year">
            {monthNames[displayMonth]} {displayYear}
        </button>
        <button class="nav-button" onclick={nextMonth} aria-label="Next month">
            &gt;
        </button>
    </div>
    
    {#if showMonthYearSelector}
        <div class="month-year-selector">
            {#each availableMonthYears as option}
                <button
                    class="month-year-option"
                    class:active={option.month === displayMonth && option.year === displayYear}
                    onclick={() => selectMonthYear(option.month, option.year)}
                >
                    {monthNames[option.month]} {option.year}
                </button>
            {/each}
        </div>
    {:else}
        <div class="calendar-grid">
            {#each weekDays as day}
            <div class="weekday-header">{day}</div>
        {/each}
        
        {#each calendarDays as dayObj (dayObj.monthOffset * 1000 + dayObj.day)}
            {#if dayObj.isCurrentMonth}
                {@const date = new Date(displayYear, displayMonth, dayObj.day)}
                {@const inRange = isDateInRange(date)}
                {@const selected = isSelectedDate(dayObj.day, dayObj.isCurrentMonth)}
                <button
                    class="day-button"
                    class:selected
                    class:disabled={!inRange}
                    onclick={() => selectDate(dayObj.day)}
                    disabled={!inRange}
                    aria-label="Select {monthNames[displayMonth]} {dayObj.day}, {displayYear}"
                >
                    {dayObj.day}
                </button>
            {:else}
                <div class="day-other">
                    {dayObj.day}
                </div>
            {/if}
        {/each}
        </div>
    {/if}
</div>

<style>
    .calendar-popup {
        position: absolute;
        top: 0;
        left: 100%;
        margin-left: 0.5rem;
        background: var(--sidebar-background);
        border: 1px solid var(--sidebar-deep-background);
        border-radius: 0.5rem;
        padding: 0.75rem;
        min-width: 280px;
        z-index: 1001;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .calendar-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
        gap: 0.5rem;
    }
    
    .month-year {
        font-weight: bold;
        color: var(--sidebar-icon);
        font-size: 1rem;
        white-space: nowrap;
        flex: 1;
        text-align: center;
        background: transparent;
        border: 1px solid transparent;
        cursor: pointer;
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        transition: all 0.2s;
    }
    
    .month-year:hover {
        background-color: var(--sidebar-deep-background);
        border-color: var(--sidebar-icon);
    }
    
    .month-year-selector {
        display: flex;
        flex-direction: column;
        gap: 0.25rem;
        max-height: 200px;
        overflow-y: auto;
        border-top: 1px solid var(--sidebar-deep-background);
        padding-top: 0.5rem;
        margin-top: 0.5rem;
    }
    
    .month-year-option {
        padding: 0.5rem;
        border: 1px solid transparent;
        background: transparent;
        color: var(--sidebar-icon);
        cursor: pointer;
        border-radius: 0.25rem;
        font-size: 0.9rem;
        transition: all 0.2s;
        text-align: left;
    }
    
    .month-year-option:hover {
        background-color: var(--sidebar-deep-background);
    }
    
    .month-year-option.active {
        background-color: var(--sidebar-deep-background);
        border-color: var(--sidebar-icon);
        font-weight: bold;
    }
    
    .nav-button {
        background: transparent;
        border: none;
        color: var(--sidebar-icon);
        cursor: pointer;
        font-size: 1.25rem;
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        transition: background-color 0.2s;
    }
    
    .nav-button:hover {
        background-color: var(--sidebar-deep-background);
    }
    
    .calendar-grid {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: 0.25rem;
    }
    
    .weekday-header {
        text-align: center;
        font-weight: bold;
        color: var(--sidebar-icon);
        font-size: 0.85rem;
        padding: 0.5rem 0;
    }
    
    .day-button {
        aspect-ratio: 1;
        border: 1px solid transparent;
        border-radius: 0.25rem;
        background: transparent;
        color: var(--sidebar-icon);
        cursor: pointer;
        font-size: 0.9rem;
        transition: all 0.2s;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .day-button:hover:not(.disabled) {
        background-color: var(--sidebar-deep-background);
    }
    
    .day-button.selected {
        background-color: var(--sidebar-deep-background);
        border-color: var(--sidebar-icon);
        font-weight: bold;
    }
    
    .day-button.disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }
    
    .day-other {
        aspect-ratio: 1;
        display: flex;
        align-items: center;
        justify-content: center;
        color: var(--sidebar-icon);
        opacity: 0.3;
        font-size: 0.9rem;
    }
</style>
