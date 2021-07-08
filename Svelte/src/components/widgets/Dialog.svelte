<script>
    import {navigate} from 'svelte-routing';
    import {createEventDispatcher} from 'svelte';
    import inject from "svelte-inject";
    import Header from '../../layout/Header.svelte';

    export let resolve;
    export let reject = null;
    export let title;
    export let text;
    export let btnOkText = 'Ok';
    export let btnCancelText = 'Cancel';
    export let routeOk = null;
    export let routeCancel = null;

    let active = true;
    let dialog;

    const dispatch = createEventDispatcher();

    const onOk = () => {
        resolve();
        close();
        if (routeOk) navigate(routeOk);
    };

    const onCancel = () => {
        if (reject)
            reject();
        close();
        if (routeCancel) navigate(routeCancel);
    };

    const close = () => {
        dialog.style.display = 'none';
        active = false;
        dispatch('close', {});
    };

</script>

<div bind:this={dialog} class="dialog {active ? 'active' : ''}" use:inject>
    <div>
        <Header {title}/>
        <p>{text}</p>
        <div class="buttons">
            <button type="button" on:click={onOk}>
                {btnOkText}
            </button>
            <button type="button" on:click={onCancel}>
                {btnCancelText}
            </button>
        </div>
    </div>
</div>

<style>
    .dialog {
        width: 100vw;
    }

    .dialog > div {
        display: flex;
        flex-direction: column;
        opacity: 1;
        z-index: 73;
        width: 100%;
        margin-top: 50px;
        background-color: var(--background-component);
    }

    .dialog.active {
        position: fixed;
        top: 0;
        bottom: 0;
        left: 0;
        right: 0;
        opacity: 0.8;
        transition: 0.5s ease;
        background-color: var(--background);
        overflow: hidden;
        z-index: 101;
        width: 100vw;
    }

    .buttons {
        display: flex;
        align-items: center;
        justify-content: center;
    }

</style>
