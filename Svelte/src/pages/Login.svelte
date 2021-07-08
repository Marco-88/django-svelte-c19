<script>
    import {Link} from 'svelte-routing';
    import LoginForm from '../components/auth/LoginForm.svelte';
    import ContentWrapper from '../layout/ContentWrapper.svelte';
</script>

<ContentWrapper>
    <div slot="header" class="content-header row">
        <h4 class="col-8 offset-2">
            Login or <Link to="/register">Register</Link>?
        </h4>
    </div>
    <div slot="body"class="content-body">
        <LoginForm/>
    </div>
</ContentWrapper>
