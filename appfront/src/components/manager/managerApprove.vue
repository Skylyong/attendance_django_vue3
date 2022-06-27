<template>
  <a-table bordered :data-source="dataSource" :columns="columns">
    <template #operation="{ record }">
      <template v-if="record.approveState != '作废'">
        <a @click="clickApply(record)">审批</a>
      </template>
    </template>
  </a-table>
  <template>
    <div>
      <a-modal
        v-model:visible="visible"
        title="请审批..."
        width="400pt"
        :footer="null"
      >
        <a-form
          :model="formState"
          v-bind="layout"
          class="center"
          name="nest-messages"
          :validate-messages="validateMessages"
          @finish="onFinish"
        >
          <a-row :gutter="20">
            <a-col :span="10">
              <a-form-item
                style="width: 300px; display: inline-flex"
                label="工 &nbsp &nbsp  &nbsp 号"
              >
                {{ formState.userId }}
              </a-form-item>
            </a-col>

            <a-col :span="10">
              <a-form-item
                style="width: 300px; display: inline-flex"
                label="姓 &nbsp &nbsp  &nbsp  名"
              >
                {{ formState.name }}
              </a-form-item>
            </a-col>
          </a-row>

          <a-row :gutter="20">
            <a-col :span="10">
              <a-form-item
                style="width: 300px; display: inline-flex"
                label="开始时间"
              >
                {{ formState.applyStartTime }}
              </a-form-item>
            </a-col>
            <a-col :span="10">
              <a-form-item
                style="width: 300px; display: inline-flex"
                label="结束时间"
              >
                {{ formState.applyEndTime }}
              </a-form-item>
            </a-col>
          </a-row>
          <a-row :gutter="20">
            <a-col :span="10">
              <a-form-item
                style="width: 300px; display: inline-flex"
                label="申请时长"
              >
                {{ formState.applyTimeLast }}
              </a-form-item>
            </a-col>

            <a-col :span="10">
              <a-form-item
                style="width: 300px; display: inline-flex"
                label="申请类型"
              >
                {{ formState.applyType }}
              </a-form-item>
            </a-col>
          </a-row>
          <a-row :gutter="20">
            <a-col :span="10">
              <a-form-item
                style="width: 300px; display: inline-flex"
                label="是否节假"
              >
                {{ formState.isHoliday }}
              </a-form-item>
            </a-col>
            <a-col :span="10">
              <a-form-item
                style="width: 300px; display: inline-flex"
                label="换算类型"
              >
                {{ formState.conversionType }}
              </a-form-item>
            </a-col>
          </a-row>
          <a-form-item
            style="width: 300px; display: inline-flex"
            label="申请原因"
          >
            {{ formState.applyReason }}
          </a-form-item>

          <a-form-item
            style="width: 300px; display: inline-flex"
            label="当前状态"
          >
            {{ formState.approveState }}
          </a-form-item>

          <a-row>
            <a-form-item
              style="width: 300px; display: inline-flex"
              label="填写批注"
            >
              <a-textarea
                v-model:value="approveNote"
                show-count
                :maxlength="100"
              />
            </a-form-item>
          </a-row>
          <a-row>
            <a-form-item
              style="width: 300px; display: inline-flex"
              label="审批结果"
            >
              <a-radio-group
                v-model:value="approveResult"
                style="margin-right: auto"
              >
                <template v-if="formState.approveState == '未审批'">
                  <a-radio :value="2">通过</a-radio>
                  <a-radio :value="1">驳回</a-radio>
                </template>

                <template v-if="formState.approveState == '驳回'">
                  <a-radio :value="2">通过</a-radio>
                </template>

                <template v-if="formState.approveState == '通过'">
                  <a-radio :value="0">作废</a-radio>
                </template>
              </a-radio-group>
            </a-form-item>
          </a-row>

          <a-form-item
            :wrapper-col="{
              xs: { span: 24, offset: 0 },
              sm: { span: 16, offset: 8 },
            }"
          >
            <a-button type="primary" html-type="submit">提交</a-button>
          </a-form-item>
        </a-form>
      </a-modal>
    </div>
  </template>
