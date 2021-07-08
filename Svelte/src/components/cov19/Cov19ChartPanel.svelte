<style>
    .chart-wrapper {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin-top: 15px;
    }
    section {
        background: var(--background);
        margin: 0;
        border-left: 1px solid var(--primary);
        border-right: 1px solid var(--primary);
    }

    .chart {
        width: 70%;
        margin-bottom: 15px;
    }

    .chart h5 {
        text-align: left;
    }
</style>

<script>
    import Header from '../../layout/Header.svelte';
    import { cov19Store } from '../../services/cov19/cov19Store';
    import {formatDateOnly, formatInputDate} from '../../utils';
    import Cov19ChartForm from './Cov19ChartForm.svelte';
    import Cov19Chart from './Cov19Chart.svelte';

    $: rows = $cov19Store.rows;
    $: all = $cov19Store.all;
    $: cols = $cov19Store.cols;
    $: dates = $cov19Store.dates;

    let selectedCountries = ['China', 'Italy', 'France', 'Spain', 'Germany', 'US'];

    const getCountryData = (names, data) => {
        return names.map(name => {
            const country = {};
            country[name] = data[name];
            return country;
        });
    };

    let countryData = getCountryData(selectedCountries, $cov19Store.dates);

    const formData = {
        categories: ['Confirmed', 'Deaths', 'Recovered'],
        countries: Object.keys($cov19Store.dates),
        startDate: countryData[0][selectedCountries[0]][0].date,
        endDate: countryData[0][selectedCountries[0]][countryData[0][selectedCountries[0]].length - 1].date,
    };

    $: filterParams = {
        category: 'Confirmed',
        countries: selectedCountries,
        startDate: formatInputDate(formData.startDate),
        endDate: formatInputDate(formData.endDate),
    };

    const getDateYesterday = date => {
        return date.setDate(date.getDate() - 1);
    };

    const update = event => {
        filterParams = event.detail.filterParams;
        countryData = getCountryData(filterParams.countries, $cov19Store.dates);
    };
</script>


{#if $cov19Store && $cov19Store.dates}
    <section>
        <Header title="Corona (CoV19) Chart - {formatDateOnly(getDateYesterday(new Date()))}" />
        <div class="chart-wrapper">
            <Cov19ChartForm {...formData} {filterParams} on:update={update}/>
            <div class="chart">
                <h5>{filterParams.category}</h5>
                <Cov19Chart {countryData} filter={filterParams}/>
            </div>
        </div>
    </section>
{/if}
