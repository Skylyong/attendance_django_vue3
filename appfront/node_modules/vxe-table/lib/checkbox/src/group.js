"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;

var _vue = require("vue");

var _conf = _interopRequireDefault(require("../../v-x-e-table/src/conf"));

var _xeUtils = _interopRequireDefault(require("xe-utils"));

var _size = require("../../hooks/size");

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

var _default2 = (0, _vue.defineComponent)({
  name: 'VxeCheckboxGroup',
  props: {
    modelValue: Array,
    disabled: Boolean,
    size: {
      type: String,
      default: function _default() {
        return _conf.default.checkbox.size || _conf.default.size;
      }
    }
  },
  emits: ['update:modelValue', 'change'],
  setup: function setup(props, context) {
    var slots = context.slots,
        emit = context.emit;

    var xID = _xeUtils.default.uniqueId();

    var $xecheckboxgroup = {
      xID: xID,
      props: props,
      context: context
    };
    (0, _size.useSize)(props);
    var checkboxGroupMethods = {
      dispatchEvent: function dispatchEvent(type, params, evnt) {
        emit(type, Object.assign({
          $checkboxGroup: $xecheckboxgroup,
          $event: evnt
        }, params));
      }
    };
    var checkboxGroupPrivateMethods = {
      handleChecked: function handleChecked(params, evnt) {
        var checked = params.checked,
            label = params.label;
        var checklist = props.modelValue || [];
        var checkIndex = checklist.indexOf(label);

        if (checked) {
          if (checkIndex === -1) {
            checklist.push(label);
          }
        } else {
          checklist.splice(checkIndex, 1);
        }

        emit('update:modelValue', checklist);
        $xecheckboxgroup.dispatchEvent('change', Object.assign({
          checklist: checklist
        }, params), evnt);
      }
    };
    Object.assign($xecheckboxgroup, checkboxGroupMethods, checkboxGroupPrivateMethods);

    var renderVN = function renderVN() {
      return (0, _vue.h)('div', {
        class: 'vxe-checkbox-group'
      }, slots.default ? slots.default({}) : []);
    };

    $xecheckboxgroup.renderVN = renderVN;
    (0, _vue.provide)('$xecheckboxgroup', $xecheckboxgroup);
    return renderVN;
  }
});

exports.default = _default2;