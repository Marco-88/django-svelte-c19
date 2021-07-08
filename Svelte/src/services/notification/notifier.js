import { notificationStore } from './notificationStore.js';

export function send (message, type = 'info', timeout = 3000) {
  notificationStore.set({ type, message, timeout });
}

export function error (msg, timeout) {
  send(msg, 'error', timeout);
}

export function info (msg, timeout) {
  send(msg, 'info', timeout);
}

export function success (msg, timeout) {
  send(msg, 'success', timeout)
}