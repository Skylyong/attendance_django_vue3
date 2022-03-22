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
      <h1>提交申请</h1>
      <br />
      <br />
      <a-form-item label="申请类型">
        <a-select
          ref="select"
          v-model:value="formState.user.applyType"
          style="width: 180px"
          @change="applyTypeChange"
          :options="options_apply_type"
        >
        </a-select>
      </a-form-item>

      <template v-if="formState.user.applyType == '值班'">
        <a-form-item label="值班日期">
          <a-date-picker
            @ok="onRangeOk"
            @change="onRangeChange"
            v-model:value="formState.user.applyDate"
          />
        </a-form-item>
        <a-form-item label="是否节假  " @click="info">
          <a-radio-group
            v-model:value="formState.user.isHoliday"
            style="margin-right: auto"
          >
            <a-radio :style="radioStyle" :value="1">是</a-radio>
            <a-radio :style="radioStyle" :value="0">否</a-radio>
          </a-radio-group>
        </a-form-item>

        <a-form-item label="值班时长">
          <p style="text-align: left">{{ formState.user.applyTimeLast }}</p>
        </a-form-item>
        <a-form-item label="值班原因">
          <a-textarea
            style="width: 160pt"
            v-model:value="formState.user.applyReason"
            show-count
            :maxlength="50"
          />
        </a-form-item>
      </template>

      <template v-else-if="formState.user.applyType == '加班'">
        <a-form-item label="换算类型">
          <a-radio-group v-model:value="formState.user.conversionType">
            <a-radio :style="radioStyle" :value="1">累加积休</a-radio>
            <a-radio :style="radioStyle" :value="0">加班费</a-radio>
          </a-radio-group>
        </a-form-item>
        <a-form-item label="加班日期">
          <a-range-picker
            style="width: 225px"
            :show-time="{ format: 'HH' }"
            format="YYYY-MM-DD HH"
            :placeholder="['开始时间', '结束时间']"
            @change="onRangeChange"
            @ok="onRangeOk"
          />
        </a-form-item>

        <a-form-item label="加班时长">
          <p style="text-align: left">{{ formState.user.applyTimeLast }}</p>
        </a-form-item>
        <a-form-item label="加班原因">
          <a-textarea
            style="width: 160pt"
            v-model:value="formState.user.applyReason"
            show-count
            :maxlength="50"
          />
        </a-form-item>
      </template>
      <template v-else>
        <a-form-item label="请假时间">
          <a-range-picker
            style="width: 225px"
            :show-time="{ format: 'HH' }"
            format="YYYY-MM-DD HH"
            :placeholder="['开始时间', '结束时间']"
            @change="onRangeChange"
            @ok="onRangeOk"
          />
        </a-form-item>
        <a-form-item label="请假时长">
          <p style="text-align: left">{{ formState.user.applyTimeLast }}</p>
        </a-form-item>
        <a-form-item label="请假原因">
          <a-textarea
            style="width: 160pt"
            v-model:value="formState.user.applyReason"
            show-count
            :maxlength="50"
          />
        </a-form-item>
      </template>
      <br />

      <a-button type="primary" html-type="Submit">提交</a-button>
    </a-form>
  </div>
</template>

<script>
import dayjs from "dayjs";
import { message } from "ant-design-vue";
import { defineComponent, ref, reactive } from "vue";
import moment from "moment";
import { workerApply } from "../../api/api.js";

export default defineComponent({
  setup() {
    const formState = reactive({
      user: {
        applyTimeLast: "",
        applyReason: "",
        applyType: "值班",
        applyDate: "",
        isHoliday: 1,
        conversionType: 1,
      },
    });
    const options_apply_type = ref([
      {
        value: "值班",
        label: "值班",
      },
      {
        value: "加班",
        label: "加班",
      },
      {
        value: "请假",
        label: "请假",
      },
    ]);

    const onRangeChange = (value, dateString) => {
      if (formState.user.applyType == "值班") {
        let week = moment(value).day();
        if (week == 0 || week == 6) {
          formState.user.applyTimeLast = "1.5 天";
        } else {
          formState.user.applyTimeLast = "0.5 天";
        }
      }
    };

    const onRangeOk = (value) => {
      // console.log(value);
      var hour = moment(value[1]).diff(moment(value[0]), "hour");
      var day = moment(value[1]).diff(moment(value[0]), "day");
      hour = hour - day * 24;

      formState.user.applyTimeLast =
        day.toString() + "天" + hour.toString() + "时";
    };

    const applyTypeChange = (value) => {
      formState.user.applyTimeLast = "";
      formState.user.applyReason = "";
    };

    const onFinish = (value) => {
      const dataJson = {};
      if (formState.user.applyTimeLast != "") {
        if (
          formState.user.conversionType == 0 &&
          formState.user.applyReason.length == 0
        ) {
          message.error("请输入加班原因!");
        } else {
          if (formState.user.applyType == "值班") {
            dataJson["applyType"] = formState.user.applyType;
            dataJson["applyDate"] = formState.user.applyDate;
            dataJson["isHoliday"] = formState.user.isHoliday;
            dataJson["applyTimeLast"] = formState.user.applyTimeLast;
            dataJson["applyReason"] = formState.user.applyReason;
          } else if (formState.user.applyType == "加班") {
            dataJson["applyType"] = formState.user.applyType;
            dataJson["conversionType"] = formState.user.conversionType;
            dataJson["applyDate"] = formState.user.applyDate;
            dataJson["applyTimeLast"] = formState.user.applyTimeLast;
            dataJson["applyReason"] = formState.user.applyReason;
          } else {
            dataJson["applyType"] = formState.user.applyType;
            dataJson["applyDate"] = formState.user.applyDate;
            dataJson["applyTimeLast"] = formState.user.applyTimeLast;
            dataJson["applyReason"] = formState.user.applyReason;
          }


      workerApply(
       formState.user
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





        }
      } else {
        message.error("数据录入不完整！");
      }

      // console.log(dataJson);
      // 接下来把dataJson传给后端服务器完成数据提交任务


    };
    return {
      onFinish,
      applyTypeChange,
      onRangeChange,
      onRangeOk,
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