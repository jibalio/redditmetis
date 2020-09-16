<template>

<div class="col-md-6 col-sm-6 col-6 statistic-container">
      <div>
          <div class="row"><div class="col-12 d-flex justify-content-center"><p class="stat-num">{{ value }}</p></div></div>
          <div class="row"><div class="col-12 d-flex justify-content-center"><p class="sublabel">{{ m_key }}</p></div></div> 
      </div>
  </div>
</template>
<script>

import Constants from "@/assets/js/config/Constants.js";
export default {
    name: "StatContainer",
    props: ["m_key", "value"],
    data: function() {
        return {
            Constants,
        };
    }
};
</script>

<style>

</style>