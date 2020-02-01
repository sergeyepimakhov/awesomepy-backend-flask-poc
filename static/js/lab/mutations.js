export { observeMutations };

const observer = new MutationObserver(function () {
    // inputWrapper mutations
    $('div.CodeMirror').addClass('jp-CodeMirror-editor')
    .addClass('jp-editor')
    .addClass('jp-InputArea-editor');

    // outputWrapper mutations
    $('div.jp-OutputArea').addClass('jp-Cell-outputArea');
});


function observeMutations() {
    observer.observe(document.documentElement,
        {
            childList: true,
            subtree: true,
            characterDataOldValue: true
        });
}