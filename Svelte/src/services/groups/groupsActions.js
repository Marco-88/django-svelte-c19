import {mutate} from "svelte-apollo";
import {JOIN_GROUP, REMOVE_MEMBER, DELETE_GROUP} from "../../services/groups/groupsApi";
import {error, success} from "../../services/notification/notifier";
import {navigate} from "svelte-routing";


export const joinGroup = (client, groupId, userId) => {
    mutate(client, {
        mutation: JOIN_GROUP,
        variables: {groupId, userId}
    }).then(res => {
        if(res.data.joinGroup.errors)
            error(res.data.joinGroup.errors.message, 4000);
        else
            success(`You joined "${res.data.joinGroup.group.name}"!`, 4000);
    }).catch(err => {
        error(err.message, 4000)
    });
};

export const removeMember = (client, groupId, userId) => {
    mutate(client, {
        mutation: REMOVE_MEMBER,
        variables: {groupId, userId}
    }).then(res => {
        success(`${res.data.removeMember.user.username} was removed or left "${res.data.removeMember.group.name}"!`, 4000);
    }).catch(err => {
        error(err.message, 4000)
    });
};

export const deleteGroup = (client, id) => {
    mutate(client, {
        mutation: DELETE_GROUP,
        variables: {id}
    }).then(res => {
        console.log(res);
        success(`Delete Group: Successful!`, 4000);
        navigate("/");
    }).catch(err => {
        error(err.message, 4000)
    });
};