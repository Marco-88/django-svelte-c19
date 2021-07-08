<script>
    import ContentWrapper from '../layout/ContentWrapper.svelte';
    import {authStore} from '../services/auth/authStore';
    import GroupView from "../components/groups/GroupView.svelte";
    import GroupForm from "../components/groups/GroupForm.svelte";

    export let id;

</script>

<ContentWrapper authNeeded={true} showInfo={true}>
    <div slot="body">
        {#if id === $authStore.user.id}
            <GroupForm/>
        {:else}
            <GroupView {id}/>
        {/if}
    </div>
</ContentWrapper>
