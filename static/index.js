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

// 全站右上角悬浮GitHub图标
(function() {
  var githubDiv = document.createElement('div');
  githubDiv.style.position = 'fixed';
  githubDiv.style.top = '24px';
  githubDiv.style.right = '24px';
  githubDiv.style.zIndex = '9999';
  githubDiv.style.cursor = 'pointer';
  githubDiv.title = '访问 GitHub 仓库';

  var githubLink = document.createElement('a');
  githubLink.href = 'https://github.com/xixiwenxuanhe/learn-liangliang';
  githubLink.target = '_blank';
  githubLink.rel = 'noopener noreferrer';

  // 使用本地SVG图片
  var githubImg = document.createElement('img');
  githubImg.src = '/img/github.svg';
  githubImg.alt = 'GitHub';
  githubImg.style.width = '40px';
  githubImg.style.height = '40px';
  githubImg.style.display = 'block';

  githubLink.appendChild(githubImg);
  githubDiv.appendChild(githubLink);
  document.body.appendChild(githubDiv);
})();

// 移除"因收到Google相关通知，网站将会择期关闭"提示
(function() {
  var allDivs = document.getElementsByTagName('div');
  for (var i = 0; i < allDivs.length; i++) {
    var div = allDivs[i];
    if (
      div.getAttribute('align') === 'center' &&
      div.innerText &&
      div.innerText.indexOf('因收到Google相关通知，网站将会择期关闭') !== -1 &&
      div.querySelector('a[href*="lumendatabase.org/notices/44265620"]')
    ) {
      div.parentNode.removeChild(div);
      break; // 只移除第一个找到的即可
    }
  }
})();

// 右下角悬浮Live2D模型
(function() {
  // 动态插入 live2d.js 脚本
  var script = document.createElement('script');
  script.src = '/live-2d/js/live2d.js';
  script.onload = function() {
    // 插入canvas元素
    var canvas = document.createElement('canvas');
    canvas.className = 'live2d';
    canvas.id = 'live2d';
    canvas.width = 150;
    canvas.height = 200;
    document.body.appendChild(canvas);

    // 插入css样式
    var style = document.createElement('style');
    style.innerHTML = '.live2d { position: fixed; bottom: 0; right: 0; z-index: 9999; pointer-events: none; }';
    document.head.appendChild(style);

    // 初始化live2d
    if (typeof loadlive2d === 'function') {
      loadlive2d('live2d', '/live-2d/hijiki/hijiki.model.json');
    }
  };
  document.body.appendChild(script);
})();

