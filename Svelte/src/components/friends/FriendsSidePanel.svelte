<script>
    import ListItem from "../widgets/ListItem.svelte";
    import ActionIcons from "../widgets/ActionIcons.svelte";
    import Dialog from "../widgets/Dialog.svelte";
    import {removeFriend} from "../../services/profiles/profilesActions";
    import {getClient} from 'svelte-apollo';
    import ToggleBox from "../widgets/ToggleBox.svelte";

    export let friends = [];
    export let active = 'active';

    const client = getClient();

    let data = null;

    const createDialogData = friend => {
        data = {
            title: `Removing Friend "${friend.username}"`,
            text: `Really wanna delete "${friend.username}"?`,
            resolve:  () => removeFriend(client, friend.id),
            reject: () => data = null
        }
    };
</script>

<div class={active + " col-12 col-md-6 col-lg-3 order-1 order-lg-3"}>
    <slot name="info"></slot>
    {#if friends}
        <section id="friends-side-panel">
            <ToggleBox title="Friends"
                   actionIconOpen={{tooltip: 'Open Friends', actionName: 'actionPlus'}}
                   actionIconClose={{tooltip: 'Close Friends', actionName: 'actionMinus'}}
                   clickOutside={false}
                   hidden={false}>
                <div slot="toggle-content">
                    <ul>
                        {#each friends as friend}
                            <ListItem data={{
                                id: friend.node.id, url: 'profile', name: friend.node.username, image: friend.node.profile.image,
                                }} options={{args: {user: friend.node}}}>
                                <div slot="actionIcons" class="action-icons">
                                    <ActionIcons
                                            actions={{actionUserMinus: () => createDialogData(friend.node)}}
                                            tooltips={{actionUserMinus: 'Remove Friend'}}/>
                                </div>
                            </ListItem>
                            {#if data}
                                <Dialog {...data} on:close={() => data = null}/>
                            {/if}
                        {/each}
                    </ul>
                </div>
            </ToggleBox>
        </section>
    {/if}
</div>

<style>
    ul {
        margin: 0;
        padding: 0;
    }

    #friends-side-panel {
        background: var(--background-component);
        margin: 15px 0;
        border: 1px solid var(--primary);
        border-bottom: 2px solid var(--primary);
    }
</style>