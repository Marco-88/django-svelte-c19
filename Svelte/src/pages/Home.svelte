<style>
    :global(.card) {
        background: var(--background-component);
    }

    .card {
        margin-bottom: .5rem;
    }
    .post-card {
        margin-bottom: 1rem;
    }


</style>

<script>
    import { getClient, query, mutate } from 'svelte-apollo';
    import { GET_POSTS, DELETE_POST } from '../services/posts/postsApi';
    import PostForm from '../components/posts/PostForm.svelte';
    import ContentWrapper from '../layout/ContentWrapper.svelte';
    import { authStore } from '../services/auth/authStore';
    import { fetchMore } from '../utils';
    import PostCard from '../components/posts/PostCard.svelte';
    import { afterUpdate } from 'svelte';

    let pageInfo;
    let first = 5;
    let after;

    const client = getClient();
    let posts = query(client, { query: GET_POSTS, variables: { first } });

    const getDefaultPost = () => {
        return {
            title: '',
            body: '',
            id: null,
        };
    };

    $: posts.refetch();

    // afterUpdate(() => {
    //     posts.refetch();
    // });

    const setState = queryData => {
        pageInfo = queryData.getPosts.pageInfo;
        after = pageInfo.endCursor;
        return '';
    };

    window.onscroll = function(ev) {
        if (Math.round(window.scrollY + window.innerHeight) >= Math.round(document.body.scrollHeight) &&
            pageInfo && pageInfo.hasNextPage) {
            fetchMore(posts, 'getPosts', first, after);
        }
    };

</script>

<ContentWrapper authNeeded={true} showInfo={true} showFriends={true}>
    <div slot="header">
        <div class="card">
            <PostForm on:refetchPosts={posts.refetch}/>
        </div>
    </div>
    <div slot="body">
        {#await $posts}
            <h3>Loading...</h3>
        {:then result}
            {setState(result.data)}
            {#each result.data.getPosts.edges as post}
                <div class="post-card">
                    <PostCard post={post.node} on:refetchPosts={posts.refetch}/>
                </div>
            {/each}
        {:catch error}
            {console.log(error)}
        {/await}
    </div>
</ContentWrapper>
