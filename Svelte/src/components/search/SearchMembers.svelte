<script>
    import { getClient, query } from 'svelte-apollo';
    import Header from '../../layout/Header.svelte';
    import { GET_USERS } from '../../services/auth/authApi';
    import ListItem from '../widgets/ListItem.svelte';
    import { error } from '../../services/notification/notifier';
    import { createEventDispatcher } from 'svelte';
    import ActionIcons from '../widgets/ActionIcons.svelte';
    import { writable } from 'svelte/store';

    export let userList = [];
    const selectedUsers = writable(userList);

    const dispatch = createEventDispatcher();
    let searchText;

    const client = getClient();
    let data;
    let users;

    const validateText = text => {
        return text && text.trim() !== '';
    };

    const onChange = () => {
        if (validateText(searchText)) {
            users = query(client, { query: GET_USERS, variables: { username: searchText, first: 10 } });
        } else {
            console.log('Text is not valid!');
        }
    };

    const setState = res => {
        data = res.data.getUsers.edges;
        return '';
    };

    const addUser = user => {
        selectedUsers.set(Array.from(new Set([user, ...$selectedUsers])));
        dispatch('updateUsers', $selectedUsers);
    };

    const removeUser = user => {
        $selectedUsers.splice(user, 1);
        selectedUsers.set($selectedUsers);
        dispatch('updateUsers', $selectedUsers);
    };
</script>

<form on:submit|preventDefault={event => event}>
    <div class="card">
        <Header title="Search for..."/>
        <div class="card-content">
            <div class="form-group inputSearch">
                <label for="search">Users</label>
                <input type="text" id="search" class="form-control" bind:value={searchText} on:change={onChange}
                       on:keyup={onChange} placeholder="Search..."/>
            </div>
            <div class="result-header">
                <Header title="Result"/>
            </div>
            {#if users}
                {#await $users}
                    <h3>Loading...</h3>
                {:then result}
                    {setState(result)}
                    <ul class="result-list">
                        {#each result.data.getUsers.edges as user}
                            {#if user && user.node && user.node.profile}
                                <ListItem data={{
                                        id: user.node.id, url: 'user', name: user.node.username, image: user.node.profile.image,
                                    }} options={{args: {user: user.node}}}>
                                    <div slot="actionIcons" class="action-icons">
                                        <ActionIcons
                                                actions={{actionUserPlus: () => addUser(user.node)}}
                                                tooltips={{actionUserPlus: 'Add User to Members'}}/>
                                    </div>
                                </ListItem>
                            {/if}
                        {/each}
                    </ul>
                {:catch err}
                    {error(err.message, 4000)}
                {/await}
            {/if}
            <div class="members-header">
                <Header title="Members"/>
            </div>
            <ul class="members-list">
                {#each $selectedUsers as user}
                    {#if user && user.profile}
                        <ListItem data={{
                                id: user.id, url: 'user', name: user.username, image: user.profile.image
                            }} options={{args: {user}}}>
                            <div slot="actionIcons" class="action-icons">
                                <ActionIcons
                                        actions={{actionUserMinus: () => removeUser(user)}}
                                        tooltips={{actionUserPlus: 'Remove User from Members'}}/>
                            </div>
                        </ListItem>
                    {/if}
                {/each}
            </ul>
        </div>
    </div>
</form>

<style>
    ul {
        padding: 0;
    }

    .inputSearch {
        grid-area: inputSearch;
    }

    .result-header {
        grid-area: result-header;
    }

    .result-list {
        grid-area: result-list;
    }

    .members-header {
        grid-area: members-header;
    }

    .members-list {
        grid-area: members-list;
    }


    form .card-content {
        display: grid;
        grid-template-columns: 1% 46% 46% 1%;
        grid-column-gap: 2%;
        align-items: center;
        grid-template-rows: auto;
        grid-template-areas:
                ". inputSearch inputSearch ."
                ". result-header members-header ."
                ". result-list members-list .";
    }
</style>
