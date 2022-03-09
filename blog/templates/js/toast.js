const content = document.querySelector('#content').value;
console.log(content);

const editor = new toastui.Editor({
    el: document.querySelector('#editor'),
    previewStyle: 'vertical',
    height: '500px',
    initialValue: content
});

submitFrm = function(){
            cont = document.getElementById('content');
            cont.value=editor.getMarkdown();
            document.getElementById('frm').submit();
		}
