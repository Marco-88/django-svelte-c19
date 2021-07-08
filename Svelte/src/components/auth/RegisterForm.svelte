<script>
    import {Link} from 'svelte-routing';
    import {register} from '../../services/auth/authActions';
    import {authStore} from '../../services/auth/authStore';

    let username = '';
    let email = '';
    let password = '';
    let confirmPassword = '';

    const submitRegister = () => {
        if (username.trim() === '' || email.trim() === '' ||
                password.trim() === '' || confirmPassword.trim() === '') {
            error('input is invalid', 4000);
            return;
        }
        if (password.length < 8) {
            error('Password has a min length of 8 signs.', 4000);
            return;
        }
        if (password !== confirmPassword) {
            error('Passwords do not match.', 4000);
            return;
        }

        register(username, email, password);
    };
</script>

<form on:submit|preventDefault={submitRegister}>
    <div id="register">
        <div class="form-group input-username">
            <label for="username">Username</label>
            <input type="text" id="username" class="form-control" required bind:value={username}/>
        </div>
        <div class="form-group input-email">
            <label for="email">Email</label>
            <input type="email" id="email" class="form-control" required bind:value={email}/>
        </div>
        <div class="form-group input-password">
            <label for="password">Password</label>
            <input type="password" id="password" class="form-control" required bind:value={password}/>
        </div>
        <div class="form-group input-confirm-password">
            <label for="confirm-password">Confirm Password</label>
            <input type="password" id="confirm-password" class="form-control" required bind:value={confirmPassword}/>
        </div>
        <div class="action">
            <button type="submit" class="btn btn-submit">Register</button>
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

    .input-email {
        grid-area: input-email;
    }

    .input-password {
        grid-area: input-password;
    }

    .input-confirm-password {
        grid-area: input-confirm-password;
    }

    .action {
        grid-area: action;
    }

    .reset-password {
        grid-area: reset-password;
    }

    #register {
        display: grid;
        grid-template-columns: 2% 23% 50% 23% 2%;
        grid-template-rows: auto;
        align-items: center;
        grid-template-areas:
                ". input-username input-username input-username ."
                ". input-email input-email input-email ."
                ". input-password input-password input-password ."
                ". input-confirm-password input-confirm-password input-confirm-password ."
                ". action . reset-password .";
        margin: 10px auto 0;
        padding: 5px;
        width: 50%;
        background: var(--background-component);
    }
</style>
