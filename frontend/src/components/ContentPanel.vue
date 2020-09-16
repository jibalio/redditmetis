<template>
    <div class="row">
        <div class="col mpanel round-edge shadow-sm">
            <div class="mpanel-header row">
                <div class="col d-flex justify-content-center">
                    <p>{{title}}</p>
                </div>
            </div>
            <slot></slot>
        </div>
    </div>
</template>

<script>
export default {
    name: "ContentPanel",
    props: ["title"]
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
