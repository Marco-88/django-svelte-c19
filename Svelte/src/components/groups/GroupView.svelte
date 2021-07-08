<script>
    import { afterUpdate } from 'svelte';
    import { getClient, query } from 'svelte-apollo';
    import { Link } from 'svelte-routing';
    import Header from '../../layout/Header.svelte';
    import { error } from '../../services/notification/notifier';
    import { authStore } from '../../services/auth/authStore';
    import { GENRES } from '../../constants';
    import { GET_GROUP } from '../../services/groups/groupsApi';
    import ActionIcons from '../widgets/ActionIcons.svelte';
    import { joinGroup, removeMember, deleteGroup } from '../../services/groups/groupsActions';
    import ListItem from '../widgets/ListItem.svelte';
    import GroupForm from './GroupForm.svelte';

    export let id;
    let editingGroup = false;

    const client = getClient();

    let group = query(client, { query: GET_GROUP, variables: { id } });
    $: group.refetch();

    afterUpdate(() => {
        group = query(client, { query: GET_GROUP, variables: { id } });
    });

    const editGroup = () => {
        editingGroup = true;
    };

    const stopEditing = () => {
        editingGroup = false;
    };

    const removeMemberandRefetch = (client, id, userId) => {
        removeMember(client, id, userId);
        group = query(client, { query: GET_GROUP, variables: { id } });
    };

</script>
{#if group}
    {#await $group}
        <h3>Loading...</h3>
    {:then result}
        {#if editingGroup}
            <GroupForm on:refetchGroups={group.refetch} on:cancel={stopEditing} group={{...result.data.getGroup, usernames: result.data.getGroup.users.map(user => user.username)}}/>
        {:else}
            <div class="card">
                <Header title="Group"/>
                <div class="card-content">
                    <div class="image">
                        <img class="circle" src={result.data.getGroup.image} alt="group image">
                    </div>
                    <div class="name">
                        <h4>{result.data.getGroup.name}</h4>
                        <div>
                            Owner:
                            <Link to={`profile/${result.data.getGroup.owner.id}`}>
                                {result.data.getGroup.owner.username}
                            </Link>
                        </div>
                    </div>
                    <div class="group-action-icons">
                        <ActionIcons
                                size="2x"
                                permissions={{actionEdit: $authStore.user.id === result.data.getGroup.owner.id,
                                          actionTrash: $authStore.user.id === result.data.getGroup.owner.id}}
                                tooltips={{actionUserPlus: 'Join Group', actionEdit: 'Edit Group', actionTrash: 'Delete Group'}}
                                actions={{actionUserPlus: () => joinGroup(client, result.data.getGroup.id, $authStore.user.id),
                                      actionEdit: () => editGroup(),
                                      actionTrash: () => deleteGroup(client, result.data.getGroup.id)}}
                        />
                    </div>
                    <div class="description">
                        <p>{result.data.getGroup.description}</p>
                    </div>
                    {#if result.data.getGroup.genres && result.data.getGroup.genres.length > 0}
                        <div class="genres">
                            <Header title="Genres"/>
                            <ul class="genres-list">
                                {#each Object.values(result.data.getGroup.genres) as key}
                                    <li>{GENRES[key]}</li>
                                {/each}
                            </ul>
                        </div>
                    {/if}
                    {#if result.data.getGroup.users && result.data.getGroup.users.length > 0}
                        <div class="members">
                            <Header title="Members"/>
                            <ul class="members-list">
                                {#each Object.values(result.data.getGroup.users) as user}
                                    {#if user && user.profile}
                                        <ListItem data={{
                                        id: user.id, url: 'profile', name: user.username, image: user.profile.image
                                    }}>
                                            <div slot="actionIcons" class="action-icons">
                                                <ActionIcons
                                                        tooltips={{actionUserMinus: 'Remove Member'}}
                                                        actions={{actionUserMinus: () => removeMemberandRefetch(client, id, user.id)}}/>
                                            </div>
                                        </ListItem>
                                    {/if}
                                {/each}
                            </ul>
                        </div>
                    {/if}
                </div>
            </div>
        {/if}
    {:catch err}
        {error(err.message, 4000)}
    {/await}
{/if}

<style>
    ul, p {
        padding: 0;
        margin: 0;
    }

    li {
        float: left;
        width: 25%;
    }

    img {
        width: 128px;
        height: 128px;
    }

    h4 {
        text-align: left;
    }

    .genres-list {
        padding-top: 10px;
    }

    .members-list {
        padding-top: 10px;
    }

    .image {
        grid-area: image;
    }

    .name {
        grid-area: name;
    }

    .group-action-icons {
        grid-area: group-action-icons;
        display: flex;
        align-items: center;
        justify-content: flex-end;
        align-self: flex-start;
        padding: 5px;
    }

    .description {
        grid-area: description;
        padding-top: 10px;
        padding-bottom: 5px;
    }

    .genres {
        grid-area: genres;
        padding-top: 10px;
        padding-bottom: 5px;
    }

    .members {
        grid-area: members;
        padding-top: 10px;
        padding-bottom: 5px;
    }

    .card .card-content {
        display: grid;
        grid-template-columns: 1% 22% 22% 22% 22% 1%;
        grid-column-gap: 2%;
        align-items: center;
        grid-template-rows: auto;
        grid-template-areas: ". image name . group-action-icons ." ". description description description description ." ". genres genres genres genres ." ". members members members members .";
        padding-bottom: 10px;
        padding-top: 15px;
    }
</style>
