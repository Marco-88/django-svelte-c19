<style>
    form {
        width: 40%;
    }
    .card.form {
        display: grid;
        grid-template-columns: 2% 49% 49% 2%;
        grid-template-areas: '. categories countries .' '. start-date end-date .';
    }

    select, input {
        width: 96%;
    }

    .categories {
        grid-area: categories;
    }

    .countries {
        grid-area: countries;
    }

    .startDate {
        grid-area: start-date;
    }

    .endDate {
        grid-area: end-date;
    }
</style>

<script>
    import {createEventDispatcher} from 'svelte';
    import {checkDate} from '../../utils';

    export let categories = [];
    export let countries = [];
    export let startDate = new Date();
    export let endDate = new Date();

    export let filterParams;

    let optionsCategories;
    let optionsCountries;

    const dispatch = createEventDispatcher();

    const changeFilter = event => {
        const elem = event.target;
        if (elem.id.includes('Date')) {
            try {
                const date = new Date(elem.value)
                if (validateDate(date))
                    filterParams[elem.id] = elem.value;
            } catch (err) {
                console.log(err);
            }
        } else if (elem.selectedOptions && elem.id.includes('countries')) {
            filterParams.countries = Object.values(elem.selectedOptions).map(option => option.value);
        }  else {
            filterParams[elem.id] = elem.value;
        }
        dispatch('update', {filterParams});
    };

    const validateDate = date => {
        return checkDate(date, filterParams.startDate, filterParams.endDate);
    }

</script>

<form>
    <h5>Filter</h5>
    <div class="card form">
        <div class="form-group categories">
            <label for="categories">Categories</label>
            <select id="categories" bind:value={filterParams.category}
                    on:change={changeFilter}>
                {#each categories as category}
                    <option value="{category}">{category}</option>
                {/each}
            </select>
        </div>
        <div class="form-group countries">
            <label for="countries">Countries</label>
            <select
                    id="countries"
                    multiple
                    bind:value={filterParams.countries}
                    on:change={changeFilter}
            >
                {#each countries as country}
                    <option value="{country}">{country}</option>
                {/each}
            </select>
        </div>
        <div class="form-group startDate">
            <label for="startDate">From</label>
            <input
                    type="date"
                    id="startDate"
                    bind:value={filterParams.startDate}
                    class="form-control"
                    on:change={changeFilter}
                    min={startDate}
                    max={filterParams.endDate}
            />
        </div>
        <div class="form-group endDate">
            <label for="endDate">To</label>
            <input
                    type="date"
                    id="endDate"
                    bind:value={filterParams.endDate}
                    class="form-control"
                    on:change={changeFilter}
                    min={filterParams.startDate}
                    max={endDate}
            />
        </div>
    </div>
</form>
