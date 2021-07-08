<script>
    import {Link} from 'svelte-routing';
    import RegisterForm from '../components/auth/RegisterForm.svelte';
    import ContentWrapper from "../layout/ContentWrapper.svelte";
</script>

<ContentWrapper>
    <div slot="header" class="content-header row">
        <h4 class="col-8 offset-2">
            Register or <Link to="/login">Login</Link>?
        </h4>
    </div>
    <div slot="body" class="content-body">
        <RegisterForm/>
    </div>
</ContentWrapper>
