<script>
    import { Link, navigate } from 'svelte-routing';
    import { onMount } from 'svelte';
    import ActionIcons from './ActionIcons.svelte';
    import {timeAgo} from '../../utils';

    export let data = {};
    export let options = {};
    export let hoverable = false;

    let size;

    let color = getComputedStyle(document.documentElement).getPropertyValue('--primary');
    let background = getComputedStyle(document.documentElement).getPropertyValue('--background-component');
    let route;

    const init = () => {
        size = options.size || 32;
        color = options.color || color;
        route = `/${data.url}/${data.id}`;
    };

    onMount(() => {
        init();
    });
</script>

<li class="list-item row {hoverable ? 'hover' : ''} z-depth-1-half"
    on:click={() => hoverable ? navigate(route) : ''}>
    <div class="col-9 data">
        <div class="image-wrapper"
             style={`width: ${size}px; height: ${size}px; min-width: ${size}px; min-height: ${size}px; max-width: ${size}px; max-height: ${size}px;`}>
            {#if data.image}
                <img src={data.image} alt="img"
                     style={`width: ${size}px; height: ${size}px; min-width: ${size}px; min-height: ${size}px; max-width: ${size}px; max-height: ${size}px;`}>
            {/if}
        </div>
        {#if hoverable}
            <p style={`color: ${color.color}; height: ${size}px;`}>{data.name}</p>
        {:else}
            <Link to={route}>
                <p style={`color: ${color.color}; height: ${size}px;`}>{data.name}</p>
            </Link>
        {/if}
        {#if data.info}
            <p class="date">{timeAgo(data.date) + ' - ' + data.info}</p>
        {/if}
    </div>
    <div class="col-3 icons">
        <slot name="actionIcons">
            {#if data.tile}
                <p>{data.tile}</p>
            {/if}
        </slot>
    </div>
</li>

<style>
    li.list-item.row {
        background: var(--background-list-item);
    }

    li.list-item.row.hover:hover {
        background: var(--background-component-hover);
        cursor: pointer;
    }

    .list-item p {
        padding: 0;
        margin: 0;
        margin-left: 1rem;
        width: 100%;
        line-height: 1.2rem;
    }

    .list-item, .list-item a, .list-item p {
        display: flex;
        align-items: center;
    }

    .row, .col-3, .col-9 {
        padding: 0;
        margin: 0;
    }

    .list-item p {
        padding: 0 10px;
        margin: 0;
    }

    .list-item .col-3, .list-item .col-9 {
        display: flex;
        align-items: center;
    }

    .list-item .col-3.icons, .icon p {
        justify-content: flex-end;
    }

    .list-item {
        padding: 3px;
        /*margin: 3px 0;*/
        border: 1px solid var(--background);
    }

    .icons p {
        text-align: right;
    }

    .data {
        display: flex;
    }

    .data p {
        text-align: left;
    }

    .list-item p.date {
        width: 50%;
    }

</style>
