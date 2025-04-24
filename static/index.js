window.dataLayer = window.dataLayer || [];

function gtag() {
    dataLayer.push(arguments);
}

gtag('js', new Date());
gtag('config', 'G-NPSEEVD756');
var path = window.location.pathname
var cookie = getCookie("lastPath");
console.log(path)
if (path.replace("/", "") === "") {
    if (cookie.replace("/", "") !== "") {
        console.log(cookie)
        document.getElementById("tip").innerHTML = "<a href='" + cookie + "'>跳转到上次进度</a>"
    }
} else {
    setCookie("lastPath", path)
}

window.onload = function () {
    var titleEle = document.getElementById("title");
    if (!titleEle) {
        return
    }
    var title = titleEle.getAttribute("data-id")
    console.log("title=" + title)
    var eleList = document.getElementsByClassName("menu-item")
    for (var i = 0; i < eleList.length; i++) {  //遍历数组
        console.log("eleText=" + eleList[i].id)
        if (eleList[i].id.startsWith(title)) {
            eleList[i].classList.add("current-tab")
            if (i > 0) {
                document.getElementById("prePage").innerHTML = "<a href='" + eleList[i - 1].getAttribute("href") + "'>上一页</a>"
            }
            if (i < eleList.length) {
                document.getElementById("nextPage").innerHTML = "<a href='" + eleList[i + 1].getAttribute("href") + "'>下一页</a>"
            }

        }
    }
}

function setCookie(cname, cvalue) {
    var d = new Date();
    d.setTime(d.getTime() + (180 * 24 * 60 * 60 * 1000));
    var expires = "expires=" + d.toGMTString();
    document.cookie = cname + "=" + cvalue + "; " + expires + ";path = /";
}

function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i].trim();
        if (c.indexOf(name) === 0) return c.substring(name.length, c.length);
    }
    return "";
}

hljs.initHighlightingOnLoad()

function add_inner() {
    let inner = document.querySelector('.sidebar-toggle-inner')
    inner.classList.add('show')
}

function remove_inner() {
    let inner = document.querySelector('.sidebar-toggle-inner')
    inner.classList.remove('show')
}

function sidebar_toggle() {
    let sidebar_toggle = document.querySelector('.sidebar-toggle')
    let sidebar = document.querySelector('.book-sidebar')
    let content = document.querySelector('.off-canvas-content')
    if (sidebar_toggle.classList.contains('extend')) { // show
        sidebar_toggle.classList.remove('extend')
        sidebar.classList.remove('hide')
        content.classList.remove('extend')
    } else { // hide
        sidebar_toggle.classList.add('extend')
        sidebar.classList.add('hide')
        content.classList.add('extend')
    }
}


function open_sidebar() {
    let sidebar = document.querySelector('.book-sidebar')
    let overlay = document.querySelector('.off-canvas-overlay')
    sidebar.classList.add('show')
    overlay.classList.add('show')
}
function hide_canvas() {
    let sidebar = document.querySelector('.book-sidebar')
    let overlay = document.querySelector('.off-canvas-overlay')
    sidebar.classList.remove('show')
    overlay.classList.remove('show')
}
