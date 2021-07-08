<script>
    import ContentWrapper from '../layout/ContentWrapper.svelte';
    import {authStore} from '../services/auth/authStore';
    import PostView from "../components/posts/PostView.svelte";

    export let id;
</script>

<ContentWrapper authNeeded={true} showInfo={true}>
    <div slot="body">
        <PostView {id}/>
    </div>
</ContentWrapper>
