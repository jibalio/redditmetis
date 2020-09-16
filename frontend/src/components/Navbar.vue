<template>
    <div>
        <nav class="navbar navbar-expand-md navbar-light" id="navbars" style="padding-left:0">
            <div class="col d-flex justify-content-start align-items-center">
                <div v-b-toggle.collapse-1 v-if="!search && isMobile()"  variant="primary" class="menu-btn">
                    <svg color="white" class="bi bi-list" width="1em" height="1em" viewBox="0 0 16 16" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                        <path fill-rule="evenodd" d="M2.5 11.5A.5.5 0 013 11h10a.5.5 0 010 1H3a.5.5 0 01-.5-.5zm0-4A.5.5 0 013 7h10a.5.5 0 010 1H3a.5.5 0 01-.5-.5zm0-4A.5.5 0 013 3h10a.5.5 0 010 1H3a.5.5 0 01-.5-.5z" clip-rule="evenodd"/>
                    </svg>
                </div>
                <a v-if="!search" href="/" class="disable-link-underline ml-2"><div><p class="metis-brand"><span style="color: rgb(195, 255, 231);">Reddit</span><span style="color:white">Metis</span></p></div></a>
                
                <div v-if="search && isMobile()" class="col-md-2 col-lg-2 col-12 d-flex justify-content-start align-items-center" style="padding-left:0;padding-right:0;">
                    <div class="d-flex" tabindex="0" style="width: 100%;">
                        <div class="input-group-prepend">
                            <span id="basic-addon3" class="input-group-text round-edge-left">u/</span>
                        </div>
                        <input v-model="searchBoxText" v-on:keyup.enter="searchUser()" type="text" id="input_username" aria-describedby="basic-addon3" placeholder="Username" class="form-control round-edge-right" 
                        style="height: calc(1.4em + 0.75rem + 2px);border:none;font-family: 'Nunito', Tahoma, Geneva, Verdana, sans-serif;
                        font-size: 0.9rem;
                        color: #353535;
                        margin: 0 0 0 0;">
                        </div>
                    </div>
                
                    
            
            </div>
            <div @click="search=!search" v-if="isMobile()">
                <svg v-if="!search" color="white" class="bi bi-search" width="1em" height="1em" viewBox="0 0 16 16" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                    <path fill-rule="evenodd" d="M10.442 10.442a1 1 0 011.415 0l3.85 3.85a1 1 0 01-1.414 1.415l-3.85-3.85a1 1 0 010-1.415z" clip-rule="evenodd"/>
                    <path fill-rule="evenodd" d="M6.5 12a5.5 5.5 0 100-11 5.5 5.5 0 000 11zM13 6.5a6.5 6.5 0 11-13 0 6.5 6.5 0 0113 0z" clip-rule="evenodd"/>
                </svg>
                <svg v-if="search" color="white" class="bi bi-x-square" width="1em" height="1em" viewBox="0 0 16 16" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                    <path fill-rule="evenodd" d="M14 1H2a1 1 0 00-1 1v12a1 1 0 001 1h12a1 1 0 001-1V2a1 1 0 00-1-1zM2 0a2 2 0 00-2 2v12a2 2 0 002 2h12a2 2 0 002-2V2a2 2 0 00-2-2H2z" clip-rule="evenodd"/>
                    <path fill-rule="evenodd" d="M11.854 4.146a.5.5 0 010 .708l-7 7a.5.5 0 01-.708-.708l7-7a.5.5 0 01.708 0z" clip-rule="evenodd"/>
                    <path fill-rule="evenodd" d="M4.146 4.146a.5.5 0 000 .708l7 7a.5.5 0 00.708-.708l-7-7a.5.5 0 00-.708 0z" clip-rule="evenodd"/>
                </svg>
            </div>
            <b-collapse v-if="isMobile()" id="collapse-1" class="collapse navbar-collapse">
                    <ul class="navbar-nav ml-auto mt-2 mt-lg-0">
                        <li class="nav-item ml-1">
                            <p><a class="nav-link" href="/">Home</a></p>
                        </li>
                        <li class="nav-item">
                            <p><a class="nav-link ml-1" href="/about">About</a></p>
                        </li>
                        <li class="nav-item ml-1">
                            <p><a class="nav-link" href="/faq">FAQ</a></p>
                        </li>
                        <li class="nav-item ml-1">
                            <p><a class="nav-link" href="/donate">Donate</a></p>
                        </li>
                        <li class="nav-item ml-1">
                            <p><a class="nav-link" href="https://reddit.com/r/RedditMetis">r/RedditMetis on Reddit</a></p>
                        </li>
                    </ul>
                </b-collapse>
            <div v-if="!isMobile()" id="collapse-1" class="collapse navbar-collapse">
                <ul class="navbar-nav ml-auto mt-2 mt-lg-0">
                    <li class="nav-item ml-1">
                        <p><a class="nav-link" href="/">Home</a></p>
                    </li>
                    <li class="nav-item">
                        <p><a class="nav-link ml-1" href="/about">About</a></p>
                    </li>
                    <li class="nav-item ml-1">
                        <p><a class="nav-link" href="/faq">FAQ</a></p>
                    </li>
                    <li class="nav-item ml-1">
                        <p><a class="nav-link" href="/donate">Donate</a></p>
                    </li>
                    <li class="nav-item ml-1">
                        <p><a class="nav-link" href="https://reddit.com/r/RedditMetis">r/RedditMetis on Reddit</a></p>
                    </li>
                </ul>
            </div>
            <div v-if="!isMobile()" class="col-md-2 col-lg-2 col-12 d-flex justify-content-start align-items-center" style="padding-left:0;padding-right:0;">
                <div class="d-flex" tabindex="0" style="width: 100%;">
                    <div class="input-group-prepend">
                        <span id="basic-addon3" class="input-group-text round-edge-left">u/</span>
                    </div>
                    <input v-model="searchBoxText" v-on:keyup.enter="searchUser()" type="text" id="input_username" aria-describedby="basic-addon3" placeholder="Username" class="form-control round-edge-right" 
                    style="height: calc(1.4em + 0.75rem + 2px);border:none;font-family: 'Nunito', Tahoma, Geneva, Verdana, sans-serif;
                    font-size: 0.9rem;
                    color: #353535;
                    margin: 0 0 0 0;">
                </div>
            </div>
            <!--<button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarTogglerDemo02" aria-controls="navbarTogglerDemo02" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>-->

            
            </nav>
    </div>
</template>
<style scoped>
#navbars {
    background-image: linear-gradient(120deg,#86f2be 0,#8ddae7 100%);
}

#collapse-1 p a {
    color:white;
}

::placeholder {
  opacity: 0.5; /* Firefox */
}

input::-webkit-input-placeholder{
    opacity: 0.5
}
input:-moz-placeholder {
    opacity: 0.5
}

.input-group-text { 
    background-color: #f3f3f3;
    color: #bdacac;
    border: none;
    font-size: 0.7rem;
    font-weight: 600;
    line-height: 1;
}

input:focus,
select:focus,
textarea:focus,
button:focus {
    outline: none;
}

[contenteditable="true"]:focus {
    outline: none;
}

*:focus {
    outline: none;
}

</style>
<script>

export default {
    name: "Navbar",
    data: function() {
        return {
            searchBoxText: "",
            search: false,
        };
    },
    methods: {
        searchUser() {
            this.$router.push({name:"userpage",params:{
                uname: this.searchBoxText.trim() 
            }});
        },
        isMobile() {
            if(/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
                return true;
            } else {
                return false;
            }
        }
    }
};
</script>
