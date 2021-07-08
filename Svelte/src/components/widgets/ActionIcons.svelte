<style>
    .icon {
        cursor: pointer;
    }

    ul {
        display: flex;
        padding: 0;
        margin: 0;
    }

    ul li:not(:last-child) {
        margin-right: 3px;
    }

    .icon.actionPlus,
    .icon.actionUserPlus,
    .icon.actionThumbsUp {
        color: var(--success);
    }

    .icon.actionPlus:hover,
    .icon.actionUserPlus:hover,
    .icon.actionThumbsUp:hover {
        color: var(--success-hover);
    }

    .icon.actionMinus,
    .icon.actionTrash,
    .icon.actionUserMinus,
    .icon.actionThumbsDown {
        color: var(--btn-delete);
    }

    .icon.actionMinus:hover,
    .icon.actionTrash:hover,
    .icon.actionUserMinus:hover,
    .icon.actionThumbsDown:hover {
        color: var(--btn-delete-hover);
    }

    .icon.actionEdit,
    .icon.actionBars,
    .icon.actionSearch {
        color: var(--color-component-info);
    }

    .icon.actionEdit:hover,
    .icon.actionBars:hover,
    .icon.actionSearch:hover {
        color: var(--color);
    }

    .icon.actionSignOut,
    .icon.actionTimes {
        color: var(--background);
    }

    .icon.actionSignOut:hover,
    .icon.actionTimes:hover {
        color: var(--color-component);
    }
</style>

<script>
    import Fa from 'svelte-fa';
    import {
        faUserPlus,
        faUserMinus,
        faTrash,
        faPlus,
        faMinus,
        faSignOutAlt,
        faSearch,
        faEdit,
        faThumbsUp,
        faThumbsDown,
        faBars,
        faTimes,
    } from '@fortawesome/free-solid-svg-icons';
    import { onMount } from 'svelte';

    export let size = 'lg';
    export let actions = {};
    export let permissions = {};
    export let text = {};
    export let tooltips = {};

    let icons = {
        actionPlus: faPlus,
        actionUserPlus: faUserPlus,
        actionMinus: faMinus,
        actionUserMinus: faUserMinus,
        actionTrash: faTrash,
        actionSignOut: faSignOutAlt,
        actionSearch: faSearch,
        actionEdit: faEdit,
        actionThumbsUp: faThumbsUp,
        actionThumbsDown: faThumbsDown,
        actionBars: faBars,
        actionTimes: faTimes,
    };

    let currentPermissions = {};

    const initPermissions = () => {
        Object.keys(actions).forEach(key => {
            currentPermissions[key] =
                typeof permissions[key] === 'boolean' ? permissions[key] : true;
        });
    };

    onMount(() => initPermissions());

    initPermissions();
</script>

<ul>
    {#each Object.keys(actions) as key}
        {#if currentPermissions[key]}
            <li
                class="icon {key}"
                on:click|stopPropagation="{actions[key]}"
                title="{tooltips[key]}"
            >
                {#if text[key]}{text[key]}{/if}
                <Fa fw icon="{icons[key]}" {size} />
            </li>
        {/if}
    {/each}
</ul>
