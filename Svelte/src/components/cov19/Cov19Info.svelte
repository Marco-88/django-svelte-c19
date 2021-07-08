<style>
    #cov19-panel {
        background: var(--background);
        margin: 0;
        border-left: 1px solid var(--primary);
        border-right: 1px solid var(--primary);
    }

    #cov19-panel td,
    #cov19-panel th {
        border: 1px solid var(--primary);
        background: var(--background-component);
    }

    .cases-all-head {
        grid-area: cases-all-head;
        color: var(--background);
        background: var(--cov19-all-cases);
    }

    .deaths-all-head {
        grid-area: deaths-all-head;
        color: var(--background);
        background: var(--cov19-all-deaths);
    }

    .recovered-all-head {
        grid-area: recovered-all-head;
        color: var(--background);
        background: var(--cov19-all-recovered);
    }

    .active-all-head {
        grid-area: active-all-head;
        color: var(--background);
        background: var(--cov19-all-active);
    }

    .todaycases-all-head {
        grid-area: todaycases-all-head;
        color: var(--background);
        background: var(--cov19-all-today-cases);
    }

    .todaydeaths-all-head {
        grid-area: todaydeaths-all-head;
        color: var(--background);
        background: var(--cov19-all-today-deaths);
    }

    .cases-all-val {
        grid-area: cases-all-val;
        color: var(--cov19-all-cases);
        background: var(--background);
    }

    .deaths-all-val {
        grid-area: deaths-all-val;
        color: var(--cov19-all-deaths);
        background: var(--background);
    }

    .recovered-all-val {
        grid-area: recovered-all-val;
        color: var(--cov19-all-recovered);
        background: var(--background);
    }

    .active-all-val {
        grid-area: active-all-val;
        color: var(--cov19-all-active);
        background: var(--background);
    }

    .todaycases-all-val {
        grid-area: todaycases-all-val;
        color: var(--cov19-all-today-cases);
        background: var(--background-component);
    }

    .todaydeaths-all-val {
        grid-area: todaydeaths-all-val;
        color: var(--cov19-all-today-deaths);
        background: var(--background-component);
    }

    #cov19-panel .cov-all-panel {
        margin: 0 auto;
        display: grid;
        grid-template-columns: 50% 50%;
        grid-template-rows: auto;
        grid-template-areas: 'todaycases-all-head todaycases-all-val' 'todaydeaths-all-head todaydeaths-all-val' 'cases-all-head cases-all-val' 'deaths-all-head deaths-all-val' 'recovered-all-head recovered-all-val' 'active-all-head active-all-val';
        align-items: center;
        background: var(--background);
    }

    .cov-all-panel p {
        margin: 0;
        padding: 0;
        text-align: center;
        font-weight: bold;
        font-size: 1.2rem;
        border: 1px solid var(--background-component);
    }

    .date {
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
    }
</style>

<script>
    import Header from '../../layout/Header.svelte';
    import { error } from '../../services/notification/notifier';
    import { cov19Store } from '../../services/cov19/cov19Store';
    import { getDate, getTime, getColSum } from '../../utils';

    let covTable;

    $: rows = $cov19Store.rows;
    $: all = $cov19Store.all;
    $: cols = $cov19Store.cols;

</script>

{#if !$cov19Store.rows.length > 0 || !$cov19Store.all || !$cov19Store.cols}
    <h5>Waiting for Corona...</h5>
{:else}
    <section id="cov19-panel" class="z-depth-2">
        <div class="date">{getDate()} - {getTime()}</div>
        <div class="cov-all-panel">
            {#each ['todayCases', 'todayDeaths'] as value}
                <div class="{value.toLowerCase()}-all-head">
                    <p>{value.toUpperCase()}</p>
                </div>
                <div class="{value.toLowerCase()}-all-val">
                    <p>{getColSum(value, rows)}</p>
                </div>
            {/each}
            {#each Object.keys(all) as key}
                <div class="{key}-all-head">
                    <p>{key.toUpperCase()}</p>
                </div>
                <div class="{key}-all-val">
                    <p>{all[key]}</p>
                </div>
            {/each}
            <div class="active-all-head">
                <p>ACTIVE</p>
            </div>
            <div class="active-all-val">
                <p>{all['cases'] - all['deaths'] - all['recovered']}</p>
            </div>
        </div>
    </section>
{/if}
