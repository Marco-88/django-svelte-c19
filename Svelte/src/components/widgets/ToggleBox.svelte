<script>
    import ClickOutside from 'svelte-click-outside';
    import Header from '../../layout/Header.svelte';
    import ActionIcons from './ActionIcons.svelte';
    import { afterUpdate, onMount } from 'svelte';

    export let title;
    export let hidden = true;
    export let clickOutside = true;
    export let actionIconOpen;
    export let actionIconClose;
    let modal;

    const hideModal = () => {
        modal.hidden = true;
    };

    const showModal = () => {
        modal.hidden = false;
        const input = modal.querySelector('input');
        if(input)
            input.focus();
    };

    let actionOpen = {};
    let permissionOpen = {};
    let actionClose = {};
    let permissionClose = {};

    onMount(() => {
        modal.hidden = hidden;
        actionOpen[actionIconOpen.actionName] = showModal;
        permissionOpen[actionIconOpen.actionName] = modal.hidden;
        actionClose[actionIconClose.actionName] = hideModal;
        permissionClose[actionIconClose.actionName] = !modal.hidden;
    });

    afterUpdate(() => {
        actionOpen[actionIconOpen.actionName] = showModal;
        permissionOpen[actionIconOpen.actionName] = modal.hidden;
        actionClose[actionIconClose.actionName] = hideModal;
        permissionClose[actionIconClose.actionName] = !modal.hidden;
    });
</script>

<div class="toggle-box">
    <Header {title}>
        <div slot="actionIcons">
            {#if modal}
                {#if modal.hidden}
                    <ActionIcons
                            permissions={permissionOpen}
                            tooltips={actionIconOpen.tooltip}
                            actions={actionOpen}
                    />
                {:else}
                    <ActionIcons
                            permissions={permissionClose}
                            tooltips={actionIconClose.tooltip}
                            actions={actionClose}
                    />
                {/if}
            {/if}
        </div>
    </Header>
    <slot name="content"></slot>
    <ClickOutside on:clickoutside={() => clickOutside ? hideModal() : ''}>
        <div class="toggle-content" bind:this={modal} hidden>
            <slot name="toggle-content"></slot>
        </div>
    </ClickOutside>
</div>
