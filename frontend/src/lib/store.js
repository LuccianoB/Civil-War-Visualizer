import { writable } from 'svelte/store';

export const currentDate = writable(new Date('1864-06-02'));