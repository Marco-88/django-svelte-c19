import {gql} from 'apollo-boost';

export const CREATE_GROUP = gql`
    mutation($name: String!, $ownerId: String!, $description: String!, $usernames: [String]!, $image: Upload, $genres: [String]) {
        createGroup(input: {
            data : {
                name: $name, ownerId: $ownerId, description: $description, usernames: $usernames, image: $image, genres: $genres
            }
        }) {
            group{
                id
                name
                owner {
                    id
                    username
                    profile {
                        id
                        image
                    }
                }
                description
                users {
                    id
                    username
                    profile {
                        id
                        image
                    }
                }
                image
                genres
            }
        }
    }
`;

export const GET_GROUP = gql`
    query($id: ID!) {
        getGroup(id: $id) {
            id
            name
            owner {
                id
                username
                profile {
                    id
                    image
                }
            }
            description
            users {
                id
                username
                profile {
                    id
                    image
                }
            }
            image
            genres
        }
    }
`;

export const GET_GROUPS = gql`
    query($userId: String) {
        getGroups (userId: $userId){
            edges {
                node {
                    id
                    name
                    owner {
                        id
                        username
                        profile {
                            id
                            image
                        }
                    }
                    description
                    users {
                        id
                        username
                        profile {
                            id
                            image
                        }
                    }
                    image
                    genres
                }
            }
        }
    }
`;

export const JOIN_GROUP = gql`
    mutation($groupId: String!, $userId: String!) {
        joinGroup(input: {
            groupId: $groupId,
            userId: $userId
        }) {
            errors
            group {
                id
                name
                owner {
                    id
                    username
                    profile {
                        id
                        image
                    }
                }
                description
                users {
                    id
                    username
                    profile {
                        id
                        image
                    }
                }
                image
                genres
            }
        }
    }
`;

export const REMOVE_MEMBER = gql`
    mutation($groupId: String!, $userId: String!) {
        removeMember(input: {
            groupId: $groupId,
            userId: $userId
        }) {
            errors
            group {
                id
                name
            }
            user {
                id
                username
            }
        }
    }
`;

export const DELETE_GROUP = gql`
    mutation($id: String!) {
        deleteGroup(input: {
            id: $id,
        }) {
            errors
            success
        }
    }
`;
