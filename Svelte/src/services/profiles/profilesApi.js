import {gql} from 'apollo-boost';

export const UPDATE_PROFILE = gql`
    mutation($userId: String!, $image: Upload, $description: String, $genres: [String], $birthdate: Date!, $dark: Boolean!) {
        updateProfile(input: {
            userId: $userId,
            data : {
                image: $image, description: $description, genres: $genres, birthdate: $birthdate, dark: $dark
            }
        }) {
            profile{
                id
                dark
                birthdate
                description
                genres
                image
                friends {
                    id
                    username
                    profile {
                        id
                        image
                    }
                }
            }
        }
    }
`;

export const GET_PROFILE = gql`
    query($id: ID) {
        getProfile(id: $id) {
            id
            dark
            birthdate
            description
            genres
            image
            friends {
                edges {
                    node {
                        id
                        username
                        profile {
                            id
                            image
                        }
                    }
                }
            }
        }
    }
`;

export const GET_PROFILES = gql`
    query {
        getProfiles {
            id
            dark
            birthdate
            description
            genres
            image
            friends {
                id
                username
                profile {
                    id
                    image
                }
            }
        }
    }
`;

export const ADD_FRIEND = gql`
    mutation($friendId: String!) {
        addFriend(
            input: {friendId: $friendId}
        ) {
            friend {
                id
                username
                profile {
                    id
                    image
                }
            }
        }
    }
`;

export const REMOVE_FRIEND = gql`
    mutation($friendId: String!) {
        removeFriend(
            input: {friendId: $friendId}
        ) {
            friend {
                id
                username
                profile {
                    id
                    image
                }
            }
        }
    }
`;

