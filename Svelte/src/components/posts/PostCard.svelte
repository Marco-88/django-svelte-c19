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

    img {
        width: 64px;
        height: 64px;
    }

    h4 {
        text-align: left;
    }

    .image {
        grid-area: image;
    }

    .info {
        grid-area: info;
    }

    .body {
        grid-area: body;
        margin-top: 5px;
    }

    .inputComment {
        grid-area: inputComment;
    }

    .post-action-icons {
        grid-area: post-action-icons;
        display: flex;
        align-items: center;
        justify-content: flex-end;
        align-self: flex-start;
        padding: 5px;
    }

    .social-action-icons {
        grid-area: social-action-icons;
        display: flex;
        align-items: center;
        justify-content: flex-start;
        align-self: flex-start;
        padding: 5px;
    }

    .comments {
        display: flex;
        flex-direction: column;
        padding-left: 15px;
        background: var(--background);
        border: 1px solid var(--primary);
    }

    .card.post .card-content {
        display: grid;
        grid-template-columns: 1% 22% 22% 22% 22% 1%;
        grid-column-gap: 2%;
        grid-row-gap: 1%;
        align-items: center;
        grid-template-rows: auto;
        grid-template-areas: '. image info info post-action-icons .' '. body body body body .' '. social-action-icons social-action-icons inputComment inputComment .';
        padding-bottom: 10px;
        padding-top: 15px;
    }

    .comment-modal {
        /*position: fixed;*/
        /*width: 768px;*/
        /*height: 512px;*/
        /*left: 50%;*/
        /*top: 50%;*/
        /*transform: translate(-50%, -50%);*/
        /*z-index: 2;*/
        /*overflow-y: scroll;*/
        /*overflow-x: hidden;*/
        /*border: 2px solid var(--background-component-modal);*/
    }
</style>

<script>
    import { afterUpdate, createEventDispatcher } from 'svelte';
    import { getClient, mutate } from 'svelte-apollo';
    import { Link } from 'svelte-routing';
    import ClickOutside from 'svelte-click-outside';
    import Header from '../../layout/Header.svelte';
    import { authStore } from '../../services/auth/authStore';
    import ActionIcons from '../widgets/ActionIcons.svelte';
    import {
        DELETE_POST,
        CREATE_POST_VOTE,
    } from '../../services/posts/postsApi';
    import { success, error } from '../../services/notification/notifier';
    import { getActiveRoute } from '../../utils';
    import PostForm from './PostForm.svelte';
    import CommentCard from '../comments/CommentCard.svelte';
    import { formatDate, timeAgo, getVotes } from '../../utils';
    import CommentForm from '../comments/CommentForm.svelte';

    export let post = {};
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

    const getDefaultPost = () => {
        return {
            title: '',
            body: '',
            id: null,
        };
    };

    let activeRoute = getActiveRoute();
    export let editingPost = getDefaultPost();
    let initingEditing = false;
    let commentBody = '';
    let inputComment;

    const like = (client, postId, userId) => {
        mutate(client, {
            mutation: CREATE_POST_VOTE,
            variables: { vote: 'UP', postId, userId },
        })
            .then(res => {
                success(`You Liked a Post!`, 4000);
            })
            .catch(err => {
                error(err.message, 4000);
            });
    };

    const dislike = (client, postId, userId) => {
        mutate(client, {
            mutation: CREATE_POST_VOTE,
            variables: { vote: 'DOWN', postId, userId },
        })
            .then(res => {
                success(`You Disliked a Post!`, 4000);
            })
            .catch(err => {
                error(err.message, 4000);
            });
    };

    const onEdit = post => {
        editingPost = post;
        initingEditing = true;
    };

    const onDelete = id => {
        mutate(client, {
            mutation: DELETE_POST,
            variables: { id },
        })
            .then(res => {
                success(`Post with id "${post.id}" got deleted!`, 4000);
                editingPost = getDefaultPost();
            })
            .catch(err => {
                error(err.message, 4000);
            });
    };

    const clickOutside = () => {
        if (initingEditing) initingEditing = false;
        else {
            editingPost = getDefaultPost();
        }
    };

    const stopEditing = () => {
        editingPost = getDefaultPost();
    };

    const getRoute = () => {
        return !$activeRoute.route.path.startsWith('post/')
            ? `post/${post.id}`
            : null;
    };
</script>

<div class="card post">
    {#if editingPost.id === post.id}
        <ClickOutside on:clickoutside="{clickOutside}">
            <PostForm
                on:refetchPosts="{dispatch('refetchPosts', {})}"
                on:stopEditing="{stopEditing}"
                {editingPost}
            />
        </ClickOutside>
    {:else}
        <Header title="{post.title}" route="{getRoute()}" />
        <div class="card-content">
            <div class="image">
                <Link to="{`/profile/${post.user.id}`}">
                    <img
                        class="circle card-img"
                        src="{post.user.profile.image}"
                        alt="profile image"
                    />
                </Link>
            </div>
            <p class="info">
                {`by ${post.user.username}, on ${timeAgo(post.createdAt)}`}
            </p>
            <p class="body">{post.body}</p>
            <div class="post-action-icons">
                <ActionIcons
                    permissions="{{ actionEdit: $authStore.user.id === post.user.id, actionTrash: $authStore.user.id === post.user.id }}"
                    tooltips="{{ actionEdit: 'Edit', actionTrash: 'Delete' }}"
                    actions="{{ actionEdit: () => onEdit(post), actionTrash: () => onDelete(post.id) }}"
                />
            </div>
            <div class="social-action-icons">
                <ActionIcons
                    text="{{ actionThumbsUp: getVotes(post, 'UP'), actionThumbsDown: getVotes(post, 'DOWN') }}"
                    tooltips="{{ actionThumbsUp: 'Like', actionThumbsDown: 'Dislike' }}"
                    actions="{{ actionThumbsUp: () => like(client, post.id, $authStore.user.id), actionThumbsDown: () => dislike(client, post.id, $authStore.user.id) }}"
                />
            </div>
        </div>
        {#if !commentDialog}
            <div class="comments">
                <Header
                    title="{`Comments (${post.postComments.edges.length})`}"
                >
                    <div slot="actionIcons">
                        {#if modal}
                            {#if modal.hidden}
                                <ActionIcons
                                    permissions="{{ actionPlus: modal.hidden }}"
                                    tooltips="{{ actionPlus: 'Comment the Post' }}"
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
                </Header>
                <ClickOutside on:clickoutside="{hideModal}">
                    <div class="comment-modal" bind:this="{modal}" hidden>
                        <CommentForm
                            on:cancel="{hideModal}"
                            parent="{{ type: 'post', id: post.id }}"
                        />
                    </div>
                </ClickOutside>
                {#each post.postComments.edges as comment}
                    <CommentCard comment="{comment.node}" />
                {/each}
            </div>
        {/if}
    {/if}
</div>
