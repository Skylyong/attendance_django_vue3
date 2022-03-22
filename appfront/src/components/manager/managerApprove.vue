<template>
  <a-table bordered :data-source="dataSource" :columns="columns">
    <template #approveNote="{ text, record }">
      <div class="editable-cell">
        <div v-if="editableData[record.id]" class="editable-cell-input-wrapper">
          <a-input
            v-model:value="editableData[record.id].approveNote"
            @pressEnter="save(record.id)"
          />
        </div>
        <div v-else class="editable-cell-text-wrapper">
          {{ text || " " }}
          <edit-outlined class="editable-cell-icon" @click="edit(record.id)" />
        </div>
      </div>
    </template>


    <template #approveState="{ record }">
      <div class="editable-cell">
        <div v-if="editableData[record.id]" class="editable-cell-input-wrapper">
          <a-select
            v-model:value="editableData[record.id].approveState"
            label-in-value
            style="width: 120px"
            :options="options"
            @pressEnter="save(record.id)"
          >
          </a-select>
          <check-outlined
            class="editable-cell-icon-check"
            @click="save_server(record.id)"
          />
        </div>
        <div v-else class="editable-cell-text-wrapper">
          {{ record.approveState || " " }}
          <edit-outlined class="editable-cell-icon" @click="edit(record.id)" />
        </div>
      </div>
    </template>

    <template #operation="{ record }">
      <a-popconfirm
        v-if="dataSource.length"
        title="Sure to delete?"
        @confirm="onDelete(record.key)"
      >
        <a>Delete</a>
      </a-popconfirm>
    </template>
  </a-table>
</template>
<script>
import { getworkerApplyHistory, submitApplication } from "../../api/api.js";
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
    const options = ref([
      {
        value: "2",
        label: "通过",
      },
      {
        value: "1",
        label: "驳回",
      },
    ]);

    const columns = [
      {
        title: "工号",
        dataIndex: "userId",
        width: "5%",
        sorter: (a, b) => a.length - b.length,
      },
      {
        title: "姓名",
        dataIndex: "name",
        width: "5%",
        // sorter: (a, b) => a.length - b.length,
      },

      {
        title: "开始时间",
        dataIndex: "applyStartTime",
        // sorter: true,
        width: "8%",
        // sorter: (a, b) => a.applyStartTime - b.applyStartTime,
      },
      {
        title: "结束时间",
        dataIndex: "applyEndTime",
        // sorter: true,
        width: "8%",
        // sorter: (a, b) => a.applyEndTime - b.applyEndTime,
      },

      {
        title: "申请时长",
        dataIndex: "applyTimeLast",
        width: "8%",
      },
      {
        title: "申请类型",
        dataIndex: "applyType",
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
        width: "5%",
      },
      {
        title: "是否节假",
        dataIndex: "isHoliday",
        width: "5%",
      },
        {
        title: "换算类型",
        dataIndex: "conversionType",
        width: "5%",
      },
      ,
      {
        title: "申请原因",
        dataIndex: "applyReason",
        width: "20%",
        // sorter: (a, b) => a.applyReason.length - b.applyReason.length,
      },
      {
        title: "填写批注",
        dataIndex: "approveNote",
        // sorter: true,
        width: "20%",
        slots: {
          customRender: "approveNote",
        },
      },
      {
        title: "审批状态",
        dataIndex: "approveState", //approveState
        // sorter: (a, b) => a.approveState.length - b.approveState.length,
        // onFilter: (value, record) => record.approveState.indexOf(value) === 0,
        width: "5%",
        slots: {
          customRender: "approveState",
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
    const count = computed(() => dataSource.value.length + 1);
    const editableData = reactive({});

    const edit = (key) => {
      console.log("key:", key);
      editableData[key] = cloneDeep(
        dataSource.value.filter((item) => key === item.id)[0]
      );
    };

    const save = (key) => {
      Object.assign(
        dataSource.value.filter((item) => key === item.id)[0],
        editableData[key]
      );
      delete editableData[key];
    };

    const save_server = (key) => {
      Object.assign(
        dataSource.value.filter((item) => key === item.id)[0],
        editableData[key]
      );

      submitApplication(
        getid,
        key,
        editableData[key].approveState.value,
        editableData[key].approveNote
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
      delete editableData[key];
    };

    const onDelete = (key) => {
      dataSource.value = dataSource.value.filter((item) => item.key !== key);
    };

    const handleAdd = () => {
      const newData = {
        key: `${count.value}`,
        name: `Edward King ${count.value}`,
        age: 32,
        address: `London, Park Lane no. ${count.value}`,
      };
      dataSource.value.push(newData);
    };

    return {
      getworkerApplyHistory,
      options,
      columns,
      onDelete,
      handleAdd,
      dataSource,
      editableData,
      count,
      edit,
      save,
      save_server,
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