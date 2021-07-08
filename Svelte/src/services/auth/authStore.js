import { writable } from 'svelte/store';

function createAuthStore() {
    const { subscribe, set, update } = writable({
        user: null,
        token: localStorage.getItem('token'),
        loading: false
    });
    
    return {
        subscribe,
        start: () =>
            update(() => ({
                user: null,
                token: null,
                loading: true,
            })),
        loggedIn: token => {
            localStorage.setItem('token', token);
            update(() => ({
                user: null,
                token,
                loading: false,
            }));
        },
        userLoaded: (token, user) => {
            localStorage.setItem('user', user);
            localStorage.setItem('token', token);
            update(() => ({
                user,
                token,
                loading: false,
            }));
        },
        loggedOut: () => {
            localStorage.removeItem('user');
            localStorage.removeItem('token');
            set({
                user: null,
                token: null,
                loading: false
            });
        },
        registered: user => {
            localStorage.setItem('user', user);
            set({
                user,
                token: null,
                loading: false
            });
        },
        updateUser: user => {
            localStorage.setItem('user', user);
            update({
                user
            });
        }
    };
}

export const authStore = createAuthStore();