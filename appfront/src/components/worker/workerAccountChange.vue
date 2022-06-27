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
    >
      <br />
      <br />
      <h1>更改密码</h1>
      <br />
      <br />

           <a-form-item label="原始密码">
        <a-input-password v-model:value="formState.key0">
          <template #prefix>
            <LockOutlined class="site-form-item-icon" />
          </template>
        </a-input-password>
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
        >确定</a-button
      >
    </a-form>
  </div>
</template>

<script>
import dayjs from "dayjs";
import { message } from "ant-design-vue";
import { defineComponent, ref, reactive } from "vue";
import moment from "moment";
import { resetPwdWork } from "../../api/api.js";
import md5 from "js-md5";
import { JSEncrypt } from "jsencrypt";
import { useStore } from "vuex";



export default defineComponent({
  setup() {
    const store = useStore();
    const formState = reactive({
        key0: "",
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

    let userid = localStorage.getItem("Userid");


    const handleOk = () => {
    console.log('formState.key0',formState.key0)
      if (formState.key1 == formState.key2 &&  formState.key1 != '' && formState.key2 !='') {
        formState.key1 = md5(formState.key1);
        formState.key1 = getCode(formState.key1);
        formState.key2 = md5(formState.key2);
        formState.key2 = getCode(formState.key2);
        formState.key0 = md5(formState.key0);
        formState.key0 = getCode(formState.key0);
        

        resetPwdWork(formState.key1, userid, formState.key0).then(
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
      handleOk,
      formState,
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