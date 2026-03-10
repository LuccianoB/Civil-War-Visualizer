import { writable } from 'svelte/store';

export const currentDate = writable(new Date('1861-04-12'));