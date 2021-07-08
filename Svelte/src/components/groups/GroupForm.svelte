<script>
    import {getClient, mutate} from 'svelte-apollo';
    import {createEventDispatcher} from 'svelte';
    import Header from '../../layout/Header.svelte';
    import {error, success} from '../../services/notification/notifier';
    import {authStore} from '../../services/auth/authStore';
    import {GENRES} from '../../constants';
    import {CREATE_GROUP} from "../../services/groups/groupsApi";
    import SearchMembers from '../search/SearchMembers.svelte';
    import {navigate} from "svelte-routing";

    const dispatch = createEventDispatcher();
    const user = $authStore.user;
    export let group;

    if (!group) {
        group = {};
        group.name = '';
        group.description = '';
        group.usernames = [];
        group.image = undefined;
        group.genres = [];
    }

    let name = group.name;
    let description = group.description;
    let usernames = group.usernames;
    let users = group.users;
    let image = group.image;
    let genres = new Set(group.genres);

    const client = getClient();
    const submitGroup = () => {
        mutate(client, {
            mutation: CREATE_GROUP,
            variables: {
                name,
                ownerId: user.id,
                description,
                usernames: [user.username, ...usernames],
                image: image ? image[0] : null,
                genres: Array.from(genres)
            }
        }).then(res => {
            success('Create-Group: Successful!', 4000);
            navigate(`/group/${res.data.createGroup.group.id}`);
            dispatch('refetchGroups', {});
        }).catch(err => {
            error(err.message, 4000)
        });
    };

    const toggleGenre = event => {
        genres.delete(event.target.id) || genres.add(event.target.id);
    };

    const updateUsers = users => {
        usernames = users.detail.map(user => user.username);
    };

    const cancel = () => {
        dispatch('cancel', {});
    };
</script>

<form on:submit|preventDefault={submitGroup}>
    <div class="card">
        <Header title="Create your Group"/>
        <div class="card-content">
            <div class="form-group inputName">
                <label for="name">Name</label>
                <input type="text" id="name" bind:value={name} class="form-control"/>
            </div>
            <div class="form-group inputFile">
                <label for="image-file">Group Image</label>
                <input type="file" class="form-control-file" id="image-file" bind:files={image}
                       title="Upload Group Image">
            </div>
            <div class="form-group inputDesc">
                <label for="description">Description</label>
                <textarea type="text" id="description" bind:value={description} class="form-control"></textarea>
            </div>
            <div class="search">
                <SearchMembers on:updateUsers={updateUsers} userList={users}/>
            </div>
            <div class="genres">
                <Header title="Genres"/>
                <ul class="genres-list">
                    {#each Object.keys(GENRES) as key}
                        <li class="form-check">
                            <input type="checkbox" class="form-check-input" id={key}
                                   on:click={toggleGenre} checked={genres.has(key)}>
                            <label class="form-check-label" for={key}>{GENRES[key]}</label>
                        </li>
                    {/each}
                </ul>
            </div>
            <div class="action">
                <button type="submit" class="btn btn-submit">
                    CREATE
                </button>
                <button type="button" class="btn btn-cancel" on:click={cancel}>
                    CANCEL
                </button>
            </div>
        </div>
    </div>
</form>

<style>

    ul.genres-list {
        padding: 10px 0;
        margin: 0;
    }

    li {
        float: left;
        width: 25%;
    }

    form, .card, .card-content {
        background: var(--background);
    }

    .inputName {
        grid-area: inputName;
    }

    .inputFile {
        grid-area: inputFile;
    }

    .inputDesc {
        grid-area: inputDesc;
    }

    .search {
        grid-area: search;
    }

    .action {
        grid-area: action;
    }

    .genres {
        grid-area: genres;
    }

    textarea {
        width: 100%;
    }

    form .card-content {
        display: grid;
        grid-template-columns: 1% 22% 22% 22% 22% 1%;
        grid-column-gap: 2%;
        align-items: center;
        grid-template-rows: auto;
        grid-template-areas:
                ". inputName inputName inputFile inputFile ."
                ". inputDesc inputDesc inputDesc inputDesc ."
                ". search search search search ."
                ". genres genres genres genres ."
                ". action action . . .";
    }
</style>
