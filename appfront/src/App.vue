<template>
  <!-- <login/> -->
  <!-- <about-view/> -->
  <!-- <worker-viem/> -->
  <!-- <manager-approve/> -->
  <router-view></router-view>
  <!-- <temp/> -->
  <!-- <worker-account-manager/>
  <overtime-statistics/> -->
  <!-- <worker-apply/> -->
</template>

<script>
import { defineComponent } from "vue";
// import Login from "./views/login.vue";
// import workerView from "./views/workerHome.vue"
import managerApprove from "./components/manager/managerApprove.vue";
import OvertimeStatistics from "./components/manager/overtimeStatistics.vue";
import WorkerAccountManager from "./components/manager/workerAccountManager.vue";
import WorkerAccount from "./components/worker/workerAccount.vue";
import WorkerApply from "./components/worker/workerApply.vue";
import workerHome from "./views/workerHome.vue"
import managerHome from "./views/managerHome.vue"

export default defineComponent({
  components: {
    managerApprove,
    WorkerAccount,
    WorkerAccountManager,
    workerHome,
    managerHome,
    // workerView,
    // Login,
    OvertimeStatistics,
    WorkerApply  },
});
</script>