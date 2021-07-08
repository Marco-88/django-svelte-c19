<script>
    import ClickOutside from 'svelte-click-outside';
    import GroupForm from './GroupForm.svelte';
    import Header from '../../layout/Header.svelte';
    import { authStore } from '../../services/auth/authStore';
    import { getClient, query } from 'svelte-apollo';
    import { GET_GROUPS } from '../../services/groups/groupsApi';
    import { error, success } from '../../services/notification/notifier';
    import ListItem from '../widgets/ListItem.svelte';
    import ActionIcons from '../widgets/ActionIcons.svelte';
    import { removeMember, deleteGroup } from '../../services/groups/groupsActions';
    import { afterUpdate } from 'svelte';


    const client = getClient();
    let groups = query(client, { query: GET_GROUPS, variables: { userId: $authStore.user.id } });
    $: groups.refetch();
    let modal;

    const hideModal = () => {
        modal.hidden = true;
    };

    const showModal = () => {
        modal.hidden = false;
        modal.querySelector('.form-control').focus();
    };

    const refetchGroups = () => {
        groups.refetch();
        hideModal();
    };

    afterUpdate(() => {
       groups.refetch();
    });

</script>

<section id="group-panel" class="z-depth-2">
    <Header title="Your Groups">
        <div slot="actionIcons">
            {#if modal}
                {#if modal.hidden}
                    <ActionIcons
                            permissions={{actionPlus: modal.hidden}}
                            tooltips={{actionPlus: 'Create new Group'}}
                            actions={{actionPlus: showModal}}
                    />
                {:else}
                    <ActionIcons
                            permissions={{actionMinus: !modal.hidden}}
                            tooltips={{actionMinus: 'Minimize Group Window'}}
                            actions={{actionMinus: hideModal}}
                    />
                {/if}
            {/if}
        </div>
    </Header>
    <ul id="group-list">
        {#await $groups}
            <h3>Loading...</h3>
        {:then result}
            {#each result.data.getGroups.edges as group}
                {#if group.node.users.map(user => user.id).includes($authStore.user.id)}
                    <ListItem data={{id: group.node.id, url: 'group', name: group.node.name, image: group.node.image}}>
                        <div slot="actionIcons">
                            <ActionIcons
                                    actions={{actionUserMinus: () => removeMember(client, group.node.id, $authStore.user.id),
                                          actionTrash: () => deleteGroup(client, group.node.id)}}
                                    permissions={{actionTrash: group.node.owner.id === $authStore.user.id}}
                                            tooltips={{actionUserMinus: 'Leave Group', actionTrash: 'Delete Group'}}
                                            />
                        </div>
                    </ListItem>
                {/if}
            {/each}
        {:catch err}
            {error(err.message, 4000)}
        {/await}
    </ul>
    <ClickOutside on:clickoutside={hideModal}>
        <div id="modal" bind:this={modal} hidden>
            <GroupForm on:refetchGroups={refetchGroups} on:cancel={hideModal}/>
        </div>
    </ClickOutside>
</section>

<style>
    #group-panel, #group-list {
        background: var(--background-component);
        margin: 0;
    }

    #group-list {
        padding: 5px;
    }

    #modal {
        position: fixed;
        width: 600px;
        height: 400px;
        left: 50%;
        top: 50%;
        transform: translate(-50%, -50%);
        z-index: 2;
        overflow-y: scroll;
        overflow-x: hidden;
        border: 2px solid var(--background-component-modal);
    }
</style>
