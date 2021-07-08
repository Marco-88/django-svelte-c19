<script>
    import { getClient, query } from 'svelte-apollo';
    import { GET_USERS } from '../../services/auth/authApi';
    import { error } from '../../services/notification/notifier';

    let searchText;
    let results;
    let genres;

    let postFilters = {
        dateStart: null,
        dateEnd: null
    };

    let userFilters = {
        age: null,
        country: null,
        city: null
    };

    let groupFilters = {
        tags: null
    };

    const client = getClient();

    const validateText = text => {
        return text && text.trim() !== '';
    };

    const onChange = () => {
        if (validateText(searchText)) {
            results = query(client, { query: GET_USERS, variables: { username: searchText, first: 10 } });
        } else {
            console.log('Text is not valid!');
        }
    };
</script>

<form on:submit|preventDefault={event => event}>
    <div class="form-group inputSearch">
        <label for="search">Users</label>
        <input type="text" id="search" class="form-control" bind:value={searchText} on:change={onChange}
               on:keyup={onChange}/>
    </div>
    {#if result}
        {#await $result}
            <h3>Loading...</h3>
        {:then result}
            <ul class="result-list">
                {#each result.data.search.edges as all}
                    {#if all}

                    {/if}
                {/each}
            </ul>
        {:catch err}
            {error(err.message, 4000)}
        {/await}
    {/if}
</form>

<style>
</style>
