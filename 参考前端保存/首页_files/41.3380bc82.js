(window.webpackJsonp=window.webpackJsonp||[]).push([[41],{TkZh:function(e,t,n){"use strict";n.d(t,"a",(function(){return s}));var r=n("+enf"),c=n("cnCt"),a=n("fNXc");function ownKeys(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,r)}return n}function _objectSpread(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?ownKeys(Object(n),!0).forEach((function(t){_defineProperty(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):ownKeys(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function _defineProperty(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}var o=function getFetchRuducers(e){return function(t,n){var r,c="".concat(n,"Success"),o="".concat(n,"Failed"),i="".concat(n,"SilentSuccess"),u="".concat(n,"SilentFailed");if(!Object(a.a)(e))throw"对于fetch类型reducer, state必须是一个对象！";return _objectSpread(_objectSpread({},t),{},(_defineProperty(r={},n,(function(e,r){var c=_objectSpread(_objectSpread({},e),{},{loading:!0,error:!1});return t[n]?t[n](c,r):c})),_defineProperty(r,c,(function(e,n){var r=_objectSpread(_objectSpread({},e),{},{loading:!1});return t[c]?t[c](r,n):r})),_defineProperty(r,i,(function(e,n){return t[i]?t[i](e,n):e})),_defineProperty(r,u,(function(e,n){return t[u]?t[u](e,n):e})),_defineProperty(r,o,(function(e,n){var r=_objectSpread(_objectSpread({},e),{},{loading:!1,error:n});return t[o]?t[o](r,n):r})),r))}},i=function handleFetchReducers(e){if(!e.fetch)return e;var t=e.state,n=e.reducers,r=e.fetch,c={};return c=Array.isArray(r)?r.reduce(o(t),n):o(t)(n,r),{state:_objectSpread(_objectSpread({},t),{},{loading:!1,error:!1}),reducers:c}},u=function initReducers(e,t){var n=i(e),r=n.state,a=n.reducers,o,u=Object.keys(a).map((function(e){var n="".concat(t,"/").concat(e);return c.a.setActionByNamespace(n),{name:c.a.toAction(n),fn:a[e]}}));return function(){var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:r,t=arguments.length>1?arguments[1]:void 0,n=u.find((function(e){return e.name===t.type}));return n?n.fn&&n.fn(e,t.payload):e}},s=function combinceReducer(e,t){var n={},c=Object.keys(e),a=function getReducerMap(t){return c.forEach((function(r){var c=e[r],a="/"===t?"/".concat(r):"".concat(t,"/").concat(r);n[r]="function"==typeof c?c(a):u(c,a)})),Object(r.combineReducers)(n)};return t?a(t):a}},cnCt:function(e,t,n){"use strict";t.a={namespaces:{},set:function set(e,t){this.namespaces[e]=t},setActionByNamespace:function setActionByNamespace(e){var t=this.toAction(e);this.namespaces[e]=t},get:function get(e){return this.namespaces[e]},toAction:function toAction(e){var t=e;return 0===e.indexOf("/")&&(t=e.slice(1)),t.split("/").join("_")}}},fNXc:function(e,t,n){"use strict";n.d(t,"b",(function(){return r})),n.d(t,"a",(function(){return c}));var r=function splitObject(e,t){var n={};return t.forEach((function(t){n[t]=e[t]})),n},c=function isObj(e){return"[object Object]"===String(e)}},wJHw:function(e,t,n){"use strict";n.r(t);var r=n("TkZh"),c=n("dpRb"),a=n.n(c),o,i={state:{nav:[{group:[{name:a.a.get("威胁态势"),link:"/web/dashboard",icon:"perception",role:[1,2],subs:[{name:a.a.get("首页"),link:"/web/dashboard"},{name:a.a.get("大屏"),link:"/web/index"}]},{name:a.a.get("威胁感知"),icon:"perception",role:[1,2],subs:[{name:a.a.get("攻击列表"),link:"/web/threatList"},{name:a.a.get("扫描感知"),link:"/web/scanners"},{name:a.a.get("失陷感知"),link:"/web/decoy"}]},{name:a.a.get("威胁实体"),icon:"environment",role:[1,2],subs:[{name:a.a.get("攻击来源"),link:"/web/attackip"},{name:a.a.get("账号资源"),link:"/web/username"},{name:a.a.get("样本检测"),link:"/web/sampledata"},{name:a.a.get("威胁检测"),link:"/web/detection"}]},{name:a.a.get("环境管理"),icon:"environment",role:[1],subs:[{name:a.a.get("节点管理"),link:"/web/nodeList"},{name:a.a.get("模板管理"),link:"/web/templateList"},{name:a.a.get("服务管理"),link:"/web/service"}]},{name:a.a.get("平台管理"),icon:"setting",role:[1],subs:!window.localStorage.getItem("lang")||null!==(o=window.localStorage.getItem("lang"))&&void 0!==o&&o.includes("zh")?[{name:a.a.get("报告管理"),link:"/web/report"},{name:a.a.get("系统配置"),link:"/web/systemConfig"},{name:a.a.get("系统信息"),link:"/web/message"}]:[{name:a.a.get("系统配置"),link:"/web/systemConfig"},{name:a.a.get("系统信息"),link:"/web/message"}]}]}]},reducers:{}};function ownKeys(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,r)}return n}function _objectSpread(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?ownKeys(Object(n),!0).forEach((function(t){_defineProperty(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):ownKeys(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function _defineProperty(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}var u={fetch:"get",state:{data:{}},reducers:{getSuccess:function getSuccess(e,t){return e}}},s={fetch:"get",state:{},reducers:{getSuccess:function getSuccess(e,t){return _objectSpread(_objectSpread({},e),t)},get:function get(e,t){return t}}},f={fetch:"get",state:{},reducers:{getSuccess:function getSuccess(e,t){return _objectSpread(_objectSpread({},e),t)},get:function get(e,t){return t}}},b=t.default=Object(r.a)({mainData:u,loginData:s,nav:i,database:f},"/main")}}]);