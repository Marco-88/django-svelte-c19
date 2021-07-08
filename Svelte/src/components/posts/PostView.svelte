<script>
    import { afterUpdate } from 'svelte';
    import { getClient, query } from 'svelte-apollo';
    import { Link } from 'svelte-routing';
    import Header from '../../layout/Header.svelte';
    import { error } from '../../services/notification/notifier';
    import { authStore } from '../../services/auth/authStore';
    import { GET_POST } from '../../services/posts/postsApi';
    import PostCard from './PostCard.svelte';

    export let id;
    let isEditing = false;
    const client = getClient();

    let post = query(client, { query: GET_POST, variables: { id } });

    afterUpdate(() => {
        post = query(client, { query: GET_POST, variables: { id } });
    });
</script>

{#if post}
    {#await $post}
        <h3>Loading...</h3>
    {:then result}
        <PostCard post={result.data.getPost}/>
    {:catch err}
        {error(err.message, 4000)}
    {/await}
{/if}
