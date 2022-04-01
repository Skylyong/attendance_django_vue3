<template>
  <!-- <a-button class="editable-add-btn" style="margin-bottom: 8px" @click="handleAdd">Add</a-button> -->
  <a-table
    bordered
    :data-source="dataSource"
    :columns="columns"
    :@handleTableChange="handleTableChange"
  >
    <template #operation="{ record }">
      <a-popconfirm
        v-if="dataSource.length && record.approveState == '未审批'"
        title="确定删除吗?"
        @confirm="onDelete(record.id)"
      >
        <a>删除</a>
      </a-popconfirm>
    </template>
  </a-table>
</template>

<script>
import { usePagination } from "vue-request";
import { getworkerApplyHistory, delApplication } from "../../api/api.js";
import { computed, defineComponent, ref, reactive } from "vue";
import { cloneDeep } from "lodash-es";
import axios from "axios";
import { CheckOutlined, EditOutlined } from "@ant-design/icons-vue";
import { message } from "ant-design-vue";
const columns = [
  // {
  //   title: "序号",
  //   dataIndex: "id",
  //   width: "8%",
  //   sorter: (a, b) => a.id - b.id,
  // },
  {
    title: "申请时间",
    dataIndex: "applyTime",
    width: "8%",
    sorter: (a, b) => a.id - b.id,
  },

  {
    title: "开始时间",
    dataIndex: "applyStartTime",
    sorter: true,
    width: "8%",
    sorter: (a, b) => a.applyStartTime - b.applyStartTime,
  },
  {
    title: "结束时间",
    dataIndex: "applyEndTime",
    sorter: true,
    width: "8%",
    sorter: (a, b) => a.applyEndTime - b.applyEndTime,
  },
  {
    title: "申请时长",
    dataIndex: "applyTimeLast",
    sorter: true,
    width: "8%",
    // sorter: (a, b) => a.timeLast.length - b.timeLast.length,
  },
  {
    title: "申请类型",
    dataIndex: "applyType",
    filters: [
      {
        text: "值班",
        value: "值班",
      },
      {
        text: "加班",
        value: "加班",
      },
      {
        text: "请假",
        value: "请假",
      },
    ],
    onFilter: (value, record) => record.applyType.indexOf(value) === 0,
    // sorter: (a, b) => a.applyType.length - b.applyType.length,
    width: "12%",
  },
  {
    title: "是否节假",
    dataIndex: "isHoliday",
    filters: [
      {
        text: "是",
        value: "是",
      },
      {
        text: "否",
        value: "否",
      },
     
    ],
    onFilter: (value, record) => record.isHoliday.indexOf(value) === 0,
    width: "12%",
  },
  {
    title: "换算类型",
    dataIndex: "conversionType",
    filters: [
      {
        text: "累加积休",
        value: "累加积休",
      },
      {
        text: "加班费",
        value: "加班费",
      },
    
    ],
    onFilter: (value, record) => record.conversionType.indexOf(value) === 0,
    width: "12%",
  },
  {
    title: "申请原因",
    dataIndex: "applyReason",
    width: "20%",
    sorter: (a, b) => a.applyReason.length - b.applyReason.length,
  },
  {
    title: "审批状态",
    dataIndex: "approveState",
    sorter: (a, b) => a.approveState.length - b.approveState.length,
    onFilter: (value, record) => record.approveState.indexOf(value) === 0,
    width: "8%",
    filters: [
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
      {
        text: "未审批",
        value: "未审批",
      },
    ],
  },
  {
    title: "批注",
    dataIndex: "approveNote",
    sorter: true,
    width: "10%",
    sorter: (a, b) => a.applyReason.length - b.applyReason.length,
  },

  {
    title: "操作",
    dataIndex: "operation",
    slots: {
      customRender: "operation",
    },
  },
];

export default defineComponent({
  components: {
    CheckOutlined,
    EditOutlined,
  },
  setup() {
    const handleTableChange = (pag, filters, sorter) => {
      run({
        results: pag.pageSize,
        page: pag?.current,
        sortField: sorter.field,
        sortOrder: sorter.order,
        ...filters,
      });
    };
    const editableData = reactive({});
    const edit = (key) => {
      editableData[key] = cloneDeep(
        dataSource.value.filter((item) => key === item.key)[0]
      );
    };

    let dataSource = ref();

    let getid = localStorage.getItem("Userid");
    getworkerApplyHistory(getid).then((response) => {
      if (response["code"] == 1) {
        console.log(response["data"]);
        dataSource.value = response["data"];
      }
    });
    const save = (key) => {
      Object.assign(
        dataSource.value.filter((item) => key === item.key)[0],
        editableData[key]
      );
      delete editableData[key];
    };
    const onDelete = (key) => {
      delApplication(getid, key).then(
        (response) => {
          if (1 === response["code"]) {
            dataSource.value = dataSource.value.filter(
              (item) => item.id !== key
            );
            message.success("从服务器删除成功！");
            getworkerApplyHistory(getid).then((response) => {
              if (response["code"] == 1) {
                console.log(response["data"]);
                dataSource.value = response["data"];
              }
            });
          } else {
            message.error("服务端删除失败！");
          }
        },
        (response) => {
          message.error("服务端删除失败！");
        }
      );
    };

    return {
      dataSource,
      editableData,
      save,
      onDelete,

      columns,
      handleTableChange,
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
