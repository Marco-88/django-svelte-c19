<script>
    import { getClient, mutate } from 'svelte-apollo';
    import { createEventDispatcher } from 'svelte';
    import Header from '../../layout/Header.svelte';
    import { error, success } from '../../services/notification/notifier';
    import { authStore } from '../../services/auth/authStore';
    import { GENRES } from '../../constants';
    import { UPDATE_PROFILE } from '../../services/profiles/profilesApi';

    const dispatch = createEventDispatcher();

    export let user = $authStore.user;
    const profile = user.profile;

    $: username = user.username;
    $: email = user.email;
    $: description = profile.description;
    $: birthdate = profile.birthdate;
    $: dark = profile.dark;

    let image;
    let genres = new Set(profile.genres);

    const client = getClient();
    const submitProfile = () => {
        console.log(image);
        mutate(client, {
            mutation: UPDATE_PROFILE,
            variables: {
                userId: user.id,
                image: image[0].name ? image[0] : undefined,
                description,
                genres: Array.from(genres),
                birthdate,
                dark,
            },
        }).then(res => {
            success('Profile-Update: Successful!', 4000);
            authStore.updateUser({ username, email, profile: res.data.updateProfile.profile });
        }).catch(err => {
            error(err.message, 4000);
        });
    };

    const toggleGenre = event => {
        genres.delete(event.target.id) || genres.add(event.target.id);
    };

    const cancel = () => {
        window.history.back();
    }
</script>

<form on:submit|preventDefault={submitProfile}>
    <div class="card">
        <Header title="Your Profile"/>
        <div class="card-content">
            <div class="image">
                <img class="circle" src={profile.image} alt="profile image">
            </div>
            <div class="inputUser">
                <div class="form-group">
                    <label for="username">Username</label>
                    <input type="text" id="username" bind:value={user.username} class="form-control"/>
                </div>
                <div class="form-group">
                    <label for="email">Email</label>
                    <input type="email" id="email" bind:value={user.email} class="form-control"/>
                </div>
            </div>
            <div class="form-group inputFile">
                <label for="file">Profile Image</label>
                <input type="file" class="form-control-file" id="file" bind:files={profile.image}>
            </div>
            <div class="form-group inputDate">
                <label for="birthdate">Date of Birth</label>
                <input type="date" id="birthdate" bind:value={profile.birthdate} class="form-control"/>
            </div>
            <div class="custom-control custom-switch inputSwitch">
                <input type="checkbox" class="custom-control-input" id="dark" bind:checked={profile.dark}>
                <label class="custom-control-label" for="dark">Darkmode</label>
            </div>
            <div class="form-group inputDesc">
                <label for="description">Description</label>
                <textarea type="text" id="description" bind:value={profile.description}></textarea>
            </div>
            <div class="genres">
                <Header title="Genres"/>
                <ul class="genres-list">
                    {#each Object.keys(GENRES) as key}
                        <li class="form-check">
                            <input type="checkbox" class="form-check-input" id={key}
                                   on:click={toggleGenre} checked={genres.has(key)}>
                            <label class="form-check-label" for={key}>{GENRES[key]}</label>
                        </li>
                    {/each}
                </ul>
            </div>
            <div class="action">
                <button type="submit" class="btn btn-submit">
                    UPDATE
                </button>
                <button type="button" class="btn btn-cancel" on:click={cancel}>
                    CANCEL
                </button>
            </div>
        </div>
    </div>
</form>

<style>

    ul.genres-list {
        padding: 10px 0;
        margin: 0;
    }

    li {
        float: left;
        width: 20%;
    }

    .image {
        grid-area: image;
    }

    .inputUser {
        grid-area: inputUser;
    }

    .inputFile {
        grid-area: inputFile;
    }

    .inputDate {
        grid-area: inputDate;
    }

    .inputSwitch {
        grid-area: inputSwitch;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .inputDesc {
        grid-area: inputDesc;
    }

    .genres {
        grid-area: genres;
        padding-bottom: 20px;
    }

    .action {
        grid-area: action;
    }

    textarea {
        width: 100%;
    }

    form .card-content {
        display: grid;
        grid-template-columns: 1% 22% 22% 22% 22% 1%;
        grid-column-gap: 2%;
        align-items: center;
        grid-template-rows: auto;
        grid-template-areas:
                ". image inputUser inputUser inputUser ."
                ". inputFile inputFile inputDate inputSwitch ."
                ". inputDesc inputDesc inputDesc inputDesc ."
                ". genres genres genres genres ."
                ". action action . . .";
    }

    /* Extra small devices (phones, 600px and down) */
    @media only screen and (max-width: 600px) {
        li {
            float: left;
            width: 50%;
        }

        form .card-content {
            grid-template-areas:
                    ". image inputUser inputUser inputUser ."
                    ". inputFile inputFile inputFile inputFile ."
                    ". inputDate inputDate inputSwitch inputSwitch ."
                    ". inputDesc inputDesc inputDesc inputDesc ."
                    ". genres genres genres genres ."
                    ". . action action . .";
        }
    }
</style>
