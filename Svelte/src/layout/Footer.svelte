<script>
    import {Link} from 'svelte-routing';

    export let title;
    export let route = null;
</script>

<style>
    .panel-footer .left {
        grid-area: left;
        display: flex;
        justify-content: flex-start;
        padding: 0;
        margin: 0;
    }

    .panel-footer .right {
        grid-area: right;
        display: flex;
        justify-content: flex-end;
        padding: 0;
        margin: 0;
    }

    .panel-footer {
        padding: 0 5px;
        display: grid;
        grid-template-columns: 2% 48% 48% 2%;
        grid-template-rows: auto;
        grid-template-areas: ". left right .";
        background: var(--primary);
        height: 48px;
    }

    :global(.panel-footer a) {
        color: var(--color-component);
    }

    :global(.panel-footer a:hover) {
        color: var(--background);
        text-decoration: none;
    }
</style>

<div class="panel-footer">
    <div class="left">
        <slot name="left"/>
    </div>
    <div class="right">
        <slot name="right"/>
    </div>
</div>
