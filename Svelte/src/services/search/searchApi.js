import {gql} from 'apollo-boost';

export const SEARCH = gql`
    query($text: String!, $types: [String]!, $first: Int){
        search(text: $text, types: $types, first: $first) {
            __typename
            ... on PostNode {
                id
                title
            }
            ... on UserNode {
                id
                username
                profile {
                    id
                    image
                }
            }
            ... on GroupNode {
                id
                name
                image
            }
        }
    }
`;
