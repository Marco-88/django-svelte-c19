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

    #cov19-panel td {
        color: var(--color-component);
        padding: 0 5px;
    }

    #cov19-panel th {
        color: var(--cov19-color-header);
        font-weight: bold;
    }

    .cases-all-head {
        grid-area: cases-all-head;
        color: var(--cov19-color-header);
    }

    .deaths-all-head {
        grid-area: deaths-all-head;
        color: var(--cov19-color-header);
    }

    .recovered-all-head {
        grid-area: recovered-all-head;
        color: var(--cov19-color-header);
    }

    .active-all-head {
        grid-area: active-all-head;
        color: var(--cov19-color-header);
    }

    .critical-all-head {
        grid-area: critical-all-head;
        color: var(--cov19-color-header);
    }

    .todaycases-all-head {
        grid-area: todaycases-all-head;
        color: var(--cov19-color-header);
    }

    .todaydeaths-all-head {
        grid-area: todaydeaths-all-head;
        color: var(--cov19-color-header);
    }

    .cases-all-val {
        grid-area: cases-all-val;
        color: var(--cov19-all-cases);
    }

    .deaths-all-val {
        grid-area: deaths-all-val;
        color: var(--cov19-all-deaths);
    }

    .recovered-all-val {
        grid-area: recovered-all-val;
        color: var(--cov19-all-recovered);
    }

    .active-all-val {
        grid-area: active-all-val;
        color: var(--cov19-all-active);
    }

    .critical-all-val {
        grid-area: critical-all-val;
        color: var(--cov19-all-critical);
    }

    .todaycases-all-val {
        grid-area: todaycases-all-val;
        color: var(--cov19-all-cases);
    }

    .todaydeaths-all-val {
        grid-area: todaydeaths-all-val;
        color: var(--cov19-all-deaths);
    }

    #cov19-panel .cov-all-panel {
        margin: 0 auto;
        width: 70%;
        display: grid;
        grid-template-columns: 20% 20% 20% 20% 20%;
        grid-template-rows: auto;
        grid-template-areas: 'cases-all-head deaths-all-head recovered-all-head active-all-head critical-all-head' 'cases-all-val deaths-all-val recovered-all-val active-all-val critical-all-val' 'todaycases-all-head todaycases-all-head . todaydeaths-all-head todaydeaths-all-head' 'todaycases-all-val todaycases-all-val . todaydeaths-all-val todaydeaths-all-val';
        align-items: center;
        background: var(--background);
    }

    .cov-all-panel p,
    .cov-all-panel h3 {
        margin: 0;
        padding: 5px;
        text-align: center;
        font-weight: bold;
    }

    .cov-all-panel p {
        font-size: 1.6rem;
    }

    .cov-all-panel h3 {
        font-size: 1.9rem;
    }
</style>

<script>
    import Header from '../../layout/Header.svelte';
    import { cov19Store } from '../../services/cov19/cov19Store';
    import { TableSort } from 'svelte-tablesort';
    import { formatDate, getColSum } from '../../utils';

    let covTable;

    $: rows = $cov19Store.rows;
    $: all = $cov19Store.all;
    $: cols = $cov19Store.cols;

    const thMap = {
        COUNTRY: 'Country',
        CASES: 'Cases',
        TODAYCASES: 'Today Cases',
        DEATHS: 'Deaths',
        TODAYDEATHS: 'Today Deaths',
        RECOVERED: 'Recovers',
        ACTIVE: 'Active',
        CRITICAL: 'Critical',
        TOTALTEST: 'Total Tests',
        CASESPERONEMILLION: 'Cases / 1 Mil',
        DEATHSPERONEMILLION: 'Deaths / 1 Mil',
        TESTSPERONEMILLION: 'Tests / 1 Mil',
    };

    const thStyleMap = {
        COUNTRY: 'Width: 90px',
        CASES: 'Width: 105px',
        TODAYCASES: 'Width: 65px',
        DEATHS: 'Width: 95px',
        TODAYDEATHS: 'Width: 60px',
        RECOVERED: 'Width: 90px',
        ACTIVE: 'Width: 90px',
        CRITICAL: 'Width: 75px',
        TOTALTEST: 'Width: 100px',
        CASESPERONEMILLION: 'Width: 65px',
        DEATHSPERONEMILLION: 'Width: 50px',
        TESTSPERONEMILLION: 'Width: 65px',
    };

    const worldHeaders = ['cases', 'deaths', 'recovered', 'active', 'critical', 'todayCases', 'todayDeaths'];

    const getTdStyle = (item, key) => {
        if (item['cases'] - item['recovered'] === 0) {
            return 'background: var(--cov19-bg-closed-recovered);';
        }
        if (item['cases'] - item['deaths'] - item['recovered'] === 0) {
            return 'background: var(--cov19-bg-closed);';
        }
        let style = '';
        style =
            key === 'todayCases' && item[key] !== 0
                ? 'background: var(--cov19-bg-new-cases);'
                : '';
        style +=
            key === 'todayDeaths' && item[key] !== 0
                ? 'background: var(--cov19-bg-new-deaths);'
                : '';
        return style;
    };
</script>

{#if !$cov19Store || !$cov19Store.rows || !$cov19Store.rows.length > 0 || !$cov19Store.all || !$cov19Store.cols}
    <h5>Waiting for Corona...</h5>
{:else}
    <section id="cov19-panel" class="z-depth-2">
        <Header title="Corona (CoV19) Table - {formatDate(new Date())}" />
        <div class="cov-all-panel">
            {#each worldHeaders as key}
                <div class="{key.toLowerCase()}-all-head">
                    <h3>{thMap[key.toUpperCase()]}</h3>
                </div>
                <div class="{key.toLowerCase()}-all-val">
                    <p>{rows[0][key]}</p>
                </div>
            {/each}
        </div>
        <TableSort items="{rows}">
            <tr slot="thead">
                {#each Object.keys(cols) as key}
                    <th data-sort="{key}" style={thStyleMap[key.toUpperCase()]}>
                        {thMap[key.toUpperCase()]}
                    </th>
                {/each}
            </tr>
            <tr slot="tbody" let:item>
                {#each Object.keys(item) as key}
                    {#if item['country'] === 'World'}
                        {#if key === 'totalTests'}
                            <td style="{getTdStyle(item, key)}">{getColSum(key, rows)}</td>
                        {:else if key === 'testsPerOneMillion'}
                            <td style="{getTdStyle(item, key)}">{Math.floor(getColSum('totalTests', rows) * 1000000 / 7700000000)}</td>
                        {:else}
                            <td style="{getTdStyle(item, key)}">{item[key]}</td>
                        {/if}
                    {:else}
                        <td style="{getTdStyle(item, key)}">{item[key]}</td>
                    {/if}
                {/each}
            </tr>
        </TableSort>
    </section>
{/if}
