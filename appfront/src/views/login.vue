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
      <!-- <a class="login-form-forgot" href="">忘记密码</a> -->
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

  <template>
    <div>
      <a-modal
        v-model:visible="visible"
        title="您首次登录系统，请设置新密码!"
        @ok="handleOk"
      >
        <a-form
          :model="formState"
          v-bind="layout"
          class="center"
          name="nest-messages"
          :validate-messages="validateMessages"
        >
          <a-form-item
            style="width: 300px; display: inline-flex"
            label="输入密码"
            name="password"
            :rules="[{ required: true, message: '' }]"
          >
            <a-input-password v-model:value="formState.key1">
              <template #prefix>
                <LockOutlined class="site-form-item-icon" />
              </template>
            </a-input-password>
          </a-form-item>

          <a-form-item
            style="width: 300px; display: inline-flex"
            label="确认密码"
            name="password"
            :rules="[{ required: true, message: '' }]"
          >
            <a-input-password v-model:value="formState.key2">
              <template #prefix>
                <LockOutlined class="site-form-item-icon" />
              </template>
            </a-input-password>
          </a-form-item>
        </a-form>

        <template #footer>
          <a-button key="return" @click="handleCancel">取消</a-button>
          <a-button key="submin" type="primary" @click="handleOk"
            >确定</a-button
          >
        </template>
      </a-modal>
    </div>
  </template>
</template>

<script>
import { defineComponent, reactive, computed, ref } from "vue";
import { UserOutlined, LockOutlined } from "@ant-design/icons-vue";
// import {getCode} from '../assets/js/jsencryptKey'
// import router from '@/router';
import { JSEncrypt } from "jsencrypt";
import { useRouter } from "vue-router";
import { postSubmit, resetPwd } from "../api/api.js";
import { useStore } from "vuex";
import { message } from "ant-design-vue";
import md5 from "js-md5";

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
      key1: "",
      key2: "",
    });

    function getCode(password) {
      let encrypt = new JSEncrypt();
      // console.log('store.state.pubkey:',store.state.pubkey)
      encrypt.setPublicKey(store.state.pubkey);
      let data = encrypt.encrypt(password);
      return data;
    }
    var that = this; //827ccb0eea8a706c4c34a16891f84e7b
    const resetPassword = true; // 是否弹出重置初始密码窗口
    const onFinish = (values) => {
      let temp_password = values.password;
      values.password = md5(values.password);
      values.password = getCode(values.password);
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
            console.log("temp_password:", temp_password);
            if (temp_password == "12345678" && resetPassword) {
              showModal();
            } 
            else {
              if (visible.value == false) {
                if (response["data"]["accountType"] == 2) {
                  router.push({ path: "/manager/managerApprove" });
                } else {
                  router.push({ path: "/worker/account" });
                }
              }
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

    const visible = ref(false);

    const showModal = () => {
      visible.value = true;
    };

    const handleOk = () => {
      if (formState.key1 != "12345678" && formState.key1 == formState.key2) {
        let userid = localStorage.getItem("Userid");

        formState.key1 = md5(formState.key1);
        formState.key1 = getCode(formState.key1);
        formState.key2 = md5(formState.key2);
        formState.key2 = getCode(formState.key2);

        resetPwd(formState.key1, userid).then(
          (response) => {
            if (response["code"] == 1) {
              message.success("重置密码成功");
              visible.value = false;
            } else {
              message.error("重置密码失败");
            }
          },
          (response) => {
            message.error("重置密码失败");
          }
        );
      } else {
        message.error("两次输入不一致或密码等于初始密码");
      }
    };

    const handleCancel = () => {
      visible.value = false;
    };

    return {
      visible,
      showModal,
      handleOk,
      handleCancel,
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
