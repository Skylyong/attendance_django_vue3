"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;

var _vue = require("vue");

var _xeUtils = _interopRequireDefault(require("xe-utils"));

var _utils = require("../../tools/utils");

var _conf = _interopRequireDefault(require("../../v-x-e-table/src/conf"));

var _size = require("../../hooks/size");

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

var _default2 = (0, _vue.defineComponent)({
  name: 'VxeCheckbox',
  props: {
    modelValue: [String, Number, Boolean],
    label: {
      type: [String, Number],
      default: null
    },
    indeterminate: Boolean,
    title: [String, Number],
    checkedValue: {
      type: [String, Number, Boolean],
      default: true
    },
    uncheckedValue: {
      type: [String, Number, Boolean],
      default: false
    },
    content: [String, Number],
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

    var $xecheckbox = {
      xID: xID,
      props: props,
      context: context
    };
    var checkboxMethods = {};
    var computeSize = (0, _size.useSize)(props);
    var $xecheckboxgroup = (0, _vue.inject)('$xecheckboxgroup', null);
    var computeDisabled = (0, _vue.computed)(function () {
      return props.disabled || $xecheckboxgroup && $xecheckboxgroup.props.disabled;
    });
    var computeChecked = (0, _vue.computed)(function () {
      return $xecheckboxgroup ? _xeUtils.default.includes($xecheckboxgroup.props.modelValue, props.label) : props.modelValue === props.checkedValue;
    });

    var changeEvent = function changeEvent(evnt) {
      var checkedValue = props.checkedValue,
          uncheckedValue = props.uncheckedValue;
      var isDisabled = computeDisabled.value;

      if (!isDisabled) {
        var checked = evnt.target.checked;
        var value = checked ? checkedValue : uncheckedValue;
        var params = {
          checked: checked,
          value: value,
          label: props.label
        };

        if ($xecheckboxgroup) {
          $xecheckboxgroup.handleChecked(params, evnt);
        } else {
          emit('update:modelValue', value);
          checkboxMethods.dispatchEvent('change', params, evnt);
        }
      }
    };

    checkboxMethods = {
      dispatchEvent: function dispatchEvent(type, params, evnt) {
        emit(type, Object.assign({
          $checkbox: $xecheckbox,
          $event: evnt
        }, params));
      }
    };
    Object.assign($xecheckbox, checkboxMethods);

    var renderVN = function renderVN() {
      var _a;

      var vSize = computeSize.value;
      var isDisabled = computeDisabled.value;
      return (0, _vue.h)('label', {
        class: ['vxe-checkbox', (_a = {}, _a["size--" + vSize] = vSize, _a['is--indeterminate'] = props.indeterminate, _a['is--disabled'] = isDisabled, _a)],
        title: props.title
      }, [(0, _vue.h)('input', {
        class: 'vxe-checkbox--input',
        type: 'checkbox',
        disabled: isDisabled,
        checked: computeChecked.value,
        onChange: changeEvent
      }), (0, _vue.h)('span', {
        class: 'vxe-checkbox--icon'
      }), (0, _vue.h)('span', {
        class: 'vxe-checkbox--label'
      }, slots.default ? slots.default({}) : (0, _utils.getFuncText)(props.content))]);
    };

    $xecheckbox.renderVN = renderVN;
    return $xecheckbox;
  },
  render: function render() {
    return this.renderVN();
  }
});

exports.default = _default2;