<script>
    import Notification from './Notification.svelte';
    import {authStore} from '../services/auth/authStore';
    import {Link} from 'svelte-routing';
    import {getContext} from 'svelte';
    import {ROUTER} from 'svelte-routing/src/contexts';
    import GroupPanel from '../components/groups/GroupPanel.svelte';
    import InfoPanel from '../components/widgets/InfoPanel.svelte';
    import Cov19Panel from "../components/cov19/Cov19Panel.svelte";
    import FriendsSidePanel from "../components/friends/FriendsSidePanel.svelte";

    export let authNeeded = false;
    export let showInfo = false;
    export let showFriends = false;

    const {activeRoute} = getContext(ROUTER);

    const noInfo = () => $activeRoute.route.path === 'profile/:id/';
</script>

<section class="row">
    <div class="col-12">
        <div class="content-notification col-4 offset-4">
            <Notification/>
        </div>
    </div>
    {#if authNeeded}
        {#if !$authStore.token}
            <div class="col-8 offset-2">
                <h3>Please
                    <Link to="login">Login</Link>
                    or
                    <Link to="register">Register</Link>
                    !
                </h3>
            </div>
        {:else if $authStore.user}
            <div class="col-12 col-md-6 {noInfo() ? 'col-lg-4' : 'col-lg-3'} order-2 order-lg-1">
                <GroupPanel/>
            </div>
            {#if showInfo}
                {#if showFriends && $authStore.user.profile.friends}
                    <FriendsSidePanel active="active" friends={$authStore.user.profile.friends.edges}>
                        <div slot="info">
                            <InfoPanel/>
                        </div>
                    </FriendsSidePanel>
                {:else}
                    <div class="col-12 col-md-6 col-lg-3 order-1 order-lg-3">
                        <InfoPanel/>
                    </div>
                {/if}
            {/if}
            <div class="col-12 {noInfo() ? 'col-lg-8' : 'col-lg-6'} order-3 order-lg-2">
                <slot name="header"></slot>
                <slot name="body"></slot>
            </div>
        {/if}
    {:else}
        <div class="col-12 col-md-10 offset-md-1">
            <slot name="header"></slot>
            <slot name="body"></slot>
        </div>
    {/if}
</section>

<style>
    section {
        padding-top: 16px;
    }
    h3 {
        text-align: center;
    }
</style>
