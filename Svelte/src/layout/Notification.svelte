<style>
    :global(.toasts) {
        list-style: none;
        position: fixed;
        top: 0;
        padding: 0;
        margin: 0;
        z-index: 9999;
    }

    :global(.toasts) > .toast {
        position: relative;
        padding: 10px;
        animation: animate-in 350ms forwards;
        color: #fff;
    }

    :global(.toasts) > .toast > .content {
        padding: 10px;
        display: block;
        font-weight: 500;
    }

    :global(.toasts) > .toast > .progress {
        position: absolute;
        bottom: 0;
        background-color: rgb(0, 0, 0, 0.3);
        height: 6px;
        width: 100%;
        animation-name: shrink;
        animation-timing-function: linear;
        animation-fill-mode: forwards;
    }

    :global(.toasts) > .toast:before,
    :global(.toasts) > .toast:after {
        content: '';
        position: absolute;
        z-index: -1;
        top: 50%;
        bottom: 0;
        left: 10px;
        right: 10px;
        border-radius: 100px / 10px;
    }

    :global(.toasts) > .toast:after {
        right: 10px;
        left: auto;
        transform: skew(8deg) rotate(3deg);
    }

    @keyframes animate-in {
        0% {
            width: 0;
            opacity: 0;
            transform: scale(1.15) translateY(20px);
        }
        100% {
            width: 20vw;
            opacity: 1;
            transform: scale(1) translateY(0);
        }
    }

    @keyframes shrink {
        0% {
            width: 20vw;
        }
        100% {
            width: 0;
        }
    }
</style>

<script>
    import { notificationStore } from '../services/notification/notificationStore.js';
    import { onMount, onDestroy } from 'svelte';

    export let themes = {
        error: {
            background: '#bb2124',
            color: '#ffffff'
        },
        success: {
            background: '#22bb33',
            color: '#ffffff'
        },
        info: {
            background: '#5bc0de',
            color: '#ffffff'
        }
    };

    export let timeout = 3000;

    let count = 0;
    let toasts = [];
    let unsubscribe;

    function animateOut(node, { delay = 0, duration = 300 }) {
        function vhTOpx(value) {
            let e = document.documentElement,
                g = document.getElementsByTagName('body')[0],
                x = window.innerWidth || e.clientWidth || g.clientWidth,
                y = window.innerHeight || e.clientHeight || g.clientHeight;

            return (y * value) / 100;
        }

        return {
            delay,
            duration,
            css: t =>
                `opacity: ${(t - 0.5) * 1};
                transform-origin: top right;
                transform: scaleX(${(t - 0.5) * 1});`,
        };
    }

    function createToast(msg, theme, to) {
        const {background, color} = themes[theme];
        toasts = [
            {
                id: count,
                msg,
                background,
                color,
                timeout: to || timeout,
            },
            ...toasts,
        ];
        count = count + 1;
    }

    unsubscribe = notificationStore.subscribe(value => {
        if (!value) {
            return;
        }
        createToast(value.message, value.type, value.timeout);
        notificationStore.set();
    });

    onDestroy(unsubscribe);

    function removeToast(id) {
        toasts = toasts.filter(t => t.id != id);
    }
</script>

<ul class="toasts">
    {#each toasts as toast (toast.id)}
        <li
            class="toast"
            style="{`background: ${toast.background}`}; {`color: ${toast.color}`};"
            out:animateOut
        >
            <div class="content">{toast.msg}</div>
            <div
                class="progress"
                style="animation-duration: {toast.timeout}ms;"
                on:animationend="{() => removeToast(toast.id)}"
            ></div>
        </li>
    {/each}
</ul>
