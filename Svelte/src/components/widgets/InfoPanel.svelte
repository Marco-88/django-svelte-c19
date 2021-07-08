<script>
    import Header from '../../layout/Header.svelte';
    import Cov19Info from '../cov19/Cov19Info.svelte';
    import { formatDate } from '../../utils';
    import ToggleBox from './ToggleBox.svelte';
</script>

<section id="info-panel" class="z-depth-2">
    <ToggleBox title="CoV-19 Info"
               actionIconOpen={{tooltip: 'Open Info', actionName: 'actionPlus'}}
               actionIconClose={{tooltip: 'Close Info', actionName: 'actionMinus'}}
               clickOutside={false}
               hidden={false}>
        <div slot="toggle-content">
            <Cov19Info/>
        </div>
    </ToggleBox>
</section>

<style>
    #info-panel {
        background: var(--background-component);
        margin: 0;
        border: 1px solid var(--primary);
        border-bottom: 2px solid var(--primary);
    }
</style>
