<template>
  <!-- <login/> -->
  <!-- <about-view/> -->
  <!-- <worker-viem/> -->
  <!-- <manager-approve/> -->
  <router-view></router-view>
</template>

<script>
import { defineComponent } from "vue";
// import Login from "./views/login.vue";
// import workerView from "./views/workerHome.vue"
import managerApprove from "./components/manager/managerApprove.vue";

export default defineComponent({
  components: {
    managerApprove,
    // workerView,
    // Login,
  },
});
</script>