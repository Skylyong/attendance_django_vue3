<template>
  <a-layout-header :style="{ background: '#fff', padding: 0 }" />
  <a-layout>
    <a-layout-sider
      :style="{
        overflow: 'auto',
        height: '50vh',
        position: 'fixed',
        left: 0,
        theme: 'light',
      }"
    >
      <div class="logo" />
      <a-menu>
        <a-menu-item key="count_message">
          <user-outlined />

          <span class="nav-text" v-on:click="applyApproval">
            待审批
            <a-badge :count="3" dot> </a-badge>
          </span>
        </a-menu-item>
        <a-menu-item key="2">
          <upload-outlined />
          <span class="nav-text" v-on:click="viewTimePool">查看休息池</span>
        </a-menu-item>
        <a-menu-item key="3">
          <bar-chart-outlined />
          <span class="nav-text" v-on:click="workerManager">伙伴管理</span>
        </a-menu-item>
      </a-menu>
    </a-layout-sider>

    <a-layout :style="{ marginLeft: '200px' }">
      <!-- <a-layout-header :style="{ background: '#fff', padding: 0 }" /> -->
      <a-layout-content :style="{ margin: '24px 16px 0', overflow: 'initial' }">
        <div
          :style="{
            padding: '24px',
            background: '#fff',
            textAlign: 'center',
            height: '600pt',
          }"
        >
          <router-view></router-view>
        </div>
      </a-layout-content>
      <a-layout-footer :style="{ textAlign: 'center' }">
        Design ©2022 Created by Leon
      </a-layout-footer>
    </a-layout>
  </a-layout>
</template>
<script>
import { useRouter } from "vue-router";
import {
  UserOutlined,
  VideoCameraOutlined,
  UploadOutlined,
  BarChartOutlined,
  CloudOutlined,
  AppstoreOutlined,
  TeamOutlined,
  ShopOutlined,
} from "@ant-design/icons-vue";
import { defineComponent, ref } from "vue";
import { get_no_history_count } from "../api/api.js";
export default defineComponent({
  components: {
    UserOutlined,
    VideoCameraOutlined,
    UploadOutlined,
    BarChartOutlined,
    CloudOutlined,
    AppstoreOutlined,
    TeamOutlined,
    ShopOutlined,
  },

  setup() {
    let router = useRouter();

    let applyApproval = () => {
      router.push({ path: "/manager/managerApprove" });
    };
    let viewTimePool = () => {
      router.push({ path: "/manager/allWorkerStatisticsData" });
    };
    let workerManager = () => {
      router.push({ path: "/manager/workerAccountManager" });
    };

    return {
      get_no_history_count,
      selectedKeys: ref(["2"]),
      applyApproval,
      viewTimePool,
      workerManager,
    };
  },
});
</script>
<style>
#components-layout-demo-fixed-sider .logo {
  height: 32px;
  background: rgba(255, 255, 255, 0.2);
  margin: 16px;
}
.site-layout .site-layout-background {
  background: #fff;
}

[data-theme="dark"] .site-layout .site-layout-background {
  background: #141414;
}
</style>