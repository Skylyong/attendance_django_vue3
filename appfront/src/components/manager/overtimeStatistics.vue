<template>
  <br />
  <br />
  <br />
  <h1 style="text-align: center">加班汇总</h1>
  <br />

  <a-table
    :columns="columns"
    :data-source="dataGroups"
    class="components-table-demo-nested"
    :rowKey="(item) => item.userid"
    >>

    <template #expandedRowRender="{ record }">
      <a-table
        :columns="innerColumns"
        :data-source="record.groupItem"
        :rowKey="(item) => item.id"
        :pagination="false"
      >>
        <!-- <template #operation="{ record }">
          <a-popconfirm
             v-if=" record.approveState != '作废'"
            title="确定作废吗?"
            @confirm="onDelete(record.id)"
          >
            <a>作废</a>
          </a-popconfirm>
        </template> -->
      </a-table>
    </template>
  </a-table>
</template>











<script>
import { DownOutlined } from "@ant-design/icons-vue";
import { getOverTimeData, getPoolData } from "../../api/api.js";
import { defineComponent, ref, reactive } from "vue";
let columns = ref([
  {
    title: "年 月 ",
    dataIndex: "endYearMonth",
    width: "30%",
    onFilter: (value, record) => record.endYearMonth.indexOf(value) === 0,
  },
  {
    title: "工 号",
    dataIndex: "userId",
    width: "20%",
    onFilter: (value, record) => record.userId.indexOf(value) === 0,
  },

  {
    title: "姓 名",
    dataIndex: "name",
    width: "20%",
  },
  {
    title: "加班时长",
    dataIndex: "overtime",
  },
]);

let innerColumns = ref([
  {
    title: "加班时间",
    dataIndex: "applyStartTime",
    width: "30%",
    sorter: (a, b) => a.id - b.id,
  },
  {
    title: "加班时长",
    dataIndex: "applyTimeLast",
    sorter: false,
    width: "30%",
    // sorter: (a, b) => a.applyTimeLast - b.applyTimeLast,
  },

  {
    title: "加班原因",
    dataIndex: "applyReason",
    sorter: (a, b) => a.applyReason.length - b.applyReason.length,
  },

//  {
//     title: "状态",
//     dataIndex: "approveState",
//     onFilter: (value, record) => record.approveState.indexOf(value) === 0,
//     width: "15%",
//     filters: [
//       {
//         text: "通过",
//         value: "通过",
//       },
//       {
//         text: "驳回",
//         value: "驳回",
//       },
//        {
//         text: "作废",
//         value: "作废",
//       },
//     ],
//   },


  // {
  //   title: "操作",
  //   dataIndex: "operation",
  //   slots: {
  //     customRender: "operation",
  //   },
  // },
]);

export default defineComponent({
  components: {
    DownOutlined,
  },

  setup() {
    let getid = localStorage.getItem("Userid");
    let dataGroups = ref();
    // let columns = ref()


// const onDelete = (key) => {
// console.log('key:', key)

// }


    getOverTimeData(getid).then((response) => {
      if (response["code"] == 1) {
        columns.value = [
          {
            title: "年 月 ",
            dataIndex: "endYearMonth",
            width: "25%",
            filters: response["data"]["filters"]["endYearMonth_filters"],
            onFilter: (value, record) =>
              record.endYearMonth.indexOf(value) === 0,
          },
          {
            title: "工 号",
            dataIndex: "userId",
            width: "20%",
            filters: response["data"]["filters"]["userId_filters"],
            onFilter: (value, record) => record.userId.indexOf(value) === 0,
          },

          {
            title: "姓 名",
            dataIndex: "name",
            width: "20%",
          },
          {
            title: "加班时长",
            dataIndex: "overtime",
          },
        ];
        // columns.value = new_columns

        dataGroups.value = response["data"]["data"];
        console.log(columns);
        // columns[1]["filters"] =response["data"]["filters"]["userId_filters"];

        // console.log(response["data"]);
      }
    });
    return {
      dataGroups,
      getOverTimeData,
      columns,
      innerColumns,
      // onDelete
    };
  },
});
</script>