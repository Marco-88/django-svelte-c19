<script>
    import ProfileForm from '../components/profiles/ProfileForm.svelte';
    import ContentWrapper from '../layout/ContentWrapper.svelte';
    import ProfileView from '../components/profiles/ProfileView.svelte';
    import {authStore} from '../services/auth/authStore';
    export let id;

</script>

<ContentWrapper authNeeded={true}>
    <div slot="body">
        {#if id === $authStore.user.id}
            <ProfileForm/>
        {:else}
            <ProfileView {id}/>
        {/if}
    </div>
</ContentWrapper>