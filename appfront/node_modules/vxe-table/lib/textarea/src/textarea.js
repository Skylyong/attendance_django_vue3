"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;

var _vue = require("vue");

var _xeUtils = _interopRequireDefault(require("xe-utils"));

var _conf = _interopRequireDefault(require("../../v-x-e-table/src/conf"));

var _utils = require("../../tools/utils");

var _size = require("../../hooks/size");

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

var autoTxtElem;

var _default2 = (0, _vue.defineComponent)({
  name: 'VxeTextarea',
  props: {
    modelValue: [String, Number],
    className: String,
    immediate: {
      type: Boolean,
      default: true
    },
    name: String,
    readonly: Boolean,
    disabled: Boolean,
    placeholder: String,
    maxlength: [String, Number],
    rows: {
      type: [String, Number],
      default: 2
    },
    cols: {
      type: [String, Number],
      default: null
    },
    showWordCount: Boolean,
    countMethod: Function,
    autosize: [Boolean, Object],
    form: String,
    resize: {
      type: String,
      default: function _default() {
        return _conf.default.textarea.resize;
      }
    },
    size: {
      type: String,
      default: function _default() {
        return _conf.default.textarea.size || _conf.default.size;
      }
    }
  },
  emits: ['update:modelValue', 'input', 'keydown', 'keyup', 'click', 'change', 'focus', 'blur'],
  setup: function setup(props, context) {
    var emit = context.emit;

    var xID = _xeUtils.default.uniqueId();

    var computeSize = (0, _size.useSize)(props);
    var reactData = (0, _vue.reactive)({
      inputValue: props.modelValue
    });
    var refElem = (0, _vue.ref)();
    var refTextarea = (0, _vue.ref)();
    var refMaps = {
      refElem: refElem,
      refTextarea: refTextarea
    };
    var $xetextarea = {
      xID: xID,
      props: props,
      context: context,
      reactData: reactData,
      getRefMaps: function getRefMaps() {
        return refMaps;
      }
    };
    var textareaMethods = {};
    var computeInputCount = (0, _vue.computed)(function () {
      return _xeUtils.default.getSize(reactData.inputValue);
    });
    var computeIsCountError = (0, _vue.computed)(function () {
      var inputCount = computeInputCount.value;
      return props.maxlength && inputCount > _xeUtils.default.toNumber(props.maxlength);
    });
    var computeSizeOpts = (0, _vue.computed)(function () {
      return Object.assign({
        minRows: 1,
        maxRows: 10
      }, _conf.default.textarea.autosize, props.autosize);
    });

    var updateAutoTxt = function updateAutoTxt() {
      var size = props.size,
          autosize = props.autosize;
      var inputValue = reactData.inputValue;

      if (autosize) {
        if (!autoTxtElem) {
          autoTxtElem = document.createElement('div');
        }

        if (!autoTxtElem.parentNode) {
          document.body.appendChild(autoTxtElem);
        }

        var textElem = refTextarea.value;
        var textStyle = getComputedStyle(textElem);
        autoTxtElem.className = ['vxe-textarea--autosize', size ? "size--" + size : ''].join(' ');
        autoTxtElem.style.width = textElem.clientWidth + "px";
        autoTxtElem.style.padding = textStyle.padding;
        autoTxtElem.innerHTML = ('' + (inputValue || '　')).replace(/\n$/, '\n　');
      }
    };

    var handleResize = function handleResize() {
      if (props.autosize) {
        (0, _vue.nextTick)(function () {
          var sizeOpts = computeSizeOpts.value;
          var minRows = sizeOpts.minRows,
              maxRows = sizeOpts.maxRows;
          var textElem = refTextarea.value;
          var sizeHeight = autoTxtElem.clientHeight;
          var textStyle = getComputedStyle(textElem);

          var lineHeight = _xeUtils.default.toNumber(textStyle.lineHeight);

          var paddingTop = _xeUtils.default.toNumber(textStyle.paddingTop);

          var paddingBottom = _xeUtils.default.toNumber(textStyle.paddingBottom);

          var borderTopWidth = _xeUtils.default.toNumber(textStyle.borderTopWidth);

          var borderBottomWidth = _xeUtils.default.toNumber(textStyle.borderBottomWidth);

          var intervalHeight = paddingTop + paddingBottom + borderTopWidth + borderBottomWidth;
          var rowNum = (sizeHeight - intervalHeight) / lineHeight;
          var textRows = rowNum && /[0-9]/.test('' + rowNum) ? rowNum : Math.floor(rowNum) + 1;
          var vaildRows = textRows;

          if (textRows < minRows) {
            vaildRows = minRows;
          } else if (textRows > maxRows) {
            vaildRows = maxRows;
          }

          textElem.style.height = vaildRows * lineHeight + intervalHeight + "px";
        });
      }
    };

    var triggerEvent = function triggerEvent(evnt) {
      var value = reactData.inputValue;
      $xetextarea.dispatchEvent(evnt.type, {
        value: value
      }, evnt);
    };

    var emitUpdate = function emitUpdate(value, evnt) {
      reactData.inputValue = value;
      emit('update:modelValue', value);

      if (_xeUtils.default.toValueString(props.modelValue) !== value) {
        textareaMethods.dispatchEvent('change', {
          value: value
        }, evnt);
      }
    };

    var inputEvent = function inputEvent(evnt) {
      var immediate = props.immediate;
      var textElem = evnt.target;
      var value = textElem.value;
      reactData.inputValue = value;

      if (immediate) {
        emitUpdate(value, evnt);
      }

      $xetextarea.dispatchEvent('input', {
        value: value
      }, evnt);
      handleResize();
    };

    var changeEvent = function changeEvent(evnt) {
      var immediate = props.immediate;

      if (immediate) {
        triggerEvent(evnt);
      } else {
        emitUpdate(reactData.inputValue, evnt);
      }
    };

    var blurEvent = function blurEvent(evnt) {
      var immediate = props.immediate;
      var inputValue = reactData.inputValue;

      if (!immediate) {
        emitUpdate(inputValue, evnt);
      }

      $xetextarea.dispatchEvent('blur', {
        value: inputValue
      }, evnt);
    };

    textareaMethods = {
      dispatchEvent: function dispatchEvent(type, params, evnt) {
        emit(type, Object.assign({
          $textarea: $xetextarea,
          $event: evnt
        }, params));
      },
      focus: function focus() {
        var textElem = refTextarea.value;
        textElem.focus();
        return (0, _vue.nextTick)();
      },
      blur: function blur() {
        var textElem = refTextarea.value;
        textElem.blur();
        return (0, _vue.nextTick)();
      }
    };
    Object.assign($xetextarea, textareaMethods);
    (0, _vue.watch)(function () {
      return props.modelValue;
    }, function (val) {
      reactData.inputValue = val;
      updateAutoTxt();
    });
    (0, _vue.nextTick)(function () {
      var autosize = props.autosize;

      if (autosize) {
        updateAutoTxt();
        handleResize();
      }
    });

    var renderVN = function renderVN() {
      var _a;

      var className = props.className,
          resize = props.resize,
          placeholder = props.placeholder,
          disabled = props.disabled,
          maxlength = props.maxlength,
          autosize = props.autosize,
          showWordCount = props.showWordCount,
          countMethod = props.countMethod,
          rows = props.rows,
          cols = props.cols;
      var inputValue = reactData.inputValue;
      var vSize = computeSize.value;
      var isCountError = computeIsCountError.value;
      var inputCount = computeInputCount.value;
      return (0, _vue.h)('div', {
        ref: refElem,
        class: ['vxe-textarea', className, (_a = {}, _a["size--" + vSize] = vSize, _a['is--autosize'] = autosize, _a['is--disabled'] = disabled, _a['def--rows'] = !_xeUtils.default.eqNull(rows), _a['def--cols'] = !_xeUtils.default.eqNull(cols), _a)]
      }, [(0, _vue.h)('textarea', {
        ref: refTextarea,
        class: 'vxe-textarea--inner',
        value: inputValue,
        name: props.name,
        placeholder: placeholder ? (0, _utils.getFuncText)(placeholder) : null,
        maxlength: maxlength,
        readonly: props.readonly,
        disabled: disabled,
        rows: rows,
        cols: cols,
        style: resize ? {
          resize: resize
        } : null,
        onInput: inputEvent,
        onChange: changeEvent,
        onKeydown: triggerEvent,
        onKeyup: triggerEvent,
        onClick: triggerEvent,
        onFocus: triggerEvent,
        onBlur: blurEvent
      }), showWordCount ? (0, _vue.h)('span', {
        class: ['vxe-textarea--count', {
          'is--error': isCountError
        }]
      }, countMethod ? "" + countMethod({
        value: inputValue
      }) : "" + inputCount + (maxlength ? "/" + maxlength : '')) : null]);
    };

    $xetextarea.renderVN = renderVN;
    return $xetextarea;
  },
  render: function render() {
    return this.renderVN();
  }
});

exports.default = _default2;