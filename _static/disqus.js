(function() {
  var d = document, s = d.createElement('script');
  s.src = 'https://esphomelib.disqus.com/embed.js';
  s.setAttribute('data-timestamp', +new Date());
  (d.head || d.body).appendChild(s);
})();

var disqus_config = function () {
  let disqusThread = document.getElementById("disqus_thread");
  if (disqusThread === null)
    return;
  this.page.identifier = disqusThread.getAttribute('data-disqus-identifier');
};
