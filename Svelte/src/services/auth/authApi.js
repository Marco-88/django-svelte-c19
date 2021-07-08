import {gql} from 'apollo-boost';

export const REGISTER = gql`
    mutation($username: String!, $email: String!, $password: String!) {
        register(input: {data : {
            username: $username, email: $email, password: $password
        }}) {
            user {
                id
                username
                email
                profile {
                    id
                    dark
                    birthdate
                    description
                    genres
                    image
                }
            }
        }
    }
`;

export const TOKEN_AUTH = gql`
    mutation ($username: String!, $password: String!){
        tokenAuth(username: $username, password: $password){
            token
        }
    }
`;

export const VERIFY_TOKEN = gql`
    mutation($token: String!) {
        verifyToken(token: $token) {
            payload
        }
    }
`;

export const REFRESH_TOKEN = gql`
    mutation($token: String!) {
        refreshToken(token: $token) {
            payload
        }
    }
`;

export const GET_VIEWER = gql`
    query {
        getViewer {
            id
            username
            email
            profile {
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
            ownerGroups {
                edges {
                    node {
                        id
                        name
                        description
                        image
                        owner {
                            id
                            username
                        }
                        users {
                            id
                            username
                        }
                    }
                }
            }
            memberGroups {
                edges {
                    node {
                        id
                        name
                        description
                        image
                        owner {
                            id
                            username
                        }
                    }
                }
            }
        }
    }
`;

export const GET_USER = gql`
    query($id: ID!) {
        getUser(id: $id) {
            id
            username
            email
            profile {
                id
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
            ownerGroups {
                edges {
                    node {
                        id
                        name
                        description
                        image
                        owner {
                            id
                            username
                        }
                        users {
                            id
                            username
                        }
                    }
                }
            }
            memberGroups {
                edges {
                    node {
                        id
                        name
                        description
                        image
                        owner {
                            id
                            username
                        }
                        users {
                            id
                            username
                        }
                    }
                }
            }
        }
    }
`;

export const GET_USERS = gql`
    query($username: String, $email: String, $first: Int, $after: String, $last: Int, $before: String) {
        getUsers(username: $username, email: $email, first: $first, after: $after, last: $last, before: $before) {
            pageInfo {
                hasNextPage
                hasPreviousPage
                startCursor
                endCursor
            }
            edges {
                node {
                    id
                    username
                    email
                    profile {
                        id
                        dark
                        birthdate
                        description
                        genres
                        image
                    }
                    ownerGroups {
                        edges {
                            node {
                                id
                                name
                                description
                                image
                                users {
                                    id
                                    username
                                }
                            }
                        }
                    }
                    memberGroups {
                        edges {
                            node {
                                id
                                name
                                description
                                image
                                users {
                                    id
                                    username
                                }
                            }
                        }
                    }
                }
            }
        }
    }
`;