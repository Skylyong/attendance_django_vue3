"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;

var _vue = require("vue");

var _conf = _interopRequireDefault(require("../../v-x-e-table/src/conf"));

var _vXETable = require("../../v-x-e-table");

var _utils = require("../../tools/utils");

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

var _default = (0, _vue.defineComponent)({
  name: 'VxeTableFilter',
  props: {
    filterStore: Object
  },
  setup: function setup(props) {
    var $xetable = (0, _vue.inject)('$xetable', {});
    var tableReactData = $xetable.reactData,
        tableInternalData = $xetable.internalData;
    var computeHasCheckOption = (0, _vue.computed)(function () {
      var filterStore = props.filterStore;
      return filterStore && filterStore.options.some(function (option) {
        return option.checked;
      });
    }); // 全部筛选事件

    var filterCheckAllEvent = function filterCheckAllEvent(evnt, value) {
      var filterStore = props.filterStore;
      filterStore.options.forEach(function (option) {
        option._checked = value;
        option.checked = value;
      });
      filterStore.isAllSelected = value;
      filterStore.isIndeterminate = false;
    };
    /*************************
     * Publish methods
     *************************/
    // 确认筛选


    var confirmFilter = function confirmFilter(evnt) {
      var filterStore = props.filterStore;
      filterStore.options.forEach(function (option) {
        option.checked = option._checked;
      });
      $xetable.confirmFilterEvent(evnt);
    }; // （单选）筛选发生改变


    var changeRadioOption = function changeRadioOption(evnt, checked, item) {
      var filterStore = props.filterStore;
      filterStore.options.forEach(function (option) {
        option._checked = false;
      });
      item._checked = checked;
      $xetable.checkFilterOptions();
      confirmFilter(evnt);
    };
    /**
     * 重置筛选
     * 当筛选面板中的重置按钮被按下时触发
     * @param {Event} evnt 事件
     */


    var resetFilter = function resetFilter(evnt) {
      var filterStore = props.filterStore;
      $xetable.handleClearFilter(filterStore.column);
      $xetable.confirmFilterEvent(evnt);
    }; // （多选）筛选发生改变


    var changeMultipleOption = function changeMultipleOption(evnt, checked, item) {
      item._checked = checked;
      $xetable.checkFilterOptions();
    }; // 筛选发生改变


    var changeOption = function changeOption(evnt, checked, item) {
      var filterStore = props.filterStore;

      if (filterStore.multiple) {
        changeMultipleOption(evnt, checked, item);
      } else {
        changeRadioOption(evnt, checked, item);
      }
    };

    var changeAllOption = function changeAllOption(evnt, checked) {
      var filterStore = props.filterStore;

      if (filterStore.multiple) {
        filterCheckAllEvent(evnt, checked);
      } else {
        resetFilter(evnt);
      }
    };
    /*************************
     * Publish methods
     *************************/


    var $panel = {
      changeRadioOption: changeRadioOption,
      changeMultipleOption: changeMultipleOption,
      changeAllOption: changeAllOption,
      changeOption: changeOption,
      confirmFilter: confirmFilter,
      resetFilter: resetFilter
    };

    var renderOptions = function renderOptions(filterRender, compConf) {
      var filterStore = props.filterStore;
      var column = filterStore.column,
          multiple = filterStore.multiple,
          maxHeight = filterStore.maxHeight;
      var slots = column.slots;
      var filterSlot = slots ? slots.filter : null;
      var params = Object.assign({}, tableInternalData._currFilterParams, {
        $panel: $panel,
        $table: $xetable
      });

      if (filterSlot) {
        return [(0, _vue.h)('div', {
          class: 'vxe-table--filter-template'
        }, $xetable.callSlot(filterSlot, params))];
      } else if (compConf && compConf.renderFilter) {
        return [(0, _vue.h)('div', {
          class: 'vxe-table--filter-template'
        }, compConf.renderFilter(filterRender, params))];
      }

      return [(0, _vue.h)('ul', {
        class: 'vxe-table--filter-header'
      }, [(0, _vue.h)('li', {
        class: ['vxe-table--filter-option', {
          'is--checked': multiple ? filterStore.isAllSelected : !filterStore.options.some(function (item) {
            return item._checked;
          }),
          'is--indeterminate': multiple && filterStore.isIndeterminate
        }],
        title: _conf.default.i18n(multiple ? 'vxe.table.allTitle' : 'vxe.table.allFilter'),
        onClick: function onClick(evnt) {
          changeAllOption(evnt, !filterStore.isAllSelected);
        }
      }, (multiple ? [(0, _vue.h)('span', {
        class: 'vxe-checkbox--icon vxe-checkbox--checked-icon'
      }), (0, _vue.h)('span', {
        class: 'vxe-checkbox--icon vxe-checkbox--unchecked-icon'
      }), (0, _vue.h)('span', {
        class: 'vxe-checkbox--icon vxe-checkbox--indeterminate-icon'
      })] : []).concat([(0, _vue.h)('span', {
        class: 'vxe-checkbox--label'
      }, _conf.default.i18n('vxe.table.allFilter'))]))]), (0, _vue.h)('ul', {
        class: 'vxe-table--filter-body',
        style: maxHeight ? {
          maxHeight: maxHeight + "px"
        } : {}
      }, filterStore.options.map(function (item) {
        return (0, _vue.h)('li', {
          class: ['vxe-table--filter-option', {
            'is--checked': item._checked
          }],
          title: item.label,
          onClick: function onClick(evnt) {
            changeOption(evnt, !item._checked, item);
          }
        }, (multiple ? [(0, _vue.h)('span', {
          class: 'vxe-checkbox--icon vxe-checkbox--checked-icon'
        }), (0, _vue.h)('span', {
          class: 'vxe-checkbox--icon vxe-checkbox--unchecked-icon'
        }), (0, _vue.h)('span', {
          class: 'vxe-checkbox--icon vxe-checkbox--indeterminate-icon'
        })] : []).concat([(0, _vue.h)('span', {
          class: 'vxe-checkbox--label'
        }, (0, _utils.formatText)(item.label, 1))]));
      }))];
    };

    var renderFooters = function renderFooters() {
      var filterStore = props.filterStore;
      var column = filterStore.column,
          multiple = filterStore.multiple;
      var hasCheckOption = computeHasCheckOption.value;
      var filterRender = column.filterRender;
      var compConf = filterRender ? _vXETable.VXETable.renderer.get(filterRender.name) : null;
      var isDisabled = !hasCheckOption && !filterStore.isAllSelected && !filterStore.isIndeterminate;
      return multiple && (!compConf || compConf.showFilterFooter !== false) ? [(0, _vue.h)('div', {
        class: 'vxe-table--filter-footer'
      }, [(0, _vue.h)('button', {
        class: {
          'is--disabled': isDisabled
        },
        disabled: isDisabled,
        onClick: confirmFilter
      }, _conf.default.i18n('vxe.table.confirmFilter')), (0, _vue.h)('button', {
        onClick: resetFilter
      }, _conf.default.i18n('vxe.table.resetFilter'))])] : [];
    };

    var renderVN = function renderVN() {
      var filterStore = props.filterStore;
      var initStore = tableReactData.initStore;
      var column = filterStore.column;
      var filterRender = column ? column.filterRender : null;
      var compConf = filterRender ? _vXETable.VXETable.renderer.get(filterRender.name) : null;
      return (0, _vue.h)('div', {
        class: ['vxe-table--filter-wrapper', 'filter--prevent-default', compConf && compConf.className ? compConf.className : '', {
          'is--animat': $xetable.props.animat,
          'is--multiple': filterStore.multiple,
          'is--active': filterStore.visible
        }],
        style: filterStore.style
      }, initStore.filter && filterStore.visible ? renderOptions(filterRender, compConf).concat(renderFooters()) : []);
    };

    return renderVN;
  }
});

exports.default = _default;