</template>
<script>
import {
  getworkerApplyHistory,
  submitApplication,
  cancellation,
} from "../../api/api.js";
import { computed, defineComponent, reactive, ref } from "vue";
import { CheckOutlined, EditOutlined } from "@ant-design/icons-vue";
import { cloneDeep } from "lodash-es";
import { message } from "ant-design-vue";
export default defineComponent({
  components: {
    CheckOutlined,
    EditOutlined,
  },

  setup() {
    const columns = [
      {
        title: "工号",
        dataIndex: "userId",
        width: "15%",
        // sorter: (a, b) => a.length- b.length,
        key: "userId",
      },
      {
        title: "姓名",
        dataIndex: "name",
        width: "15%",
        key: "name",

        // sorter: (a, b) => a.length - b.length,
      },

      {
        title: "开始时间",
        dataIndex: "applyStartTime",
        // sorter: true,
        width: "15%",
        // sorter: (a, b) => a.applyStartTime - b.applyStartTime,
      },
      {
        title: "结束时间",
        dataIndex: "applyEndTime",
        // sorter: true,
        width: "15%",
        // sorter: (a, b) => a.applyEndTime - b.applyEndTime,
      },

      {
        title: "申请时长",
        dataIndex: "applyTimeLast",
        width: "15%",
      },
      // {
      //   title: "申请类型",
      //   dataIndex: "applyType",
      // filters: [{
      //   text: '公休',
      //   value: '公休',
      // }, {
      //   text: '值班加班',
      //   value: '值班加班',
      // }
      // ],
      // onFilter: (value, record) => record.applyType.indexOf(value) === 0,
      // sorter: (a, b) => a.applyType.length - b.applyType.length,
      //   width: "5%",
      // },
      // {
      //   title: "是否节假",
      //   dataIndex: "isHoliday",
      //   width: "5%",
      // },
      // {
      //   title: "换算类型",
      //   dataIndex: "conversionType",
      //   width: "5%",
      // },
      // ,
      // {
      //   title: "申请原因",
      //   dataIndex: "applyReason",
      //   width: "20%",
      // sorter: (a, b) => a.applyReason.length - b.applyReason.length,
      // },
      // {
      //   title: "填写批注",
      //   dataIndex: "approveNote",
      //   // sorter: true,
      //   width: "20%",
      //   slots: {
      //     customRender: "approveNote",
      //   },
      // },
      {
        title: "状态",
        dataIndex: "approveState", //approveState
        // sorter: (a, b) => a.approveState.length - b.approveState.length,
        // onFilter: (value, record) => record.approveState.indexOf(value) === 0,
        width: "10%",
        onFilter: (value, record) => record.approveState.indexOf(value) === 0,

        filters: [
          {
            text: "未审批",
            value: "未审批",
          },
          {
            text: "通过",
            value: "通过",
          },
          {
            text: "驳回",
            value: "驳回",
          },
          {
            text: "作废",
            value: "作废",
          },
        ],

        // slots: {
        //   customRender: "approveState",
        // },
      },

      {
        title: "点击审批",
        width: "30%",
        dataIndex: "operation",
        slots: {
          customRender: "operation",
        },
      },
    ];

    const dataSource = ref();
    let getid = localStorage.getItem("Userid");

    getworkerApplyHistory(getid, 0).then((response) => {
      // message.success(getid+'aaaaa:'+response['code'])
      if (response["code"] == 1) {
        dataSource.value = response["data"];
        console.log(response["data"]);
      }
    });
    // const count = computed(() => dataSource.value.length + 1);

    let visible = ref(false);

    let formState = ref({
      userId: "",
      name: "",
      applyStartTime: "",
      applyEndTime: "",
      applyTimeLast: "",
      applyType: "",
      isHoliday: "",
      conversionType: "",
      applyReason: "",
      approveState: "",
    });

    let approveNote = ref("");
    let approveResult = ref(-1);
    let approveId = ref();
    const onFinish = () => {
      if (approveResult.value === -1) {
        message.error("请选择审批结果");
      } else {
        if (approveResult.value === 0) {
          cancellation(getid, approveId.value).then((response) => {
            if (response["code"] == 1) {
              getworkerApplyHistory(getid, 0).then((response) => {
                if (response["code"] == 1) {
                  dataSource.value = response["data"];
                } else {
                  dataSource.value = "";
                }
              });

              message.success("作废操作成功！");
            } else {
              message.error("作废操作失败！");
            }
          });
        } else {
          submitApplication(
            getid,
            approveId.value,
            approveResult.value,
            approveNote.value
          ).then((response) => {
            if (response["code"] == 1) {
              message.success("提交成功！");
              getworkerApplyHistory(getid, 0).then((response) => {
                if (response["code"] == 1) {
                  dataSource.value = response["data"];
                } else {
                  dataSource.value = "";
                }
              });
            } else {
              message.error("提交失败！");
            }
          });
        }
        visible.value = false;
        approveResult.value = -1;
      }
    };

    const clickApply = (record) => {
      formState.value = {
        userId: record.userId,
        name: record.name,
        applyStartTime: record.applyStartTime,
        applyEndTime: record.applyEndTime,
        applyTimeLast: record.applyTimeLast,
        applyType: record.applyType,
        isHoliday: record.isHoliday,
        conversionType: record.conversionType,
        applyReason: record.applyReason,
        approveState: record.approveState,
      };

      approveId.value = record.id;
      visible.value = true;

      // console.log("clickApply", record);
      //  visible.value = true;
    };

    return {
      clickApply,
      approveId,
      approveResult,
      approveNote,
      onFinish,
      formState,
      visible,
      getworkerApplyHistory,
      // options,
      columns,
      dataSource,
      // editableData,
      // count,
      // edit,
      // save,
      // save_server,
    };
  },
});
</script>
<style lang="less">
.editable-cell {
  position: relative;
  .editable-cell-input-wrapper,
  .editable-cell-text-wrapper {
    padding-right: 24px;
  }

  .editable-cell-text-wrapper {
    padding: 5px 24px 5px 5px;
  }

  .editable-cell-icon,
  .editable-cell-icon-check {
    position: absolute;
    right: 0;
    width: 20px;
    cursor: pointer;
  }

  .editable-cell-icon {
    margin-top: 4px;
    display: none;
  }

  .editable-cell-icon-check {
    line-height: 28px;
  }

  .editable-cell-icon:hover,
  .editable-cell-icon-check:hover {
    color: #108ee9;
  }

  .editable-add-btn {
    margin-bottom: 8px;
  }
}
.editable-cell:hover .editable-cell-icon {
  display: inline-block;
}
</style>