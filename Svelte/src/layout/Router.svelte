<script>
    import { Router, Route } from 'svelte-routing';
    import Home from '../pages/Home.svelte';
    import About from '../pages/About.svelte';
    import Login from '../pages/Login.svelte';
    import Register from '../pages/Register.svelte';
    import Profile from '../pages/Profile.svelte';
    import Group from '../pages/Group.svelte';
    import Navigation from './Navigation.svelte';
    import Post from '../pages/Post.svelte';
    import CoV19 from '../pages/CoV19.svelte';
</script>

<Router>
    <Navigation/>
    <main>
        <div class="container-min">
            <Route path="cov19" component={CoV19} />
            <Route path="about" component={About} />
            <Route path="login" component={Login} />
            <Route path="register" component={Register} />
            <Route path="post/:id" let:params >
                <Post id="{params.id}"/>
            </Route>
            <Route path="profile/:id" let:params >
                <Profile id="{params.id}"/>
            </Route>
            <Route path="group/:id" let:params >
                <Group id="{params.id}"/>
            </Route>
            <Route path="/">
                <Home />
            </Route>
        </div>
    </main>
</Router>
