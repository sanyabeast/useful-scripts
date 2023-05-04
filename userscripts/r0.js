// ==UserScript==
// @name         retr0 userscript
// @description  retr0 userscript
// @version      1
// @grant        none
// @run-at       document-start
// @match        *://*/*
// @author       @sanyabeast
// ==/UserScript==

(function () {
    'use strict';

    /** * @license * Lodash (Custom Build) lodash.com/license | Underscore.js 1.8.3 underscorejs.org/LICENSE * Build: \`lodash core -o ./dist/lodash.core.js\` */
    const load_lodash = () => {
        ; (function () { function n(n) { return H(n) && pn.call(n, "callee") && !yn.call(n, "callee") } function t(n, t) { return n.push.apply(n, t), n } function r(n) { return function (t) { return null == t ? Z : t[n] } } function e(n, t, r, e, u) { return u(n, function (n, u, o) { r = e ? (e = false, n) : t(r, n, u, o) }), r } function u(n, t) { return j(t, function (t) { return n[t] }) } function o(n) { return n instanceof i ? n : new i(n) } function i(n, t) { this.__wrapped__ = n, this.__actions__ = [], this.__chain__ = !!t } function c(n, t, r) { if (typeof n != "function") throw new TypeError("Expected a function"); return setTimeout(function () { n.apply(Z, r) }, t) } function f(n, t) { var r = true; return mn(n, function (n, e, u) { return r = !!t(n, e, u) }), r } function a(n, t, r) { for (var e = -1, u = n.length; ++e < u;) { var o = n[e], i = t(o); if (null != i && (c === Z ? i === i : r(i, c))) var c = i, f = o } return f } function l(n, t) { var r = []; return mn(n, function (n, e, u) { t(n, e, u) && r.push(n) }), r } function p(n, r, e, u, o) { var i = -1, c = n.length; for (e || (e = R), o || (o = []); ++i < c;) { var f = n[i]; 0 < r && e(f) ? 1 < r ? p(f, r - 1, e, u, o) : t(o, f) : u || (o[o.length] = f) } return o } function s(n, t) { return n && On(n, t, Dn); } function h(n, t) { return l(t, function (t) { return U(n[t]) }) } function v(n, t) { return n > t } function b(n, t, r, e, u) { return n === t || (null == n || null == t || !H(n) && !H(t) ? n !== n && t !== t : y(n, t, r, e, b, u)) } function y(n, t, r, e, u, o) { var i = Nn(n), c = Nn(t), f = i ? "[object Array]" : hn.call(n), a = c ? "[object Array]" : hn.call(t), f = "[object Arguments]" == f ? "[object Object]" : f, a = "[object Arguments]" == a ? "[object Object]" : a, l = "[object Object]" == f, c = "[object Object]" == a, a = f == a; o || (o = []); var p = An(o, function (t) { return t[0] == n }), s = An(o, function (n) { return n[0] == t }); if (p && s) return p[1] == t; if (o.push([n, t]), o.push([t, n]), a && !l) { if (i) r = T(n, t, r, e, u, o); else n: { switch (f) { case "[object Boolean]": case "[object Date]": case "[object Number]": r = J(+n, +t); break n; case "[object Error]": r = n.name == t.name && n.message == t.message; break n; case "[object RegExp]": case "[object String]": r = n == t + ""; break n }r = false } return o.pop(), r } return 1 & r || (i = l && pn.call(n, "__wrapped__"), f = c && pn.call(t, "__wrapped__"), !i && !f) ? !!a && (r = B(n, t, r, e, u, o), o.pop(), r) : (i = i ? n.value() : n, f = f ? t.value() : t, r = u(i, f, r, e, o), o.pop(), r) } function g(n) { return typeof n == "function" ? n : null == n ? X : (typeof n == "object" ? d : r)(n) } function _(n, t) { return n < t } function j(n, t) { var r = -1, e = M(n) ? Array(n.length) : []; return mn(n, function (n, u, o) { e[++r] = t(n, u, o) }), e } function d(n) { var t = _n(n); return function (r) { var e = t.length; if (null == r) return !e; for (r = Object(r); e--;) { var u = t[e]; if (!(u in r && b(n[u], r[u], 3))) return false } return true } } function m(n, t) { return n = Object(n), C(t, function (t, r) { return r in n && (t[r] = n[r]), t }, {}) } function O(n) { return xn(I(n, void 0, X), n + ""); } function x(n, t, r) { var e = -1, u = n.length; for (0 > t && (t = -t > u ? 0 : u + t), r = r > u ? u : r, 0 > r && (r += u), u = t > r ? 0 : r - t >>> 0, t >>>= 0, r = Array(u); ++e < u;)r[e] = n[e + t]; return r } function A(n) { return x(n, 0, n.length) } function E(n, t) { var r; return mn(n, function (n, e, u) { return r = t(n, e, u), !r }), !!r } function w(n, r) { return C(r, function (n, r) { return r.func.apply(r.thisArg, t([n], r.args)) }, n) } function k(n, t, r) { var e = !r; r || (r = {}); for (var u = -1, o = t.length; ++u < o;) { var i = t[u], c = Z; if (c === Z && (c = n[i]), e) r[i] = c; else { var f = r, a = f[i]; pn.call(f, i) && J(a, c) && (c !== Z || i in f) || (f[i] = c); } } return r } function N(n) { return O(function (t, r) { var e = -1, u = r.length, o = 1 < u ? r[u - 1] : Z, o = 3 < n.length && typeof o == "function" ? (u--, o) : Z; for (t = Object(t); ++e < u;) { var i = r[e]; i && n(t, i, e, o) } return t }) } function F(n) { return function () { var t = arguments, r = dn(n.prototype), t = n.apply(r, t); return V(t) ? t : r } } function S(n, t, r) { function e() { for (var o = -1, i = arguments.length, c = -1, f = r.length, a = Array(f + i), l = this && this !== on && this instanceof e ? u : n; ++c < f;)a[c] = r[c]; for (; i--;)a[c++] = arguments[++o]; return l.apply(t, a) } if (typeof n != "function") throw new TypeError("Expected a function"); var u = F(n); return e } function T(n, t, r, e, u, o) { var i = n.length, c = t.length; if (i != c && !(1 & r && c > i)) return false; var c = o.get(n), f = o.get(t); if (c && f) return c == t && f == n; for (var c = -1, f = true, a = 2 & r ? [] : Z; ++c < i;) { var l = n[c], p = t[c]; if (void 0 !== Z) { f = false; break } if (a) { if (!E(t, function (n, t) { if (!P(a, t) && (l === n || u(l, n, r, e, o))) return a.push(t) })) { f = false; break } } else if (l !== p && !u(l, p, r, e, o)) { f = false; break } } return f } function B(n, t, r, e, u, o) { var i = 1 & r, c = Dn(n), f = c.length, a = Dn(t).length; if (f != a && !i) return false; for (a = f; a--;) { var l = c[a]; if (!(i ? l in t : pn.call(t, l))) return false; } var p = o.get(n), l = o.get(t); if (p && l) return p == t && l == n; for (p = true; ++a < f;) { var l = c[a], s = n[l], h = t[l]; if (void 0 !== Z || s !== h && !u(s, h, r, e, o)) { p = false; break } i || (i = "constructor" == l) } return p && !i && (r = n.constructor, e = t.constructor, r != e && "constructor" in n && "constructor" in t && !(typeof r == "function" && r instanceof r && typeof e == "function" && e instanceof e) && (p = false)), p } function R(t) { return Nn(t) || n(t) } function D(n) { var t = []; if (null != n) for (var r in Object(n)) t.push(r); return t } function I(n, t, r) { return t = jn(t === Z ? n.length - 1 : t, 0), function () { for (var e = arguments, u = -1, o = jn(e.length - t, 0), i = Array(o); ++u < o;)i[u] = e[t + u]; for (u = -1, o = Array(t + 1); ++u < t;)o[u] = e[u]; return o[t] = r(i), n.apply(this, o) } } function $(n) { return (null == n ? 0 : n.length) ? p(n, 1) : [] } function q(n) { return n && n.length ? n[0] : Z } function P(n, t, r) { var e = null == n ? 0 : n.length; r = typeof r == "number" ? 0 > r ? jn(e + r, 0) : r : 0, r = (r || 0) - 1; for (var u = t === t; ++r < e;) { var o = n[r]; if (u ? o === t : o !== o) return r } return -1 } function z(n, t) { return mn(n, g(t)) } function C(n, t, r) { return e(n, g(t), r, 3 > arguments.length, mn); } function G(n, t) { var r; if (typeof t != "function") throw new TypeError("Expected a function"); return n = Fn(n), function () { return 0 < --n && (r = t.apply(this, arguments)), 1 >= n && (t = Z), r } } function J(n, t) { return n === t || n !== n && t !== t } function M(n) { var t; return (t = null != n) && (t = n.length, t = typeof t == "number" && -1 < t && 0 == t % 1 && 9007199254740991 >= t), t && !U(n) } function U(n) { return !!V(n) && (n = hn.call(n), "[object Function]" == n || "[object GeneratorFunction]" == n || "[object AsyncFunction]" == n || "[object Proxy]" == n) } function V(n) { var t = typeof n; return null != n && ("object" == t || "function" == t) } function H(n) { return null != n && typeof n == "object" } function K(n) { return typeof n == "number" || H(n) && "[object Number]" == hn.call(n) } function L(n) { return typeof n == "string" || !Nn(n) && H(n) && "[object String]" == hn.call(n) } function Q(n) { return typeof n == "string" ? n : null == n ? "" : n + "" } function W(n) { return null == n ? [] : u(n, Dn(n)) } function X(n) { return n } function Y(n, r, e) { var u = Dn(r), o = h(r, u); null != e || V(r) && (o.length || !u.length) || (e = r, r = n, n = this, o = h(r, Dn(r))); var i = !(V(e) && "chain" in e && !e.chain), c = U(n); return mn(o, function (e) { var u = r[e]; n[e] = u, c && (n.prototype[e] = function () { var r = this.__chain__; if (i || r) { var e = n(this.__wrapped__); return (e.__actions__ = A(this.__actions__)).push({ func: u, args: arguments, thisArg: n }), e.__chain__ = r, e } return u.apply(n, t([this.value()], arguments)) }) }), n } var Z, nn = 1 / 0, tn = /[&<>"']/g, rn = RegExp(tn.source), en = /^(?:0|[1-9]\d*)$/, un = typeof self == "object" && self && self.Object === Object && self, on = typeof global == "object" && global && global.Object === Object && global || un || Function("return this")(), cn = (un = typeof exports == "object" && exports && !exports.nodeType && exports) && typeof module == "object" && module && !module.nodeType && module, fn = function (n) { return function (t) { return null == n ? Z : n[t] } }({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }), an = Array.prototype, ln = Object.prototype, pn = ln.hasOwnProperty, sn = 0, hn = ln.toString, vn = on._, bn = Object.create, yn = ln.propertyIsEnumerable, gn = on.isFinite, _n = function (n, t) { return function (r) { return n(t(r)) } }(Object.keys, Object), jn = Math.max, dn = function () { function n() { } return function (t) { return V(t) ? bn ? bn(t) : (n.prototype = t, t = new n, n.prototype = Z, t) : {} } }(); i.prototype = dn(o.prototype), i.prototype.constructor = i; var mn = function (n, t) { return function (r, e) { if (null == r) return r; if (!M(r)) return n(r, e); for (var u = r.length, o = t ? u : -1, i = Object(r); (t ? o-- : ++o < u) && false !== e(i[o], o, i);); return r } }(s), On = function (n) { return function (t, r, e) { var u = -1, o = Object(t); e = e(t); for (var i = e.length; i--;) { var c = e[n ? i : ++u]; if (false === r(o[c], c, o)) break } return t } }(), xn = X, An = function (n) { return function (t, r, e) { var u = Object(t); if (!M(t)) { var o = g(r); t = Dn(t), r = function (n) { return o(u[n], n, u) } } return r = n(t, r, e), -1 < r ? u[o ? t[r] : r] : Z } }(function (n, t, r) { var e = null == n ? 0 : n.length; if (!e) return -1; r = null == r ? 0 : Fn(r), 0 > r && (r = jn(e + r, 0)); n: { for (t = g(t), e = n.length, r += -1; ++r < e;)if (t(n[r], r, n)) { n = r; break n } n = -1 } return n }), En = O(function (n, t, r) { return S(n, t, r) }), wn = O(function (n, t) { return c(n, 1, t) }), kn = O(function (n, t, r) { return c(n, Sn(t) || 0, r) }), Nn = Array.isArray, Fn = Number, Sn = Number, Tn = N(function (n, t) { k(t, _n(t), n) }), Bn = N(function (n, t) { k(t, D(t), n) }), Rn = O(function (n, t) { n = Object(n); var r, e = -1, u = t.length, o = 2 < u ? t[2] : Z; if (r = o) { r = t[0]; var i = t[1]; if (V(o)) { var c = typeof i; if ("number" == c) { if (c = M(o)) var c = o.length, f = typeof i, c = null == c ? 9007199254740991 : c, c = !!c && ("number" == f || "symbol" != f && en.test(i)) && -1 < i && 0 == i % 1 && i < c; } else c = "string" == c && i in o; r = !!c && J(o[i], r) } else r = false } for (r && (u = 1); ++e < u;)for (o = t[e], r = In(o), i = -1, c = r.length; ++i < c;) { var f = r[i], a = n[f]; (a === Z || J(a, ln[f]) && !pn.call(n, f)) && (n[f] = o[f]) } return n }), Dn = _n, In = D, $n = function (n) { return xn(I(n, Z, $), n + "") }(function (n, t) { return null == n ? {} : m(n, t) }); o.assignIn = Bn, o.before = G, o.bind = En, o.chain = function (n) { return n = o(n), n.__chain__ = true, n }, o.compact = function (n) { return l(n, Boolean) }, o.concat = function () { var n = arguments.length; if (!n) return []; for (var r = Array(n - 1), e = arguments[0]; n--;)r[n - 1] = arguments[n]; return t(Nn(e) ? A(e) : [e], p(r, 1)) }, o.create = function (n, t) { var r = dn(n); return null == t ? r : Tn(r, t) }, o.defaults = Rn, o.defer = wn, o.delay = kn, o.filter = function (n, t) { return l(n, g(t)) }, o.flatten = $, o.flattenDeep = function (n) { return (null == n ? 0 : n.length) ? p(n, nn) : [] }, o.iteratee = g, o.keys = Dn, o.map = function (n, t) { return j(n, g(t)) }, o.matches = function (n) { return d(Tn({}, n)) }, o.mixin = Y, o.negate = function (n) { if (typeof n != "function") throw new TypeError("Expected a function"); return function () { return !n.apply(this, arguments) } }, o.once = function (n) { return G(2, n) }, o.pick = $n, o.slice = function (n, t, r) { var e = null == n ? 0 : n.length; return r = r === Z ? e : +r, e ? x(n, null == t ? 0 : +t, r) : [] }, o.sortBy = function (n, t) { var e = 0; return t = g(t), j(j(n, function (n, r, u) { return { value: n, index: e++, criteria: t(n, r, u) } }).sort(function (n, t) { var r; n: { r = n.criteria; var e = t.criteria; if (r !== e) { var u = r !== Z, o = null === r, i = r === r, c = e !== Z, f = null === e, a = e === e; if (!f && r > e || o && c && a || !u && a || !i) { r = 1; break n } if (!o && r < e || f && u && i || !c && i || !a) { r = -1; break n } } r = 0 } return r || n.index - t.index }), r("value")) }, o.tap = function (n, t) { return t(n), n }, o.thru = function (n, t) { return t(n) }, o.toArray = function (n) { return M(n) ? n.length ? A(n) : [] : W(n) }, o.values = W, o.extend = Bn, Y(o, o), o.clone = function (n) { return V(n) ? Nn(n) ? A(n) : k(n, _n(n)) : n }, o.escape = function (n) { return (n = Q(n)) && rn.test(n) ? n.replace(tn, fn) : n }, o.every = function (n, t, r) { return t = r ? Z : t, f(n, g(t)) }, o.find = An, o.forEach = z, o.has = function (n, t) { return null != n && pn.call(n, t) }, o.head = q, o.identity = X, o.indexOf = P, o.isArguments = n, o.isArray = Nn, o.isBoolean = function (n) { return true === n || false === n || H(n) && "[object Boolean]" == hn.call(n); }, o.isDate = function (n) { return H(n) && "[object Date]" == hn.call(n) }, o.isEmpty = function (t) { return M(t) && (Nn(t) || L(t) || U(t.splice) || n(t)) ? !t.length : !_n(t).length }, o.isEqual = function (n, t) { return b(n, t) }, o.isFinite = function (n) { return typeof n == "number" && gn(n) }, o.isFunction = U, o.isNaN = function (n) { return K(n) && n != +n }, o.isNull = function (n) { return null === n }, o.isNumber = K, o.isObject = V, o.isRegExp = function (n) { return H(n) && "[object RegExp]" == hn.call(n) }, o.isString = L, o.isUndefined = function (n) { return n === Z }, o.last = function (n) { var t = null == n ? 0 : n.length; return t ? n[t - 1] : Z }, o.max = function (n) { return n && n.length ? a(n, X, v) : Z }, o.min = function (n) { return n && n.length ? a(n, X, _) : Z }, o.noConflict = function () { return on._ === this && (on._ = vn), this }, o.noop = function () { }, o.reduce = C, o.result = function (n, t, r) { return t = null == n ? Z : n[t], t === Z && (t = r), U(t) ? t.call(n) : t }, o.size = function (n) { return null == n ? 0 : (n = M(n) ? n : _n(n), n.length) }, o.some = function (n, t, r) { return t = r ? Z : t, E(n, g(t)) }, o.uniqueId = function (n) { var t = ++sn; return Q(n) + t }, o.each = z, o.first = q, Y(o, function () { var n = {}; return s(o, function (t, r) { pn.call(o.prototype, r) || (n[r] = t) }), n }(), { chain: false }), o.VERSION = "4.17.21", mn("pop join replace reverse split push shift sort splice unshift".split(" "), function (n) { var t = (/^(?:replace|split)$/.test(n) ? String.prototype : an)[n], r = /^(?:push|sort|unshift)$/.test(n) ? "tap" : "thru", e = /^(?:pop|join|replace|shift)$/.test(n); o.prototype[n] = function () { var n = arguments; if (e && !this.__chain__) { var u = this.value(); return t.apply(Nn(u) ? u : [], n) } return this[r](function (r) { return t.apply(Nn(r) ? r : [], n); }) } }), o.prototype.toJSON = o.prototype.valueOf = o.prototype.value = function () { return w(this.__wrapped__, this.__actions__) }, typeof define == "function" && typeof define.amd == "object" && define.amd ? (on._ = o, define(function () { return o })) : cn ? ((cn.exports = o)._ = o, un._ = o) : on._ = o }).call(this);
    };

    window.load_lodash = load_lodash;

    const r0 = {
        signals: {
            notify(text) {
                // Create a new notification element
                var notification = document.createElement('div');
                notification.classList.add('notification');
                notification.textContent = text;

                // Add the notification to the page
                var container = document.getElementById('notification-container');
                container.appendChild(notification);

                // Set the timeout to remove the notification after 10 seconds
                setTimeout(function () {
                    container.removeChild(notification);
                }, 10000);
            }
        },
        utils: {
            async load_script_url(url) {
                return new Promise(resolve => {
                    const script = document.createElement('script');
                    script.src = url;
                    script.onload = () => resolve(true);
                    document.head.appendChild(script);
                });
            },
            dispatch_event_on_element(event_name, element) {
                const event = new Event(event_name, {
                    "view": window,
                    "bubbles": true,
                    "cancelable": false
                });

                element.dispatchEvent(event);
                // Try calling on<event> property
                if (typeof element['on' + event_name] === 'function') {
                    element['on' + event_name]();
                }
            },
            inject_css(css) {
                var style = document.createElement('style');
                style.textContent = css;
                document.head.appendChild(style);
            },
            inject_css_url(cssUrl) {
                var head = document.head || document.getElementsByTagName('head')[0];
                var link = document.createElement('link');
                link.rel = 'stylesheet';
                link.type = 'text/css';
                link.href = cssUrl;
                head.appendChild(link);
            },
            download_file(content, filename) {
                const element = document.createElement('a');
                element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(content));
                element.setAttribute('download', filename);
                element.style.display = 'none';
                document.body.appendChild(element);
                element.click();
                document.body.removeChild(element);
            },
            download_json(content, filename) {
                return r0.utils.download_file(JSON.stringify(content, null, 2), filename)
            },
            download_first_image(element, filename) {
                let img;
                if (element.tagName === 'IMG') {
                    img = element;
                } else {
                    img = element.querySelector('img');
                }
                if (img) {
                    const canvas = document.createElement('canvas');
                    canvas.width = img.naturalWidth;
                    canvas.height = img.naturalHeight;
                    const ctx = canvas.getContext('2d');
                    ctx.drawImage(img, 0, 0, img.naturalWidth, img.naturalHeight);
                    canvas.toBlob(blob => {
                        const element = document.createElement('a');
                        element.href = URL.createObjectURL(blob);
                        element.download = filename;
                        element.style.display = 'none';
                        document.body.appendChild(element);
                        element.click();
                        document.body.removeChild(element);
                    });
                } else {
                    console.error('No image element found.');
                }
            },
            download_largest_image(element, filename) {
                let img;
                if (element.tagName === 'IMG') {
                    img = element;
                } else {
                    const images = Array.from(element.querySelectorAll('img'));
                    const sortedImages = _.sortBy(images, img => img.naturalWidth * img.naturalHeight);
                    img = sortedImages[sortedImages.length - 1];
                }
                if (img) {
                    const canvas = document.createElement('canvas');
                    canvas.width = img.naturalWidth;
                    canvas.height = img.naturalHeight;
                    const ctx = canvas.getContext('2d');
                    ctx.drawImage(img, 0, 0, img.naturalWidth, img.naturalHeight);
                    canvas.toBlob(blob => {
                        const element = document.createElement('a');
                        element.href = URL.createObjectURL(blob);
                        element.download = filename;
                        element.style.display = 'none';
                        document.body.appendChild(element);
                        element.click();
                        document.body.removeChild(element);
                    });
                } else {
                    console.error('No image element found.');
                }
            },
            download_largest_image_xhr(element, filename) {
                let img;
                if (element.tagName === 'IMG') {
                    img = element;
                } else {
                    const images = Array.from(element.querySelectorAll('img'));
                    const sortedImages = _.sortBy(images, img => img.naturalWidth * img.naturalHeight);
                    img = sortedImages[sortedImages.length - 1];
                }
                if (img) {
                    const xhr = new XMLHttpRequest();
                    xhr.open('GET', img.src, true);
                    xhr.responseType = 'arraybuffer';
                    xhr.onload = function () {
                        const blob = new Blob([xhr.response], { type: 'image/png' });
                        const url = URL.createObjectURL(blob);
                        const link = document.createElement('a');
                        link.href = url;
                        link.download = filename;
                        link.click();
                        URL.revokeObjectURL(url);
                    };
                    xhr.send();
                } else {
                    console.error('No image element found.');
                }
            },
            download_largest_image_fetch(element, filename) {
                let img;
                if (element.tagName === 'IMG') {
                    img = element;
                } else {
                    const images = Array.from(element.querySelectorAll('img'));
                    const sortedImages = _.sortBy(images, img => img.naturalWidth * img.naturalHeight);
                    img = sortedImages[sortedImages.length - 1];
                }
                if (img) {
                    fetch(img.src)
                        .then(response => response.blob())
                        .then(blob => {
                            const url = URL.createObjectURL(blob);
                            const link = document.createElement('a');
                            link.href = url;
                            link.download = filename;
                            link.click();
                            URL.revokeObjectURL(url);
                        })
                        .catch(error => {
                            console.error(error);
                        });
                } else {
                    console.error('No image element found.');
                }
            },
            get_texts_or_attributes(selector, attribute_name) {
                const elements = document.querySelectorAll(selector);
                const result = [];
                for (let i = 0; i < elements.length; i++) {
                    const element = elements[i];
                    if (attribute_name) {
                        const value = element.getAttribute(attribute_name);
                        if (value) {
                            result.push(value);
                        }
                    } else {
                        const text = element.textContent.trim();
                        if (text) {
                            result.push(text);
                        }
                    }
                }
                return result;
            },
            wait(seconds = 1) {
                return new Promise((resolve) => setTimeout(resolve, seconds))
            },
            wait_for_elements(selector, elements_count = 1, timeout = 30 * 1000) {
                return new Promise((resolve, reject) => {
                    let started_at = +new Date()
                    let id = setInterval(() => {
                        let elements = document.querySelectorAll(selector)
                        if (elements.length == elements_count) {
                            clearInterval(id)
                            resolve(elements)
                        }
                        if (+new Date() - started_at >= timeout) {
                            clearInterval(id)
                            reject()
                        }
                    }, 1000 / 15)
                })
            }
        },
        libs_loaders: {
            lodash: load_lodash
        },
        initializers: {
            libs() {
                r0.libs_loaders.lodash()
            },
            notifications() {
                // Add CSS styles for the notifications
                r0.utils.inject_css(`
                    #notification-container {
                        position: fixed;
                        bottom: 8px;
                        left: 8px;
                        width: 100%;
                        max-width: 300px;
                        min-width: 100px;
                        display: flex;
                        flex-direction: column-reverse;
                        z-index: 9999;
                    }

                    .notification {
                        background-color: #333;
                        color: #fff;
                        padding: 10px;
                        margin-bottom: 10px;
                        animation: slide-up 0.25s ease-out;
                    }

                    @keyframes slide-up {
                        0% {
                        transform: translateY(100%);
                        }
                        100% {
                        transform: translateY(0);
                        }
                    }
                `)

                // Create the container element for the notifications
                var container = document.createElement('div');
                container.id = 'notification-container';
                document.body.appendChild(container);
            }
        },
        async init() {
            r0.initializers.libs()
            r0.initializers.notifications()

            r0.signals.notify('r0 intialized')
        }
    }

    window.r0 = r0;
})();