import { writable } from 'svelte/store';
import { CIVIL_WAR_START } from './utils/constants';

export const currentDate = writable(CIVIL_WAR_START);