import {setClient, getClient, query, mutate} from 'svelte-apollo';
import {navigate} from "svelte-routing";
import {createClient} from '../../utils';
import {authStore} from './authStore';
import {TOKEN_AUTH, GET_VIEWER, REGISTER} from './authApi';
import {success, error} from "../notification/notifier";

export const login = (username, password) => {
    authStore.start();
    const client = getClient();

    mutate(client, {
        mutation: TOKEN_AUTH,
        variables: {username, password},
    })
        .then(res => {
            let token = res.data.tokenAuth.token;
            authStore.loggedIn(token);
            setClient(createClient(token));
            loadUser(token);
            success('You got logged in!', 4000);
            navigate("/");
        })
        .catch(err => {
            error('Login: ' + err.message, 4000);
        });
};

export const register = (username, email, password) => {
    authStore.start();

    const client = getClient();

    mutate(client, {
        mutation: REGISTER,
        variables: {username, email, password},
    })
        .then(res => {
            const user = res.data.register.user;
            authStore.registered(user);
            navigate('/login', {state: {username: user.username}});
        })
        .catch(err => {
            error('Register: ' + err.message, 4000);
        });
};

export const loadUser = (token) => {
    const client = getClient();

    const user = query(client, {query: GET_VIEWER});
    user.result()
        .then(res => {
            authStore.userLoaded(token, res.data.getViewer);
        }).catch(err => {
            error('Load User: ' + err.message, 4000);
        });
};