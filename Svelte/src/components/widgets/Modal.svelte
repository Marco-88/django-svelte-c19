<script>
    import ClickOutside from 'svelte-click-outside';
    import {createEventDispatcher} from 'svelte';

    const dispatch = createEventDispatcher();
    export let hidden = true;

    let initingModal = false;

    const hideModal = () => {
        if (initingModal) {
            initingModal = false;
            dispatch('show', {});
        }
        else {
            hidden = true;
            initingModal = true;
            dispatch('hide', {});
        }
    };

</script>

<ClickOutside on:clickoutside={hideModal}>
    {#if !hidden}
        <div id="modal">
            <slot name="modal-content"></slot>
        </div>
    {/if}
</ClickOutside>

<style>
    #modal {
        position: fixed;
        width: 768px;
        height: 512px;
        left: 50%;
        top: 50%;
        transform: translate(-50%, -50%);
        z-index: 2;
        overflow-y: scroll;
        overflow-x: hidden;
        border: 2px solid var(--background-component-modal);
    }
</style>
