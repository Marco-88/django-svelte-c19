import {getClient, query, mutate} from 'svelte-apollo';
import {UPDATE_PROFILE, ADD_FRIEND, REMOVE_FRIEND} from './profilesApi';
import {success, error} from "../notification/notifier";

export const updateProfile = (DATA) => {
    const client = getClient();

    mutate(client, {
        mutation: UPDATE_PROFILE,
        variables: {...DATA},
    })
        .then(res => {
            success('Your profile data update was successful!', 4000);
        })
        .catch(err => {
            error(err.message, 4000);
        });
};

export const addFriend = (client, friendId) => {
    mutate(client, {
        mutation: ADD_FRIEND,
        variables: { friendId },
    })
        .then(res => {
            success(`You send a Friend Request!`, 4000);
        })
        .catch(err => {
            error(err.message, 4000);
        });
};

export const removeFriend = (client, friendId) => {
    mutate(client, {
        mutation: REMOVE_FRIEND,
        variables: { friendId },
    })
        .then(res => {
            success(`You removed a Friend!`, 4000);
        })
        .catch(err => {
            error(err.message, 4000);
        });
};