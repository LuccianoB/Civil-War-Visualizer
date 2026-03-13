export function filterBattlesByDate(battles, currentDateString) {
    return battles.filter(
        (b) => b.start_date <= currentDateString && b.end_date >= currentDateString
    );
}