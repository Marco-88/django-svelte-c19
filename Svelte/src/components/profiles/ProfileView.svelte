<script>
    import { Link } from 'svelte-routing';
    import { getClient, query, mutate } from 'svelte-apollo';
    import Header from '../../layout/Header.svelte';
    import {error, success} from '../../services/notification/notifier';
    import { authStore } from '../../services/auth/authStore';
    import { GENRES } from '../../constants';
    import { GET_USER } from '../../services/auth/authApi';
    import { ADD_FRIEND, REMOVE_FRIEND } from '../../services/profiles/profilesApi';
    import {addFriend, removeFriend} from "../../services/profiles/profilesActions";
    import { formatLongText } from '../../utils';
    import ActionIcons from '../widgets/ActionIcons.svelte';
    import ListItem from '../widgets/ListItem.svelte';
    import { joinGroup, removeMember, deleteGroup } from '../../services/groups/groupsActions';
    import { afterUpdate } from 'svelte';

    export let id;

    const client = getClient();
    let user = query(client, { query: GET_USER, variables: { id } });

    afterUpdate(() => {
        user = query(client, { query: GET_USER, variables: { id } });
    });
</script>

{#if user}
    {#await $user}
        <h3>Loading...</h3>
    {:then result}
        <div class="card">
            <Header title={`${result.data.getUser.username}'s Profile`}/>
            <div class="card-content">
                <div class="image">
                    <img class="circle" src={result.data.getUser.profile.image} alt="group image">
                </div>
                <div class="name">
                    <h4>{result.data.getUser.username}</h4>
                    <p>{result.data.getUser.profile.birthdate}</p>
                </div>
                <div class="user-action-icons">
                    <ActionIcons
                            size="2x"
                            tooltips={{actionUserPlus: 'Add Friend', actionUserMinus: 'Remove Friend'}}
                            actions={{actionUserPlus: () => addFriend(client, result.data.getUser.id),
                                      actionUserMinus: () => removeFriend(client, result.data.getUser.id)}}
                    />
                </div>
                <div class="description">
                    <p>{result.data.getUser.profile.description}</p>
                </div>
                {#if result.data.getUser.profile.genres && result.data.getUser.profile.genres.length > 0}
                    <div class="genres">
                        <section class="panel-header">
                            <h4>Genres</h4>
                        </section>
                        <ul class="genres-list">
                            {#each Object.values(result.data.getUser.profile.genres) as genre}
                                <li>{genre}</li>
                            {/each}
                        </ul>
                    </div>
                {/if}
                {#if result.data.getUser.memberGroups && result.data.getUser.memberGroups.edges.length > 0}
                    <div class="groups">
                        <section class="panel-header">
                            <h4>Groups</h4>
                        </section>
                        <ul class="groups-list">
                            {#each result.data.getUser.memberGroups.edges as {node}}
                                {#if node}
                                    <ListItem data={{
                                        id: node.id, url: 'group', name: node.name, image: node.image,
                                    }}>
                                        <div slot="actionIcons" class="action-icons">
                                            <ActionIcons
                                                    permissions={{actionUserMinus: node.users.map(user => user.id).includes($authStore.user.id),
                                                                  actionTrash: node.owner.id === $authStore.user.id}}
                                                    tooltips={{actionUserMinus: 'Leave Group', actionTrash: 'Delete Group'}}
                                                    actions={{actionUserMinus: () => removeMember(client, node.id, $authStore.user.id),
                                                              actionTrash: () => deleteGroup(client, node.id)}}
                                            />
                                        </div>
                                    </ListItem>
                                {/if}
                            {/each}
                        </ul>
                    </div>
                {/if}
            </div>
        </div>
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

    .groups-list {
        padding-top: 10px;
    }

    .image {
        grid-area: image;
    }

    .name {
        grid-area: name;
    }

    .user-action-icons {
        grid-area: user-action-icons;
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

    .groups {
        grid-area: groups;
        padding-top: 10px;
        padding-bottom: 5px;
    }

    .card .card-content {
        display: grid;
        grid-template-columns: 1% 22% 22% 22% 22% 1%;
        grid-column-gap: 2%;
        align-items: center;
        grid-template-rows: auto;
        grid-template-areas: ". image name . user-action-icons ." ". description description description description ." ". genres genres genres genres ." ". groups groups groups groups .";
        padding-bottom: 10px;
        padding-top: 15px;
    }

</style>
