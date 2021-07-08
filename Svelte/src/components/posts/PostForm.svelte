<script>
    import { getClient, mutate } from 'svelte-apollo';
    import ClickOutside from 'svelte-click-outside';
    import { authStore } from '../../services/auth/authStore';
    import { CREATE_POST, UPDATE_POST } from '../../services/posts/postsApi';
    import { createEventDispatcher, onMount } from 'svelte';
    import { error, success } from '../../services/notification/notifier';
    import Header from '../../layout/Header.svelte';
    import ActionIcons from '../widgets/ActionIcons.svelte';

    let modal;

    const hideModal = () => {
        modal.hidden = true;
    };

    const showModal = () => {
        modal.hidden = false;
        modal.querySelector('.form-control').focus();
    };

    const dispatch = createEventDispatcher();

    const getDefaultPost = () => {
        return {
            title: '',
            body: '',
            id: null,
        };
    };

    export let editingPost = getDefaultPost();

    $: title = editingPost.title;
    $: body = editingPost.body;
    let id = editingPost.id;
    let inputTitle, inputBody;

    const client = getClient();

    const submitPost = () => {
        if (title.trim() === '' || body.trim() === '') {
            console.log('Error: input is invalid');
            return;
        }

        mutate(client, {
            mutation: id ? UPDATE_POST : CREATE_POST,
            variables: id ? { title, body, id } : { title, body, userId: $authStore.user.id },
        }).then(res => {
            editingPost.title = '';
            editingPost.body = '';
            dispatch('refetchPosts', {});
            if (id) {
                success(`You updated a Post!`, 4000);
                dispatch('stopEditing', {});
            } else {
                success(`You created a new Post!`, 4000);
            }
        }).catch(err => {
            error(err.message, 4000);
        });
    };

    const onCancel = () => {
        editingPost = getDefaultPost();
        dispatch('stopEditing', {});
    }
</script>

<form on:submit|preventDefault={submitPost}>
    <div class="card">
        <!--        TODO ToggleBox-->
        <Header title={editingPost.id ? 'Editing Post' : 'Create a Post'}>
            <div slot="actionIcons">
                {#if !editingPost.id}
                    {#if modal}
                        {#if modal.hidden}
                            <ActionIcons
                                    permissions={{actionPlus: modal.hidden}}
                                    tooltips={{actionPlus: 'Create a Post'}}
                                    actions={{actionPlus: showModal}}
                            />
                        {:else}
                            <ActionIcons
                                    permissions={{actionMinus: !modal.hidden}}
                                    tooltips={{actionMinus: 'Minimize'}}
                                    actions={{actionMinus: hideModal}}
                            />
                        {/if}
                    {/if}
                {/if}
            </div>
        </Header>
        {#if !editingPost.id}
            <ClickOutside on:clickoutside={hideModal}>
                <div class="comment-modal" bind:this={modal} hidden>
                    <div class="card-content">
                        <div class="form-group inputTitle">
                            <label for="title">Title</label>
                            <input type="text" id="title" class="form-control" required
                                   bind:value={editingPost.title} bind:this={inputTitle}/>
                        </div>
                        <div class="form-group inputBody">
                            <label for="body">Body</label>
                            <textarea type="text" id="body" class="form-control" required
                                      bind:value={editingPost.body} bind:this={inputBody}></textarea>
                        </div>
                    </div>
                    <div class="card-action">
                        <button type="submit" class="waves-effect waves-light btn btn-submit">
                            {id ? 'UPDATE' : 'ADD'}
                        </button>
                        {#if id}
                            <button type="submit" class="waves-effect waves-light btn btn-cancel">
                                CANCEL
                            </button>
                        {/if}
                    </div>
                </div>
            </ClickOutside>
        {:else}
            <div class="card-content">
                <div class="form-group inputTitle">
                    <label for="title">Title</label>
                    <input type="text" id="title" class="form-control" required
                           bind:value={editingPost.title} bind:this={inputTitle}/>
                </div>
                <div class="form-group inputBody">
                    <label for="body">Body</label>
                    <textarea type="text" id="body" class="form-control" required
                              bind:value={editingPost.body} bind:this={inputBody}></textarea>
                </div>
            </div>
            <div class="card-action">
                <button type="submit" class="waves-effect waves-light btn btn-submit">
                    {id ? 'UPDATE' : 'ADD'}
                </button>
                {#if id}
                    <button type="button" class="waves-effect waves-light btn btn-cancel" on:click={onCancel}>
                        CANCEL
                    </button>
                {/if}
            </div>
        {/if}
    </div>
</form>

<style>

    form {
        background: var(--background);
    }

    .inputTitle, .inputBody {
        width: 95%;
        margin: 0 auto;
        padding: 10px 0;
    }

    h4 {
        font-size: 1.2rem;
        text-align: center;
        padding: 0;
        margin: 0;
    }

    .panel-header {
        padding: 5px 5px 8px 5px;
        text-align: left;
        display: flex;
        justify-content: space-around;
        align-items: center;
        background: var(--primary);
    }

    .card {
        margin-bottom: 10px;
    }

    /*form .card-content {*/
    /*    display: grid;*/
    /*    grid-template-columns: 1% 22% 22% 22% 22% 1%;*/
    /*    grid-column-gap: 2%;*/
    /*    align-items: center;*/
    /*    grid-template-rows: auto;*/
    /*    grid-template-areas: ". image inputUser inputUser inputUser ." ". inputFile inputFile inputDate inputSwitch ." ". inputDesc inputDesc inputDesc inputDesc ." ". genres genres genres genres ." ". . action action . .";*/
    /*}*/
</style>
