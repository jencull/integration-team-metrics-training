#!/usr/bin/env python3
"""
Build the Konflux Metrics Training Guide HTML document.
Extracts content from Obsidian vault and generates a self-contained HTML file.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple

# Prism.js for syntax highlighting (minified, embedded inline)
# Languages: YAML, Bash, PromQL
# Theme: Tomorrow Night
PRISM_CSS = """
code[class*=language-],pre[class*=language-]{color:#ccc;background:0 0;font-family:Consolas,Monaco,'Andale Mono','Ubuntu Mono',monospace;font-size:1em;text-align:left;white-space:pre;word-spacing:normal;word-break:normal;word-wrap:normal;line-height:1.5;tab-size:4;hyphens:none}pre[class*=language-]{padding:1em;margin:.5em 0;overflow:auto}:not(pre)>code[class*=language-],pre[class*=language-]{background:#2d2d2d}:not(pre)>code[class*=language-]{padding:.1em;border-radius:.3em;white-space:normal}.token.comment,.token.block-comment,.token.prolog,.token.doctype,.token.cdata{color:#999}.token.punctuation{color:#ccc}.token.tag,.token.attr-name,.token.namespace,.token.deleted{color:#e2777a}.token.function-name{color:#6196cc}.token.boolean,.token.number,.token.function{color:#f08d49}.token.property,.token.class-name,.token.constant,.token.symbol{color:#f8c555}.token.selector,.token.important,.token.atrule,.token.keyword,.token.builtin{color:#cc99cd}.token.string,.token.char,.token.attr-value,.token.regex,.token.variable{color:#7ec699}.token.operator,.token.entity,.token.url{color:#67cdcc}.token.important,.token.bold{font-weight:700}.token.italic{font-style:italic}.token.entity{cursor:help}.token.inserted{color:green}
"""

PRISM_JS = """
var _self="undefined"!=typeof window?window:"undefined"!=typeof WorkerGlobalScope&&self instanceof WorkerGlobalScope?self:{},Prism=function(u){var t=/(?:^|\\s)lang(?:uage)?-(\\w+)(?=\\s|$)/i,n=0,e={},M={manual:u.Prism&&u.Prism.manual,disableWorkerMessageHandler:u.Prism&&u.Prism.disableWorkerMessageHandler,util:{encode:function e(n){return n instanceof W?new W(n.type,e(n.content),n.alias):Array.isArray(n)?n.map(e):n.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/\\u00a0/g," ")},type:function(e){return Object.prototype.toString.call(e).slice(8,-1)},objId:function(e){return e.__id||Object.defineProperty(e,"__id",{value:++n}),e.__id},clone:function t(e,r){var a,n;switch(r=r||{},M.util.type(e)){case"Object":if(n=M.util.objId(e),r[n])return r[n];for(var i in a={},r[n]=a,e)e.hasOwnProperty(i)&&(a[i]=t(e[i],r));return a;case"Array":return n=M.util.objId(e),r[n]?r[n]:(a=[],r[n]=a,e.forEach(function(e,n){a[n]=t(e,r)}),a);default:return e}},getLanguage:function(e){for(;e;){var n=t.exec(e.className);if(n)return n[1].toLowerCase();e=e.parentElement}return"none"},setLanguage:function(e,n){e.className=e.className.replace(RegExp(t,"gi"),""),e.classList.add("language-"+n)},currentScript:function(){if("undefined"==typeof document)return null;if("currentScript"in document)return document.currentScript;try{throw new Error}catch(e){var n=(/at [^(\\r\\n]*\\((.*):[^:]+:[^:]+\\)$/i.exec(e.stack)||[])[1];if(n){var t=document.getElementsByTagName("script");for(var r in t)if(t[r].src==n)return t[r]}return null}},isActive:function(e,n,t){for(var r="no-"+n;e;){var a=e.classList;if(a.contains(n))return!0;if(a.contains(r))return!1;e=e.parentElement}return!!t}},languages:{plain:e,plaintext:e,text:e,txt:e,extend:function(e,n){var t=M.util.clone(M.languages[e]);for(var r in n)t[r]=n[r];return t},insertBefore:function(t,e,n,r){var a=(r=r||M.languages)[t],i={};for(var l in a)if(a.hasOwnProperty(l)){if(l==e)for(var o in n)n.hasOwnProperty(o)&&(i[o]=n[o]);n.hasOwnProperty(l)||(i[l]=a[l])}var s=r[t];return r[t]=i,M.languages.DFS(M.languages,function(e,n){n===s&&e!=t&&(this[e]=i)}),i},DFS:function e(n,t,r,a){a=a||{};var i=M.util.objId;for(var l in n)if(n.hasOwnProperty(l)){t.call(n,l,n[l],r||l);var o=n[l],s=M.util.type(o);"Object"!==s||a[i(o)]?"Array"!==s||a[i(o)]||(a[i(o)]=!0,e(o,t,l,a)):(a[i(o)]=!0,e(o,t,null,a))}}},plugins:{},highlightAll:function(e,n){M.highlightAllUnder(document,e,n)},highlightAllUnder:function(e,n,t){var r={callback:t,container:e,selector:'code[class*="language-"], [class*="language-"] code, code[class*="lang-"], [class*="lang-"] code'};M.hooks.run("before-highlightall",r),r.elements=Array.prototype.slice.apply(r.container.querySelectorAll(r.selector)),M.hooks.run("before-all-elements-highlight",r);for(var a,i=0;a=r.elements[i++];)M.highlightElement(a,!0===n,r.callback)},highlightElement:function(e,n,t){var r=M.util.getLanguage(e),a=M.languages[r];M.util.setLanguage(e,r);var i=e.parentElement;i&&"pre"===i.nodeName.toLowerCase()&&M.util.setLanguage(i,r);var l={element:e,language:r,grammar:a,code:e.textContent};function o(e){l.highlightedCode=e,M.hooks.run("before-insert",l),l.element.innerHTML=l.highlightedCode,M.hooks.run("after-highlight",l),M.hooks.run("complete",l),t&&t.call(l.element)}if(M.hooks.run("before-sanity-check",l),(i=l.element.parentElement)&&"pre"===i.nodeName.toLowerCase()&&!i.hasAttribute("tabindex")&&i.setAttribute("tabindex","0"),!l.code)return M.hooks.run("complete",l),void(t&&t.call(l.element));if(M.hooks.run("before-highlight",l),l.grammar)if(n&&u.Worker){var s=new Worker(M.filename);s.onmessage=function(e){o(e.data)},s.postMessage(JSON.stringify({language:l.language,code:l.code,immediateClose:!0}))}else o(M.highlight(l.code,l.grammar,l.language));else o(M.util.encode(l.code))},highlight:function(e,n,t){var r={code:e,grammar:n,language:t};if(M.hooks.run("before-tokenize",r),!r.grammar)throw new Error('The language "'+r.language+'" has no grammar.');return r.tokens=M.tokenize(r.code,r.grammar),M.hooks.run("after-tokenize",r),W.stringify(M.util.encode(r.tokens),r.language)},tokenize:function(e,n){var t=n.rest;if(t){for(var r in t)n[r]=t[r];delete n.rest}var a=new i;return I(a,a.head,e),function e(n,t,r,a,i,l){for(var o in r)if(r.hasOwnProperty(o)&&r[o]){var s=r[o];s=Array.isArray(s)?s:[s];for(var u=0;u<s.length;++u){if(l&&l.cause==o+","+u)return;var c=s[u],g=c.inside,f=!!c.lookbehind,h=!!c.greedy,d=c.alias;if(h&&!c.pattern.global){var p=c.pattern.toString().match(/[imsuy]*$/)[0];c.pattern=RegExp(c.pattern.source,p+"g")}for(var v=c.pattern||c,m=a.next,y=i;m!==t.tail&&!(l&&y>=l.reach);y+=m.value.length,m=m.next){var k=m.value;if(t.length>n.length)return;if(!(k instanceof W)){var x,b=1;if(h){if(!(x=z(v,y,n,f))||x.index>=n.length)break;var w=x.index,A=x.index+x[0].length,P=y;for(P+=m.value.length;P<=w;)m=m.next,P+=m.value.length;if(P-=m.value.length,y=P,m.value instanceof W)continue;for(var E=m;E!==t.tail&&(P<A||"string"==typeof E.value);E=E.next)b++,P+=E.value.length;b--,k=n.slice(y,P),x.index-=y}else if(!(x=z(v,0,k,f)))continue;var w=x.index,L=x[0],S=k.slice(0,w),O=k.slice(w+L.length),j=y+k.length;l&&j>l.reach&&(l.reach=j);var C=m.prev;S&&(C=I(t,C,S),y+=S.length),q(t,C,b);var N=new W(o,g?M.tokenize(L,g):L,d,L);if(m=I(t,C,N),O&&I(t,m,O),1<b){var _={cause:o+","+u,reach:j};e(n,t,r,m.prev,y,_),l&&_.reach>l.reach&&(l.reach=_.reach)}}}}}}(e,a,n,a.head,0),function(e){var n=[],t=e.head.next;for(;t!==e.tail;)n.push(t.value),t=t.next;return n}(a)},hooks:{all:{},add:function(e,n){var t=M.hooks.all;t[e]=t[e]||[],t[e].push(n)},run:function(e,n){var t=M.hooks.all[e];if(t&&t.length)for(var r,a=0;r=t[a++];)r(n)}},Token:W};function W(e,n,t,r){this.type=e,this.content=n,this.alias=t,this.length=0|(r||"").length}function z(e,n,t,r){e.lastIndex=n;var a=e.exec(t);if(a&&r&&a[1]){var i=a[1].length;a.index+=i,a[0]=a[0].slice(i)}return a}function i(){var e={value:null,prev:null,next:null},n={value:null,prev:e,next:null};e.next=n,this.head=e,this.tail=n,this.length=0}function I(e,n,t){var r=n.next,a={value:t,prev:n,next:r};return n.next=a,r.prev=a,e.length++,a}function q(e,n,t){for(var r=n.next,a=0;a<t&&r!==e.tail;a++)r=r.next;(n.next=r).prev=n,e.length-=a}if(u.Prism=M,W.stringify=function n(e,t){if("string"==typeof e)return e;if(Array.isArray(e)){var r="";return e.forEach(function(e){r+=n(e,t)}),r}var a={type:e.type,content:n(e.content,t),tag:"span",classes:["token",e.type],attributes:{},language:t},i=e.alias;i&&(Array.isArray(i)?Array.prototype.push.apply(a.classes,i):a.classes.push(i)),M.hooks.run("wrap",a);var l="";for(var o in a.attributes)l+=" "+o+'="'+(a.attributes[o]||"").replace(/"/g,"&quot;")+'"';return"<"+a.tag+' class="'+a.classes.join(" ")+'"'+l+">"+a.content+"</"+a.tag+">"},!u.document)return u.addEventListener&&(M.disableWorkerMessageHandler||u.addEventListener("message",function(e){var n=JSON.parse(e.data),t=n.language,r=n.code,a=n.immediateClose;u.postMessage(M.highlight(r,M.languages[t],t)),a&&u.close()},!1)),M;var r=M.util.currentScript();function a(){M.manual||M.highlightAll()}if(r&&(M.filename=r.src,r.hasAttribute("data-manual")&&(M.manual=!0)),!M.manual){var l=document.readyState;"loading"===l||"interactive"===l&&r&&r.defer?document.addEventListener("DOMContentLoaded",a):window.requestAnimationFrame?window.requestAnimationFrame(a):window.setTimeout(a,16)}return M}(_self);"undefined"!=typeof module&&module.exports&&(module.exports=Prism),"undefined"!=typeof global&&(global.Prism=Prism);
Prism.languages.yaml={scalar:{pattern:/([-:]\\s*(?:![^\\s]+)?[ \\t]*[|>])[ \\t]*(?:((?:\\r?\\n|\\r)[ \\t]+)\\S[^\\r\\n]*(?:\\2[^\\r\\n]+)*)/,lookbehind:!0,alias:"string"},comment:/#.*/,key:{pattern:/(\s*(?:^|[:\\-,[{\\r\\n?])[ \\t]*(?:![^\\s]+)?[ \\t]*)[^\\r\\n{[\\]},#\\s]+?(?=\\s*:\\s)/,lookbehind:!0,alias:"atrule"},directive:{pattern:/(^[ \\t]*)%.+/m,lookbehind:!0,alias:"important"},datetime:{pattern:/([:\\-,[{]\\s*(?:![^\\s]+)?[ \\t]*)\\d{4}-\\d\\d?-\\d\\d?(?:[tT]|[ \\t]+)\\d\\d?:\\d{2}:\\d{2}(?:\\.\\d*)?[ \\t]*(?:Z|[-+]\\d\\d?(?::\\d{2})?)?(?=[ \\t]*(?:$|,|]|}))/m,lookbehind:!0,alias:"number"},boolean:{pattern:/([:\\-,[{]\\s*(?:![^\\s]+)?[ \\t]*)(?:true|false)[ \\t]*(?=$|,|]|})/im,lookbehind:!0,alias:"important"},null:{pattern:/([:\\-,[{]\\s*(?:![^\\s]+)?[ \\t]*)(?:null|~)[ \\t]*(?=$|,|]|})/im,lookbehind:!0,alias:"important"},string:{pattern:/([:\\-,[{]\\s*(?:![^\\s]+)?[ \\t]*)("|')(?:(?!\\2)[^\\\\\\r\\n]|\\\\.)*\\2(?=[ \\t]*(?:$|,|]|}))/m,lookbehind:!0,greedy:!0},number:{pattern:/([:\\-,[{]\\s*(?:![^\\s]+)?[ \\t]*)[+\\-]?(?:0x[\\da-f]+|0o[0-7]+|(?:\\d+(?:\\.\\d*)?|\\.\\d+)(?:e[+\\-]?\\d+)?|\\.inf|\\.nan)[ \\t]*(?=$|,|]|})/im,lookbehind:!0},tag:/![^\\s]+/,important:/[&*][\\w]+/,punctuation:/---|[:,[\\]{}\\-?|>?]|\\.\\.\\.}/;
Prism.languages.bash={shebang:{pattern:/^#!\\s*\\/.*/,alias:"important"},comment:{pattern:/(^|[^"{\\\\$])#.*/,lookbehind:!0},string:[{pattern:/((?:^|[^<])<<\\s*)["']?(\\w+?)["']?\\s*\\r?\\n(?:[\\s\\S])*?\\r?\\n\\2/,lookbehind:!0,greedy:!0},{pattern:/(["'])(?:\\\\[\\s\\S]|(?!\\1)[^\\\\])*\\1/g,greedy:!0}],variable:[{pattern:/\\$(?:\\w+(?:_\\w+)*|{[^}]+})/},{pattern:/\\$\\([^)]+\\)/,inside:{variable:/^\\$\\(/,string:/^\\(|\\)$/}},{pattern:/`[^`]+`/,inside:{variable:/^`|`$/}}],function:{pattern:/(^|[\\s;|&])(?:alias|apropos|apt-get|aptitude|aspell|awk|basename|bash|bc|bg|builtin|bzip2|cal|cat|cd|cfdisk|chgrp|chmod|chown|chroot|chkconfig|cksum|clear|cmp|comm|command|cp|cron|crontab|csplit|cut|date|dc|dd|ddrescue|declare|df|diff|diff3|dig|dir|dircolors|dirname|dirs|dmesg|du|echo|egrep|eject|enable|env|ethtool|eval|exec|exit|expand|expect|export|expr|fdformat|fdisk|fg|fgrep|file|find|fmt|fold|format|free|fsck|ftp|function|fuser|gawk|getopts|git|grep|groupadd|groupdel|groupmod|groups|gzip|hash|head|help|hg|history|hostname|htop|iconv|id|ifconfig|ifdown|ifup|import|install|jobs|join|kill|killall|less|let|link|ln|local|locate|logname|logout|look|lpc|lpr|lprint|lprintd|lprintq|lprm|ls|lsof|make|man|mkdir|mkfifo|mkisofs|mknod|more|most|mount|mtools|mtr|mv|mmv|nano|netstat|nice|nl|nohup|notify-send|nslookup|open|op|passwd|paste|pathchk|ping|pkill|popd|pr|printcap|printenv|printf|ps|pushd|pv|pwd|quota|quotacheck|quotactl|ram|rar|rcp|read|readarray|readonly|reboot|rename|renice|remsync|rev|rm|rmdir|rsync|screen|scp|sdiff|sed|select|seq|service|sftp|shift|shopt|shutdown|sleep|slocate|sort|source|split|ssh|stat|strace|su|sudo|sum|suspend|sync|tail|tar|tee|test|time|timeout|times|touch|top|traceroute|trap|tr|tsort|tty|type|ulimit|umask|umount|unalias|uname|unexpand|uniq|units|unrar|unset|unshar|uptime|useradd|userdel|usermod|users|uuencode|uudecode|v|vdir|vi|vmstat|wait|watch|wc|wget|whereis|which|who|whoami|write|xargs|xdg-open|yes|zip)(?=$|[)\\s;|&])/,lookbehind:!0},keyword:{pattern:/(^|[\\s;|&])(?:if|then|else|elif|fi|for|while|in|case|esac|function|select|do|done|until)(?=$|[)\\s;|&])/,lookbehind:!0},boolean:{pattern:/(^|[\\s;|&])(?:true|false)(?=$|[)\\s;|&])/,lookbehind:!0},operator:/&&?|\\|\\|?|==?|!=?|<<<?|>>|<=?|>=?|=~/,punctuation:/[{}()[\\];]/};
"""

# Main CSS styles
MAIN_CSS = """
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

:root {
    --bg-color: #ffffff;
    --text-color: #333333;
    --heading-color: #ee0000;
    --code-bg: #f5f5f5;
    --code-border: #e0e0e0;
    --sidebar-bg: #f8f8f8;
    --sidebar-active: #ee0000;
    --link-color: #0066cc;
}

html {
    scroll-behavior: smooth;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
    line-height: 1.6;
    color: var(--text-color);
    background: var(--bg-color);
    display: grid;
    grid-template-columns: 300px 1fr;
    min-height: 100vh;
}

/* Sidebar Navigation */
.sidebar {
    background: var(--sidebar-bg);
    padding: 2rem 1.5rem;
    position: sticky;
    top: 0;
    height: 100vh;
    overflow-y: auto;
    border-right: 1px solid var(--code-border);
}

.sidebar h2 {
    font-size: 1.2rem;
    margin-bottom: 1rem;
    color: var(--heading-color);
}

.sidebar nav ul {
    list-style: none;
}

.sidebar nav li {
    margin-bottom: 0.5rem;
}

.sidebar nav a {
    color: var(--text-color);
    text-decoration: none;
    display: block;
    padding: 0.5rem 0.75rem;
    border-radius: 4px;
    transition: all 0.2s;
}

.sidebar nav a:hover {
    background: rgba(238, 0, 0, 0.1);
    color: var(--heading-color);
}

.sidebar nav a.active {
    background: rgba(238, 0, 0, 0.1);
    color: var(--heading-color);
    border-left: 3px solid var(--sidebar-active);
    padding-left: calc(0.75rem - 3px);
}

.sidebar nav ul ul {
    margin-left: 1rem;
    margin-top: 0.25rem;
}

.sidebar nav ul ul a {
    font-size: 0.9rem;
}

/* Main Content */
.content {
    max-width: 900px;
    margin: 0 auto;
    padding: 3rem 2rem;
}

header {
    margin-bottom: 3rem;
    border-bottom: 3px solid var(--heading-color);
    padding-bottom: 1.5rem;
}

h1 {
    font-size: 2.5rem;
    color: var(--heading-color);
    margin-bottom: 0.5rem;
}

.subtitle {
    font-size: 1.25rem;
    color: #666;
    font-weight: normal;
}

.intro {
    margin-top: 1.5rem;
    font-size: 1.1rem;
    line-height: 1.8;
}

/* Sections */
section {
    margin-bottom: 4rem;
}

h2 {
    font-size: 2rem;
    color: var(--heading-color);
    margin-top: 2rem;
    margin-bottom: 1rem;
    padding-top: 1rem;
}

h3 {
    font-size: 1.5rem;
    color: var(--text-color);
    margin-top: 1.5rem;
    margin-bottom: 0.75rem;
}

h4 {
    font-size: 1.25rem;
    color: var(--text-color);
    margin-top: 1rem;
    margin-bottom: 0.5rem;
}

p {
    margin-bottom: 1rem;
}

/* Code Blocks */
code {
    font-family: Consolas, Monaco, 'Courier New', monospace;
    font-size: 0.9em;
}

p code, li code {
    background: var(--code-bg);
    padding: 0.2em 0.4em;
    border-radius: 3px;
    border: 1px solid var(--code-border);
}

pre {
    background: #2d2d2d;
    padding: 1.5rem;
    border-radius: 6px;
    overflow-x: auto;
    margin: 1.5rem 0;
    position: relative;
}

pre code {
    background: none;
    color: #ccc;
    padding: 0;
    border: none;
}

.code-block {
    position: relative;
}

.copy-button {
    position: absolute;
    top: 0.5rem;
    right: 0.5rem;
    background: rgba(255, 255, 255, 0.1);
    color: #ccc;
    border: 1px solid rgba(255, 255, 255, 0.2);
    padding: 0.25rem 0.75rem;
    border-radius: 4px;
    cursor: pointer;
    font-size: 0.8rem;
    opacity: 0;
    transition: opacity 0.2s;
}

.code-block:hover .copy-button {
    opacity: 1;
}

.copy-button:hover {
    background: rgba(255, 255, 255, 0.2);
}

/* Lists */
ul, ol {
    margin: 1rem 0 1rem 2rem;
}

li {
    margin-bottom: 0.5rem;
}

/* Links */
a {
    color: var(--link-color);
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}

a[target="_blank"]::after {
    content: " ↗";
    font-size: 0.8em;
}

/* Callout Boxes */
.callout {
    padding: 1rem 1.5rem;
    margin: 1.5rem 0;
    border-radius: 6px;
    border-left: 4px solid;
}

.callout.info {
    background: #e3f2fd;
    border-color: #2196f3;
}

.callout.warning {
    background: #fff8e1;
    border-color: #ffc107;
}

.callout.danger {
    background: #ffebee;
    border-color: #f44336;
}

.callout-title {
    font-weight: bold;
    margin-bottom: 0.5rem;
}

/* Back to Top Button */
.back-to-top {
    position: fixed;
    bottom: 2rem;
    right: 2rem;
    background: var(--heading-color);
    color: white;
    width: 50px;
    height: 50px;
    border-radius: 50%;
    border: none;
    font-size: 1.5rem;
    cursor: pointer;
    opacity: 0;
    transition: opacity 0.3s;
    z-index: 100;
}

.back-to-top.visible {
    opacity: 1;
}

.back-to-top:hover {
    background: #cc0000;
}

/* Responsive */
@media (max-width: 768px) {
    body {
        grid-template-columns: 1fr;
    }

    .sidebar {
        position: static;
        height: auto;
    }

    .content {
        padding: 2rem 1rem;
    }
}
"""

# JavaScript for interactivity
MAIN_JS = """
// Table of Contents active section highlighting
const observerOptions = {
    root: null,
    rootMargin: '-20% 0px -70% 0px',
    threshold: 0
};

const sections = document.querySelectorAll('section[id]');
const navLinks = document.querySelectorAll('.sidebar nav a');

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            navLinks.forEach(link => {
                link.classList.remove('active');
                if (link.getAttribute('href') === '#' + entry.target.id) {
                    link.classList.add('active');
                }
            });
        }
    });
}, observerOptions);

sections.forEach(section => observer.observe(section));

// Copy button functionality
document.querySelectorAll('.code-block').forEach(block => {
    const button = block.querySelector('.copy-button');
    const code = block.querySelector('code');

    if (button && code) {
        button.addEventListener('click', () => {
            navigator.clipboard.writeText(code.textContent).then(() => {
                button.textContent = 'Copied!';
                setTimeout(() => {
                    button.textContent = 'Copy';
                }, 2000);
            });
        });
    }
});

// Back to top button
const backToTop = document.querySelector('.back-to-top');

window.addEventListener('scroll', () => {
    if (window.scrollY > 300) {
        backToTop.classList.add('visible');
    } else {
        backToTop.classList.remove('visible');
    }
});

backToTop.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
});

// Syntax highlighting
if (typeof Prism !== 'undefined') {
    Prism.highlightAll();
}
"""

# Configuration
VAULT_PATH = Path("/Users/jcullina/ObsidianVault/Metrics")
OUTPUT_PATH = Path("/Users/jcullina/metrics-training-guide.html")
VAULT_COPY_PATH = Path("/Users/jcullina/ObsidianVault/Metrics/metrics-training-guide.html")

# Source files to extract content from
SOURCE_FILES = {
    "testing": "testing metrics changes.md",
    "severity": "Reducing or increasing severity or slo status.md",
    "push_dash": "Push dash prod.md",
    "dashboards": "Dashboard links.md",
    "observability": "Observability explanation.md",
    "prometheus": "Prometheus.md",
    "graph_types": "Graph types.md",
    "flapping": "Flapping alerts.md",
    "slo_epic": "Availability SLO 2 epic.md",
}


def read_vault_file(filename: str) -> str:
    """Read a file from the Obsidian vault."""
    file_path = VAULT_PATH / filename
    if not file_path.exists():
        print(f"Warning: {filename} not found")
        return ""

    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def extract_code_blocks(content: str, language: str = None) -> List[str]:
    """Extract code blocks from markdown content."""
    pattern = r'```(\w*)\n(.*?)```'
    matches = re.findall(pattern, content, re.DOTALL)

    if language:
        return [code for lang, code in matches if lang == language]
    return [code for _, code in matches]


def extract_links(content: str) -> List[Tuple[str, str]]:
    """Extract markdown links from content. Returns list of (url, text) tuples."""
    # Match [text](url) format
    pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    return re.findall(pattern, content)


def extract_dashboard_links(content: str) -> List[Dict[str, str]]:
    """Extract dashboard links with descriptions from Dashboard links.md."""
    dashboards = []
    lines = content.split('\n')

    for line in lines:
        # Match format: - [Name](URL) or - [Name](URL) - Description
        match = re.match(r'-\s+\[([^\]]+)\]\(([^)]+)\)(?:\s+-\s+(.+))?', line)
        if match:
            name, url, description = match.groups()
            dashboards.append({
                'name': name.strip(),
                'url': url.strip(),
                'description': description.strip() if description else ''
            })

    return dashboards


def extract_commands(content: str) -> List[str]:
    """Extract bash commands from markdown content."""
    return extract_code_blocks(content, 'bash') + extract_code_blocks(content, '')


def process_obsidian_links(content: str) -> str:
    """Convert Obsidian wiki-links [[Page]] to plain text."""
    # Remove [[]] wiki-links, keeping just the text
    content = re.sub(r'\[\[([^\]]+)\]\]', r'\1', content)
    return content


def extract_yaml_examples(content: str) -> List[str]:
    """Extract YAML code blocks."""
    return extract_code_blocks(content, 'yaml')


def build_section_1_modifying_alerts(source_content: Dict[str, str]) -> str:
    """Build Section 1: Modifying Alerts in the o11y Repository."""

    # Extract example from severity file
    severity_content = source_content.get('severity', '')
    yaml_examples = extract_yaml_examples(severity_content)
    bash_commands = extract_commands(severity_content)

    html = """
<section id="section-1">
    <h2>1. Modifying Alerts in the o11y Repository</h2>

    <p>Alerts notify the team when something goes wrong in Konflux. As an engineer, you'll often need to modify existing alerts - changing their severity, updating thresholds, or adjusting when they fire. This section teaches you how to make these changes safely.</p>

    <h3 id="section-1-1">What Alerts Are and Why We Modify Them</h3>
    <p>Alerts are rules defined in YAML files that monitor metrics. When a metric crosses a threshold (e.g., availability drops below 99%), the alert fires and sends a notification. We modify alerts to:</p>
    <ul>
        <li>Adjust sensitivity (change thresholds to reduce false positives)</li>
        <li>Change severity levels (downgrade from critical to warning if not paging-worthy)</li>
        <li>Update SLO status (control whether the alert pages SRE or just notifies the team)</li>
        <li>Fix bugs in PromQL expressions</li>
    </ul>

    <h3 id="section-1-2">File Locations</h3>
    <p>Alerts live in the <code>redhat-appstudio/o11y</code> repository:</p>
    <ul>
        <li><code>rhobs/alerting/data_plane/prometheus.*_alerts.yaml</code> - Alert rules for the data plane</li>
        <li><code>rhobs/recording/*.yaml</code> - Recording rules (pre-computed metrics used by alerts)</li>
    </ul>

    <div class="code-block">
        <button class="copy-button">Copy</button>
        <pre><code class="language-bash"># Clone the repo
git clone https://github.com/redhat-appstudio/o11y.git

# Navigate to alerts
cd rhobs/alerting/data_plane/

# List alert files
ls -la prometheus.*_alerts.yaml</code></pre>
    </div>

    <h3 id="section-1-3">Understanding Alert Structure</h3>
    <p>Here's the anatomy of an alert definition in YAML:</p>

    <div class="code-block">
        <button class="copy-button">Copy</button>
        <pre><code class="language-yaml">- alert: IntegrationServiceAvailabilitySLOViolation
  expr: |
    (
      avg_over_time(redhat_appstudio_integrationservice_global_github_app_available[24h]) * 100
    ) &lt; 99
  for: 10m
  labels:
    severity: warning
    slo: "false"
  annotations:
    summary: "Integration Service GitHub App availability below SLO"
    description: "Availability is {{ $value }}%, below the 99% threshold"
    alert_routing_key: "integration-service"</code></pre>
    </div>

    <p><strong>Key Fields:</strong></p>
    <ul>
        <li><code>alert</code> - Unique alert name (must be descriptive)</li>
        <li><code>expr</code> - PromQL expression that triggers the alert when true</li>
        <li><code>for</code> - How long the condition must be true before firing (prevents flapping)</li>
        <li><code>labels.severity</code> - <code>critical</code>, <code>warning</code>, or <code>info</code></li>
        <li><code>labels.slo</code> - <code>"true"</code> pages SRE, <code>"false"</code> notifies team only</li>
        <li><code>annotations</code> - Human-readable descriptions (support template variables like <code>{{ $value }}</code>)</li>
        <li><code>alert_routing_key</code> - Where to route when <code>slo: "false"</code> (replaces <code>alert_team_handle</code>)</li>
        <li><code>alert_team_handle</code> - SRE team handle when <code>slo: "true"</code></li>
    </ul>

    <h3 id="section-1-4">Common Modifications</h3>

    <h4>Changing Severity Levels</h4>
    <p>Severity controls urgency:</p>
    <ul>
        <li><strong>critical</strong> - Production outage, immediate response needed</li>
        <li><strong>warning</strong> - Issue that needs attention but not immediate</li>
        <li><strong>info</strong> - Informational, for awareness only</li>
    </ul>

    <p>When changing from <code>critical</code> to <code>warning</code>, you must also update the <code>slo</code> label and routing field:</p>

    <div class="callout warning">
        <div class="callout-title">⚠️ Important Gotcha</div>
        <p>Changing severity from <code>critical</code> (SLO alert) to <code>warning</code> requires THREE changes:</p>
        <ol>
            <li>Set <code>severity: warning</code></li>
            <li>Set <code>slo: "false"</code></li>
            <li>Change <code>alert_team_handle</code> to <code>alert_routing_key</code></li>
        </ol>
        <p>Missing any of these will cause deployment failures or incorrect routing.</p>
    </div>

    <h4>Updating SLO Status</h4>
    <p>The <code>slo</code> label controls whether an alert pages the SRE team on-call:</p>
    <ul>
        <li><code>slo: "true"</code> - Alert violates an SLO, pages SRE immediately</li>
        <li><code>slo: "false"</code> - Alert is important but not SLO-breaking, routes to team only</li>
    </ul>

    <h4>Modifying Thresholds and PromQL Expressions</h4>
    <p>Example: Changing availability threshold from 99% to 98%:</p>

    <div class="code-block">
        <button class="copy-button">Copy</button>
        <pre><code class="language-yaml"># Before
expr: |
  (
    avg_over_time(redhat_appstudio_integrationservice_global_github_app_available[24h]) * 100
  ) &lt; 99

# After
expr: |
  (
    avg_over_time(redhat_appstudio_integrationservice_global_github_app_available[24h]) * 100
  ) &lt; 98</code></pre>
    </div>

    <h3 id="section-1-5">Real-World Example</h3>
    <p>Let's walk through a real modification: downgrading <code>IntegrationServiceAvailabilitySLOViolation</code> from critical (SLO) to warning.</p>

    <p><strong>Before:</strong></p>
    <div class="code-block">
        <button class="copy-button">Copy</button>
        <pre><code class="language-yaml">- alert: IntegrationServiceAvailabilitySLOViolation
  expr: |
    (
      avg_over_time(redhat_appstudio_integrationservice_global_github_app_available[24h]) * 100
    ) &lt; 99
  for: 10m
  labels:
    severity: critical
    slo: "true"
  annotations:
    summary: "Integration Service GitHub App availability below SLO"
    description: "Availability is {{ $value }}%, below the 99% threshold"
    alert_team_handle: "integration-service-sre"</code></pre>
    </div>

    <p><strong>After:</strong></p>
    <div class="code-block">
        <button class="copy-button">Copy</button>
        <pre><code class="language-yaml">- alert: IntegrationServiceAvailabilitySLOViolation
  expr: |
    (
      avg_over_time(redhat_appstudio_integrationservice_global_github_app_available[24h]) * 100
    ) &lt; 99
  for: 10m
  labels:
    severity: warning
    slo: "false"
  annotations:
    summary: "Integration Service GitHub App availability below SLO"
    description: "Availability is {{ $value }}%, below the 99% threshold"
    alert_routing_key: "integration-service"</code></pre>
    </div>

    <p><strong>What Changed:</strong></p>
    <ol>
        <li><code>severity: critical</code> → <code>severity: warning</code></li>
        <li><code>slo: "true"</code> → <code>slo: "false"</code></li>
        <li><code>alert_team_handle: "integration-service-sre"</code> → <code>alert_routing_key: "integration-service"</code></li>
    </ol>

    <p><strong>Why:</strong> The team decided this alert doesn't warrant waking up SRE in the middle of the night. It's important but can wait until business hours.</p>

    <h3 id="section-1-6">Updating Alert and Recording Rule Tests</h3>

    <p>When you modify alerts or recording rules, you may need to update their corresponding tests. Tests validate that your PromQL expressions work correctly and that alerts fire at the right thresholds.</p>

    <h4>Test File Locations</h4>
    <p>Tests live alongside the rules they validate:</p>
    <ul>
        <li><strong>Alert tests:</strong> <code>test/promql/tests/data_plane/</code> (~52 test files)</li>
        <li><strong>Recording rule tests:</strong> <code>test/promql/tests/recording/</code> (~25 test files)</li>
    </ul>

    <h4>Naming Convention</h4>
    <p>Test files follow a predictable naming pattern:</p>
    <ul>
        <li><strong>Alert file:</strong> <code>rhobs/alerting/data_plane/prometheus.integration_service_availability_alerts.yaml</code></li>
        <li><strong>Test file:</strong> <code>test/promql/tests/data_plane/integration_service_availability_test.yaml</code></li>
    </ul>

    <h4>When to Update Tests</h4>
    <p>You <strong>must update tests</strong> when you change:</p>
    <ul>
        <li><strong>Alert thresholds</strong> - If you change a percentage from 99% to 98%, update test expectations</li>
        <li><strong>Time windows</strong> - If you change <code>for: 5m</code> to <code>for: 10m</code>, update test timing</li>
        <li><strong>PromQL expressions</strong> - If the metric or calculation changes, update test inputs/outputs</li>
        <li><strong>Label filters</strong> - If you add/remove label selectors, update test series labels</li>
    </ul>

    <div class="callout warning">
        <div class="callout-title">⚠️ Tests Prevent Broken Alerts</div>
        <p>If you change an alert threshold but don't update the test, the test will fail in CI. This catches mistakes before they reach production. Always update tests when you modify alert logic.</p>
    </div>

    <div class="callout info">
        <div class="callout-title">ℹ️ Don't Forget the SOP</div>
        <p>When you change alert thresholds (<code>for:</code> duration, percentages, etc.), you must also update the corresponding SOP to reflect the new values. If your alert now fires after 10 minutes instead of 5 minutes, the SOP runbook should document the correct threshold. See <strong>Section 2: Standard Operating Procedures</strong> for more details on updating SOPs.</p>
    </div>

    <h4>Alert Test Structure</h4>
    <p>Alert tests simulate time-series data and verify that alerts fire (or don't fire) at the correct thresholds. Here's an example structure:</p>

    <div class="code-block">
        <button class="copy-button">Copy</button>
        <pre><code class="language-yaml">evaluation_interval: 1m

rule_files:
  - prometheus.integration_service_availability_alerts.yaml

tests:
  # Test 1: Downtime exceeds threshold - alert SHOULD fire
  - interval: 1m
    input_series:
      - series: 'konflux_up{service="integration-service", check="replicas-available"}'
        values: '1x1434 0x6'  # 6 minutes down
    alert_rule_test:
      - eval_time: 1440m
        alertname: IntegrationServiceAvailabilitySLOViolation
        exp_alerts:
          - exp_labels:
              severity: critical
              slo: "true"

  # Test 2: Downtime below threshold - alert should NOT fire
  - interval: 1m
    input_series:
      - series: 'konflux_up{service="integration-service", check="replicas-available"}'
        values: '1x1436 0x4'  # Only 4 minutes down
    alert_rule_test:
      - eval_time: 1440m
        alertname: IntegrationServiceAvailabilitySLOViolation
        exp_alerts: []  # No alert expected</code></pre>
    </div>

    <p><strong>Key points:</strong></p>
    <ul>
        <li><code>input_series</code> - Simulates metric values over time (<code>1x1434</code> = value 1 for 1434 minutes)</li>
        <li><code>eval_time</code> - When to check if the alert fired</li>
        <li><code>exp_alerts</code> - Expected alerts at evaluation time (empty array = no alert)</li>
        <li>Tests validate boundary conditions (just over and just under threshold)</li>
    </ul>

    <h4>Recording Rule Test Structure</h4>
    <p>Recording rule tests verify that PromQL expressions produce the expected output metrics:</p>

    <div class="code-block">
        <button class="copy-button">Copy</button>
        <pre><code class="language-yaml">evaluation_interval: 1m

rule_files:
  - integration_service_availability_recording_rules.yaml

tests:
  - interval: 1m
    input_series:
      # Service is available (1 replica spec, 1 replica available)
      - series: 'kube_deployment_spec_replicas{namespace="integration-service", deployment="my-service"}'
        values: '1 1 1 1 1'
      - series: 'kube_deployment_status_replicas_available{namespace="integration-service", deployment="my-service"}'
        values: '1 1 1 1 1'

    promql_expr_test:
      - expr: konflux_up
        eval_time: 5m
        exp_samples:
          - labels: 'konflux_up{service="my-service", check="replicas-available"}'
            value: 1  # Expect value 1 (available)</code></pre>
    </div>

    <p><strong>Key points:</strong></p>
    <ul>
        <li><code>promql_expr_test</code> - Tests the output of the recording rule expression</li>
        <li><code>exp_samples</code> - Expected metric values with their labels</li>
        <li>Tests verify the PromQL calculation produces correct results</li>
    </ul>

    <div class="callout info">
        <div class="callout-title">ℹ️ Not All Alerts Have Recording Rules</div>
        <p>Recording rules are used to pre-compute expensive or complex queries, reducing the computational cost when alerts evaluate. We typically use recording rules for:</p>
        <ul>
            <li><strong>Availability metrics</strong> - Like <code>konflux_up</code> and <code>image-rbac-proxy</code> availability calculations</li>
            <li><strong>Complex aggregations</strong> - Queries that would be expensive to run every time an alert evaluates</li>
        </ul>
        <p>However, <strong>not all SLO alerts need recording rules</strong>. Many alerts query metrics directly if the query is simple enough. The decision depends on computational cost and query complexity. If you're modifying an alert that doesn't have a corresponding recording rule, you only need to update the alert test - there's no recording rule test to update.</p>
    </div>

    <h4>Example: Updating Tests After Changing Alert Threshold</h4>

    <p>Let's say you change an alert's <code>for:</code> duration from 5 minutes to 10 minutes:</p>

    <p><strong>Step 1: Update the alert</strong></p>
    <div class="code-block">
        <button class="copy-button">Copy</button>
        <pre><code class="language-yaml"># Before
for: 5m

# After
for: 10m</code></pre>
    </div>

    <p><strong>Step 2: Update the test</strong></p>
    <p>You need to adjust test scenarios to match the new threshold:</p>

    <div class="code-block">
        <button class="copy-button">Copy</button>
        <pre><code class="language-yaml"># OLD TEST: 6 minutes down triggers alert (threshold was 5m)
values: '1x1434 0x6'  # 6 minutes down - SHOULD fire

# NEW TEST: 11 minutes down triggers alert (threshold is now 10m)
values: '1x1428 0x12'  # 12 minutes down - SHOULD fire

# Also update the "just under threshold" test:
# OLD: 4 minutes should NOT fire
values: '1x1436 0x4'

# NEW: 9 minutes should NOT fire
values: '1x1431 0x9'</code></pre>
    </div>

    <p><strong>Step 3: Run tests locally</strong></p>
    <p>After updating, run the test suite (see Section 4: Testing Changes) to verify your changes work correctly.</p>

    <div class="callout info">
        <div class="callout-title">ℹ️ Test File Reference</div>
        <p>Each test file references its corresponding alert or recording rule file using the <code>rule_files:</code> field. This tells the test runner which YAML file to load for validation.</p>
    </div>

    <h3 id="section-1-7">Committing and Creating Pull Requests</h3>

    <p>After making changes to alert YAML files and updating tests, commit your changes and create a pull request:</p>

    <div class="code-block">
        <button class="copy-button">Copy</button>
        <pre><code class="language-bash">cd ~/repo/o11y
git add rhobs/alerting/data_plane/prometheus.*_alerts.yaml
git add test/promql/tests/data_plane/*_test.yaml
git commit -m "feat: update Integration Service availability alert threshold"
git push origin your-branch-name</code></pre>
    </div>

    <p>Create a pull request for your changes.</p>

    <div class="callout info">
        <div class="callout-title">📢 Notify the Team</div>
        <p>After creating your PR in the O11Y repository, post the PR link to the <strong>#forum-konflux-o11y</strong> Slack channel (<a href="https://redhat.enterprise.slack.com/archives/C04FDFTF8EB" target="_blank">link</a>) and tag <code>@konflux-o11y-ic</code> to request approval.</p>
    </div>

    <p>Once approved and merged, your alert changes will be automatically deployed to production via the RHOBS pipeline.</p>
</section>
"""

    return html


def build_section_2_sops(source_content: Dict[str, str]) -> str:
    """Build Section 2: Standard Operating Procedures (SOPs)."""

    html = """
<section id="section-2">
    <h2>2. Standard Operating Procedures (SOPs)</h2>

    <p>Standard Operating Procedures (SOPs) are runbooks that guide the team through responding to alerts and incidents. When an alert fires, the SOP provides step-by-step instructions for diagnosing and resolving the issue. This section explains what SOPs are, where to find them, and how they connect to alerts.</p>

    <h3 id="section-2-1">What Are SOPs?</h3>
    <p>An SOP (Standard Operating Procedure) is a documented procedure that describes how to respond to a specific situation. In the context of Konflux metrics and alerts:</p>
    <ul>
        <li><strong>SOPs provide actionable steps</strong> - They tell you exactly what to do when an alert fires</li>
        <li><strong>SOPs reduce response time</strong> - Clear instructions mean faster resolution</li>
        <li><strong>SOPs enable self-service</strong> - SREs can often resolve issues without waiting for the dev team</li>
        <li><strong>SOPs ensure consistency</strong> - Everyone follows the same procedure</li>
    </ul>

    <h3 id="section-2-2">Two Categories of SOPs</h3>

    <p>SOPs are organized into two main categories based on who uses them:</p>

    <h4>SRE SOPs (SLO Alerts)</h4>
    <p>Located in: <code>sop/integration-service/SRE/</code></p>
    <p>These SOPs are used by SRE (Site Reliability Engineering) when critical alerts fire. Characteristics:</p>
    <ul>
        <li><strong>Linked to SLO alerts</strong> - Triggered when <code>slo: "true"</code> alerts fire</li>
        <li><strong>Must have actionable steps</strong> - SRE must be able to diagnose and ideally resolve without dev team</li>
        <li><strong>Linked via runbook_url</strong> - The alert YAML includes a <code>runbook_url</code> annotation pointing to the SOP</li>
        <li><strong>Critical for on-call</strong> - These are used during incidents, often outside business hours</li>
    </ul>

    <h4>Team SOPs (Non-SLO)</h4>
    <p>Located in: <code>sop/integration-service/</code> (outside the SRE folder)</p>
    <p>These SOPs are for the development team's use. Characteristics:</p>
    <ul>
        <li><strong>Internal procedures</strong> - How the team handles specific situations</li>
        <li><strong>May be less time-critical</strong> - Not used for middle-of-the-night pages</li>
        <li><strong>Broader scope</strong> - Can cover operational tasks, not just alerts</li>
    </ul>

    <h3 id="section-2-3">Where SOPs Are Located</h3>

    <p><strong>Repository:</strong> <a href="https://gitlab.cee.redhat.com/konflux/docs/sop/-/tree/main/integration-service?ref_type=heads" target="_blank">gitlab.cee.redhat.com/konflux/docs/sop</a></p>

    <p><strong>Directory structure:</strong></p>
    <div class="code-block">
        <button class="copy-button">Copy</button>
        <pre><code class="language-bash">sop/
└── integration-service/
    ├── SRE/                    # SOPs for SRE on-call (SLO alerts)
    │   ├── alert-name-1.md
    │   ├── alert-name-2.md
    │   └── ...
    └── team-procedure-1.md     # Team SOPs (non-SLO)
    └── team-procedure-2.md
    └── ...</code></pre>
    </div>

    <h3 id="section-2-4">How SOPs Link to Alerts</h3>

    <p>For SLO alerts (<code>slo: "true"</code>), the alert YAML file includes a <code>runbook_url</code> annotation that points to the SOP:</p>

    <div class="code-block">
        <button class="copy-button">Copy</button>
        <pre><code class="language-yaml">- alert: IntegrationServiceAvailabilitySLOViolation
  expr: |
    (
      avg_over_time(redhat_appstudio_integrationservice_global_github_app_available[24h]) * 100
    ) &lt; 99
  for: 10m
  labels:
    severity: critical
    slo: "true"
  annotations:
    summary: "Integration Service GitHub App availability below SLO"
    description: "Availability is {{ $value }}%, below the 99% threshold"
    runbook_url: "https://gitlab.cee.redhat.com/konflux/docs/sop/-/blob/main/integration-service/SRE/IntegrationServiceAvailabilitySLOViolation.md"
    alert_team_handle: "integration-service-sre"</code></pre>
    </div>

    <p>When the alert fires, the <code>runbook_url</code> is displayed in the alert notification, giving SRE immediate access to the response procedure.</p>

    <h3 id="section-2-5">Working with SOPs</h3>

    <p>As an engineer, you'll typically interact with SOPs in these scenarios:</p>

    <h4>Editing an Existing SOP</h4>
    <p>When you modify an alert or fix a recurring issue, you may need to update the corresponding SOP:</p>
    <ul>
        <li>Update steps if the resolution procedure changes</li>
        <li>Add new diagnostic commands based on lessons learned</li>
        <li>Clarify ambiguous instructions</li>
        <li>Update links to dashboards or tools</li>
    </ul>

    <h4>Creating a New SOP</h4>
    <p>When creating a new SLO alert, write the SOP first, then link it in the alert PR. This ensures:</p>
    <ul>
        <li>The runbook_url points to a real document when the alert goes live</li>
        <li>SRE can respond immediately if the alert fires</li>
        <li>You've thought through the response procedure before the alert exists</li>
    </ul>

    <div class="callout info">
        <div class="callout-title">ℹ️ Using Existing SOPs as Templates</div>
        <p>There's no formal SOP template, but all existing SOPs follow a similar structure. When creating a new SOP, browse the <code>SRE/</code> folder and use an existing one as a guide for layout and sections.</p>
    </div>

    <h4>SOP Review and Approval</h4>
    <p>SOP changes follow a review process:</p>
    <ul>
        <li><strong>Approvers:</strong> One Integration Service team member + one SRE</li>
        <li><strong>SRE review focus:</strong> Ensuring steps are actionable and SRE can resolve without dev team</li>
        <li><strong>Tagging SRE:</strong> SRE team members like to be explicitly tagged on MRs to review new/updated SOPs</li>
    </ul>

    <div class="callout warning">
        <div class="callout-title">⚠️ Important: Actionable Steps Required</div>
        <p>SRE SOPs must have actionable, specific steps. Vague instructions like "check the logs" aren't enough. Specify:</p>
        <ul>
            <li>Exact commands to run</li>
            <li>What output to look for</li>
            <li>How to determine if the issue is resolved</li>
            <li>When to escalate to the dev team</li>
        </ul>
    </div>

    <h3 id="section-2-6">Common SOP Workflow</h3>

    <p>Here's the typical workflow when working with alerts and SOPs:</p>

    <p><strong>When editing an existing alert:</strong></p>
    <ol>
        <li>Make your alert changes in the o11y repository</li>
        <li>If the alert behavior changes, update the linked SOP</li>
        <li>Submit both changes (alert + SOP) for review</li>
        <li>Tag an SRE team member if the SOP changes</li>
    </ol>

    <p><strong>When creating a new SLO alert:</strong></p>
    <ol>
        <li><strong>First:</strong> Write the SOP with clear actionable steps</li>
        <li>Submit the SOP for review and merge it</li>
        <li><strong>Then:</strong> Create the alert with <code>runbook_url</code> pointing to the merged SOP</li>
        <li>Submit the alert PR with the SOP link already working</li>
    </ol>

    <div class="callout info">
        <div class="callout-title">ℹ️ Browse the SOP Repository</div>
        <p>The best way to understand SOPs is to read a few examples. Visit the <a href="https://gitlab.cee.redhat.com/konflux/docs/sop/-/tree/main/integration-service?ref_type=heads" target="_blank">SOP repository</a> and browse the <code>SRE/</code> folder to see real runbooks.</p>
    </div>
</section>
"""

    return html


def build_section_3_updating_dashboards(source_content: Dict[str, str]) -> str:
    """Build Section 3: Updating Grafana Dashboards."""

    push_dash_content = source_content.get('push_dash', '')

    # Load dashboard screenshot images as base64
    import base64
    try:
        with open("/Users/jcullina/Desktop/Screenshot 2026-05-27 at 16.26.11.png", "rb") as f:
            img1_edit_button = base64.b64encode(f.read()).decode('utf-8')
        with open("/Users/jcullina/Desktop/Screenshot 2026-05-27 at 16.26.22.png", "rb") as f:
            img2_settings_button = base64.b64encode(f.read()).decode('utf-8')
        with open("/Users/jcullina/Desktop/Screenshot 2026-05-27 at 16.26.35.png", "rb") as f:
            img3_json_model = base64.b64encode(f.read()).decode('utf-8')
        with open("/Users/jcullina/Desktop/Screenshot 2026-05-27 at 16.31.51.png", "rb") as f:
            img4_panel_menu = base64.b64encode(f.read()).decode('utf-8')
        with open("/Users/jcullina/Desktop/Screenshot 2026-05-27 at 16.32.12.png", "rb") as f:
            img5_panel_editor = base64.b64encode(f.read()).decode('utf-8')
    except FileNotFoundError:
        # If images aren't found, use placeholders
        img1_edit_button = ""
        img2_settings_button = ""
        img3_json_model = ""
        img4_panel_menu = ""
        img5_panel_editor = ""

    # Build the HTML with image tags
    img1_tag = f'<img src="data:image/png;base64,{img1_edit_button}" alt="Grafana dashboard showing Edit button highlighted in top-right corner" style="max-width: 100%; border: 1px solid #ddd; border-radius: 4px; margin: 1rem 0;" />' if img1_edit_button else '<p><em>Screenshot: Grafana dashboard header with the "Edit" button highlighted</em></p>'

    img2_tag = f'<img src="data:image/png;base64,{img2_settings_button}" alt="Grafana dashboard showing Settings button highlighted in top-right corner" style="max-width: 100%; border: 1px solid #ddd; border-radius: 4px; margin: 1rem 0;" />' if img2_settings_button else '<p><em>Screenshot: Grafana dashboard with the "Settings" button highlighted</em></p>'

    img3_tag = f'<img src="data:image/png;base64,{img3_json_model}" alt="Grafana Settings page showing JSON Model tab with complete dashboard JSON" style="max-width: 100%; border: 1px solid #ddd; border-radius: 4px; margin: 1rem 0;" />' if img3_json_model else '<p><em>Screenshot: Settings page with "JSON Model" tab selected, displaying the full dashboard JSON</em></p>'

    img4_tag = f'<img src="data:image/png;base64,{img4_panel_menu}" alt="Grafana panel showing the three-dot menu in top-right corner with Edit option highlighted" style="max-width: 100%; border: 1px solid #ddd; border-radius: 4px; margin: 1rem 0;" />' if img4_panel_menu else '<p><em>Screenshot: Panel three-dot menu with "Edit" option</em></p>'

    img5_tag = f'<img src="data:image/png;base64,{img5_panel_editor}" alt="Grafana panel editor showing queries at the bottom and panel design options on the right" style="max-width: 100%; border: 1px solid #ddd; border-radius: 4px; margin: 1rem 0;" />' if img5_panel_editor else '<p><em>Screenshot: Panel editor with queries and design layout options</em></p>'

    html = """
<section id="section-3">
    <h2>3. Updating Grafana Dashboards</h2>

    <p>Grafana dashboards visualize metrics and SLOs. You'll update dashboards to add new panels, fix queries, or change visualizations. The recommended approach is to edit dashboards in the Grafana UI, export the JSON, and save it to the repository.</p>

    <h3 id="section-3-1">Where Dashboards Are Defined</h3>
    <p>Dashboards have two locations:</p>
    <ul>
        <li><strong>Source repository</strong> - Where dashboard JSON lives:
            <ul>
                <li><code>redhat-appstudio/o11y/dashboards/</code> - All Integration Service dashboards</li>
            </ul>
        </li>
        <li><strong>Deployment configuration</strong> - References which commit to deploy:
            <ul>
                <li><code>app-interface/data/services/stonesoup/cicd/saas-stonesoup-dashboards.yml</code> (GitLab internal)</li>
            </ul>
        </li>
    </ul>

    <h3 id="section-3-2">Dashboard Development Workflow</h3>

    <p>The recommended workflow is to edit dashboards in the Grafana UI, then export the JSON to the repository. This is <strong>much easier</strong> than editing JSON files directly.</p>

    <ol>
        <li><strong>Edit the dashboard in Grafana</strong> - Make changes using Grafana's visual editor</li>
        <li><strong>Export the JSON model</strong> - Go to Settings → JSON Model and copy the complete JSON</li>
        <li><strong>Update the repository</strong> - Paste the JSON into the dashboard file in <code>redhat-appstudio/o11y</code></li>
        <li><strong>Commit and merge</strong> - Push changes to the o11y repository</li>
        <li><strong>Update app-interface</strong> - Update the commit SHA in <code>saas-stonesoup-dashboards.yml</code></li>
        <li><strong>Changes deploy automatically</strong> - Once the app-interface MR merges</li>
    </ol>

    <div class="callout info">
        <div class="callout-title">ℹ️ Why Edit in Grafana UI?</div>
        <p>Editing dashboards in the Grafana UI is much easier than manually editing JSON. You can see your changes immediately, use Grafana's panel editors, and preview queries. Once you're happy with the changes, export the JSON and save it to the repository.</p>
    </div>

    <h3 id="section-3-3">Step-by-Step: Editing a Dashboard in Grafana</h3>

    <p>Here's the complete workflow for updating the Integration Service SLO dashboard:</p>

    <h4>Step 1: Open the Dashboard in Grafana</h4>
    <p>Navigate to the production Grafana dashboard you want to edit. For Integration Service dashboards:</p>
    <ul>
        <li><a href="https://grafana.app-sre.devshift.net/d/cerzhj80cyvi8c/konflux-integration-service?orgId=1" target="_blank">Konflux Integration Service SLO Dashboard</a></li>
    </ul>

    <h4>Step 2: Enter Edit Mode</h4>
    <p>Click the <strong>Edit</strong> button in the top-right corner of the dashboard:</p>

    """ + img1_tag + """

    <p>In edit mode, you can:</p>
    <ul>
        <li>Click on any panel to edit it</li>
        <li>Add new panels using the "Add panel" button</li>
        <li>Rearrange panels by dragging them</li>
    </ul>

    <h4>Step 3: Edit a Panel</h4>
    <p>To edit an existing panel, click the <strong>three-dot menu</strong> in the top-right corner of the panel and select <strong>Edit</strong>:</p>

    """ + img4_tag + """

    <h4>Step 4: Modify Panel Queries and Design</h4>
    <p>Once in the panel editor, you can modify both the data queries and the visual design:</p>

    """ + img5_tag + """

    <p>The panel editor has two main areas:</p>
    <ul>
        <li><strong>Query section (bottom)</strong> - Update PromQL queries to change what data is displayed</li>
        <li><strong>Panel options (right sidebar)</strong> - Modify visualization type, thresholds, colors, formatting, and layout settings</li>
    </ul>

    <p>Common changes you might make:</p>
    <ul>
        <li>Update PromQL queries to show different metrics</li>
        <li>Change visualization types (graph, gauge, stat, table, etc.)</li>
        <li>Update thresholds and alert colors</li>
        <li>Modify panel titles and descriptions</li>
        <li>Adjust time ranges and refresh intervals</li>
    </ul>

    <p>Test your changes by viewing the panel and ensuring the data looks correct.</p>

    <h4>Step 5: Return to Dashboard</h4>
    <p>After editing panels, click <strong>Back to dashboard</strong> (in the top-right) to return to the main dashboard view. You'll see all your changes applied.</p>

    <h4>Step 6: Access Dashboard Settings</h4>
    <p>Once you're satisfied with your changes, click the <strong>Settings</strong> button (gear icon) in the top-right corner:</p>

    """ + img2_tag + """

    <h4>Step 7: Export the JSON Model</h4>
    <p>In the Settings page, click the <strong>JSON Model</strong> tab. This shows the complete JSON representation of the dashboard with all panels, queries, layout, variables, and settings:</p>

    """ + img3_tag + """

    <p><strong>Copy the entire JSON</strong> - Select all the JSON text and copy it to your clipboard.</p>

    <h4>Step 8: Update the Dashboard File in o11y Repository</h4>

    <p>Open the corresponding dashboard file in the <code>redhat-appstudio/o11y</code> repository:</p>

    <div class="code-block">
        <button class="copy-button">Copy</button>
        <pre><code class="language-bash">cd ~/repo/o11y
# Integration Service SLO dashboard is at:
vim dashboards/grafana-dashboard-konflux-integration-service-slo.configmap.yaml</code></pre>
    </div>

    <p>Find the JSON content within the ConfigMap and <strong>replace it entirely</strong> with the JSON you copied from Grafana.</p>

    <p>The file structure looks like this:</p>
    <div class="code-block">
        <button class="copy-button">Copy</button>
        <pre><code class="language-yaml">apiVersion: v1
kind: ConfigMap
metadata:
  name: grafana-dashboard-konflux-integration-service-slo
data:
  konflux-integration-service-slo.json: |
    # ← Replace everything from here down with the JSON you copied from Grafana
    {
      "annotations": {
        ...
      },
      "panels": [
        ...
      ],
      ...
    }</code></pre>
    </div>

    <div class="callout warning">
        <div class="callout-title">⚠️ Don't Edit JSON Directly</div>
        <p>While it's technically possible to edit dashboard JSON files manually, it's <strong>much easier and less error-prone</strong> to make changes in the Grafana UI and export the JSON. Manual JSON editing is difficult and mistakes can break the dashboard.</p>
    </div>

    <h4>Step 9: Commit and Push Changes</h4>

    <div class="code-block">
        <button class="copy-button">Copy</button>
        <pre><code class="language-bash">git add dashboards/grafana-dashboard-konflux-integration-service-slo.configmap.yaml
git commit -m "feat: update Integration Service SLO dashboard - add new panel for X"
git push origin your-branch-name</code></pre>
    </div>

    <p>Create a pull request for your changes.</p>

    <div class="callout info">
        <div class="callout-title">📢 Notify the Team</div>
        <p>After creating your PR in the O11Y repository, post the PR link to the <strong>#forum-konflux-o11y</strong> Slack channel (<a href="https://redhat.enterprise.slack.com/archives/C04FDFTF8EB" target="_blank">link</a>) and tag <code>@konflux-o11y-ic</code> to request approval.</p>
    </div>

    <p>Once the PR is approved and merged, the dashboard changes are saved in the O11Y repository. However, <strong>they won't appear in production until you update app-interface</strong> with the new commit SHA (see next section).</p>

    <h3 id="section-3-3">Pushing Dashboard Changes to Production</h3>

    <h4>Step 10: Get the Latest O11Y Repository SHA</h4>

    <p>After your dashboard PR merges to main in the O11Y repository, get the most recent SHA of the entire O11Y repository (not just your commit):</p>
    <div class="code-block">
        <button class="copy-button">Copy</button>
        <pre><code class="language-bash">cd ~/repo/o11y
git pull origin main
git log -1 --format="%H"
# Output: abc123def456789... (this is the SHA of the latest commit on main)</code></pre>
    </div>

    <p>This SHA represents the current state of the entire O11Y repository, including your dashboard changes and any other recent commits.</p>

    <h3 id="section-3-4">Updating app-interface to Deploy to Production</h3>

    <p><strong>Repository:</strong> <code>gitlab.cee.redhat.com/service/app-interface</code> (GitLab internal)</p>
    <p><strong>File path:</strong> <code>data/services/stonesoup/cicd/saas-stonesoup-dashboards.yml</code></p>

    <h4>Step 11: Clone app-interface and Update the SHA</h4>

    <p>Clone app-interface (if you haven't already) and update the dashboard SHA:</p>

    <div class="code-block">
        <button class="copy-button">Copy</button>
        <pre><code class="language-bash">git clone https://gitlab.cee.redhat.com/service/app-interface.git
cd app-interface

# Edit the dashboard deployment config
vim data/services/stonesoup/cicd/saas-stonesoup-dashboards.yml</code></pre>
    </div>

    <p>Find the Integration Service dashboard section and update the <code>ref:</code> field with your new SHA:</p>

    <div class="code-block">
        <button class="copy-button">Copy</button>
        <pre><code class="language-yaml">resourceTemplates:
- name: stonesoup-dashboards
  url: https://github.com/redhat-appstudio/o11y
  path: /dashboards
  provider: directory
  targets:
  - namespace:
      $ref: /services/observability/namespaces/app-sre-observability-production-int.appsrep09ue1.yml
    ref: abc123def456789...  # ← Update with the O11Y repo SHA from Step 10</code></pre>
    </div>

    <h4>Step 12: Create and Merge the app-interface MR</h4>

    <div class="code-block">
        <button class="copy-button">Copy</button>
        <pre><code class="language-bash">git add data/services/stonesoup/cicd/saas-stonesoup-dashboards.yml
git commit -m "Update Integration Service SLO dashboard to abc123d"
git push origin HEAD:refs/for/master
# This creates a merge request in GitLab</code></pre>
    </div>

    <div class="callout info">
        <div class="callout-title">📢 Request Approval for app-interface MR</div>
        <p>After creating your app-interface MR, post the MR link to the <strong>#forum-konflux-o11y</strong> Slack channel (<a href="https://redhat.enterprise.slack.com/archives/C04FDFTF8EB" target="_blank">link</a>) and tag <code>@konflux-o11y-ic</code> to request approval for the production deployment.</p>
    </div>

    <p>Once the app-interface MR is approved and merged, the updated dashboard automatically deploys to production.</p>

    <div class="callout info">
        <div class="callout-title">ℹ️ Note About infra-deployments</div>
        <p>Integration Service dashboards are deployed via <code>app-interface</code> only. The <code>infra-deployments</code> repo has a legacy reference at <code>components/monitoring/grafana/base/dashboards/integration/kustomization.yaml</code> pointing to an old commit - this is not used for production deployments.</p>
    </div>
</section>
"""

    return html


def build_section_4_testing_changes(source_content: Dict[str, str]) -> str:
    """Build Section 4: Testing Changes."""

    testing_content = source_content.get('testing', '')

    html = """
<section id="section-4">
    <h2>4. Testing Changes</h2>

    <p>Before your alerts or dashboards go to production, you need to test them. Testing validates that your PromQL expressions work correctly and that your configuration doesn't break existing functionality. This section covers how to run the Konflux test suite locally.</p>

    <h3 id="section-5-1">Why Test Your Changes</h3>
    <p>Testing is critical because:</p>
    <ul>
        <li><strong>PromQL syntax errors</strong> - A typo in your expression will cause the entire alert or dashboard to fail</li>
        <li><strong>Logic bugs</strong> - Your expression might compile but return unexpected results</li>
        <li><strong>Performance issues</strong> - Inefficient queries can overload Prometheus</li>
        <li><strong>Breaking changes</strong> - You might accidentally remove a recording rule that other alerts depend on</li>
        <li><strong>Catching issues before production</strong> - Tests prevent fire-fighting in production</li>
    </ul>

    <p>The Konflux observability infrastructure includes automated test suites that validate your changes before they go live. You can run these tests locally on your machine.</p>

    <h3 id="section-5-2">Setting Up Podman</h3>

    <p>Tests run in containers using Podman. If you don't have Podman installed, you'll need to set it up first.</p>

    <h4>Install Podman (if needed)</h4>
    <p>On macOS:</p>
    <div class="code-block">
        <button class="copy-button">Copy</button>
        <pre><code class="language-bash">brew install podman</code></pre>
    </div>

    <p>On Linux (Fedora/RHEL):</p>
    <div class="code-block">
        <button class="copy-button">Copy</button>
        <pre><code class="language-bash">sudo dnf install podman</code></pre>
    </div>

    <h4>Initialize and Start Podman Machine (macOS only)</h4>

    <div class="callout warning">
        <div class="callout-title">⚠️ macOS Required Setup</div>
        <p>On macOS, Podman requires a virtual machine. If Podman Desktop is running, you can skip this step. Otherwise:</p>
    </div>

    <div class="code-block">
        <button class="copy-button">Copy</button>
        <pre><code class="language-bash"># Create the VM (only once, on first setup)
podman machine init

# Start the VM before running tests
podman machine start</code></pre>
    </div>

    <p>You only need to run <code>podman machine init</code> once. After that, use <code>podman machine start</code> before each session.</p>

    <h3 id="section-5-3">Running Tests Locally</h3>

    <p>The test suite uses a container image that checks your PromQL syntax and validates alerting rules. There are separate tests for data plane alerts and recording rules.</p>

    <h4>Test Data Plane Alerts</h4>
    <p>Data plane alerts monitor core Konflux services:</p>

    <div class="code-block">
        <button class="copy-button">Copy</button>
        <pre><code class="language-bash">cd /path/to/o11y  # Clone of redhat-appstudio/o11y

podman run \\
  -v "$(pwd):/work" \\
  -w /work \\
  quay.io/rhobs/obsctl-reloader-rules-checker:latest \\
  -t rhtap \\
  -d rhobs/alerting/data_plane \\
  -y -p \\
  --tests-dir test/promql/tests/data_plane</code></pre>
    </div>

    <h4>Test Recording Rules</h4>
    <p>Recording rules pre-compute expensive metrics:</p>

    <div class="code-block">
        <button class="copy-button">Copy</button>
        <pre><code class="language-bash">cd /path/to/o11y

podman run \\
  -v "$(pwd):/work" \\
  -w /work \\
  quay.io/rhobs/obsctl-reloader-rules-checker:latest \\
  -t rhtap \\
  -d rhobs/recording \\
  -y -p \\
  --tests-dir test/promql/tests/recording</code></pre>
    </div>

    <p>Replace <code>/path/to/o11y</code> with your local clone of <code>redhat-appstudio/o11y</code>.</p>

    <div class="callout info">
        <div class="callout-title">ℹ️ Container Image Details</div>
        <p>The image <code>quay.io/rhobs/obsctl-reloader-rules-checker</code> is maintained by the RHOBS team. It contains validators for PromQL syntax, rule structure, and test execution.</p>
    </div>

    <h3 id="section-5-4">Understanding Test Output</h3>

    <p>Successful test runs show output like:</p>

    <div class="code-block">
        <button class="copy-button">Copy</button>
        <pre><code class="language-bash">✓ Validating prometheus rules...
✓ All PromQL expressions are valid
✓ Running test suite...
✓ 47/47 tests passed

Test Results:
  Data Plane Alerts: PASS
  Recording Rules: PASS

Errors: 0
Warnings: 0</code></pre>
    </div>

    <p><strong>Key indicators:</strong></p>
    <ul>
        <li><code>✓</code> checks pass - Your changes are valid</li>
        <li><code>✗</code> checks fail - Fix the issues before committing</li>
        <li><code>Errors: 0</code> - No syntax or logic errors</li>
        <li><code>Warnings: 0</code> - No issues flagged by validators</li>
    </ul>

    <h3 id="section-4-5">Common Test Failures and Fixes</h3>

    <h4>PromQL Syntax Errors</h4>
    <p><strong>Error:</strong></p>
    <div class="code-block">
        <button class="copy-button">Copy</button>
        <pre><code class="language-bash">ERROR: parse error at char 42: unexpected token ")"</code></pre>
    </div>

    <div class="callout danger">
        <div class="callout-title">❌ Common Cause: Missing or Extra Parentheses</div>
        <p>Check your PromQL expression for balanced parentheses. Example:</p>
        <p><code># WRONG: Missing closing paren<br/>
(avg_over_time(metric[5m]</code></p>
        <p><code># CORRECT<br/>
(avg_over_time(metric[5m]))</code></p>
    </div>

    <h4>Undefined Metrics</h4>
    <p><strong>Error:</strong></p>
    <div class="code-block">
        <button class="copy-button">Copy</button>
        <pre><code class="language-bash">ERROR: metric "undefined_metric_name" not found in test data</code></pre>
    </div>

    <div class="callout danger">
        <div class="callout-title">❌ Common Cause: Typo in Metric Name</div>
        <p>Double-check that your metric name matches exactly. Prometheus is case-sensitive:</p>
        <p><code># WRONG<br/>
redhat_appstudio_IntegrationService_available  (wrong capitalization)</code></p>
        <p><code># CORRECT<br/>
redhat_appstudio_integrationservice_available</code></p>
    </div>

    <h4>Missing Test File</h4>
    <p><strong>Error:</strong></p>
    <div class="code-block">
        <button class="copy-button">Copy</button>
        <pre><code class="language-bash">ERROR: test directory "test/promql/tests/data_plane" not found</code></pre>
    </div>

    <p><strong>Fix:</strong> Ensure you're running the command from the root of the repository. Check that <code>test/</code> directory exists:</p>

    <div class="code-block">
        <button class="copy-button">Copy</button>
        <pre><code class="language-bash">cd /path/to/o11y
ls -la test/promql/tests/</code></pre>
    </div>

    <h4>Container Image Not Available</h4>
    <p><strong>Error:</strong></p>
    <div class="code-block">
        <button class="copy-button">Copy</button>
        <pre><code class="language-bash">Error: image not found</code></pre>
    </div>

    <p><strong>Fix:</strong> Pull the image first:</p>

    <div class="code-block">
        <button class="copy-button">Copy</button>
        <pre><code class="language-bash">podman pull quay.io/rhobs/obsctl-reloader-rules-checker:latest</code></pre>
    </div>

    <h3 id="section-4-6">References and Additional Resources</h3>

    <ul>
        <li><strong>o11y repository:</strong> <a href="https://github.com/redhat-appstudio/o11y" target="_blank">redhat-appstudio/o11y</a></li>
        <li><strong>RHOBS Rules Checker:</strong> <a href="https://github.com/rhobs/obsctl-reloader-rules-checker" target="_blank">obsctl-reloader-rules-checker</a></li>
        <li><strong>PromQL Documentation:</strong> <a href="https://prometheus.io/docs/prometheus/latest/querying/basics/" target="_blank">Prometheus Query Language</a></li>
        <li><strong>Konflux Monitoring:</strong> <a href="https://github.com/redhat-appstudio" target="_blank">redhat-appstudio</a></li>
    </ul>

    <div class="callout info">
        <div class="callout-title">ℹ️ Getting Help</div>
        <p>If tests fail and you can't figure out why:</p>
        <ul>
            <li>Check the exact error message - usually points to the problem</li>
            <li>Ask your team lead or an experienced teammate to review your PromQL</li>
            <li>Look at similar existing rules for reference</li>
            <li>Test small changes before large refactors</li>
        </ul>
    </div>
</section>
"""

    return html


def build_section_5_reference(source_content: Dict[str, str]) -> str:
    """Build Section 5: Reference Materials - Observability, SLOs, Dashboards, and Tools."""

    # Extract dashboard links dynamically
    dashboards_content = source_content.get('dashboards', '')
    dashboard_links = extract_dashboard_links(dashboards_content)

    # Part 1: Observability & SLO content (static HTML, ~85 lines)
    html = """
<section id="section-5">
    <h2>5. Reference Materials</h2>

    <p>This section provides reference material for common tasks, including observability concepts, SLO definitions, dashboard links, graph types, and troubleshooting resources.</p>

    <h3 id="section-5-1">Understanding Observability & SLOs</h3>

    <p>Observability is the practice of understanding system behavior by examining its outputs. The three pillars of observability are:</p>

    <h4>1. Metrics</h4>
    <p>Quantitative measurements of system behavior. Examples:</p>
    <ul>
        <li><strong>Request latency</strong> - How long requests take to complete</li>
        <li><strong>Error rate</strong> - Percentage of failed requests</li>
        <li><strong>Throughput</strong> - Requests per second the system handles</li>
        <li><strong>Resource utilization</strong> - CPU, memory, disk usage</li>
    </ul>

    <p>In Konflux, we use <strong>Prometheus</strong> to collect and store metrics. PromQL is the language we use to query these metrics.</p>

    <h4>2. Logs</h4>
    <p>Detailed event records from applications. Logs capture:</p>
    <ul>
        <li><strong>Errors and warnings</strong> - When something goes wrong</li>
        <li><strong>Audit trails</strong> - Who did what and when</li>
        <li><strong>Debug information</strong> - Details for troubleshooting</li>
    </ul>

    <h4>3. Traces</h4>
    <p>End-to-end request journeys through distributed systems. Traces show:</p>
    <ul>
        <li><strong>Request path</strong> - Which services a request flows through</li>
        <li><strong>Latency breakdown</strong> - Where time is spent</li>
        <li><strong>Dependencies</strong> - How services interact</li>
    </ul>

    <h3 id="section-5-2">Service Level Objectives (SLOs)</h3>

    <p>An SLO is a target for how well a service should perform. SLOs have three components:</p>

    <h4>Service Level Indicator (SLI)</h4>
    <p>A metric that measures what matters to users. Examples:</p>
    <ul>
        <li>Availability: Percentage of successful requests</li>
        <li>Latency: Percentage of requests completing within acceptable time</li>
        <li>Error rate: Percentage of requests that don't fail</li>
    </ul>

    <h4>Service Level Objective (SLO)</h4>
    <p>The target for the SLI. Examples:</p>
    <ul>
        <li>"99% availability" - The SLI must stay above 99%</li>
        <li>"95th percentile latency under 500ms" - 95% of requests complete within 500ms</li>
        <li>"99.9% success rate" - Less than 0.1% errors</li>
    </ul>

    <h4>Service Level Agreement (SLA)</h4>
    <p>A contractual commitment about the SLO. SLAs define what happens if we miss the SLO (refunds, credits, etc).</p>

    <div class="callout info">
        <div class="callout-title">ℹ️ Error Budgets</div>
        <p>If your SLO is 99% availability, you have a 1% "error budget" per month. This is how much downtime you can have before violating the SLO. Once the budget is exhausted, you must focus on stability over new features.</p>
    </div>

    <h3 id="section-5-3">Dashboard Links</h3>

    <p>Use these dashboards to monitor Konflux metrics and SLOs:</p>
"""

    # Part 2: Dashboard links (DYNAMIC - iterates through extracted links)
    if dashboard_links:
        html += """
    <div class="callout info">
        <div class="callout-title">ℹ️ Dashboard Access</div>
        <p>Most dashboards require VPN and authentication. Contact your team lead for access if you don't have it.</p>
    </div>

    <ul>
"""
        for dashboard in dashboard_links:
            html += f'        <li><a href="{dashboard["url"]}" target="_blank"><strong>{dashboard["name"]}</strong></a>'
            if dashboard.get('description'):
                html += f' - {dashboard["description"]}'
            html += '</li>\n'

        html += """    </ul>
"""
    else:
        html += """
    <p><em>No dashboard links were extracted from the source content.</em></p>
"""

    # Part 3: Graph types, troubleshooting, useful links (~125 lines)
    html += """
    <h3 id="section-5-4">Graph Types in Grafana</h3>

    <p>Grafana supports several visualization types. Choose the right visualization for your data:</p>

    <h4>Graph/Time Series</h4>
    <p>Shows how a metric changes over time. Best for:</p>
    <ul>
        <li>Trends (is latency increasing?)</li>
        <li>Patterns (traffic spikes at certain times?)</li>
        <li>Comparisons (two services side by side)</li>
    </ul>

    <h4>Gauge</h4>
    <p>Shows a single current value with min/max ranges. Best for:</p>
    <ul>
        <li>Current SLO status (showing if we're above/below target)</li>
        <li>Capacity remaining</li>
        <li>Health status at a glance</li>
    </ul>

    <h4>Stat Panel</h4>
    <p>Shows a single large number with optional sparkline. Best for:</p>
    <ul>
        <li>Current error rate</li>
        <li>Total requests in a period</li>
        <li>Key metrics that changed recently</li>
    </ul>

    <h4>Heatmap</h4>
    <p>Shows distribution of values across time. Best for:</p>
    <ul>
        <li>Latency distribution (where do most requests fall?)</li>
        <li>Finding outliers</li>
        <li>Identifying time-dependent patterns</li>
    </ul>

    <h4>Table</h4>
    <p>Shows data in rows and columns. Best for:</p>
    <ul>
        <li>Listing top errors or slow operations</li>
        <li>Service health status</li>
        <li>Detailed metrics that don't need visualization</li>
    </ul>

    <h3 id="section-4-5">Troubleshooting Tips</h3>

    <p><strong>Dashboard shows no data?</strong></p>
    <ul>
        <li>Check the time range - data might be outside the selected window</li>
        <li>Verify the metric name exists in Prometheus</li>
        <li>Check that labels (filters) match your data</li>
        <li>Test the PromQL query directly in Prometheus</li>
    </ul>

    <p><strong>Alert firing when it shouldn't?</strong></p>
    <ul>
        <li>Check the alert condition - is it evaluating correctly?</li>
        <li>Look at the metric values in Grafana - are they at threshold?</li>
        <li>Check the <code>for:</code> duration - alert must be true for this long</li>
        <li>Review recent changes to the alert definition</li>
    </ul>

    <p><strong>PromQL query errors?</strong></p>
    <ul>
        <li>Check for balanced parentheses and brackets</li>
        <li>Verify metric and label names are spelled correctly (case-sensitive)</li>
        <li>Use Prometheus console to test basic queries first</li>
        <li>Start simple, then add complexity</li>
    </ul>

    <p><strong>Metrics missing or stale?</strong></p>
    <ul>
        <li>Check if the component generating the metric is running</li>
        <li>Verify scrape jobs are configured for that service</li>
        <li>Look for errors in Prometheus targets page</li>
        <li>Check application logs for export errors</li>
    </ul>

    <h3 id="section-4-6">Useful Resources and Links</h3>

    <ul>
        <li><strong>Prometheus Documentation:</strong> <a href="https://prometheus.io/docs/" target="_blank">prometheus.io/docs</a> - Official docs for metrics, querying, and alerting</li>
        <li><strong>PromQL Basics:</strong> <a href="https://prometheus.io/docs/prometheus/latest/querying/basics/" target="_blank">PromQL Query Language</a> - Learn PromQL syntax and operators</li>
        <li><strong>Grafana Dashboards:</strong> <a href="https://grafana.com/docs/grafana/latest/dashboards/" target="_blank">Grafana Dashboard Guide</a> - How to create and modify dashboards</li>
        <li><strong>Alerting Rules:</strong> <a href="https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/" target="_blank">Prometheus Alerting Rules</a> - Alert syntax and configuration</li>
        <li><strong>SLO Best Practices:</strong> <a href="https://sre.google/books/" target="_blank">Google SRE Books</a> - Industry standard guidance on SLOs and observability</li>
        <li><strong>o11y Repository:</strong> <a href="https://github.com/redhat-appstudio/o11y" target="_blank">redhat-appstudio/o11y</a> - Source of Konflux alerts and dashboards</li>
    </ul>

    <h3 id="section-4-7">Quick Reference: Common PromQL Functions</h3>

    <p>These functions appear frequently in Konflux metrics:</p>

    <ul>
        <li><code>rate(metric[5m])</code> - Per-second change over 5 minutes (used for error rates)</li>
        <li><code>avg_over_time(metric[1h])</code> - Average value over 1 hour window</li>
        <li><code>increase(metric[1h])</code> - Total increase over 1 hour</li>
        <li><code>histogram_quantile(0.95, metric)</code> - 95th percentile (latency SLOs)</li>
        <li><code>sum(metric)</code> - Total across all labels</li>
        <li><code>by(...)</code> - Group results by labels</li>
        <li><code>without(...)</code> - Exclude labels from grouping</li>
    </ul>

    <div class="callout warning">
        <div class="callout-title">⚠️ Pro Tip: Start Monitoring Simple</div>
        <p>When adding new metrics, start with simple queries. Complex queries are harder to debug and often hide issues. Add complexity only when you know the basics work.</p>
    </div>
</section>
"""

    return html


def generate_html(content_sections: Dict[str, str], toc_items: List[Dict]) -> str:
    """Generate the complete HTML document."""

    # Build table of contents
    toc_html = "<nav><ul>"
    for item in toc_items:
        toc_html += f'<li><a href="#{item["id"]}">{item["title"]}</a>'
        if "children" in item and item["children"]:
            toc_html += "<ul>"
            for child in item["children"]:
                toc_html += f'<li><a href="#{child["id"]}">{child["title"]}</a></li>'
            toc_html += "</ul>"
        toc_html += "</li>"
    toc_html += "</ul></nav>"

    # Build content sections
    content_html = ""
    for section_id, section_content in content_sections.items():
        content_html += section_content

    # Complete HTML document
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Integration Team Metrics: Modifying Alerts & Dashboards - Training Guide</title>
    <style>{PRISM_CSS}</style>
    <style>{MAIN_CSS}</style>
</head>
<body>
    <aside class="sidebar">
        <h2>Table of Contents</h2>
        {toc_html}
    </aside>

    <main class="content">
        <header>
            <h1>Integration Team Metrics: Modifying Alerts & Dashboards</h1>
            <p class="subtitle">A Practical Guide for Engineers</p>
            <p class="intro">This guide will help you understand how to modify existing metrics, update dashboards, and test changes in the Konflux observability infrastructure. Learn by doing - each section focuses on practical tasks with embedded concepts.</p>
        </header>

        {content_html}
    </main>

    <button class="back-to-top" aria-label="Back to top">↑</button>

    <script>{PRISM_JS}</script>
    <script>{MAIN_JS}</script>
</body>
</html>
"""

    return html


def load_source_content() -> Dict[str, str]:
    """Load all source files from vault."""
    content = {}

    for key, filename in SOURCE_FILES.items():
        print(f"  Loading {filename}...")
        content[key] = read_vault_file(filename)

    return content


if __name__ == "__main__":
    print("Building Konflux Metrics Training Guide...")
    print(f"Reading from: {VAULT_PATH}")
    print(f"Output to: {OUTPUT_PATH}")
    print()

    # Load all source content
    print("Loading source files...")
    source_content = load_source_content()

    print()
    print("Content loaded successfully!")
    print(f"Files processed: {len(source_content)}")

    # Build sections
    print()
    print("Building sections...")
    content_sections = {}

    print("  Building Section 1: Modifying Alerts...")
    content_sections['section-1'] = build_section_1_modifying_alerts(source_content)

    print("  Building Section 2: Standard Operating Procedures...")
    content_sections['section-2'] = build_section_2_sops(source_content)

    print("  Building Section 3: Updating Dashboards...")
    content_sections['section-3'] = build_section_3_updating_dashboards(source_content)

    print("  Building Section 4: Testing Changes...")
    content_sections['section-4'] = build_section_4_testing_changes(source_content)

    print("  Building Section 5: Reference Materials...")
    content_sections['section-5'] = build_section_5_reference(source_content)

    # Table of contents structure
    toc_items = [
        {
            "id": "section-1",
            "title": "1. Modifying Alerts in the o11y Repository",
            "children": [
                {"id": "section-1-1", "title": "What Alerts Are and Why We Modify Them"},
                {"id": "section-1-2", "title": "File Locations"},
                {"id": "section-1-3", "title": "Understanding Alert Structure"},
                {"id": "section-1-4", "title": "Common Modifications"},
                {"id": "section-1-5", "title": "Real-World Example"},
                {"id": "section-1-6", "title": "Updating Alert and Recording Rule Tests"},
                {"id": "section-1-7", "title": "Committing and Creating Pull Requests"},
            ]
        },
        {
            "id": "section-2",
            "title": "2. Standard Operating Procedures (SOPs)",
            "children": [
                {"id": "section-2-1", "title": "What Are SOPs?"},
                {"id": "section-2-2", "title": "Two Categories of SOPs"},
                {"id": "section-2-3", "title": "Where SOPs Are Located"},
                {"id": "section-2-4", "title": "How SOPs Link to Alerts"},
                {"id": "section-2-5", "title": "Working with SOPs"},
                {"id": "section-2-6", "title": "Common SOP Workflow"},
            ]
        },
        {
            "id": "section-3",
            "title": "3. Updating Grafana Dashboards",
            "children": [
                {"id": "section-3-1", "title": "Where Dashboards Are Defined"},
                {"id": "section-3-2", "title": "Dashboard Development Workflow"},
                {"id": "section-3-3", "title": "Step-by-Step: Editing a Dashboard in Grafana"},
                {"id": "section-3-4", "title": "Updating app-interface to Deploy to Production"},
            ]
        },
        {
            "id": "section-4",
            "title": "4. Testing Changes",
            "children": [
                {"id": "section-4-1", "title": "Why Test Your Changes"},
                {"id": "section-4-2", "title": "Setting Up Podman"},
                {"id": "section-4-3", "title": "Running Tests Locally"},
                {"id": "section-4-4", "title": "Understanding Test Output"},
                {"id": "section-4-5", "title": "Common Test Failures and Fixes"},
                {"id": "section-4-6", "title": "References and Additional Resources"},
            ]
        },
        {
            "id": "section-5",
            "title": "5. Reference Materials",
            "children": [
                {"id": "section-5-1", "title": "Understanding Observability & SLOs"},
                {"id": "section-5-2", "title": "Service Level Objectives (SLOs)"},
                {"id": "section-5-3", "title": "Dashboard Links"},
                {"id": "section-5-4", "title": "Graph Types in Grafana"},
                {"id": "section-5-5", "title": "Troubleshooting Tips"},
                {"id": "section-5-6", "title": "Useful Resources and Links"},
                {"id": "section-5-7", "title": "Quick Reference: Common PromQL Functions"},
            ]
        },
    ]

    print()
    print("Generating HTML...")
    html = generate_html(content_sections, toc_items)

    # Create parent directories if they don't exist
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    VAULT_COPY_PATH.parent.mkdir(parents=True, exist_ok=True)

    print(f"Writing output to: {OUTPUT_PATH}")
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"Also copying to vault: {VAULT_COPY_PATH}")
    with open(VAULT_COPY_PATH, 'w', encoding='utf-8') as f:
        f.write(html)

    # Get file size in KB
    output_file_size_kb = OUTPUT_PATH.stat().st_size / 1024

    print()
    print("✓ Build complete!")
    print(f"Output file: {OUTPUT_PATH.name}")
    print(f"File size: {output_file_size_kb:.1f} KB")
