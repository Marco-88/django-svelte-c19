import { ApolloClient } from 'apollo-client';
import { InMemoryCache } from 'apollo-cache-inmemory';
import { HttpLink } from 'apollo-link-http';
import { onError } from 'apollo-link-error';
import { ApolloLink } from 'apollo-link';
import { apiUrl } from './config';
import { createUploadLink } from 'apollo-upload-client';
import { getContext } from 'svelte';
import { ROUTER } from 'svelte-routing/src/contexts';

export const createClient = token => {
    const httpLink = createUploadLink({
        uri: apiUrl,
        credentials: 'same-origin',
    });
    if (!token) {
        return new ApolloClient({
            link: httpLink,
            cache: new InMemoryCache(),
        });
    } else {
        return new ApolloClient({
            link: new ApolloLink((operation, forward) => {
                operation.setContext({
                    headers: {
                        authorization: 'JWT ' + token,
                    },
                });
                return forward(operation);
            }).concat(httpLink),
            cache: new InMemoryCache(),
        });
    }
};

export const refreshForms = selector => {
    const elements = document.querySelectorAll(selector);
    elements.forEach(elem => elem.focus());
};

export const formatLongText = (text, length) => {
    return text.slice(0, length) + '...';
};

export const fetchMore = (query, queryName, first, after) => {
    query.fetchMore({
        variables: { first, after },
        updateQuery: (previousResult, { fetchMoreResult }) => {
            const newEdges = fetchMoreResult[queryName].edges;
            const pageInfo = fetchMoreResult[queryName].pageInfo;

            const obj = {};

            if (newEdges.length) {
                obj[queryName] = {
                    __typename: previousResult.getPosts.__typename,
                    edges: [...previousResult.getPosts.edges, ...newEdges],
                    pageInfo,
                };
            }
            return newEdges.length ? obj : previousResult;
        },
    });
};

export const getActiveRoute = () => {
    const { activeRoute } = getContext(ROUTER);
    return activeRoute;
};

export const formatDate = date => {
    return new Date(date).toLocaleString();
};

export const formatDateOnly = date => {
    return new Date(date).toLocaleDateString();
};

export const getDate = () => {
    return new Date().toLocaleDateString();
};

export const getTime = () => {
    return new Date().toLocaleTimeString();
};

const MONTH_NAMES = [
    'January',
    'February',
    'March',
    'April',
    'May',
    'June',
    'July',
    'August',
    'September',
    'October',
    'November',
    'December',
];

export const getFormattedDate = (
    date,
    prefomattedDate = false,
    hideYear = false
) => {
    const day = date.getDate();
    const month = MONTH_NAMES[date.getMonth()];
    const year = date.getFullYear();
    const hours = date.getHours();
    let minutes = date.getMinutes();

    if (minutes < 10) {
        // Adding leading zero to minutes
        minutes = `0${minutes}`;
    }

    if (prefomattedDate) {
        // Today at 10:20
        // Yesterday at 10:20
        return `${prefomattedDate} at ${hours}:${minutes}`;
    }

    if (hideYear) {
        // 10. January at 10:20
        return `${day}. ${month} at ${hours}:${minutes}`;
    }

    // 10. January 2017. at 10:20
    return `${day}. ${month} ${year}. at ${hours}:${minutes}`;
};

// --- Main function
export const timeAgo = dateParam => {
    if (!dateParam) {
        return null;
    }

    const date =
        typeof dateParam === 'object' ? dateParam : new Date(dateParam);
    const DAY_IN_MS = 86400000; // 24 * 60 * 60 * 1000
    const today = new Date();
    const yesterday = new Date(today - DAY_IN_MS);
    const seconds = Math.round((today - date) / 1000);
    const minutes = Math.round(seconds / 60);
    const isToday = today.toDateString() === date.toDateString();
    const isYesterday = yesterday.toDateString() === date.toDateString();
    const isThisYear = today.getFullYear() === date.getFullYear();

    if (seconds < 5) {
        return 'now';
    } else if (seconds < 60) {
        return `${seconds} seconds ago`;
    } else if (seconds < 90) {
        return 'about a minute ago';
    } else if (minutes < 60) {
        return `${minutes} minutes ago`;
    } else if (isToday) {
        return getFormattedDate(date, 'Today'); // Today at 10:20
    } else if (isYesterday) {
        return getFormattedDate(date, 'Yesterday'); // Yesterday at 10:20
    } else if (isThisYear) {
        return getFormattedDate(date, false, true); // 10. January at 10:20
    }

    return getFormattedDate(date); // 10. January 2017. at 10:20
};

export const checkDate = (date, startDate, endDate) => {
    if (typeof date === 'string') date = new Date(date);
    if (typeof startDate === 'string') startDate = new Date(startDate);
    if (typeof endDate === 'string') endDate = new Date(endDate);
    startDate.setHours(startDate.getHours() - 1);
    return startDate <= date && date <= endDate;
};

export const getVotes = (voteItem, type = 'UP') => {
    let voteCount = 0;
    voteItem.votes.edges.forEach(edge => {
        if (edge.node.vote === type) {
            voteCount++;
        }
    });
    return voteCount === 0 ? '0' : voteCount;
};

export const formatInputDate = date => {
    var d = new Date(date),
        month = '' + (d.getMonth() + 1),
        day = '' + d.getDate(),
        year = d.getFullYear();

    if (month.length < 2) month = '0' + month;
    if (day.length < 2) day = '0' + day;

    return [year, month, day].join('-');
};

export const getColSum = (colName, rows, startIndex = 1) => {
    let sum = 0;
    const neededRows = rows.slice(startIndex, rows.length - 2);
    neededRows.forEach(row => {
        let number = 0;
        Object.keys(row).forEach(key => {
            if (key === colName) {
                number = Number(row[key]);
            }
        });
        if (number && !Number.isNaN(number) && typeof number === 'number') {
            sum += number;
        }
    });
    return sum;
};