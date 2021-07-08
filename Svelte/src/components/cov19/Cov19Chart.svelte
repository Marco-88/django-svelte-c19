<style>
    #cov19-chart {
        background: var(--background-component);
    }
</style>
<script>
    import {afterUpdate} from "svelte";
    import Chart from "chart.js";
    import { formatDateOnly, checkDate } from '../../utils';

    export let countryData = {};
    export let filter = {};

    $: category = filter.category;
    $: countries = filter.countries;
    $: startDate = filter.startDate;
    $: endDate = filter.endDate;

    const colors = [
        '#aa0000', '#aa6600', '#aaaa00',
        '#66aa00', '#00aa00', '#00aa66',
        '#00aaaa', '#0066aa', '#0000aa'];

    const getLabels = () => {
        return countryData[0][countries[0]].map(country => country.date)
    };

    const getChartData = () => {
        let filteredLabels = [];
        const labels = getLabels();

        labels.forEach(label => {
            if (checkDate(label, startDate, endDate)) {
                filteredLabels.push(formatDateOnly(label));
            }
        });

        let datasets = [];

        countryData.forEach(country => {
            const label = Object.keys(country)[0];
            if (countries.includes(label)) {
                let values = [];

                country[label].forEach(data => {
                    if (checkDate(data.date, startDate, endDate)) {
                        values.push(data[category.toLowerCase()]);
                    }
                });

                datasets.push({
                    label,
                    data: values,
                    borderColor: colors[datasets.length],
                });
            }
        });

        return {
            type: 'line',
            data: {
                labels: filteredLabels,
                datasets
            },
            options: {}
        }
    };

    afterUpdate(() => {
        renderChart();
    });

    let chart = null;

    function renderChart() {
        if(chart)
            chart.destroy();
        const ctx = document.getElementById("cov19-chart").getContext("2d");
        chart = new Chart(ctx, getChartData());
    }
</script>

<canvas id="cov19-chart"></canvas>