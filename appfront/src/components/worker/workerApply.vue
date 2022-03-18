<template>
  <br />
  <br />
  <h1 style="text-align: center">提交申请</h1>
  <br />
  <br />
  <a-form
    :model="formState"
    v-bind="layout"
    name="nest-messages"
    :validate-messages="validateMessages"
    @finish="onFinish"
    style="text-align: center"
  >
    <a-form-item
      :name="['user', 'email']"
      label="申请类型"
      :rules="[{ required: false }]"
    >
      <a-select
        ref="select"
        v-model:value="value1"
        style="width: 120px"
        :options="options1"
        @focus="focus"
        @change="handleApplyTypeChange"
      ></a-select>
    </a-form-item>

    <a-form-item
      :name="['user', 'email']"
      label="假期种类"
      :rules="[{ required: false }]"
    >
      <a-select
        ref="select"
        v-model:value="value2"
        style="width: 120px"
        :options="options2"
        @focus="focus"
        @change="handleHolidayTypeChange"
      ></a-select>
    </a-form-item>

    <a-form-item
      :name="['user', 'name']"
      label="申请时间"
      :rules="[{ required: false }]"
    >
      <a-space direction="vertical" :size="8">
        <a-range-picker
          style="width: 225px"
          :show-time="{ format: 'HH' }"
          format="YYYY-MM-DD HH"
          :placeholder="['开始时间', '结束时间']"
          @change="onRangeChange"
          @ok="onRangeOk"
        />
      </a-space>
    </a-form-item>

    <a-form-item :name="['user', 'email']" label="申请时长" :rules="[{}]">
      <p class="ant-form-text">{{ formState.user.applyTime }}</p>
    </a-form-item>

    <a-form-item
      :name="['user', 'email']"
      label="申请原因"
      :rules="[{ required: false }]"
    >
      <a-input
        style="height: 50px; width: 220px"
        v-model:value="formState.user.applyReason"
      />
    </a-form-item>

    <a-form-item :wrapper-col="{ ...layout.wrapperCol, offset: 8 }">
      <br />
      <a-button type="primary" html-type="Submit">提交</a-button>
    </a-form-item>
  </a-form>
</template>
<script>
import { workerApply } from "../../api/api.js";
import moment from "moment";
import { defineComponent, reactive, ref } from "vue";
import { message } from "ant-design-vue";

export default defineComponent({
  setup() {
    let submit_message = ref("");
    let applyType = ref();
    let holidayType = ref();
    let myDateString = ref();
    let myData = ref();
    applyType = 0;
    holidayType = 0;
    const layout = {
      labelCol: {
        span: 8,
      },
      wrapperCol: {
        span: 9,
      },
    };
    const validateMessages = {
      required: "${label} is required!",
      types: {
        email: "${label} is not a valid email!",
        number: "${label} is not a valid number!",
      },
      number: {
        range: "${label} must be between ${min} and ${max}",
      },
    };

    const onRangeChange = (value, dateString) => {
      console.log("Selected Time: ", value);
      console.log("Formatted Selected Time: ", dateString);
      myDateString = dateString;
      myData = value;
    };

    const onRangeOk = (value) => {
      var hour = moment(myData[1]).diff(moment(myData[0]), "hour");
      var day = moment(myData[1]).diff(moment(myData[0]), "day");
      hour = hour - day * 24;
      console.log("hour", hour, "day", day);

      formState.user.applyTime = day.toString() + "天" + hour.toString() + "时";
      console.log("onOk: ", value);
    };

    const options1 = ref([
      {
        value: "0",
        label: "公休",
      },
      {
        value: "1",
        label: "值班加班",
      },
    ]);

    const options2 = ref([
      {
        value: "0",
        label: "公休请假",
      },
      {
        value: "1",
        label: "加班换积休",
      },
      {
        value: "2",
        label: "加班换公休",
      },
    ]);

    const focus = () => {
      // console.log('2222focus');
    };

    const handleChange = (value) => {
      // console.log(`1111selected ${value}`);
    };
    const handleApplyTypeChange = (value) => {
      applyType = value;
    };
    const handleHolidayTypeChange = (value) => {
      holidayType = value;
    };

    const formState = reactive({
      user: {
        applyTime: "",
        applyReason: "",
      },
    });

    const onFinish = () => {
      console.log(
        "Success:",
        applyType,
        holidayType,
        formState.user.applyTime,
        formState.user.applyReason,
        myDateString
      );
      let userid = localStorage.getItem("Userid");

      workerApply(
        userid,
        applyType,
        holidayType,
        formState.user.applyTime,
        formState.user.applyReason,
        myDateString
      ).then(
        (response) => {
          if (response["code"] == 1) {
            message.success("提交成功");
          } else {
            message.error("提交失败");
          }
        },
        (response) => {
          message.error("提交提交失败，服务器访问错误！");
        }
      );
    };

    return {
      holidayType,
      applyType,
      handleApplyTypeChange,
      handleHolidayTypeChange,
      formState,
      onFinish,
      layout,
      validateMessages,
      onRangeChange,
      onRangeOk,
      myDateString,
      myData,
      focus,
      handleChange,
      value1: ref("公休"),
      options1,
      value2: ref("公休请假"),
      options2,
      submit_message,
    };
  },
});
</script>
