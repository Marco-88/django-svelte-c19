import { gql } from 'apollo-boost';

export const GET_POSTS = gql`
    query($first: Int, $after: String, $last: Int, $before: String) {
        getPosts(
            first: $first
            after: $after
            last: $last
            before: $before
            orderBy: "-updated_at"
        ) {
            pageInfo {
                hasNextPage
                hasPreviousPage
                startCursor
                endCursor
            }
            edges {
                node {
                    id
                    title
                    body
                    createdAt
                    updatedAt
                    user {
                        id
                        username
                        profile {
                            id
                            image
                        }
                    }
                    votes {
                        edges {
                            node {
                                id
                                vote
                            }
                        }
                    }
                    postComments {
                        edges {
                            node {
                                id
                                body
                                createdAt
                                updatedAt
                                votes {
                                    edges {
                                        node {
                                            id
                                            vote
                                        }
                                    }
                                }
                                user {
                                    id
                                    username
                                    profile {
                                        id
                                        image
                                    }
                                }
                                commentComments {
                                    edges {
                                        node {
                                            id
                                            body
                                            createdAt
                                            updatedAt
                                            votes {
                                                edges {
                                                    node {
                                                        id
                                                        vote
                                                    }
                                                }
                                            }
                                            user {
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
                        }
                    }
                }
            }
        }
    }
`;

export const GET_POST = gql`
    query($id: ID!) {
        getPost(id: $id) {
            id
            title
            body
            createdAt
            updatedAt
            user {
                id
                username
                profile {
                    id
                    image
                }
            }
            votes {
                edges {
                    node {
                        id
                        vote
                    }
                }
            }
            postComments {
                edges {
                    node {
                        id
                        body
                        createdAt
                        updatedAt
                        votes {
                            edges {
                                node {
                                    id
                                    vote
                                }
                            }
                        }
                        user {
                            id
                            username
                            profile {
                                id
                                image
                            }
                        }
                        commentComments {
                            edges {
                                node {
                                    id
                                    body
                                    createdAt
                                    updatedAt
                                    votes {
                                        edges {
                                            node {
                                                id
                                                vote
                                            }
                                        }
                                    }
                                    user {
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
                }
            }
        }
    }
`;

export const CREATE_POST = gql`
    mutation($title: String!, $body: String!, $userId: String!) {
        createPost(
            input: { data: { title: $title, body: $body }, userId: $userId }
        ) {
            post {
                id
                title
                body
                createdAt
            }
        }
    }
`;

export const UPDATE_POST = gql`
    mutation($title: String!, $body: String!, $id: String!) {
        updatePost(input: { data: { title: $title, body: $body }, id: $id }) {
            errors
            post {
                id
                title
                body
                createdAt
                updatedAt
            }
        }
    }
`;

export const DELETE_POST = gql`
    mutation($id: String!) {
        deletePost(input: { id: $id }) {
            errors
            success
        }
    }
`;

export const CREATE_POST_VOTE = gql`
    mutation($vote: String!, $postId: String!, $userId: String!) {
        createPostVote(
            input: { vote: $vote, postId: $postId, userId: $userId }
        ) {
            postVote {
                id
                vote
                post {
                    id
                    title
                    body
                }
                user {
                    id
                    username
                }
            }
        }
    }
`;
