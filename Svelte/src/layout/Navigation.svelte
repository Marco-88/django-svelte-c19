<style>
    header, #nav-main {
        height: 64px;
    }

    #nav-main {
        background: var(--primary);

    }

    img.circle {
        width: 48px;
        height: 48px;
    }

    .action-icons {
        width: 64px;
        height: 64px;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .nav-wrapper {
        background: var(--primary);
    }

    .logo {
        grid-area: logo;
    }

    .search {
        grid-area: search;
        display: flex;
        align-items: center;
        justify-content: flex-end;
    }

    .items {
        grid-area: items;
        display: flex;
        align-items: center;
        justify-content: flex-end;
    }


    /* Medium devices (landscape tablets, 768px and up) */
    @media only screen and (max-width: 768px) {
        img.circle {
            width: 48px;
            height: 48px;
        }

        .search {
            grid-area: search;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .items {
            grid-area: items;
            display: flex;
            justify-content: space-around;
            align-items: center;
        }

        .nav-wrapper {
            display: grid;
            grid-template-columns: 2% 15% 58% 15% 2%;
            grid-column-gap: 2%;
            align-items: center;
            grid-template-rows: 64px;
            grid-template-areas: ". logo search items ."
        }

        nav {
            display: block;
        }
    }

    /* Medium devices (landscape tablets, 768px and up) */
    @media only screen and (min-width: 768px) {
        /*.items {*/
        /*    grid-area: items;*/
        /*    justify-content: space-around;*/
        /*    align-items: center;*/
        /*}*/
        .nav-wrapper {
            display: grid;
            grid-template-columns: 2% 10% 28% 50% 2%;
            grid-column-gap: 2%;
            align-items: center;
            grid-template-rows: 64px;
            grid-template-areas: ". logo search items ."
        }
    }

    :global(.nav-item a) {
        color: var(--color);
        height: 64px;
        display: flex;
        align-items: center;
    }

    :global(.nav-item:not(.logo) a:hover) {
        background: var(--primary-nav-hover);
    }

    :global(.nav-item a.active) {
        color: var(--color);
        font-weight: bold;
    }
    .toggle-menu {
        display: flex;
        flex-direction: column;
    }
</style>

<script>
    import Icon from 'svelte-awesome';
    import { signOut } from 'svelte-awesome/icons';
    import { navigate } from 'svelte-routing';
    import MediaQuery from 'svelte-media-query';
    import { formatDate } from '../utils';
    import NavLink from './NavLink.svelte';
    import ClickOutside from 'svelte-click-outside';
    import { authStore } from '../services/auth/authStore';
    import { success } from '../services/notification/notifier';
    import ActionIcons from '../components/widgets/ActionIcons.svelte';
    import SearchBar from '../components/search/SearchBar.svelte';
    import NavItems from './NavItems.svelte';


    let toggler;
    let search;
    let items;
    let menu;

    $: user = $authStore.user;

    const logout = () => {
        authStore.loggedOut();
        success('You got logged out!', 4000);
        navigate('/login');
    };

    const showMenu = () => {
        menu.hidden = false;
    };

    const hideMenu = () => {
        menu.hidden = true;
    };
</script>

<header>
    <nav id="nav-main">
        <div class="nav-wrapper">
            <div class="logo nav-item">
                <NavLink to="/">
                    <span class="logo">Svelte</span>
                </NavLink>
            </div>
            <div class="search" bind:this={search}>
                {#if $authStore.user}
                    <SearchBar/>
                {/if}
            </div>
            <div class="items">
                <MediaQuery query="(max-width: 768px)" let:matches>
                    {#if matches}
                        <div class="toggler nav-item">
                            <div class="action-toggler" bind:this={toggler} on:click={showMenu}>
                                {#if menu.hidden}
                                    <ActionIcons
                                            size="2x"
                                            tooltips={{actionBars: 'Open Menu'}}
                                            actions={{actionBars: showMenu}}
                                    />
                                    {:else}
                                    <ActionIcons
                                            size="2x"
                                            tooltips={{actionTimes: 'Close Menu'}}
                                            actions={{actionTimes: hideMenu}}
                                    />
                                {/if}
                            </div>
                        </div>
                    {/if}
                </MediaQuery>
                <MediaQuery query="(min-width: 768px)" let:matches>
                    {#if matches}
                        <NavItems/>
                    {/if}
                </MediaQuery>
            </div>
        </div>
        <ClickOutside on:clickoutside={hideMenu}>
            <div class="toggle-menu" bind:this={menu} on:click={hideMenu} hidden>
                <NavItems toggle={true}/>
            </div>
        </ClickOutside>
    </nav>
</header>

