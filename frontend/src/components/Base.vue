<template>
    <Banner></Banner>
</template>

<script>
import Banner from './Banner.vue'
export default {
  name: 'Base',
  props: {
    msg: String
  },
  components: {
      Banner,
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
