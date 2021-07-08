<style>
    ul,
    p {
        padding: 0;
        margin: 0;
    }

    li {
        float: left;
        width: 25%;
    }

    .user {
        grid-area: user;
    }

    .date {
        background: var(--background-list-item);
    }

    .body {
        grid-area: body;
        margin-top: 5px;
    }

    .comments {
        display: flex;
        flex-direction: column;
        padding-left: 15px;
        background: var(--background);
        border: 1px solid var(--primary);
    }

    .social-action-icons {
        grid-area: social-action-icons;
        display: flex;
        align-items: center;
        justify-content: flex-start;
        align-self: flex-start;
        padding: 5px;
    }

    .card.comment .card-content {
        display: grid;
        grid-template-columns: 1% 49% 49% 1%;
        align-items: center;
        grid-template-rows: auto;
        grid-template-areas: '. user user .' '. body body .' '. social-action-icons social-action-icons .';
        padding: 10px 0;
        border: 1px solid var(--primary);
    }

    .action-icons {
        display: flex;
    }
</style>

<script>
    import { createEventDispatcher } from 'svelte';
    import { getClient, mutate } from 'svelte-apollo';
    import ClickOutside from 'svelte-click-outside';
    import { Link } from 'svelte-routing';
    import Header from '../../layout/Header.svelte';
    import { authStore } from '../../services/auth/authStore';
    import ActionIcons from '../widgets/ActionIcons.svelte';
    import { DELETE_COMMENT, CREATE_COMMENT_VOTE } from '../../services/comments/commentsApi';
    import { success, error } from '../../services/notification/notifier';
    import { getActiveRoute } from '../../utils';
    import ListItem from '../widgets/ListItem.svelte';
    import { timeAgo, getVotes } from '../../utils';
    import CommentForm from './CommentForm.svelte';

    export let comment = {};
    export let commentDialog = null;

    let modal;

    const hideModal = () => {
        modal.hidden = true;
    };

    const showModal = () => {
        modal.hidden = false;
        modal.querySelector('.form-control').focus();
    };

    const client = getClient();
    const dispatch = createEventDispatcher();

    const getDefaultComment = () => {
        return {
            body: '',
            id: null,
        };
    };

    let activeRoute = getActiveRoute();
    let editingComment = getDefaultComment();
    let initingEditing = false;

    const like = (client, commentId, userId) => {
        mutate(client, {
            mutation: CREATE_COMMENT_VOTE,
            variables: { vote: 'UP', commentId, userId },
        })
            .then(res => {
                success(`You Liked a Comment!`, 4000);
            })
            .catch(err => {
                error(err.message, 4000);
            });
    };

    const dislike = (client, commentId, userId) => {
        mutate(client, {
            mutation: CREATE_COMMENT_VOTE,
            variables: { vote: 'DOWN', commentId, userId },
        })
            .then(res => {
                success(`You Disliked a Comment!`, 4000);
            })
            .catch(err => {
                error(err.message, 4000);
            });
    };

    const onEdit = comment => {
        editingComment = comment;
        initingEditing = true;
    };

    const onDelete = id => {
        mutate(client, {
            mutation: DELETE_COMMENT,
            variables: { id },
        })
            .then(res => {
                success(`Comment with id "${comment.id}" got deleted!`, 4000);
                editingComment = getDefaultComment();
            })
            .catch(err => {
                error(err.message, 4000);
            });
    };
    const openCommentDialog = () => {};
</script>

<div class="card comment">
    <div class="card-content">
        <div class="user">
            <ListItem
                data="{{ id: comment.user.id, url: 'profile', name: comment.user.username, image: comment.user.profile.image, date: comment.createdAt, info: `(${comment.commentComments ? comment.commentComments.edges.length : '0'})` }}"
            >
                <div slot="actionIcons" class="action-icons">
                    <ActionIcons
                        permissions="{{ actionEdit: $authStore.user.id === comment.user.id, actionTrash: $authStore.user.id === comment.user.id }}"
                        tooltips="{{ actionEdit: 'Edit', actionTrash: 'Delete' }}"
                        actions="{{ actionEdit: () => onEdit(comment), actionTrash: () => onDelete(comment.id) }}"
                    />
                    {#if modal}
                        {#if modal.hidden}
                            <ActionIcons
                                permissions="{{ actionPlus: modal.hidden }}"
                                tooltips="{{ actionPlus: 'Comment the Comment' }}"
                                actions="{{ actionPlus: showModal }}"
                            />
                        {:else}
                            <ActionIcons
                                permissions="{{ actionMinus: !modal.hidden }}"
                                tooltips="{{ actionMinus: 'Minimize' }}"
                                actions="{{ actionMinus: hideModal }}"
                            />
                        {/if}
                    {/if}
                </div>
            </ListItem>
        </div>
        <p class="body">{comment.body}</p>
        <div class="social-action-icons">
            <ActionIcons
                text="{{ actionThumbsUp: getVotes(comment, 'UP'), actionThumbsDown: getVotes(comment, 'DOWN') }}"
                tooltips="{{ actionThumbsUp: 'Like', actionThumbsDown: 'Dislike' }}"
                actions="{{ actionThumbsUp: () => like(client, comment.id, $authStore.user.id), actionThumbsDown: () => dislike(client, comment.id, $authStore.user.id) }}"
            />
        </div>
    </div>
    {#if !commentDialog}
        <ClickOutside on:clickoutside="{hideModal}">
            <div class="comment-modal" bind:this="{modal}" hidden>
                <CommentForm
                    on:cancel="{hideModal}"
                    parent="{{ type: 'comment', id: comment.id }}"
                />
            </div>
        </ClickOutside>
        {#if comment && comment.commentComments && comment.commentComments.edges.length > 0}
            <div class="comments">
                {#each comment.commentComments.edges as comment}
                    <svelte:self comment="{comment.node}" />
                {/each}
            </div>
        {/if}
    {/if}

</div>
