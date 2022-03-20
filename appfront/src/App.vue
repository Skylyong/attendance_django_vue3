<template>
  <!-- <login/> -->
  <!-- <about-view/> -->
  <!-- <worker-viem/> -->
  <!-- <manager-approve/> -->
  <!-- <router-view></router-view> -->
  <!-- <temp/> -->
  <worker-account-manager/>
</template>

<script>
import { defineComponent } from "vue";
// import Login from "./views/login.vue";
// import workerView from "./views/workerHome.vue"
import managerApprove from "./components/manager/managerApprove.vue";
import WorkerAccountManager from "./components/manager/workerAccountManager.vue";
import WorkerAccount from "./components/worker/workerAccount.vue";

export default defineComponent({
  components: {
    managerApprove,
    WorkerAccount,
    WorkerAccountManager,
    // workerView,
    // Login,
  },
});
</script>