<script>
    import '../public/css/colors.css';
    import { setClient } from 'svelte-apollo';
    import { authStore } from './services/auth/authStore';
    import Router from './layout/Router.svelte';
    import { createClient } from './utils';
    import { loadUser } from './services/auth/authActions';
    import { onMount, afterUpdate } from 'svelte';
    import { cov19Store } from './services/cov19/cov19Store';
    import {
        fetchCov19Data,
        fetchCov19DatesJson,
    } from './services/cov19/cov19Actions';

    setClient(createClient($authStore.token));

    const init = async () => {
        await fetchCov19Data(false)
            .then(res => {
                console.log('ROWS', res);
                cov19Store.updateRows(res);
            })
            .catch(err => console.log(err));

        await fetchCov19Data(false, 'all')
            .then(res => {
                console.log('ALL', res);
                cov19Store.updateAll(res);
            })
            .catch(err => console.log(err));

        await fetchCov19Data(true)
            .then(res => {
                console.log('DATES', res);
                cov19Store.updateDates(res);
            })
            .catch(err => {
                console.log(err);
            });
    };

    onMount(() => {
        const token = localStorage.getItem('token');
        if (token) loadUser(localStorage.getItem('token'));
    });

    init();
</script>

<div id="page-wrapper">
    <Router />
</div>
