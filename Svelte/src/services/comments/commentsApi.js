import { gql } from 'apollo-boost';

export const GET_COMMENTS = gql`
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
                    commentComments {
                        edges {
                            node {
                                id
                                body
                                user {
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

export const GET_COMMENT = gql`
    query($id: ID!) {
        getPost(id: $id) {
            id
            title
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
`;

export const CREATE_COMMENT = gql`
    mutation(
        $body: String!
        $userId: String!
        $postId: String
        $commentId: String
    ) {
        createComment(
            input: {
                data: { body: $body }
                userId: $userId
                postId: $postId
                commentId: $commentId
            }
        ) {
            comment {
                id
                body
                createdAt
            }
        }
    }
`;

export const UPDATE_COMMENT = gql`
    mutation($body: String!, $id: String!) {
        updateCommentt(input: { data: { body: $body }, id: $id }) {
            errors
            post {
                id
                body
                createdAt
                updatedAt
            }
        }
    }
`;

export const DELETE_COMMENT = gql`
    mutation($id: String!) {
        deleteComment(input: { id: $id }) {
            errors
            success
        }
    }
`;

export const CREATE_COMMENT_VOTE = gql`
    mutation($vote: String!, $commentId: String!, $userId: String!) {
        createCommentVote(
            input: { vote: $vote, commentId: $commentId, userId: $userId }
        ) {
            commentVote {
                id
                vote
                comment {
                    id
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