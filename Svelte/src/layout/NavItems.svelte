<script>
    import NavLink from './NavLink.svelte';
    import { authStore } from '../services/auth/authStore';
    import ActionIcons from '../components/widgets/ActionIcons.svelte';
    import { success } from '../services/notification/notifier';
    import { navigate } from 'svelte-routing';

    export let toggle = false;

    const logout = () => {
        authStore.loggedOut();
        success('You got logged out!', 4000);
        navigate('/login');
    };

</script>

{#if $authStore.user}
    {#if toggle}
        <div class="nav-item {toggle ? 'toggle-auth-item' : ''}" title="Your Profile">
            <NavLink to={`profile/${$authStore.user.id}`}>
                <div class="image-wrapper">
                    <img class="circle navbar-img" src={$authStore.user.profile.image}
                         alt="Profile Image">
                </div>
            </NavLink>
            <div class="action-icons">
                <ActionIcons
                        size="2x"
                        actions={{actionSignOut: () => logout()}}
                        tooltips={{actionSignOut: 'Logout'}}/>
            </div>
        </div>
    {/if}
{/if}
<div class="nav-item {toggle ? 'toggle-item' : ''}">
    <NavLink to="/">Home</NavLink>
</div>
<div class="nav-item {toggle ? 'toggle-item' : ''}">
    <NavLink to="about">About</NavLink>
</div>
<div class="nav-item {toggle ? 'toggle-item' : ''}">
    <NavLink to="cov19">CoV19</NavLink>
</div>
{#if $authStore.user}
    {#if !toggle}
        <div class="nav-item {toggle ? 'toggle-item' : ''}" title="Your Profile">
            <NavLink to={`profile/${$authStore.user.id}`}>
                <div class="image-wrapper">
                    <img class="circle navbar-img" src={$authStore.user.profile.image}
                         alt="Profile Image">
                </div>
            </NavLink>
        </div>
        <div class="nav-item {toggle ? 'toggle-item' : ''}">
            <div class="action-icons">
                <ActionIcons
                        size="2x"
                        actions={{actionSignOut: () => logout()}}
                        tooltips={{actionSignOut: 'Logout'}}/>
            </div>
        </div>
    {/if}
{:else}
    <div class="nav-item {toggle ? 'toggle-item' : ''}">
        <NavLink to="login">Login</NavLink>
    </div>
    <div class="nav-item {toggle ? 'toggle-item' : ''}">
        <NavLink to="register">Register</NavLink>
    </div>
{/if}

<style>
    .toggle-item {
        display: flex;
        align-items: center;
        justify-content: center;
        background: var(--primary);
        z-index: 17;
        width: 100%;
    }

    .toggle-auth-item {
        display: flex;
        align-items: center;
        justify-content: center;
        background: var(--primary);
        z-index: 17;
        width: 100%;
    }

    :global(.nav-item.toggle-item a) {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100%;
    }

    .toggle-item:hover {
        background: var(--primary-nav-hover);
    }
    img.circle {
        width: 48px;
        height: 48px;
    }
</style>
