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
    <title>Konflux Metrics: Modifying Alerts & Dashboards - Training Guide</title>
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
            <h1>Konflux Metrics: Modifying Alerts & Dashboards</h1>
            <p class="subtitle">A Practical Guide for Junior Engineers</p>
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
