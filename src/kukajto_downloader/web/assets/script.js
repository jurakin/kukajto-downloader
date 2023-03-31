const analyze = document.querySelector(".submit-btn");
const copy_video = document.querySelector(".copy-video-btn");
const copy_subs = document.querySelector(".copy-subs-btn");

const attr_text = "attr-text";
const attr_alt_text = "attr-alt-text";

let result_video = "";
let result_subs = "";

const printError = (error) => {
    alert("Error! " + error.errorText);
    console.error(error.errorTraceback);
}

eel.expose(updateAnalyzeBar);
function updateAnalyzeBar(percent) {
    analyze.style.setProperty("--percent", percent + "%");
}

analyze.addEventListener("click", () => {
    analyze.innerHTML = analyze.getAttribute(attr_alt_text);
    analyze.disabled = true;
    updateAnalyzeBar(20);

    try {
        eel.analyze()().then((data) => {
            result_video = data[0];
            result_subs = data[1];
            
            copy_video.disabled = result_video.length === 0;
            copy_video.style.setProperty("--percent", result_video.length === 0 ? "0%" : "100%");

            copy_subs.disabled = result_subs.length === 0;
            copy_subs.style.setProperty("--percent", result_subs.length === 0 ? "0%" : "100%");
        }).catch((error) => {
            printError(error);
        }).finally(() => {        
            analyze.innerHTML = analyze.getAttribute(attr_text);
            analyze.disabled = false;
            updateAnalyzeBar(100);
        });
    } catch (error) {
        console.error(error);
        analyze.innerHTML = analyze.getAttribute(attr_text);
        updateAnalyzeBar(100);
    }
});

copy_video.addEventListener("click", () => {
    window.navigator.clipboard.writeText(result_video);

    copy_video.innerHTML = copy_video.getAttribute(attr_alt_text);
    setTimeout(() => { copy_video.innerHTML = copy_video.getAttribute(attr_text) }, 500);
})

copy_subs.addEventListener("click", () => {
    window.navigator.clipboard.writeText(result_subs);

    copy_subs.innerHTML = copy_subs.getAttribute(attr_alt_text);
    setTimeout(() => { copy_subs.innerHTML = copy_subs.getAttribute(attr_text) }, 500) 
})