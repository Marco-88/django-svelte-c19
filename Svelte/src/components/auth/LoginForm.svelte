<script>
    import { Link } from 'svelte-routing';
    import Header from '../../layout/Header.svelte';
    import { login } from '../../services/auth/authActions';
    import { authStore } from '../../services/auth/authStore';
    import {success} from "../../services/notification/notifier";


    let username = '';
    let password = '';

    const historyState = window.history.state;

    if(historyState && historyState.username) {
        username = historyState.username;
        success(`Your registration was successful! Now you are able to sign in, ${username}! :)`, 4000);
    }

    const submitLogin = () => {
        if (username.trim() === '' || password.trim() === '') {
            authStore.fail('Error: input is invalid');
            return;
        }
        login(username, password);
    };
</script>

<form on:submit|preventDefault={submitLogin}>
        <div id="login">
            <div class="form-group input-username">
                <label for="username">Username</label>
                <input type="text" id="username" class="form-control" required bind:value={username}/>
            </div>
            <div class="form-group input-password">
                <label for="password">Password</label>
                <input type="password" id="password" class="form-control" required bind:value={password}/>
            </div>
            <div class="action">
                <button type="submit" class="btn btn-submit">Login</button>
            </div>
            <div class="reset-password">
                <Link to="/contact">Reset Password</Link>
            </div>
        </div>
</form>

<style>
    .input-username {
        grid-area: input-username;
    }

    .input-password {
        grid-area: input-password;
    }

    .action {
        grid-area: action;
    }

    .reset-password {
        grid-area: reset-password;
    }

    #login {
        display: grid;
        grid-template-columns: 2% 23% 50% 23% 2%;
        grid-template-rows: auto;
        align-items: center;
        grid-template-areas:
                ". input-username input-username input-username ."
                ". input-password input-password input-password ."
                ". action . reset-password .";
        margin: 10px auto 0;
        padding: 5px;
        width: 50%;
        background: var(--background-component);
    }
</style>
