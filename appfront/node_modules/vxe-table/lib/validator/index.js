"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = exports.Validator = void 0;

var _hook = _interopRequireDefault(require("./src/hook"));

var _vXETable = require("../v-x-e-table");

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

var Validator = {
  install: function install() {
    _vXETable.VXETable.hooks.add('$tableValidator', _hook.default);
  }
};
exports.Validator = Validator;
var _default = Validator;
exports.default = _default;