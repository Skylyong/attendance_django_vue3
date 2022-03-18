"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = exports.Keyboard = void 0;

var _hook = _interopRequireDefault(require("./src/hook"));

var _vXETable = require("../v-x-e-table");

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

var Keyboard = {
  install: function install() {
    _vXETable.VXETable.hooks.add('$tableKeyboard', _hook.default);
  }
};
exports.Keyboard = Keyboard;
var _default = Keyboard;
exports.default = _default;