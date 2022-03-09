const content = document.querySelector('#viewer').innerHTML;

const Viewer = toastui.Editor;
const viewer = new Viewer({
    el: document.querySelector('#viewer'),
    height: '600px',
    initialValue: content,
});
 viewer.setMarkdown(content);
