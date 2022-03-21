// Script to allow anchoring of user-selected content on html pages.
// Original idea deployed by http://archive.today
// Packaged for WordPress on http://trilema.com/2015/that-spiffy-selection-thing/

function findPos(obj) {
  var curtop = 0;
  while (obj && obj.offsetParent) {
    curtop += obj.offsetTop; // todo: + webkit-transform
    obj = obj.offsetParent;
  }
  return curtop;
}
var artificial = null;
var prevhash = "";
function scrollToHash() {
  if (document.location.hash.replace(/^#/, "")==prevhash.replace(/^#/, ""))
    return;
  prevhash = document.location.hash;
  if (document.location.hash.match(/#[0-9.]+%/)) {
    var p = parseFloat(document.location.hash.substring(1));
    if (0 < p && p < 100 /*&& p%5 != 0*/) {
      var content = document.getElementById("CONTENT")
      var y = findPos(content) + (content.offsetHeight)*p/100;
      window.scrollTo(0, y-16);
    }
  }

  var adr = document.location.hash.match(/selection-(\d+).(\d+)-(\d+).(\d+)/);
  if (adr) {
    var pos=0,begin=null,end=null;
    function recur(e) {
      if (e.nodeType==1) pos = (pos&~1)+2;
      if (e.nodeType==3) pos = pos|1;
      if (pos==adr[1]) begin=[e, adr[2]];
      if (pos==adr[3]) end  =[e, adr[4]];
      for (var i=0; i<e.childNodes.length; i++)
        recur(e.childNodes[i]);
      if (e.childNodes.length>0 && e.lastChild.nodeType==3)
        pos = (pos&~1)+2;
    }
    // remove old "artificial" span if any
    if (artificial) {
      artificial.previousSibling.data += artificial.childNodes[0].data;
      artificial.parentNode.removeChild(artificial);
    }
    var content = document.getElementById("CONTENT");
    recur(content.childNodes[content.childNodes[0].nodeType==3 ? 1 : 0]);
    if (begin!=null && end!=null) {
      // scroll to selection
      if (begin[0].nodeType==3) {
        var text = document.createTextNode(begin[0].data.substr(0, begin[1]));
        artificial = document.createElement("SPAN");
        artificial.appendChild(document.createTextNode(begin[0].data.substr(begin[1])));

        begin[0].parentNode.insertBefore(text, begin[0]);
        begin[0].parentNode.replaceChild(artificial, begin[0]);

        if (end[0]===begin[0])
          end = [artificial.childNodes[0], end[1]-begin[1]];
        begin = [artificial.childNodes[0], 0];
        /* window.scrollTo(0, findPos(artificial)-8); */ artificial.scrollIntoView(true);
      } else if (begin[0].nodeType==1) {
        /* window.scrollTo(0, findPos(begin[0])-8);   */ begin[0].scrollIntoView(true);
      }

      if (window.getSelection) {
        var sel = window.getSelection();
        sel.removeAllRanges();
        var range = document.createRange();
        range.setStart(begin[0], begin[1]);
        range.setEnd  (  end[0],   end[1]);
        sel.addRange(range);
      } else if (document.selection) { // IE
      }
    }
  }
}
window.onhashchange = scrollToHash;
var initScrollToHashDone = false;
function initScrollToHash() {
  if (!initScrollToHashDone) {
    initScrollToHashDone = true;
    scrollToHash();
  }
}
window.onload = initScrollToHash;
setTimeout(initScrollToHash, 500); /* onload can be delayed by counter code */

//document.onselectionchange = /* only webkit has working document.onselectionchange */
document.onmousedown = document.onmouseup = function(e) {
  var newhash = "";
  if (window.getSelection) {
    var sel=window.getSelection();
    if (!sel.isCollapsed) {
      var pos=0,begin=[0,0],end=[0,0];
      var range=sel.getRangeAt(0);
      function recur(e) {
        if (e===artificial) {
          if (range.startContainer===e.childNodes[0]) begin=[pos, e.previousSibling.data.length+range.startOffset];
          if (range.endContainer  ===e.childNodes[0]) end  =[pos, e.previousSibling.data.length+range.endOffset ];
        } else {
          if (e.nodeType==1) pos = (pos&~1)+2;
          if (e.nodeType==3) pos = pos|1;
          if (range.startContainer===e) begin=[pos, range.startOffset];
          if (range.endContainer  ===e) end  =[pos, range.endOffset ];
          for (var i=0; i<e.childNodes.length; i++)
            recur(e.childNodes[i]);
          if (e.childNodes.length>0 && e.lastChild.nodeType==3)
            pos = (pos&~1)+2;
        }
      }

      var content = document.getElementById("CONTENT");
      recur(content.childNodes[content.childNodes[0].nodeType==3 ? 1 : 0]);
      if (begin[0]>0 && end[0]>0) {
        newhash = "selection-"+begin[0]+"."+begin[1]+"-"+end[0]+"."+end[1];
      }
    }
  } else if (document.selection) { // IE
  }

  try {
    var oldhash = location.hash.replace(/^#/, "");
    if (oldhash != newhash) {
      prevhash = newhash; /* avoid firing window.onhashchange and scrolling */
      if (history.replaceState)
        history.replaceState('', document.title, newhash=="" ? window.location.pathname : '#'+newhash);
      else
        location.hash = newhash;
    }
  } catch(e) {
  }
};
