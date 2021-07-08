<script>
    import ContentWrapper from '../layout/ContentWrapper.svelte';
    import { authStore } from '../services/auth/authStore';
    import { cov19Store } from '../services/cov19/cov19Store';
    import Cov19Panel from '../components/cov19/Cov19Panel.svelte';
    import Cov19ChartPanel from '../components/cov19/Cov19ChartPanel.svelte';
</script>

<ContentWrapper showInfo="{true}">
    <div slot="body">
        {#if $cov19Store.dates}
            <Cov19ChartPanel />
        {/if}
        <Cov19Panel />
    </div>
</ContentWrapper>
