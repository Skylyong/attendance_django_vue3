<template>
  <a-layout-header :style="{ background: '#fff', padding: 0 }" />

  <a-layout>
    <a-layout-sider
      :style="{
        overflow: 'auto',
        height: '24vh',
        position: 'fixed',
        left: 0,
        theme: 'dark',
      }"
    >
      <div class="logo" />
      <a-menu>
        <a-menu-item key="1">
          <user-outlined />

          <span class="nav-text" v-on:click="clickAccount"> 账 户 </span>
        </a-menu-item>
        <a-menu-item key="2">
          <upload-outlined />
          <span class="nav-text" v-on:click="apply">提交申请</span>
        </a-menu-item>
        <a-menu-item key="3">
          <bar-chart-outlined />
          <span class="nav-text" v-on:click="applyHistory">申请历史</span>
        </a-menu-item>
        <a-menu-item key="4">
          <bar-chart-outlined />
          <span class="nav-text" v-on:click="accountManager">更改密码</span>
        </a-menu-item>
      </a-menu>
    </a-layout-sider>

    <a-layout :style="{ marginLeft: '200px' }">
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
    <!-- </div> -->
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

    let clickAccount = () => {
      router.push({ path: "/worker/account" });
    };
    let apply = () => {
      router.push({ path: "/worker/apply" });
    };
    let applyHistory = () => {
      router.push({ path: "/worker/applyHistory" });
    };

    let timePool = () => {
      router.push({ path: "/worker/timePool" });
    };

    let accountManager = () => {
      router.push({ path: "/worker/workerAccountChange" });
    }

    return {
      selectedKeys: ref(["2"]),
      clickAccount,
      apply,
      applyHistory,
      timePool,
      accountManager,
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