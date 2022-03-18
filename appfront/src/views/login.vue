<template>
  <a-form
    style="text-align: center; vertical-align: middle"
    :model="formState"
    name="normal_login"
    class="login-form"
    @finish="onFinish"
    @finishFailed="onFinishFailed"
  >
    <br />
    <br />
    <br />
    <h1>欢迎登录考勤系统</h1>
    <br />
    <a-form-item
      label="用户名"
      style="width: 300px; display: inline-flex"
      name="username"
      :rules="[{ required: true, message: '请输入用户名!' }]"
    >
      <a-input v-model:value="formState.username">
        <template #prefix>
          <UserOutlined class="site-form-item-icon" />
        </template>
      </a-input>
    </a-form-item>
    <br />
    <a-form-item
      style="width: 300px; display: inline-flex"
      label="密 &nbsp  码"
      name="password"
      :rules="[{ required: true, message: '请输入密码！' }]"
    >
      <a-input-password v-model:value="formState.password">
        <template #prefix>
          <LockOutlined class="site-form-item-icon" />
        </template>
      </a-input-password>
    </a-form-item>

    <div class="login-form-wrap">
      <a-form-item name="remember" no-style>
        <a-checkbox v-model:checked="formState.remember">记住我</a-checkbox>
      </a-form-item>
      <a class="login-form-forgot" href="">忘记密码</a>
    </div>

    <a-form-item>
      <a-button
        :disabled="disabled"
        type="primary"
        html-type="submit"
        class="login-form-button"
      >
        登 录
      </a-button>
    </a-form-item>
  </a-form>
</template>
<script>
import { defineComponent, reactive, computed, ref } from "vue";
import { UserOutlined, LockOutlined } from "@ant-design/icons-vue";
// import router from '@/router';
import { useRouter } from "vue-router";
import { postSubmit } from "../api/api.js";
import { useStore } from "vuex";
import { message } from "ant-design-vue";

export default defineComponent({
  components: {
    UserOutlined,
    LockOutlined,
  },

  setup() {
    const store = useStore();
    localStorage.setItem("Flag", "noLogin");
    let router = useRouter();
    const formState = reactive({
      username: "",
      password: "",
      remember: true,
    });
    var that = this;
    const onFinish = (values) => {
      postSubmit(values.username, values.password).then(
        // console.log(response),
        (response) => {
          // this.message = ''
          console.log(response);
          if (response["code"] == 1) {
            localStorage.setItem("Userid", response["data"]["userId"]);
            localStorage.setItem("Flag", "isLogin");
            localStorage.setItem("userType", response["data"]["accountType"]);
            store.dispatch("setUser", true);

            if (response["data"]["accountType"] == 2) {
              router.push({ path: "/manager/managerApprove" });
            } else {
              router.push({ path: "/worker/account" });
            }
          } else if (response["code"] == 2004) {
            message.error("找不到该用户！");
          } else {
            message.error("密码错误!");
          }
        },
        (response) => {
          message.error("服务器访问错误!");
        }
      );
    };

    const onFinishFailed = (errorInfo) => {
      console.log("Failed:", errorInfo);
    };

    const disabled = computed(() => {
      return !(formState.username && formState.password);
    });
    return {
      formState,
      onFinish,
      onFinishFailed,
      disabled,
      message,
    };
  },
});
</script>
<style>
#components-form-demo-normal-login .login-form {
  max-width: 300px;
}
#components-form-demo-normal-login .login-form-wrap {
  display: flex;
  text-align: center;
  align-items: center;
  justify-content: space-between;
}
#components-form-demo-normal-login .login-form-forgot {
  margin-bottom: 24px;
}
#components-form-demo-normal-login .login-form-button {
  width: 100%;
}
</style>
