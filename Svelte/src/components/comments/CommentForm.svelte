<script>
    import { getClient, mutate } from 'svelte-apollo';
    import { authStore } from '../../services/auth/authStore';
    import {
        CREATE_COMMENT,
        UPDATE_COMMENT,
    } from '../../services/comments/commentsApi';
    import Modal from '../widgets/Modal.svelte';
    import { afterUpdate, createEventDispatcher } from 'svelte';

    const dispatch = createEventDispatcher();

    export let parent = {};
    export let id = '';
    let textareaBody;
    let body = '';

    let client = getClient();

    const submitComment = () => {
        if (body.trim() === '') {
            console.log('Error: input is invalid');
            return;
        }

        let createCommentObject = {
            body,
            userId: $authStore.user.id,
        };

        if (parent.type === 'post') createCommentObject.postId = parent.id;
        else createCommentObject.commentId = parent.id;

        mutate(client, {
            mutation: id !== '' ? UPDATE_COMMENT : CREATE_COMMENT,
            variables: id !== '' ? { body, id } : createCommentObject,
        })
            .then(res => {
                console.log(res);
                console.log('Submit Comment Success!');
            })
            .catch(err => {
                error(err.message, 4000);
            });
    };

    const cancel = event => {
        event.stop();
        dispatch('cancel', {});
    };
</script>

<form on:submit|preventDefault="{submitComment}">
    <div class="form-group inputComment">
        <textarea
            type="text"
            id="body"
            class="form-control"
            required
            bind:value="{body}"
            bind:this="{textareaBody}"
        ></textarea>
    </div>
    <div class="action">
        <button type="submit" class="btn btn-submit">CREATE</button>
        <button type="button" class="btn btn-cancel" on:click="{cancel}">
            CANCEL
        </button>
    </div>
</form>
