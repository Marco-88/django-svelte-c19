<script>
    import {Link} from 'svelte-routing';

    export let title;
    export let route = null;
</script>

<style>
    .panel-header .title {
        grid-area: title;
        font-size: 1rem;
        padding: 3px 0 5px 0;
        margin: 0;
        height: 24px;
        line-height: 24px;
    }

    .panel-header .icons {
        grid-area: icons;
    }

    .panel-header {
        padding: 0 5px;
        display: grid;
        grid-template-columns: 2% 78% 18% 2%;
        grid-template-rows: auto;
        grid-template-areas: ". title icons .";
        align-items: center;
        background: var(--primary);
        height: 32px;
    }

    .icons {
        display: flex;
        justify-content: flex-end;
        align-items: center;
        width: 100%;
        height: 24px;
        line-height: 24px;
    }

    .title {
        display: flex;
        align-items: center;
        width: 100%;
        height: 24px;
        line-height: 24px;
    }

    :global(.panel-header a) {
        color: var(--color-component);
    }

    :global(.panel-header a:hover) {
        color: var(--background);
        text-decoration: none;
    }
</style>

<div class="panel-header">
    <div class="title">
        {#if route}
            <Link to={route}>
                <h4 title={`Go to ${route}`}>{title}</h4>
            </Link>
        {:else}
            <h4>{title}</h4>
        {/if}
    </div>
    <div class="icons">
        <slot name="actionIcons"/>
    </div>
</div>
