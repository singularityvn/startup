function docReady(fn) {
    // see if DOM is already available
    if (document.readyState === "complete" || document.readyState === "interactive") {
        // call on next available tick
        setTimeout(fn, 1);
    } else {
        document.addEventListener("DOMContentLoaded", fn);
    }
}

docReady(function() {
    var entryContent = document.getElementsByTagName("main");
    for (let index = 0; index < entryContent.length; index++) {
        var element = entryContent[index];
        var images = element.querySelectorAll('img');
        mediumZoom(images);
    }
})