<template>
  <!-- 管理用户账户，账户添加、删除、密码重置、用户信息修改等 -->

  <!-- <h1>伙伴管理，待开发</h1> -->

  <div>
    <a-form
      :model="formState"
      v-bind="layout"
      class="center"
      name="nest-messages"
      :validate-messages="validateMessages"
      @finish="onFinish"
    >
      <br />
      <br />
      <h1>修改密码</h1>
      <br />
      <br />
      <a-form-item label="选择账号">
        <a-select
          ref="select"
          v-model:value="formState.userId"
          style="width: 225px"
          :options="options_apply_type.data"
        >
        </a-select>
      </a-form-item>

      <a-form-item label="输入密码">
        <a-input-password v-model:value="formState.key1">
          <template #prefix>
            <LockOutlined class="site-form-item-icon" />
          </template>
        </a-input-password>
      </a-form-item>

      <a-form-item label="确认密码">
        <a-input-password v-model:value="formState.key2">
          <template #prefix>
            <LockOutlined class="site-form-item-icon" />
          </template>
        </a-input-password>
      </a-form-item>

      <a-button type="primary" html-type="Submit" @click="handleOk"
        >重置</a-button
      >
    </a-form>
  </div>
</template>

<script>
import dayjs from "dayjs";
import { message } from "ant-design-vue";
import { defineComponent, ref, reactive } from "vue";
import moment from "moment";
import { resetPwd, getWorkerId } from "../../api/api.js";
import md5 from "js-md5";
import { JSEncrypt } from "jsencrypt";
import { useStore } from "vuex";



export default defineComponent({
  setup() {
    const store = useStore();
    const formState = reactive({
      key1: "",
      key2: "",
      userId: "",
    });

    function getCode(password) {
      let encrypt = new JSEncrypt();
      // console.log('store.state.pubkey:',store.state.pubkey)
      encrypt.setPublicKey(store.state.pubkey);
      let data = encrypt.encrypt(password);
      return data;
    }

    let options_apply_type = ref({'data': ''});
    let userid = localStorage.getItem("Userid");
    getWorkerId(userid).then((response) => {
      if (response["code"] == 1) {
        // console.log(response["data"]);
        options_apply_type.value = {'data':response["data"]};
        // console.log(options_apply_type);
      } else {
        message.error("获取员工工号失败");
      }
    });

    const handleOk = () => {
      if (formState.key1 == formState.key2) {
        formState.key1 = md5(formState.key1);
        formState.key1 = getCode(formState.key1);
        formState.key2 = md5(formState.key2);
        formState.key2 = getCode(formState.key2);

        console.log(formState.userId)
        resetPwd(formState.key1, formState.userId).then(
          (response) => {
            if (response["code"] == 1) {
              message.success("重置密码成功");
            } else {
              message.error("重置密码失败");
            }
          },
          (response) => {
            message.error("重置密码失败");
          }
        );
      } else {
        message.error("两次输入不一致");
      }
    };
    return {
      getWorkerId,
      handleOk,
      formState,
      options_apply_type,
    };
  },
});
</script>

 <style scoped>
.center {
  text-align: center;
  margin: 0 auto;
  width: 300px;
}
</style>>