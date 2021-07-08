<script>
    import { getClient, query } from 'svelte-apollo';
    import ClickOutside from 'svelte-click-outside';
    import { SEARCH } from '../../services/search/searchApi';
    import { error } from '../../services/notification/notifier';
    import ListItem from '../widgets/ListItem.svelte';
    import ActionIcons from '../widgets/ActionIcons.svelte';

    let searchQuery;
    let hidden = false;
    let maxEntries = 10;

    let types = [
        { id: 1, name: 'User' },
        { id: 2, name: 'Group' },
        { id: 3, name: 'Post' },
    ];

    let selectedTypes = [...types];

    const getClearData = searchText => {
        return {
            searchText: searchText ? searchText : '',
            users: [],
            groups: [],
            posts: [],
        };
    };

    let data = getClearData();

    $: searchText = data.searchText;
    $: posts = data.posts;
    $: users = data.users;
    $: groups = data.groups;

    const client = getClient();

    const validateText = text => {
        return text && text.trim() !== '';
    };

    const search = () => {
        if (validateText(searchText)) {
            searchQuery = query(client, {
                query: SEARCH,
                variables: { text: searchText, types: selectedTypes.map(type => type.name), first: 10 },
                fetchPolicy: 'no-cache',
            });
            searchQuery.result()
                    .then(res => {
                        data = getClearData(searchText);
                        res.data.search.forEach(node => {
                            if (!hasMaxItems()) {
                                if (node.__typename === 'UserNode' && !data.users.map(user => user.id).includes(node.id)) {
                                    data.users.push(node);
                                } else if (node.__typename === 'GroupNode' && !data.groups.map(group => group.id).includes(node.id)) {
                                    data.groups.push(node);
                                } else if (node.__typename === 'PostNode' && !data.posts.map(post => post.id).includes(node.id)) {
                                    data.posts.push(node);
                                }
                            }
                        });
                    }).catch(err => {
                error(err.message, 4000);
            });
        } else {
            console.log('Text is not valid!');
        }
    };

    const hasMaxItems = () => data.users.length + data.groups.length + data.posts.length >= maxEntries;
    const hide = () => {
        if(!hidden) hidden = true;
    };
    const show = () => {
        if(hidden) hidden = false;
    };

    const searchAndShow = () => {
        search();
        show();
    };
</script>

<form on:submit|preventDefault={search}>
    <div id="searchBar" class="form-group">
        <ClickOutside on:clickoutside={hide}>
            <select class="selectpicker" multiple bind:value={selectedTypes} on:change={() => searchAndShow()}
                    data-selected-text-format="count > 3" data-actions-box="true" on:click={show}>
                {#each types as type}
                    <option value={type} selected on:click={show} on:blur={hide}>{type.name}</option>
                {/each}
            </select>
            <div class="search input-group">
                <input type="text" class="form-control" id="search" bind:value={data.searchText}
                       on:change={search} on:keyup={search} on:focus={show} placeholder="Search..."
                       aria-label="search" aria-describedby="basic-addon2">
                <div class="input-group-append">
                    <label for="search">
                        <ActionIcons
                                actions={{actionSearch: search}}
                                tooltips={{actionSearch: 'Search'}}/>
                    </label>
                </div>
                <ul class="result-list {hidden ? 'hidden' : ''}">
                    {#if data.users && data.users.length > 0}
                        <li class="result-header">Users</li>
                        {#each data.users as user}
                            <ListItem
                                    hoverable={true}
                                    data={{id: user.id, url: 'profile', name: user.username, image: user.profile ? user.profile.image: null}}>
                            </ListItem>
                        {/each}
                    {/if}
                    {#if data.groups && data.groups.length > 0}
                        <li class="result-header">Groups</li>
                        {#each data.groups as group}
                            <ListItem
                                    hoverable={true}
                                    data={{id: group.id, url: 'group', name: group.name, image: group.image}}/>
                        {/each}
                    {/if}
                    {#if data.posts && data.posts.length > 0}
                        <li class="result-header">Posts</li>
                        {#each data.posts as post}
                            <ListItem hoverable={true}
                                      data={{id: post.id, url: 'post', name: post.title}}/>
                        {/each}
                    {/if}
                </ul>
            </div>
        </ClickOutside>
    </div>
</form>

<style>

    form {
        width: 64%;
        height: 64px;
    }

    ul {
        margin: 0;
        padding: 0;
    }

    #searchBar {
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        height: 64px;
        width: 100%;
        margin: 0 auto;
        padding: 0;
    }

    select, .search.input-group {
        padding: 0;
        margin: 0;
        line-height: var(--search-height);
        height: var(--search-height);
    }

    label, #search {
        line-height: var(--search-height);
        height: var(--search-height);
    }

    :global(.dropdown.bootstrap-select) {
        grid-area: selectpicker;
        line-height: var(--search-height);
        height: var(--search-height);
        padding: 0;
        margin: 0;
        width: 100%;
    }

    :global(.bootstrap-select:not([class*="col-"]):not([class*="form-control"]):not(.input-group-btn)) {
        width: 100%;
    }

    :global(.filter-option-inner-inner, #searchBar .btn.dropdown-toggle, .selectpicker) {
        background: var(--background-component);
        color: var(--color-component);
        line-height: var(--search-height);
        height: var(--search-height);
        padding-left: 5px;
        border: none;
    }

    :global(.bootstrap-select .dropdown-toggle .filter-option) {
        width: 95%;
    }

    :global(button.actions-btn.bs-select-all.btn.btn-light, button.actions-btn.bs-deselect-all.btn.btn-light) {
        background: var(--primary);
        color: var(--color-component);
    }

    .btn {
        background: var(--primary);
        color: var(--color-component);
    }

    :global(.bootstrap-select > select) {
        position: relative;
    }

    #search, label {
        background: var(--background-component)
    }

    :global(.dropdown-menu.inner.show li a, .dropdown-menu.inner.show li a span, .dropdown-menu, #searchbar.btn.dropdown-toggle) {
        background: var(--background-component);
        color: var(--color-component)
    }

    :global(.dropdown-menu.inner.show li a:hover) {
        background: var(--background-component-hover);
    }

    #search {
        border: 1px solid var(--background-component);
        color: var(--color-component)
    }

    .result-list {
        position: absolute;
        top: var(--search-height);
        left: 0;
        z-index: 7;
        width: 100%;
        background: var(--background-component);
    }

    .result-header {
        padding: 0 10px;
        color: var(--primary-form-label);
        background: var(--background);
    }

    .hidden {
        display: none;
    }

    :global(#searchBar > div) {
        width: 90%;
    }
</style>
